# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 20/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
...
"""

# Built-in/Generic Imports.
from typing import Any, Dict, List

class Singleton(type):
    """_summary_
    
    Credit: https://github.com/alistair-broomhead

    Args:
        type (_type_): _description_
    """

    _instances = {}

    def __call__(cls: object, *args: List, **kwargs: Dict[Any]) -> object:
        """_summary_

        Args:
            cls (object): _description_

        Returns:
            object: _description_
        """

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]
