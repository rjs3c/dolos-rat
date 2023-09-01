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
    """Houses CTK configuration."""

    # Dict comprising CTK-specific
    # configuration.
    _conf: Dict[str, Any]

    def __init__(
        self: object,
        version: str,
        assets_path: Path,
        admin_privs: bool
    ) -> None:
        """Initialises CTkinterConfig"""

        # Version no. of DolosRAT.
        self.version = version

        # Dictionary of configuration names/values.
        self._conf = {
            'app_geometry': '700x560',
            'app_title': f'DolosRAT (v{ self.version })',
            'app_assets_dir': assets_path,
            'app_admin': admin_privs
        }

def get_ctkinter_conf(version: str, assets_path: Path, admin_privs: bool) -> CTkinterConfig:
    """Returns instance of CTkinterConfig.

    Args:
        version (str): Version number of DolosRAT.
        assets_path (Path): Absolute path of assets/ directory.
        admin_privs (bool): Boolean indicating whether DolosRAT
        was executed in privileged context.

    Returns:
        CTkinterConfig: Instance of CTkinterConfig.
    """

    return CTkinterConfig(version, assets_path, admin_privs)
