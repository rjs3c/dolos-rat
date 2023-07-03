# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 26/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
https://superfastpython.com/thread-share-variables/
"""

# Built-in/Generic Imports.
from typing import Any, Callable
from threading import Thread
from concurrent.futures import Future
from functools import wraps

def threadpooled(func: Callable[..., Any]):
    """_summary_

    Args:
        f (Callable[..., Any]): _description_
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Future:
        """_summary_

        Returns:
            Any: _description_
        """

        # ...
        return Thread(
            target=func,
            args=args,
            kwargs=kwargs
        ).start()
            
        # return ThreadPoolExecutor().submit(
        #     func, *args, **kwargs
        # ).result()

    return wrapper
