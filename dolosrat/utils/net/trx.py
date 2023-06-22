# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 20/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
https://johndanielraines.medium.com/implement-a-socket-based-service-in-python-with-socketserver-1200d290c4e3
https://pythonprogramming.net/pickle-objects-sockets-tutorial-python-3/
https://python-forum.io/thread-4305.html

https://johndanielraines.medium.com/implement-a-socket-based-service-in-python-with-socketserver-1200d290c4e3
https://stackoverflow.com/questions/47391774/send-and-receive-objects-through-sockets-in-python
"""

# Built-in/Generic Imports.
# import struct
from dataclasses import dataclass
from socket import socket
from typing import Any

class Rx: # pylint: disable=too-few-public-methods
    """_summary_
    """

    @staticmethod
    def send(sock: socket, msg: Any) -> None:
        """_summary_

        Args:
            sock (socket): _description_
        """

        ...

class Tx: # pylint: disable=too-few-public-methods
    """_summary_
    """

    @staticmethod
    def recv(sock: socket) -> bytearray:
        """_summary_

        Args:
            sock (socket): _description_
        """

        print(sock)

        rx_data = bytearray()

        return rx_data
