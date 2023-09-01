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

from .config import Config
from .logger import LoggerConfig, get_logger_conf
from .network import NetworkConfig, get_network_conf
from .ctkinter import CTkinterConfig, get_ctkinter_conf
