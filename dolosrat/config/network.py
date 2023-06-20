# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 06/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
...
"""

# Built-in/Generic Imports.
from dataclasses import dataclass
from typing import Any, Dict, Optional

# Modules.
from config import Config

@dataclass
class NetworkConfig(Config):
    """Stores network-specific configurations.
    """

    # Dict comprising network configuration.
    _conf: Dict[str, Any]

    def __init__(
        self: object,
        ifa: Optional[object] = None,
        host: Optional[object] = None
    ) -> None:
        """_summary_

        Args:
            self (object): _description_
            ifa (Optional[object], optional): _description_. Defaults to None.
            host (Optional[object], optional): _description_. Defaults to None.
        """
        self._conf = {
           'selected_ifa': ifa,
           'selected_host': host,
           'ifas_count': 0,
           'timeout': 15,
           'capture_filter': 'ip and tcp'
        }

def get_network_conf(
    chosen_ifa: Optional[object] = None,
    chosen_host: Optional[object] = None
) -> NetworkConfig:
    """Instantiates and returns NetworkConfig.

    Args:
        chosen_ifa (Optional[object], optional): Ifa object comprising
        a specific interface. Defaults to None.
        chosen_host (Optional[object], optional): Comprises an IPv4 address
        and port for a selected host. Defaults to None.

    Returns:
        NetworkConfig: A new instance of NetworkConfig.
    """

    return NetworkConfig(chosen_ifa, chosen_host)
