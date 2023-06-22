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
from socket import socket
from typing import Any, Union

# Modules.
from ..misc.wrapper import BaseWrapper

class SocketWrapper(BaseWrapper):
    """_summary_
    """

    # The bytes of the data that
    # are occupied by the payload header.
    # Simple integer to represent the length
    # of the payload - 32 bit.
    head_bytes: int = 4

    def __init__(
        self: object,
        sock: socket
    ) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        super().__init__()

        # Register handle to socket.
        self._register_handle(sock)

        # Sent and received data.
        self._tx: bytearray = bytearray()
        self._rx: bytearray = bytearray()

    def _prepare_send(self: object) -> Any:
        """_summary_

        Args:
            self (object): _description_
        """

        ...

    def _recv_raw(self: object, raw_len: int) -> Union[None, bytearray]:
        """_summary_

        Args:
            self (object): _description_
        """

        while len(self._rx) < raw_len:
            # Traverses received data from offset
            # of payload onwards.
            recv_data = self._get_handle('socket').recv(
                (raw_len - len(self._rx))
            )

            # Check if received data is present.
            if recv_data:
                self._rx.extend(recv_data)

        # Return received data in bytearray() form.
        return self._rx

    def recv(self: object) -> bytearray:
        """_summary_

        Returns:
            bytearray: _description_
        """

        # Extracts the length specified
        # within the header of the payload.
        # Converts from bytes to integer.
        raw_len = int.from_bytes(
            self._recv_raw(
                # 4 byte / 32 bit int.
                self.head_bytes
            )
        )

    def send(self: object, data: Any) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        ...

def get_socket_wrapper(sock: socket) -> SocketWrapper:
    """_summary_

    Args:
        sock (socket): _description_

    Returns:
        SocketWrapper: _description_
    """

    return SocketWrapper(sock)
