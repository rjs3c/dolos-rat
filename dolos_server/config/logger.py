# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 07/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
from dataclasses import dataclass
from typing import Any, Dict

# Modules.
from config import Config

@dataclass
class LoggerConfig(Config):
    """Stores logging-specific configuration."""

    # Dict comprising dictConfig() configuration.
    _conf: Dict[str, Any]

    def __init__(self: object, logger_name: str) -> None:
        """Initialises LoggerConfig class
        and configures initial _conf value.
        """

        self._conf = {
            'logger_name': logger_name,
            'logging_dictconf': {
                'version': 1,
                'formatters': {
                    'standard': {
                        'format': '%(asctime)s (%(module)s) [%(levelname)s] %(name)s: %(message)s',
                        'date_fmt': '%d-%m-%Y %I:%M:%S'
                    }
                },
                'loggers': {
                    f'__main__': {
                        'handlers': ['console.info'],
                        'level': 'INFO', 
                        'propagate': True
                    }
                },
                'handlers': {
                    'console.info': {
                        'class': 'logging.StreamHandler',
                        'level': 'INFO',
                        'formatter': 'standard',
                        'stream': 'ext://sys.stdout'
                    }
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
