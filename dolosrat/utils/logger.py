# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 07/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
Provides functionality to supplement application
logging and auditing.
"""

# Built-in/Generic Imports.
from typing import Union
from os import PathLike
from pathlib import Path

# Modules.
from config.logger import LoggerConfig

class LoggerWrapper:
    """Provides wrapper for easily
    interfacing with 'logger' library.
    """

    # Comprises path for 'logs' directory.
    _LOG_PATH: Union[str, PathLike] = Path("../logs")

    def __init__(self: object) -> None:
        """Initialises LoggerWrapper.
        """
        ...

    def __del__(self: object) -> None:
        """Destroys logging-specific handles and
        releases resources.
        """
        ...

def get_logger(logger_conf: LoggerConfig) -> LoggerWrapper: 
    """Returns an instantiated LoggerWrapper.

    Returns:
        _type_: Instantiated form of LoggerWrapper.
    """

    # ...
    return LoggerWrapper()
