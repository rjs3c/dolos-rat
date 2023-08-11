# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 24/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
# pylint: disable=import-error, syntax-error
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
from io import BytesIO
from enum import Enum, auto
from operator import attrgetter
from time import sleep
from typing import Any, List
from ipaddress import IPv4Address

# Modules.
from config.network import network_conf
from utils.misc.threading import threadpooled
from utils.net.capture import get_ipv4_capture
from utils.net.icmp import get_ping_wrapper
from utils.net.interface import IfaWrapper, IPv4Host
from utils.net.server import get_tcp_server_wrapper

host_status_poll_started: bool = False

class HostStatus(Enum):
    """_summary_

    Args:
        Enum (_type_): _description_
    """

    Listening = 0
    Connected = auto()
    Disconnected = auto()
    
def _update_btns_host_connected(top_level: object) -> None:
    """_summary_
    """
    
    host_addr, host_port = attrgetter(
        'ipv4_addr', 'port'
    )(network_conf.conf['selected_host'])
    
    # Enable relevant action buttons.
    if IfaWrapper.get_host_attribute(host_addr, host_port, 'connected'):
        # If host is connected to.

        # Top-left buttons - enabling all.
        top_level.top_col_frame_1.btn_1.enable_btn()
        top_level.top_col_frame_1.btn_2.enable_btn()
        top_level.top_col_frame_1.btn_3.enable_btn()
        top_level.top_col_frame_1.btn_4.enable_btn()

        # Middle-left buttons.
        top_level.top_col_frame_2.btn_2.disable_btn()
        top_level.top_col_frame_2.btn_3.disable_btn()
        top_level.top_col_frame_2.btn_4.enable_btn()

    else:
        # If host is not connected.

        # Top-left buttons.
        # top_level.top_col_frame_1.btn_1.disable_btn()
        top_level.top_col_frame_1.btn_2.disable_btn()
        top_level.top_col_frame_1.btn_3.disable_btn()
        top_level.top_col_frame_1.btn_4.disable_btn()

        # Middle-left buttons.
        top_level.top_col_frame_2.btn_4.disable_btn()
        top_level.top_col_frame_2.btn_2.enable_btn()
        top_level.top_col_frame_2.btn_3.enable_btn()
        
def _set_host_status(top_level: object, host: IPv4Host, status: HostStatus = 1) -> None:
    """_summary_

    Args:
        top_level (object): _description_
        host (IPv4Host): _description_
        status (HostStatus, optional): _description_. Defaults to 1.
    """

    # Houses the text in which to replace the older
    # status texts with.
    replacement_str = ''

    # Extract IPv4 address and port
    # from selected host.
    ipv4_addr, port = attrgetter(
        'ipv4_addr', 'port'
    )(host)

    # Get text of relevant host listbox item.
    host_btn_text = \
        top_level.top_col_frame_3.get_item_text(
            f'{ ipv4_addr }:{ port } '
        )

    # Check status value and set replacement
    # string accordingly.
    match status:
        # 'Listening'
        case 0:
            # Set string to '[Listening]'
            replacement_str = '[Listening]'
        case 1:
            # Set string to '[Connected]'
            replacement_str = '[Connected]'
        case _:
            # Defaults to '[Disconnected]'
            replacement_str = '[Disconnected]'
                
    # Remove '[Disconnected]' string and
    # append '[Connected]'.
    top_level.top_col_frame_3.edit_item_connected(
        host_btn_text,
        replacement_str
    )

def _set_host_ping(
    top_level: object,
    host_addr: IPv4Address,
    host_port: int,
    time_delta: int
) -> None:
    """_summary_

    Args:
        top_level (object): _description_
    """
    
    # Replacement time delta.
    # replacement_str = ' '
    
    # Get text of relevant host listbox item.
    host_btn_text = \
        top_level.top_col_frame_3.get_item_text(
            f'{ host_addr }:{ host_port } '
        )
        
    # Remove [<time-delta>ms] and replace with
    # [<new-time-delta>ms]
    top_level.top_col_frame_3.edit_item_ping(
        host_btn_text,
        time_delta
    )

