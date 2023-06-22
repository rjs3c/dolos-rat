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
from pprint import pformat
from enum import Enum
from typing import Any, Optional
# from os import PathLike
# from pathlib import Path

# Modules.
from config.logger import LoggerConfig
from .wrapper import BaseWrapper

class LoggerLevel(str, Enum):
    """An enum comprising available logging levels
    from 'logging'."""

    # Logging levels, accordant with Syslog.
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

    def __init__(self: object, logger_conf: Optional[LoggerConfig] = None) -> None:
        """Initialises LoggerWrapper.
        """

        super().__init__()

        # Houses the logging configuration.
        self.conf = logger_conf

        # Creates logging handle.
        self._get_logger()

    def _get_logger(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        try:
            # Configure 'logging' library via dictConfig(),
            # using the LoggerConf _conf field.
            if self.conf._conf['logger_name'] == '__main__':
                logging.config.dictConfig(
                    self.conf._conf['logging_dictconf']
                )

            # Creates new logger, and assigns to handle
            # _logger.
            self._register_handle(logging.getLogger(
                self.conf._conf['logger_name']
            ))
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
            getattr(self._get_handle('Logger'), log_level)(pformat(log_msg))
        else: pass

def get_logger(logger_conf: LoggerConfig) -> LoggerWrapper:
    """Returns an instantiated LoggerWrapper.

    Returns:
        _type_: Instantiated form of LoggerWrapper.
    """

    return LoggerWrapper(logger_conf)
