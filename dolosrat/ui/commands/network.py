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
from operator import attrgetter
from typing import List

# Modules.
from config.network import network_conf # pylint: disable=import-error
from utils.net.capture import get_ipv4_capture # pylint: disable=import-error
from utils.net.interface import IfaWrapper # pylint: disable=import-error
from utils.net.server import get_tcp_server_wrapper # pylint: disable=import-error

def _update_btns_host_connected(top_level: object) -> None:
    """_summary_
    """

    # Enable relevant action buttons.
    if network_conf.conf['selected_host'].connected:
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
        top_level.top_col_frame_1.btn_1.disable_btn()
        top_level.top_col_frame_1.btn_2.disable_btn()
        top_level.top_col_frame_1.btn_3.disable_btn()
        top_level.top_col_frame_1.btn_4.disable_btn()

        # Middle-left buttons.
        top_level.top_col_frame_2.btn_4.disable_btn()
        top_level.top_col_frame_2.btn_2.enable_btn()
        top_level.top_col_frame_2.btn_3.enable_btn()

def _set_host_connected(top_level: object) -> None:
    """_summary_

    Args:
        top_level (object): _description_
    """

    # Extract IPv4 address and port
    # from selected host.
    ipv4_addr, port = attrgetter(
        'ipv4_addr', 'port'
    )(network_conf.conf['selected_host'])

    # Get text of relevant host listbox item.
    host_btn_text = \
        top_level.top_col_frame_3.get_item_text(
            f'{ ipv4_addr }:{ port } '
        )

    # Remove '[Disconnected]' string and
    # append '[Connected]'.
    top_level.top_col_frame_3.edit_item(
        host_btn_text,
        host_btn_text.replace(
            '[Disconnected]', 
            ''
        ) + '[Connected]'
    )

def get_ifas() -> List[str]:
    """_summary_

    Returns:
        List[Ifa]: _description_
    """

    # Returh list of interface names for
    # drop-dowm list.
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

    # Initialise TCPServerWrapper and
    # commence listening for selected host.
    get_tcp_server_wrapper().listen()

    if network_conf.conf['selected_host'].connected:
        _set_host_connected(top_level)
