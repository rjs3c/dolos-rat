# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 01/08/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
from datetime import datetime
from operator import attrgetter

# External Imports.
from scapy.all import sr, IP, ICMP # pylint: disable=no-name-in-module

# Modules.
from config.network import network_conf # pylint: disable=import-error
from config.logger import get_logger_conf # pylint: disable=import-error
from utils.net.interface import IfaWrapper # pylint: disable=import-error
from ..misc.wrapper import BaseWrapper
from ..misc.logger import LoggerWrapper, LoggerLevel, get_logger
from ..misc.threading import threadpooled

class PingWrapper(BaseWrapper):
    """Transmits ICMP messages to given host."""

    def __init__(
        self: object,
        logger: LoggerWrapper
    ) -> None:
        """Initialises 'PingWrapper'."""

        super().__init__()

        # Registers handle for logger.
        self._register_handle(logger)

    @threadpooled
    def _ping(self: object) -> None:
        """Internal function for pinging supplied host."""

        # Time delta (milliseconds).
        time_delta = None

        # IPv4 address of the client to specifically
        # ping.
        host_addr, host_port = attrgetter(
            'ipv4_addr', 'port'
        )(network_conf.conf['selected_host'])

        # Craft ICMP payload using scapy.
        icmp_payload = IP(dst=str(host_addr), ttl=255)/ICMP()

        self._get_handle('LoggerWrapper').write_log(
            f'Pinging \'{host_addr}\' with TTL 255.',
            LoggerLevel.INFO
        )
 
        # Send ICMP payload.
        icmp_ans, _ = sr(
            icmp_payload,
            retry=0,
            timeout=5,
            verbose=0
        )

        # Get request and response times, subtract to get
        # time delta.
        try:
            icmp_query_time = datetime.fromtimestamp(icmp_ans[0][0].sent_time)
            icmp_reply_time = datetime.fromtimestamp(icmp_ans[0][1].time)
            time_delta = (icmp_reply_time - icmp_query_time).microseconds
            self._get_handle('LoggerWrapper').write_log(
                f'Ping reply from \'{host_addr}\' with latency {time_delta}ms.',
                LoggerLevel.INFO
            )
        except (IndexError, AttributeError):
            self._get_handle('LoggerWrapper').write_log(
                f'No ping reply from \'{host_addr}\' with timeout 5s.',
                LoggerLevel.ERROR
            )

        # Set ping host attribute accordingly.
        IfaWrapper.edit_host(host_addr, host_port, 'ping', time_delta)

    @threadpooled
    def ping(self: object) -> None:
        """External-facing function for pinging selected host."""

        self._ping()

def get_ping_wrapper() -> PingWrapper:
    """Returns an instantiated IfaWrapper.

    Returns:
        NetworkWrapper: Instance of IfaWrapper.
    """

    return PingWrapper(
        get_logger(get_logger_conf(f'__main__.{__name__}'))
    )
