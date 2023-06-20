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
import logging
import logging.config
import logging.handlers

from enum import Enum
from typing import Any, Union
from os import PathLike
from pathlib import Path

# Modules.
from config.logger import LoggerConfig
from .wrapper import BaseWrapper

class LoggerLevel(str, Enum):
    """An enum comprising available logging levels
    from 'logging'."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    NOTSET = "notset"

    @classmethod
    def value_in(cls: object, val: Any) -> bool:
        """_summary_

        Args:
            val (_type_): _description_

        Raises:
            get_logger_err: _description_

        Returns:
            _type_: _description_
        """
        return val in cls._value2member_map_

class LoggerWrapper(BaseWrapper):
    """Provides wrapper for easily
    interfacing with 'logger' library.
    """

    # Comprises path for 'logs' directory.
    # _LOG_PATH: Union[str, PathLike] = Path("../logs")

    def __init__(
        self: object,
        logger_name: str,
        logger_conf: LoggerConfig) -> None:
        """Initialises LoggerWrapper.
        """
        self._logger_name = logger_name
        self._logger_conf = logger_conf
        self._logger: Union[Any, logging.Logger] = None

        self._get_logger()

    def __del__(self: object) -> None:
        """Destroys logging-specific handles and
        releases resources.
        """
        self._logger = None
        del self

    def _get_logger(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """
        try:
            # Configure 'logging' library via dictConfig(),
            # using the LoggerConf _conf field.
            logging.config.dictConfig(self._logger_conf._conf)

            # Creates new logger, and assigns to handle
            # _logger.
            self._logger = logging.getLogger(self._logger_name)
        # Exceptions raised from using dictConfig.
        except ValueError as get_logger_err:
            raise get_logger_err

    def write_log(self: object, log_msg: str, log_level: LoggerLevel) -> None:
        """Generates a log of a supplied level.

        Args:
            self (object): _description_
        """
        # Check if supplied log_level is
        # valid logging level.
        if LoggerLevel.value_in(log_level):
            # Evaluate corresponding logging
            # method (i.e., .info(), etc.)
            getattr(self._logger, log_level)(log_msg)
        else: pass

def get_logger(logger_name: str, logger_conf: LoggerConfig) -> LoggerWrapper:
    """Returns an instantiated LoggerWrapper.

    Returns:
        _type_: Instantiated form of LoggerWrapper.
    """
    return LoggerWrapper(logger_name, logger_conf)
