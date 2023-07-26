# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 06/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

# Modules.
from config import Config # pylint: disable=import-error

@dataclass(frozen=False)
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
           'ifas_list': List[object],
           'selected_host': host,
           'hosts_list': set(),
           'ifas_count': 0,
           'timeout': 15,
           'capture_filter': 'ip and udp'
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

# Makes use of Python's inherent singleton nature
# of modules.
network_conf = get_network_conf()
