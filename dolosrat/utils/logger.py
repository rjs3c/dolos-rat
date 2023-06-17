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
import logging.config
import logging.handlers
from typing import Any, Union
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

            # Creates new logger, and assings to handle
            # _logger.
            self._logger = logging.getLogger(self._logger_name)
        # Exceptions raised from using dictConfig.
        except ValueError as get_logger_err:
            raise get_logger_err

    def _write_log(self: object) -> None: 
        """Generates a log of a supplied level.

        Args:
            self (object): _description_
        """
        

def get_logger(logger_name: str, logger_conf: LoggerConfig) -> LoggerWrapper:
    """Returns an instantiated LoggerWrapper.

    Returns:
        _type_: Instantiated form of LoggerWrapper.
    """
    return LoggerWrapper(logger_name, logger_conf)
