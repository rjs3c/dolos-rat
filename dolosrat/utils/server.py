# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 20/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
...
"""

# Built-in/Generic Imports.
import socketserver

# Modules.
from .wrapper import BaseWrapper
from .network import Ifa, IPv4Host

class SingleThreadedTCPHandler(socketserver.BaseRequestHandler):
    """_summary_

    Args:
        socketserver (_type_): _description_
    """
    ...

class SingleThreadedTCPServer(socketserver.TCPServer):
    """_summary_

    Args:
        socketserver (_type_): _description_
    """
    pass

class TCPServerWrapper(BaseWrapper):
    """_summary_
    """
    def __init__(
        self: object,
        listen_ifa: Ifa,
        listen_host: IPv4Host,
        tcp_handler: SingleThreadedTCPHandler,
        tcp_server: SingleThreadedTCPServer
    ) -> None:
        """_summary_"""

        # Comprises the interface and IPv4
        # address in which to listen to.
        self._listen_ifa = listen_ifa

        # Comprises the specific host (IPv4, port)
        # in which to specifically listen to.
        self._listen_host = listen_host

        # Handler to handler object.
        self._tcp_handler = tcp_handler

        # Handler to server object.
        self._tcp_server = tcp_server

    def listen(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """
        ...

def get_tcp_server_wrapper(): ...