# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 06/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
from dataclasses import dataclass
from typing import Any, Dict
from pathlib import Path

# Modules.
from config import Config # pylint: disable=import-error

@dataclass
class CTkinterConfig(Config):
    """_summary_

    Args:
        Config (_type_): _description_
    """

    # Dict comprising CTK-specific
    # configuration.
    _conf: Dict[str, Any]

    def __init__(
        self: object,
        version: str,
        assets_path: Path,
        admin_privs: bool
    ) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        # Version no. of DolosRAT.
        self.version = version

        self._conf = {
            'app_geometry': '700x500',
            'app_title': f'DolosRAT { self.version }',
            'app_assets_dir': assets_path,
            'app_admin': admin_privs
        }

def get_ctkinter_conf(version: str, assets_path: Path, admin_privs: bool) -> CTkinterConfig:
    """_summary_

    Returns:
        CTkinterConfig: _description_
    """

    return CTkinterConfig(version, assets_path, admin_privs)
