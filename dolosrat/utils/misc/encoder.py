# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 17/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
"""

# Built-in/Generic Imports.
from pickle import dumps, loads
from typing import Any

class Encode:
    """_summary_

    Returns:
        _type_: _description_
    """

    @staticmethod
    def enc(data: Any) -> Any:
        """_summary_

        Args:
            data (Any): _description_

        Returns:
            Any: _description_
        """

        pass

    @staticmethod
    def dec(data: Any) -> Any:
        """_summary_

        Args:
            data (Any): _description_

        Returns:
            Any: _description_
        """

        pass

class Pickle(Encode):
    """_summary_
    """
    @staticmethod
    def enc(data: object) -> bytes:
        """_summary_

        Args:
            data (object): _description_
        """

        return dumps(data)

    @staticmethod
    def dec(data: bytes) -> Any:
        """_summary_

        Args:
            data (Any): _description_

        Returns:
            Any: _description_
        """

        return loads(data)
