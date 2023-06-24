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
from typing import Any, Union
from socket import gaierror
from threading import Thread

# Modules.
from utils.misc.wrapper import BaseWrapper # pylint: disable=import-error
from utils.misc.logger import get_logger, LoggerWrapper, LoggerLevel # pylint: disable=import-error
from config.network import NetworkConfig, get_network_conf # pylint: disable=import-error
from config.logger import get_logger_conf # pylint: disable=import-error
from .interface import Ifa, IPv4Host
from .connection import Socket

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
            request (Any): _description_
            client_address (Any): _description_
            server (BaseServer): _description_
        """

        BaseRequestHandler.__init__(self, request, client_address, server)

        # Houses data received from the client.
        self._rx_data: Union[None, bytes] = None

    def setup(self: BaseRequestHandler) -> None:
        """_summary_
        """

        return BaseRequestHandler.setup(self)

    def handle(self: BaseRequestHandler) -> None:
        """_summary_
        """

        # Only process if client address is that we
        # desire.
        if self.client_address[0] == self.server.client_addr:
            # Increment request counter
            # for timeout threshold.
            self.server.inc_req()

            # Extract message from 'socket' object.
            with Socket(self.request) as test:
                print(test.recv())

class SingleThreadedTCPServer(TCPServer):
    """_summary_
    """

    timeout: int = 30

    def __init__(
        self: object,
        server_address,
        RequestHandlerClass,
        client_address: str
    ) -> None:
        """_summary_

        Args:
            self (object): _description_
            server_address (_type_): _description_
            RequestHandlerClass (_type_): _description_

        Returns:
            _type_: _description_
        """

        TCPServer.__init__(self, server_address, RequestHandlerClass)

        # Stores the client IPv4 address for the handler to filter
        # requests by. Only want to accept ingress from one,
        # specific host.
        self.client_addr = client_address

        # Allow binding to same address after closing.
        self.allow_reuse_address = True

        # Counters used to identify if no requests
        # have been receieved within interval.
        self._req_ctr: int = 0
        self._req_thres: int = 0

    def timeout_check(self: object) -> bool:
        """_summary_

        Args:
            self (obejct): _description_

        Returns:
            bool: _description_
        """

        return self._req_thres == self._req_ctr

    def inc_thres(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        self._req_thres += 1

    def inc_req(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_

        Returns:
            _type_: _description_
        """

        self._req_ctr += 1

class TCPServerWrapper(BaseWrapper): # pylint: disable=too-few-public-methods
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

        # IPv4 address of the client to specifically
        # accept connections from.
        self._client = str(
           self.config._conf['selected_host'].ipv4_addr
        )

        # The port to listen on to receive correspondance
        # from selected host.
        self._port = self.config.conf['selected_host'].port

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
        try:
            self._register_handle(
                SingleThreadedTCPServer(
                    (self._host, self._port),
                    # Handler to which requests
                    # are dispatched.
                    SingleThreadedTCPHandler,
                    self._client
                )
            )
        except gaierror:
            # Write log to inform of binding error.
            self._get_handle('LoggerWrapper').write_log(
                'Failed to create server on ' \
                    f'\'{self._host}:{self._port}\'.',
                LoggerLevel.ERROR
        )

    def close(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        # Write log to inform of shutdown.
        self._get_handle('LoggerWrapper').write_log(
                f'Server on \'{self._host}:{self._port}\' shutting down.',
                LoggerLevel.INFO
        )

        # Forcefully shuts down server and
        # releases resources.
        self._get_handle( # pylint: disable=protected-access
            'SingleThreadedTCPServer' # pylint: disable=protected-access
        )._BaseServer__shutdown_request = True # pylint: disable=protected-access

    def listen(self: object) -> None:
        """_summary_
        """

        # Generate status log that listening has started.
        self._get_handle('LoggerWrapper').write_log(
                f'Server listening on \'{self._host}:{self._port}\'...',
                LoggerLevel.INFO
        )

        # Processing one request at a time
        # within a controlled loop.
        # Timeout: 30s.
        while self._get_handle('SingleThreadedTCPServer').timeout_check():
            # Increment threshold counter for timeout.
            self._get_handle('SingleThreadedTCPServer').inc_thres()

            # handle_request() used instead of serve_forever()
            # as to avoid single-thread deadlocking issues.
            # This is the case as we want to timeout listening
            # after period of inactivity.
            try:
                self._get_handle('SingleThreadedTCPServer').handle_request()
            except KeyboardInterrupt:
                self.close()

        # Write log to warn of timing out.
        if not self._get_handle('SingleThreadedTCPServer').timeout_check():
            self._get_handle('LoggerWrapper').write_log(
                    f'Idle server on \'{self._host}:{self._port}\' timing out after 30s.',
                    LoggerLevel.WARNING
            )

        # Shutdown server, NOT connection.
        self.close()

    def run(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        self.listen()

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
