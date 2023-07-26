# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 06/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
import sys
import time
from typing import Any, Dict, Union
from pathlib import Path

# Modules.
# Configuration classes.
from config.config import Config # pylint: disable=import-error
from config.logger import get_logger_conf # pylint: disable=import-error
from config.ctkinter import get_ctkinter_conf # pylint: disable=import-error
# Other utilities.
from utils.net.interface import IfaWrapper, get_ifa_wrapper # pylint: disable=import-error
from utils.misc.logger import LoggerWrapper, LoggerLevel, get_logger # pylint: disable=import-error
from utils.misc.os import check_admin_privs # pylint: disable=import-error
from ui.ctk import get_ctkinter_app # pylint: disable=import-error

(__appname__,
 __author__,
 __licence__,
 __version__) = 'DolosRAT', 'Ryan I.', 'MIT License', '1.0'

__copyright__ = f""""
{__licence__}

Copyright (c) 2023 {__author__}.

Permission is hereby granted, free of charge, to any person obtaining a copy
import typing
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Initial class housing primary DolosRAT logic.
class DolosServer:
    """Houses the logic pertinent to the running
    application. This is responsible for initialising
    the neccessary, internal modules of the application
    and interfacing between each of these.
    """

    def __init__(
        self: object, config: Dict[str, Any]
    ) -> None:
        """Initialises DolosRAT class.

        Configures other, internal modules of DolosRAT.
        """

        self._config: Dict[str, Any] = config

        # Logger handle.
        self._logger: Union[Any, LoggerWrapper] = None

        # IfaWrapper handle.
        self._net_wrapper: Union[Any, IfaWrapper]

        # Used to calculate time taken to initialise.
        self._strt_time: float = time.time()

        # Set-up application logging.
        self._init_logger()

        # Perform networking set-up.
        self._init_net()

    def __del__(self: object) -> None:
        """Destructs DolosRAT class.

        The purpose of this is to destroy existing handles
        to modules and release other resources.
        """

        # Write log to inform of shutting down.
        self._logger.write_log(
            "DolosRAT shutting down.", 
            LoggerLevel.WARNING
        )

        # Releases handles to module objects.
        self._net_wrapper = self._logger = None
        del self

    def _init_logger(self: object) -> None:
        """Creates handle to logging wrapper class.

        Creates a handle to the class exposing methods
        to write application logs, etc.
        """

        # Create handle to LoggerWrapper.
        self._logger = get_logger(
            self._config['logger_conf']
        )

        self._logger.write_log(
            "DolosRAT initialisation started.", 
            LoggerLevel.INFO
        )

    def _init_tkinter(self: object) -> None:
        """Creates handle to Tkinter wrapper class.
        
        Creates a handle to the class providing a 
        wrapper to Tkinter and producing the UI.
        """

        # Create log to inform that the UI in
        # CTkinter is being set-up.
        self._logger.write_log(
            "Generating and rendering DolosRAT UI.", 
            LoggerLevel.INFO
        )

        # Create handle for and initialise
        # App class for CTK.
        get_ctkinter_app(
            self._config['ctk_conf']
        ).mainloop()

    def _init_net(self: object) -> None:
        """Initialises functionality for enumerating
        network interfaces.
        """

        # Creates wrapper for IfaWrapper.
        self._net_wrapper = get_ifa_wrapper()

    def _run(self: object) -> None:
        """Officially starts the internal modules.

        With handles created for the classes pertinent
        to the application, use these to commence DolosRAT.
        """

        # Time-based statistics.
        self._logger.write_log(
            f"DolosRAT initialised in { time.time() - self._strt_time }.", 
            LoggerLevel.INFO
        )

        # Checks if running as administrator/root, as
        # capturing on interface (privileged) is
        # neccessary.
        if check_admin_privs() is False:
            self._logger.write_log(
                "DolosRAT running in unprivileged mode. Continuing.", 
                LoggerLevel.WARNING
            )

        # Generate and render UI using
        # CustomTkinter.
        self._init_tkinter()

    def start(self: object) -> None:
        """Exposed method for 'starting' DolosRAT.

        This creates the neccessary handles, and 
        evaluate the method for responsible for 
        the primary logic (_run()).
        """

        # Initialise.
        self._run()

if __name__ == '__main__':

    # Houses configuration for 'DolosRAT' class.
    dolos_config: Dict[str, Config] = {}

    # Populate 'dolos_config' with configurations.
    dolos_config = {
       'logger_conf': get_logger_conf(__name__),
       'ctk_conf': get_ctkinter_conf(
           __version__,
           Path.joinpath(
               Path(__file__).parent.parent, 'dolos-server', 'assets'
            ),
           check_admin_privs()
        )
    }

    # Application entry-point.
    DolosServer(dolos_config).start()

    # Gracefully exit.
    sys.exit(0)
