# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 17/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
"""

# Built-in/Generic Imports.
import os
from ipaddress import IPv4Address, ip_address
from typing import Any, Dict, List

# External Imports.
if os.name == 'nt':
    from scapy.arch.windows import get_windows_if_list as get_if_list
else:
    # Non-NT interface retrieval using 'Scapy'.
    from scapy.all import get_if_list

class NetworkWrapper():
    """_summary_
    """

    def __init__(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """
        self._interfaces: List[Dict[str, Any]] = None

        self._collect_interfaces()

    def __str__(self: object) -> None: ...

    def _collect_interfaces(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """
        self._interfaces = [
            # Produce dictionary of interfaces.
            {
                'ifa_name': ifa['name'],
                'ifa_addrs': ifa['ips']
            }
            # Apply filter for interfaces/adapters
            # with assigned addresses.
            for ifa in get_if_list()
                if 'ips' in ifa.keys()
                if ifa['ips']
        ]

        print(self._interfaces)

        # print(filter(lambda lfa: (lfa['name'] == 'Ethernet'), self._interfaces))

    def get_ipv4_addr(self: object, ifa_name: str) -> None:
        """
        """
        ...

NetworkWrapper()._collect_interfaces()