@threadpooled
def _check_all_hosts_connected(top_level: object) -> None:
    """_summary_

    Args:
        top_level (object): _description_
    """
    
    # Indicates that this should not be repeated.
    host_status_poll_started = True
    
    # Run continously in the background.
    while True:
        
        try:
            
            _update_btns_host_connected(top_level)

            # Iterate through each enumerated host.
            # for host in network_conf.conf['hosts_list']:
            for host in network_conf.conf['hosts_list'].union({network_conf.conf['selected_host']}):
                
                # Check if listening for host.
                if host.listening:
                    # Amend to '[Listening]'.
                    _set_host_status(top_level, host, 0)
                    continue

                # Check if selected host is connected to - set
                # when TCP connection is initiated.
                elif host.connected:
                    # Amend to '[Connected]'.
                    _set_host_status(top_level, host, 1)
                    continue

                # Edge-cases or if disconnected.
                else:
                    # Amend to '[Disconnected]'.
                    _set_host_status(top_level, host, 2)
                    continue
                
        except (KeyboardInterrupt, RuntimeError):
            break
        
        # Check every 10s.
        sleep(5)

def get_ifas() -> List[str]:
    """_summary_

    Returns:
        List[Ifa]: _description_
    """

    # Returh list of interface names for
    # drop-down list.
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

        # Remove 'Please wait...' button.
        top_level.top_col_frame_3.remove_item(
            'Please wait...'
        )

        # Iterate through list of collected hosts.
        for host in list(network_conf.conf['hosts_list']):

            # Text for connection status.
            connected_str = (
                '[Connected]' if host.connected
                else '[Disconnected]'
            )

            # Add entries in listbox for each host.
            top_level.top_col_frame_3.add_item(
                f'{ host.ipv4_addr }:{ host.port } ' \
                    f'{ connected_str }'
            )

    # Add 'Please wait...' button to indicate progress.
    top_level.top_col_frame_3.add_item(
        'Please wait...',
        'disabled'
    )

    # Initialise IPv4 capture and
    # commence.
    get_ipv4_capture().capture()

    # Update host list.
    top_level.after(17000, update_host_list)

def btn_select_host(btn: object, top_level: object) -> None:
    """_summary_

    Args:
        top_level (object): _description_
    """

    # Selects the host.
    IfaWrapper.set_host(btn.cget('text'))

    # Change foreground colours of each button
    # to give the effect of deselection.
    for _btn in top_level.top_col_frame_3.get_items():
        _btn.configure(fg_color='transparent')

    # Highlight button selected.
    btn.configure(fg_color='#106A43')

    # Enable/disable relevant buttons based
    # upon connected/disconnected status.
    _update_btns_host_connected(top_level)

def btn_listen(top_level: object) -> None:
    """_summary_
    """

    host_addr, host_port = attrgetter(
        'ipv4_addr', 'port'
    )(network_conf.conf['selected_host'])

    IfaWrapper.edit_host(host_addr, host_port, 'disconnected', False)

    # Initialise TCPServerWrapper and
    # commence listening for selected host.
    get_tcp_server_wrapper().run()

    if not host_status_poll_started:
        _check_all_hosts_connected(top_level) 
        
def btn_disconnect(top_level: object) -> None:
    """_summary_

    Args:
        top_level (object): _description_
    """
    
    host_addr, host_port = attrgetter(
        'ipv4_addr', 'port'
    )(network_conf.conf['selected_host'])
    
    IfaWrapper.edit_host(host_addr, host_port, 'disconnected', True)
    
    if not host_status_poll_started:
        _check_all_hosts_connected(top_level)
    
@threadpooled
def btn_ping(top_level: object) -> None:
    """_summary_

    Args:
        top_level (object): _description_
    """
    
    host_addr, host_port = attrgetter(
        'ipv4_addr', 'port'
    )(network_conf.conf['selected_host'])

    # Initialise PingWrapper and call 'ping'
    # function.
    get_ping_wrapper().ping()
    
    # Wait for ICMP timeout period, and extract time delta.
    sleep(5)
    
    if time_delta := IfaWrapper.get_host_attribute(
        host_addr, host_port, 'ping'
    ):
        _set_host_ping(top_level, host_addr, host_port, time_delta)
