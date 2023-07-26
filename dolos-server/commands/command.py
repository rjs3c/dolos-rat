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
from abc import ABC, abstractmethod
from typing import Any

class Command(ABC):
    """_summary_

    Args:
        ABC (_type_): _description_
    """

    @abstractmethod
    def execute(self: object) -> Any:
        """_summary_

        Args:
            self (object): _description_

        Returns:
            Any: _description_
        """

        pass
