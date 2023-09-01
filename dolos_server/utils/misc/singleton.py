# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 20/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
from typing import Any, Dict, List

class Singleton(type):
    """Singleton class.
    
    Credit: https://github.com/alistair-broomhead"""

    _instances = {}

    def __call__(cls: object, *args: List, **kwargs: Dict[Any]) -> object:
        """Restricts class to single instance.

        Args:
            cls (object): The class in which to instantiate."""

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]
