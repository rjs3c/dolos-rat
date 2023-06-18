# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 18/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
...
"""

# Built-in/Generic Imports.
from typing import List, Optional, Union
from ipaddress import IPv4Address

# Modules.
from utils.network import Ifa
# from utils.parser import ipv4_list_to_ipv4

# External Imports.
from pyshark import LiveCapture

class IPv4Capture:
    """_summary_
    """

    def __init__(
        self: object,
        ifa: Ifa,
        timeout: Optional[int] = 50
    ) -> None:
        """_summary_

        Args:
            self (object): _description_
        """
        # Input network interface.
        # Comprises ifa_name and ifa_addrs fields.
        self._ifa = ifa

        # Timeout parameter passed into .sniff()
        # PyShark method.
        self._timeout = timeout

        # Handle to LiveCapture.
        self._capture: Union[None, LiveCapture] = None

        # List comprising the extracted, and parsed,
        # IPv4 addresses.
        self._ipv4_addrs: List[Union[str, IPv4Address]] = []

    def __del__(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """
        self._capture = None
        del self

    def _init_handler(self: object) -> None: ...
    
    def capture(self: object) -> None:
        ...
