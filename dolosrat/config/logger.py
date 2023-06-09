# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 07/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
Inherited from 'Config', stores logging-specific 
configuration for use within the built-in 'logging'
module.
"""

# Built-in/Generic Imports.
from dataclasses import dataclass
from typing import Any, Dict

# Modules.
from config import Config

@dataclass
class LoggerConfig(Config): 

    """ Dict comprising dictConfig() configuration. """
    _conf: Dict[str, Any]

    def __init__(self: object) -> None:
        """Initialises LoggerConfig class
        and configures initial _conf value.
        """
        self._conf = {} 