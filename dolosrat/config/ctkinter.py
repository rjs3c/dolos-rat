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
from typing import Any, Dict, Optional

# Modules.
from config import Config

@dataclass
class CTkinterConfig(Config):
    """_summary_

    Args:
        Config (_type_): _description_
    """

    # Dict comprising CTK-specific
    # configuration.
    _conf: Dict[str, Any]

    def __init__(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        self._conf = {
            'app_geometry': '600x500',
            'app_title': 'DolosRAT'
        }

def get_ctkinter_conf() -> CTkinterConfig:
    """_summary_

    Returns:
        CTkinterConfig: _description_
    """
    
    return CTkinterConfig()