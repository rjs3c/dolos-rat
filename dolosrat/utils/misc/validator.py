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
from ipaddress import IPv4Address, ip_address
from typing import Union

def validate_ipv4_addr(ipv4_addr: str) -> Union[None, IPv4Address]:
    """_summary_

    Args:
        ipv4_addr (str): _description_

    Returns:
        Union[None, IPv4Address]: _description_
    """

    try:
        return ip_address(ipv4_addr)
    except ValueError:
        return None
