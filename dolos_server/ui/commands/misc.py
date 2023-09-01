# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 24/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
# pylint: disable=import-error, syntax-error
# pyright: reportMissingModuleSource=false
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Modules
from utils.misc.installer import PayloadInstaller
from utils.misc.os import open_file_explorer

def btn_generate_payload(top_level: object) -> None:
    """Extracts desired filename and path, and
    generates .exe using PyInstaller."""

    # Render dialog, request parent directory
    # and filename.
    file_path = top_level.add_save_menu()
    file_name = top_level.add_filesave_dialog()

    if file_path and file_name:
        # Use PyInstaller to create executable of
        # client payload, with user-specified output
        # dir and filename.
        PayloadInstaller.compile(file_path, file_name)

        # Open output dir in native file explorer.
        open_file_explorer(file_path)
