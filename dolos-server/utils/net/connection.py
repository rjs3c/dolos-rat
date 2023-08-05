# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 20/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
from socket import socket, error, SHUT_RDWR
from typing import Any, List, Union, Optional

class Socket:
    """Provides a context manager for
    sending and receiving data over a supplied
    socket."""

    # The bytes of the data that
    # are occupied by the payload header.
    # Simple integer to represent the length
    # of the payload - 32 bit.
    head_bytes: int = 4

    def __init__(
        self: object,
        sock: socket,
        data: Optional[Any] = None
    ) -> None:
        """Initialises Socket.

        Args:
            sock (socket): Comprises the instance of socket.socket
            to transmit/receieve over. 
            data (Optional[Any], optional): _description_. Comprises the data 
            in which to transmit over the socket. 
        """

        # Comprises handle to socket/request
        # object.
        self._sock = sock

    def __enter__(self: object) -> object:
        """Defines the value returned when
        first entering the context.

        Returns:
            Socket: Comprises an instance to
            self, thereby exposing the methods
            recv(), send(), etc.
        """

        return self

    def __exit__(self: object, *args: List[Any]) -> None:
        """Releases resources, etc. when outside
        of context."""

        # Shuts down socket manually.
        self._sock.shutdown(SHUT_RDWR)

        self._sock.close()

        del self

    def send(self: object, data: Any) -> None:
        """Sends data over socket.socket."""

        if data:
            # Get length of data.
            data_len = len(data).to_bytes(
                self.head_bytes,
                byteorder='big'
            )

            try:
                # Transmit data, with length of
                # data prepended as header.
                self._sock.sendall(
                    data_len + data
                )
            except error:
                pass

    def recv_raw(self: object, raw_len: int) -> bytearray:
        """Receives data from socket.

        Args:
            raw_len (int): The bytes to receieve from the
            socket.

        Returns:
            bytearray: Bytes retrieved from the socket.
        """

        # Raw data receieved from socket.
        raw_rx = bytearray()

        while len(raw_rx) < raw_len:
            # Houses the raw data retrieved
            # from the client request.
            recv_data: Union[None, bytes] = None

            try:
                # Traverses received data from offset
                # of payload onwards.
                recv_data = self._sock.recv(
                    raw_len - len(raw_rx)
                )

                # Check if received data is present.
                if recv_data:
                    raw_rx.extend(recv_data)
            except error:
                # Stop attempting to retrieve data
                # from socket.
                break

        # Return received data in bytearray() form.
        return raw_rx

    def recv(self: object) -> bytearray:
        """Retrieves bytes from the socket.

        Returns:
            bytearray: Bytes representing the data
            retrieved from the socket.
        """

        # Raw length of payload; extracted
        # from header.
        raw_len: Union[None, int] = None

        # Extracted payload.
        raw_data: bytearray = bytearray()

        # Extracts the length specified
        # within the header of the payload.
        # Converts from bytes to integer.
        try:
            raw_len = int.from_bytes(
                self.recv_raw(
                    # 4 byte / 32 bit int.
                    self.head_bytes
                ),
                byteorder='big'
            )
        except ValueError:
            pass

        # Identify if header is present, or if
        # conversion from bytes to int failed.
        if raw_len:
            raw_data = self.recv_raw(raw_len)

        return raw_data
