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
from pickle import dumps, loads
from typing import Any

class Encoder:
    """Class representing the methods to inherit
    from."""

    @staticmethod
    def enc(data: Any) -> Any:
        """Encodes input data, and outputs
        encoded data.

        Args:
            data (Any): Original data.

        Returns:
            Any: Encoded data.
        """

        pass

    @staticmethod
    def dec(data: Any) -> Any:
        """Decodes input, encoded data and returns.

        Args:
            data (Any): Encoded data.

        Returns:
            Any: Decoded data.
        """

        pass

class Pickle(Encoder):
    """Wrapper for Pickle functions."""
    
    @staticmethod
    def enc(data: object) -> bytes:
        """Serialises data.

        Args:
            data (object): Object in which
            to serialise.
        """

        return dumps(data)

    @staticmethod
    def dec(data: bytes) -> Any:
        """Deserialises data.

        Args:
            data (Any): The serialised object
            in bytes.

        Returns:
            Any: The deserialised object.
        """

        return loads(data)
