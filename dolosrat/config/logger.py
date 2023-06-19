# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 07/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
Inherited from 'Config', stores logging-specific 
configuration for use within the built-in 'logging'
module.
"""

# Built-in/Generic Imports.
from dataclasses import dataclass
from time import time
from typing import Any, Dict

# Modules.
from config import Config

@dataclass
class LoggerConfig(Config):
    """Stores logging-specific configuration.
    """

    # Dict comprising dictConfig() configuration.
    _conf: Dict[str, Any]

    def __init__(self: object, logger_name: str) -> None:
        """Initialises LoggerConfig class
        and configures initial _conf value.
        """
        self._conf = {
            'version': 1,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s (%(module)s) [%(levelname)s] %(name)s: %(message)s',
                    'date_fmt': '%d-%m-%Y %I:%M:%S'
                }
            },
            'loggers': {
                f'{logger_name}': {
                    'handlers': ['file'],
                    'level': 'INFO', 
                    'propagate': True
                }
            },
            'handlers': {
                'file': {
                    'class': 'logging.FileHandler',
                    'level': 'INFO',
                    'formatter': 'standard',
                    'filename': f'dolosrat/logs/log-{int(time())}.log',
                    'mode': 'a',
                    'encoding': 'utf-8'
                }
            }
        }

# Instantiates 'LoggerConfig' and returns this.
def get_logger_conf(logger_name: str = __name__) -> LoggerConfig:
    """Exposes function to instantiate and 
    return LoggerConfig.

    Args:
        logger_name (str): A unique name to denote the
        specific logger in use.

    Returns:
        LoggerConfig: A new instance of LoggerConfig.
    """
    return LoggerConfig(logger_name)
