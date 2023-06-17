# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 07/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
"""

# Built-in/Generic Imports.
# ...

# External Imports.
import pyshark

# Modules.
from utils.net import Ifa

class CaptureWrapper:
    """_summary_
    """

    def __init__(self: object):
        self._ifa: Ifa = None
        self._capture = None

    def __del__(self: object): ...

    def live_capture(self: object):
        """_summary_
        """
        ...
