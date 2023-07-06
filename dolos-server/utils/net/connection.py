# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 20/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
https://johndanielraines.medium.com/implement-a-socket-based-service-in-python-with-socketserver-1200d290c4e3
https://stackoverflow.com/questions/47391774/send-and-receive-objects-through-sockets-in-python
https://stackoverflow.com/questions/42415207/send-receive-data-with-python-socket
https://stackoverflow.com/questions/53755390/python-socketserver-stuck-at-receiving-data
"""

# Built-in/Generic Imports.
from socket import socket, error, SHUT_RDWR
from typing import Any, List, Union, Optional
# from contextlib import contextmanager
# from inspect import isclass

# Modules.
from ..misc.command import Command

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

        # Comprises data in which to transmit.
        self._data = data

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

        self._sock.shutdown(SHUT_RDWR)

        del self

    def send(self: object) -> None:
        """Sends data over socket.socket."""

        if self._data:
            # Get length of data.
            data_len = len(self._data).to_bytes(
                self.head_bytes,
                byteorder='big'
            )

            try:
                # Transmit data, with length of
                # data prepended as header.
                self._sock.sendall(
                    data_len + self._data
                )
            except error:
                pass

    def recv_raw(self: object, raw_len: int) -> bytearray:
        """_summary_

        Args:
            self (object): _description_
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
        """_summary_

        Returns:
            bytearray: _description_
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
