# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 06/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
...
"""

# Built-in/Generic Imports.
from dataclasses import dataclass
from typing import Any, Dict

# Modules.
from config import Config

class NetworkConfig(Config):
    """_summary_

    Args:
        Config (_type_): _description_
    """
    
    # Dict comprising network configuration.
    _conf: Dict[str, Any]

    def __init__(self: object) -> None: ...
