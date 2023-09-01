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
from ipaddress import IPv4Address, ip_address
from typing import Union

def validate_ipv4_addr(ipv4_addr: str) -> Union[None, IPv4Address]:
    """Identifies whether string matches
    structure of IPv4 address.

    Args:
        ipv4_addr (str): The string in which to
        validate.

    Returns:
        Union[None, IPv4Address]: Returns either the IPv4
        address or 'None'.
    """

    try:
        return ip_address(ipv4_addr)
    except ValueError:
        return None
