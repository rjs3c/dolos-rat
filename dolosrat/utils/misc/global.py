# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 26/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
...
"""

# Built-in/Generic Imports.
from typing import Union
# from multiprocessing.pool import ThreadPool

# Modules.
from config.network import NetworkConfig

class Manager:
    """_summary_
    """

    def __init__(
        self: object
    ) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        # Houses networking configuration, settings,
        # and output.
        self._network_conf: Union[None, NetworkConfig] = None

    @property
    def network_conf(self: object) -> NetworkConfig:
        """_summary_

        Args:
            self (object): _description_

        Returns:
            NetworkConfig: _description_
        """

        return self._network_conf

    @network_conf.setter
    def network_conf(self: object, network_conf: NetworkConfig) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        self._network_conf = network_conf

# Making use of Python's singleton nature.
manager = Manager()
