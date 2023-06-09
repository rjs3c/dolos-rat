# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 07/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
Houses the primary configuration for DolosRAT. 
Provides a class wherein child configs can inherit and
provide functionality-specific configurations.
"""

# Built-in/Generic Imports.
from dataclasses import dataclass
from typing import Any

@dataclass
class Config: 
    """Stores application and functionality-specific
    config. Specific configurations shall inherit from this
    base class, overriding _conf, and other functions, as 
    neccessary.
    """

    """ ... """
    _conf: Any