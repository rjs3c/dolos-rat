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
from typing import Any, Dict, List, Optional, Union

# Modules.
from config import Config

class BaseWrapper:
    """_summary_
    """

    def __init__(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        # List of all handles. Easy to manage,
        # quick to iterate, easy to clear.
        self._handles: List[object] = []

        # Handles objects that inherit Config.
        self._conf: Optional[Config] = None

    def __del__(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        # Clear all registered handles for
        # garbage collection.
        self._handles.clear()
        del self

    def _handle_in(self: object, handle_name: str) -> bool:
        """_summary_

        Args:
            self (object): _description_
            handle_name (str): _description_

        Returns:
            bool: _description_
        """

        # Iterates list of handles.
        for handle in self._handles:
            # Object name matches that queried.
            if handle.__class__.__name__ == handle_name:
                return True

        # Defaults to False.
        return False

    def _get_handle(self: object, handle_name: str) -> Union[None, object]:
        """_summary_

        Args:
            self (object): _description_

        Returns:
            object: _description_
        """

        # Handle + list index from _handles.
        for idx, handle in enumerate(self._handles):
            # Object name and queried name match.
            if handle.__class__.__name__ == handle_name:
                return self._handles[idx]

        # Defaults to None.
        return None

    def _register_handle(self: object, handle: object) -> None:
        """_summary_

        Args:
            self (object): _description_
            handle (object): _description_

        Returns:
            _type_: _description_
        """

        # Adds new handle onto list of handles.
        self._handles.append(handle)

    @property
    def conf(self: object) -> Dict[Any, Any]:
        """_summary_

        Args:
            self (object): _description_

        Returns:
            [Dict[Any, Any]]: _description_
        """

        return self._conf

    @conf.setter
    def conf(self: object, config: Dict[Any, Any]) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        self._conf = config
