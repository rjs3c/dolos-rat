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
# import struct
from socket import socket, error
from typing import Any, Union
from contextlib import contextmanager

class Socket:
    """
    
    Credit: https://johndanielraines.medium.com/
    """

    # The bytes of the data that
    # are occupied by the payload header.
    # Simple integer to represent the length
    # of the payload - 32 bit.
    head_bytes: int = 4

    @staticmethod
    def send(sock: socket, data: Any) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        if data:
            # Get length of data.
            data_len = len(data).to_bytes(
                Socket.head_bytes,
                byteorder='big'
            )

            try:
            # Transmit data, with length of
            # data prepended as header.
                sock.sendall(
                    data_len + data
                )
            except error:
                pass

    @staticmethod
    def recv_raw(sock: socket, raw_len: int) -> bytearray:
        """_summary_

        Args:
            self (object): _description_
        """

        raw_rx = bytearray()

        while len(raw_rx) < raw_len:
            # Houses the raw data retrieved
            # from the client request.
            recv_data: Union[None, bytes] = None

            try:
                # Traverses received data from offset
                # of payload onwards.
                recv_data = sock.recv(
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

    @staticmethod
    def recv(sock: socket) -> bytearray:
        """_summary_

        Returns:
            bytearray: _description_
        """

        raw_len: Union[None, int] = None
        raw_data: bytearray = bytearray()

        # Extracts the length specified
        # within the header of the payload.
        # Converts from bytes to integer.
        try:
            raw_len = int.from_bytes(
                Socket.recv_raw(
                    sock,
                    # 4 byte / 32 bit int.
                    Socket.head_bytes
                ),
                byteorder='big'
            )
        except ValueError:
            pass

        # Identify if header is present, or if
        # conversion from bytes to int failed.
        if raw_len:
            raw_data = Socket.recv_raw(sock, raw_len)

        return raw_data

# https://stackoverflow.com/questions/3693771/understanding-the-python-with-statement-and-context-managers
@contextmanager
def send_data_handler(send_data: Any) -> Any:
    """_summary_
    """

    send_output: Union[None, Any] = None

    try:
        yield send_output
    finally:
        ...
