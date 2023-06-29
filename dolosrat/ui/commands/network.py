# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 24/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
...
"""

# Built-in/Generic Imports.
from typing import List
import time

# Modules.
from config.network import network_conf # pylint: disable=import-error
from utils.net.interface import IfaWrapper # pylint: disable=import-error
from utils.net.capture import get_ipv4_capture
from utils.misc.threading import threadpooled

def get_ifas() -> List[str]:
    """_summary_

    Returns:
        List[Ifa]: _description_
    """

    return [
        str(ifa.ifa_name)
        for ifa in network_conf.conf['ifas_list']
    ]

def option_change_ifa(ifa_name: str) -> None:
    """_summary_
    """

    # Sets new interface in global
    # networking configuration.
    IfaWrapper.set_ifa(ifa_name)

def btn_collect_ipv4s(top_level: object) -> None:
    """_summary_
    """

    def update_host_list() -> None:
        """_summary_
        """

        # Iterate through list of collected hosts.
        for host in list(network_conf.conf['hosts_list']):
            # Add entries in listbox for each host.
            top_level.top_col_frame_3.add_item(
                f'{ host.ipv4_addr }:{ host.port }'
            )

    top_level.after(1000, get_ipv4_capture().capture)
    # Initialise IPv4 capture and
    # commence.
    
    top_level.after(2000, update_host_list)
    # top_level.after(5000, update_host_list)

def btn_server_listen(top_level_object) -> None:
    """_summary_

    Args:
        top_level_object (_type_): _description_
    """
    
    ...
