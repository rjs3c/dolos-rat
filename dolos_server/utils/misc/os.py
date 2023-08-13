# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 17/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
import sys
import os
from subprocess import Popen
from ctypes import windll

def check_admin_privs() -> bool:
    """Checks if the privilege context in which 
    DolosRAT is run is that of an administator/sudoer.
    This does so in a EAFP fashion 
    (see https://en.wikiquote.org/wiki/Grace_Hopper).

    Returns:
        bool: Indicates whether the current privilege is that
        of an administrator/sudoer.
    """
    try:
        # Non-NT means of checking UID.
        return os.getuid() == 0
    # If NT, AttributeError is thrown.
    except AttributeError:
        pass

    try:
        # Alternatively, check EUID of
        # application if i.e., SUID set.
        return os.geteuid() == 0
    except AttributeError:
        pass

    try:
        # If NT, use Shell32 API to check current
        # privilege context.
        # Can be used to suggest users to run as
        # admin as to not be inundated with UAC
        # windows.
        return windll.shell32.IsUserAnAdmin() == 1
    # Should unintended issues arise, return False.
    except AttributeError:
        pass

    # Defaults to False.
    return False

def open_file_explorer(file_path: str) -> None:
    """
    
    Credit: https://stackoverflow.com/questions/17317219/is-there-an-platform-independent-equivalent-of-os-startfile
    """

    try:
        # Exposed solely for NT-based systems.
        os.startfile(file_path)
    except AttributeError:
        # Will be thrown if system is non-NT.
        file_opener = 'open' if sys.platform == "darwin" else "xdg-open"
        Popen([file_opener, file_path])

def get_loc() -> int:
    """Returns LoC for callee, for trace-backs.

    Returns:
        int: Integer representing the current
        LoC.
    """

    return sys._getframe().f_back.f_lineno
