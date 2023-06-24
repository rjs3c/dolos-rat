# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 20/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
Provides the functionalities neccessary for creating 
and managing a TCP server.
"""

# Built-in/Generic Imports.
from socketserver import BaseRequestHandler, TCPServer, BaseServer
from ipaddress import IPv4Address
from typing import Any, Union
from socket import gaierror

# Modules.
from utils.misc.wrapper import BaseWrapper # pylint: disable=import-error
from utils.misc.logger import get_logger, LoggerWrapper, LoggerLevel # pylint: disable=import-error
from config.network import NetworkConfig, get_network_conf # pylint: disable=import-error
from config.logger import get_logger_conf # pylint: disable=import-error
from .interface import Ifa, IPv4Host
from .connection import Socket

class SingleThreadedTCPHandler(BaseRequestHandler):
    """Handler for incoming requests."""

    def __init__(
        self: object,
        request: Any,
        client_address: Any,
        server: BaseServer
    ) -> None:
        """Initialises handler for
        incoming requests."""

        BaseRequestHandler.__init__(self, request, client_address, server)

        # Houses data received from the client.
        self._rx_data: Union[None, bytes] = None

    def setup(self: BaseRequestHandler) -> None:
        """Required to implement as part of
        BaseRequestHandler."""

        return BaseRequestHandler.setup(self)

    def handle(self: BaseRequestHandler) -> None:
        """The method that is evaluated for
        each request. This is where the processing occurs."""

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
    """Provides the functionality for listening
    over TCP, and passing requests to TCP handler."""

    # Time-out threshold by which a request is anticipated.
    timeout: int = 30

    def __init__(
        self: object,
        server_address,
        RequestHandlerClass,
        client_address: str
    ) -> None:
        """Initialises SingleThreadedTCPServer."""

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
        """Compares counters to identify whether a request is
        received within a given time.

        Returns:
            bool: Indicates the result of the
            comparison.
        """

        return self._req_thres == self._req_ctr

    def inc_thres(self: object) -> None:
        """Increments threshold counter
        after 30s."""

        self._req_thres += 1

    def inc_req(self: object) -> None:
        """Increments request counter when
        request is passed to handler."""

        self._req_ctr += 1

class TCPServerWrapper(BaseWrapper): # pylint: disable=too-few-public-methods
    """Wraps around functionality for socketserver
    TCPServer."""

    def __init__(
        self: object,
        network_config: NetworkConfig,
        logger: LoggerWrapper
    ) -> None:
        """Initialises TCPServerWrapper.

        Args:
            network_config (NetworkConfig): Comprises
            networking configuration. Important configurations
            include the interface to listen on, and the host/port
            to specifically accept.
            logger (LoggerWrapper): A handle to the logger.
        """

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
        """Create SingleThreadedTCPServer
        and add handler.
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
        """Stops TCPServer from listening
        by forcing shutdown. Prevents resources
        from being unneccessarily consumed."""

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
        """Listens for incoming connections, and times out
        if no request is received within 30s."""

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
        """

        self.listen()

def get_tcp_server_wrapper(network_config: NetworkConfig) -> TCPServerWrapper:
    """Returns an instance of TCPServerWrapper.

    Returns:
        TCPServerWrapper: An instance of 
        TCPServerWrapper.
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
