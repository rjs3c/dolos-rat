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
from socketserver import BaseRequestHandler, TCPServer, BaseServer
from typing import Any
from ipaddress import IPv4Address

# Modules.
from .wrapper import BaseWrapper
from config.network import NetworkConfig, get_network_conf
from utils.network import Ifa, IPv4Host

class SingleThreadedTCPHandler(BaseRequestHandler):
    """_summary_
    """

    def __init__(
        self: object,
        request: Any,
        client_address: Any,
        server: BaseServer
    ) -> None:
        """_summary_

        Args:
            self (object): _description_
            request (Any): _description_
            client_address (Any): _description_
            server (BaseServer): _description_
        """

        BaseRequestHandler.__init__(self, BaseRequestHandler, client_address, server)

    def setup(self: BaseRequestHandler) -> None:
        """_summary_
        """

        return BaseRequestHandler.setup(self)

    def handle(self: BaseRequestHandler) -> None:
        """_summary_

        Args:
            self (object): _description_

        Returns:
            _type_: _description_
        """

        print(self.__dict__)

class SingleThreadedTCPServer(TCPServer):
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
        network_config: NetworkConfig,
    ) -> None:
        """_summary_"""

        super().__init__()

        # Comprises the configuration neccessary
        # to bind to a specific interface and accept
        # connections from specific hosts.
        self.config = network_config

        self._init_server()

    def _init_server(self: object) -> None:
        """_summary_
        """

        # Extract Ifa IPv4 address and host
        # ports in which to bind to.
        (host, port) = (
            str(self.config._conf['selected_ifa'].ifa_addrs),
            self.config.conf['selected_host'].port
        )

        # Register handle for SingleThreadedTCPServer.
        self._register_handle(
            SingleThreadedTCPServer(
                (host, port),
                SingleThreadedTCPHandler
            )
        )

    def listen(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        self._get_handle('SingleThreadedTCPServer').serve_forever()

def _get_tcp_server() -> SingleThreadedTCPServer:
    """_summary_

    Returns:
        SingleThreadedTCPServer: _description_
    """

    return SingleThreadedTCPServer

def _get_tcp_handler() -> SingleThreadedTCPHandler:
    """_summary_

    Returns:
        SingleThreadedTCPHandler: _description_
    """

    return SingleThreadedTCPHandler

def get_tcp_server_wrapper(network_config: NetworkConfig) -> TCPServerWrapper:
    """_summary_

    Returns:
        TCPServerWrapper: _description_
    """
    ...

    return TCPServerWrapper(network_config)

# _ = get_network_conf(
#     Ifa('Wi-Fi', IPv4Address('192.168.1.231')),
#     IPv4Host(IPv4Address('192.168.1.231'), 8080)
# )

# TCPServerWrapper(_).listen()