# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 26/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
from typing import Any, Callable
from threading import Thread
from concurrent.futures import Future
from functools import wraps

def threadpooled(func: Callable[..., Any]):
    """Provides a wrapper for functions that need
    to be threaded.

    Args:
        f (Callable[..., Any]): A closure representing
        the function to thread.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Future:
        """Wraps the function.

        Returns:
            Any: Future representing the newly-
            created thread."""

        # Return new thread with the
        # function and arguments.
        return Thread(
            target=func,
            args=args,
            kwargs=kwargs
        ).start()

    return wrapper
