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
from ipaddress import IPv4Address
from typing import Any
# from threading import Timer # https://stackoverflow.com/questions/2697039/python-equivalent-of-setinterval

# Modules.
from utils.misc.wrapper import BaseWrapper
from utils.misc.logger import get_logger, LoggerWrapper, LoggerLevel
from .interface import Ifa, IPv4Host
from config.network import NetworkConfig, get_network_conf
from config.logger import get_logger_conf

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

        BaseRequestHandler.__init__(self, request, client_address, server)

    def setup(self: BaseRequestHandler) -> None:
        """_summary_
        """

        return BaseRequestHandler.setup(self)

    def handle(self: BaseRequestHandler) -> None:
        """_summary_
        """

        print(self.__dict__)

class SingleThreadedTCPServer(TCPServer):
    """_summary_
    """

    timeout = 5

    def __init__(self: object, server_address, RequestHandlerClass) -> None:
        """_summary_

        Args:
            self (object): _description_
            server_address (_type_): _description_
            RequestHandlerClass (_type_): _description_

        Returns:
            _type_: _description_
        """

        TCPServer.__init__(self, server_address, RequestHandlerClass)

class TCPServerWrapper(BaseWrapper):
    """_summary_
    """
    def __init__(
        self: object,
        network_config: NetworkConfig,
        logger: LoggerWrapper
    ) -> None:
        """_summary_"""

        super().__init__()

        # Comprises the configuration neccessary
        # to bind to a specific interface and accept
        # connections from specific hosts.
        self.config = network_config

        # IPv4 address of the interface to bind to.
        self._host = str(
            self.config._conf['selected_ifa'].ifa_addrs
        )

        # The port to listen on to receive correspondance
        # from selected host.
        self._port = self.config.conf['selected_host'].port

        # Captures a state by which listening
        # is conducted. Used to check if timed out.
        # By default, stopped.
        self._listen_stopped: bool = True

        # Registers handle for logger.
        self._register_handle(logger)

        # Registers handle for
        # SingleThreadedTCPServer.
        self._init_server()

    def _init_server(self: object) -> None:
        """_summary_
        """

        # Register handle for SingleThreadedTCPServer.
        # Supplied host and port on which to listen to.
        self._register_handle(
            SingleThreadedTCPServer(
                (self._host, self._port),
                # Handler to which requests
                # are dispatched.
                SingleThreadedTCPHandler
            )
        )

    def _inv_listen_state(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """
        self._listen_stopped = not self._listen_stopped

    def shutdown(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """
        ...

    def listen(self: object) -> None:
        """_summary_
        """

        self._inv_listen_state()

        self._get_handle('LoggerWrapper').write_log(
                f'Server listening on \'{self._host}:{self._port}\'...',
                LoggerLevel.INFO
        )

        # Poll interval: 0.5s.
        # Timeout: 5s.
        # while self._listen_stopped is not True:
        #     self._get_handle('SingleThreadedTCPServer').handle_request()
        #     print("hello")

        # self._get_handle('SingleThreadedTCPServer')._BaseServer__shutdown_request = True

        self._get_handle('SingleThreadedTCPServer').serve_forever()

        self._get_handle('SingleThreadedTCPServer').server_close()

def get_tcp_server_wrapper(network_config: NetworkConfig) -> TCPServerWrapper:
    """_summary_

    Returns:
        TCPServerWrapper: _description_
    """

    return TCPServerWrapper(
        network_config,
        get_logger(get_logger_conf(f'__main__.{__name__}'))
    )

_ = get_network_conf(
    Ifa('Wi-Fi', IPv4Address('192.168.1.231')),
    IPv4Host(IPv4Address('192.168.1.231'), 8080)
)

TCPServerWrapper(_, get_logger(get_logger_conf(f'__main__.{__name__}'))).listen()