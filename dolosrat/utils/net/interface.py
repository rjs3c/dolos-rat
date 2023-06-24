# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 17/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
...
"""

# Built-in/Generic Imports.
import os
from dataclasses import dataclass
from ipaddress import IPv4Address
from typing import Any, List, Union

# Modules.
from config.network import NetworkConfig # pylint: disable=import-error
from config.logger import get_logger_conf # pylint: disable=import-error
from ..misc.validator import validate_ipv4_addr
from ..misc.wrapper import BaseWrapper
from ..misc.logger import LoggerWrapper, LoggerLevel, get_logger

# External Imports.
if os.name == 'nt':
    # NT-specfic adapters list.
    from scapy.arch.windows import get_windows_if_list as get_if_list
else:
    # Non-NT interface retrieval using 'Scapy'.
    # Otherwise, NT-specific GUIDs are only shown.
    from scapy.all import get_if_list

@dataclass(unsafe_hash=True, frozen=True)
class IPv4Host:
    """_summary_
    """

    ipv4_addr: IPv4Address
    port: int

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
        network_conf: NetworkConfig,
        logger: LoggerWrapper
    ) -> None:
        """Initialises IfaWrapper."""

        super().__init__()

        # Houses NetworkConfig.
        self.conf = network_conf

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

        if self._conf._conf['selected_ifa']:
            # Readable string to denote interface for
            # being displayed within UI.
            return f"{self.conf._conf['selected_ifa'].ifa_name}" \
                f"({self.conf._conf['selected_ifa'].ifa_addrs})"

        return ""

    def _collect_ifaces(self: object) -> None:
        """Collects all interfaces on system and
        outputs a list."""

        # Creates a list of dictionaries, comprising
        # information for each adapter/interface.
        self._interfaces = [
            # Build dataclass from dict fields.
            Ifa(ifa['name'], ifa['ips'])
            # Apply filter for interfaces/adapters
            # that have assigned addresses.
            for ifa in get_if_list()
                # If addresses exist for
                # interface/adapter.
                if 'ips' in ifa.keys()
                if ifa['ips']
        ]

        # Count of interfaces for future reference.
        self.conf._conf['ifas_count'] = len(self._interfaces)

        self._get_handle('LoggerWrapper').write_log(
            f'Enumerated {self.conf._conf["ifas_count"]} (v)NICs.',
            LoggerLevel.INFO
        )

    def _set_default_ifa(self: object) -> None:
        """Implicitly sets the default interface,
        should this not be explicitly performed.
        Defaults to first entry.
        """

        # Check to see if any interfaces were
        # first enumerated.
        if self._interfaces:
            # Sets interface.
            self.set_ifa(
                # Defaults to first interface.
                self._interfaces[0].ifa_name
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

    def set_ifa(self: object, ifa_name: str) -> None:
        """Changes the interface in use.

        Args:
            ifa_name (str): Represents the interface
            name in which to change to.
        """

        # Stores filtered interface information.
        ifa_filtered: List[Any] = []

        # Check if interfaces are available.
        if self._interfaces:
            # Filter interfaces by 'ifa_name'.
            ifa_filtered = list(
                filter(
                    # Utilise lambda for terseness.
                    lambda lfa: (lfa.ifa_name == ifa_name),
                    self._interfaces
                )
            )

        if ifa_filtered:
            # Validate IPv4 address within interface
            # information and place within 'Ifa'
            # dataclass accordingly.
            self.conf._conf['selected_ifa'] = Ifa(
               ifa_filtered[0].ifa_name,
               validate_ipv4_addr([
                   ifa.ifa_addrs[1] for ifa in ifa_filtered
                ][0])
            )

    def _get_ifas_count(self: object) -> int:
        """Returns a count of all collected
        interfaces.

        Returns:
            int: An integer denoting the number
            of collected interfaces.
        """

        return self.conf._conf['ifas_count']

    def get_selected_ifa(self: object) -> Union[None, Ifa]:
        """Returns an 'Ifa' object comprising an
        interface's name and configuration.

        Returns:
            Union[None, Ifa]: Either nothing, or the 
            'Ifa' class comprising the interface information,
            shall be returned.
        """

        return self.conf._conf['selected_ifa']

def get_ifa_wrapper(network_conf: NetworkConfig) -> IfaWrapper:
    """Returns an instantiated IfaWrapper.

    Returns:
        NetworkWrapper: Instance of IfaWrapper.
    """

    return IfaWrapper(
        network_conf,
        get_logger(get_logger_conf(f'__main__.{__name__}'))
    )
