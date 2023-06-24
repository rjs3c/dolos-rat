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

    def __init__(self: object, version: str) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        self._conf = {
            'app_geometry': '600x500',
            'app_title': f'DolosRAT { version }'
        }

def get_ctkinter_conf(version: str) -> CTkinterConfig:
    """_summary_

    Returns:
        CTkinterConfig: _description_
    """

    return CTkinterConfig(version)
