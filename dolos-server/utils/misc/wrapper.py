# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 20/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
from typing import Any, Dict, List, Optional, Union

# Modules.
from config import Config # pylint: disable=import-error

class BaseWrapper:
    """Provides methods for inheriting wrappers."""

    def __init__(self: object) -> None:
        """Initialises BaseWrapper, declares list of handles
        and configuration (if required)."""

        # List of all handles. Easy to manage,
        # quick to iterate, easy to clear.
        self._handles: List[object] = []

        # Handles objects that inherit Config.
        self._conf: Optional[Config] = None

    def __del__(self: object) -> None:
        """Cleares list of handles for garbage
        collection."""

        # Clear all registered handles for
        # garbage collection.
        self._handles.clear()
        del self

    def _handle_in(self: object, handle_name: str) -> bool:
        """Checks if handle exists in currently-registered
        handles by handle name.

        Args:
            handle_name (str): __class__.__name__

        Returns:
            bool: True/False regarding whether handle is
            found in list.
        """

        # Iterates list of handles.
        for handle in self._handles:
            # Object name matches that queried.
            if handle.__class__.__name__ == handle_name:
                return True

        # Defaults to False.
        return False

    def _get_handle(self: object, handle_name: str) -> Union[None, object]:
        """Returns handle by __class__.__name__

        Returns:
            object: Returns desired handle (if present
            in list).
        """

        # Handle + list index from _handles.
        for idx, handle in enumerate(self._handles):
            # Object name and queried name match.
            if handle.__class__.__name__ == handle_name:
                return self._handles[idx]

        # Defaults to None.
        return None

    def _register_handle(self: object, handle: object) -> None:
        """Adds handle to list of handles for simple
        access.

        Args:
            handle (object): The object in which to add."""

        # Adds new handle onto list of handles.
        self._handles.append(handle)

    @property
    def conf(self: object) -> Dict[Any, Any]:
        """Returns the configuration of the wrapper
        class.

        Returns:
            [Dict[Any, Any]]: A dictionary representing the
            wrapper configuration.
        """

        return self._conf

    @conf.setter
    def conf(self: object, config: Dict[Any, Any]) -> None:
        """Sets the configuration of the wrapper
        (if required)."""

        self._conf = config
