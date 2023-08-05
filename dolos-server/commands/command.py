# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 17/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
from importlib import import_module
from typing import Any, List, Union
from os import getcwd, pardir, path as os_path
from sys import path as sys_path

# print(os_path.join(os_path.dirname(__file__), pardir))

class Command():
    """_summary_

    Args:
        ABC (_type_): _description_
    """

    def __init__(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_

        Returns:
            Any: _description_
        """

        self._mods: List[Any] = []

        # sys_path.append(os_path.join(os_path.dirname(__file__), pardir))

    def get_dep(self: object, mod_name: str) -> Union[Any, None]:
        """_summary_

        Args:
            self (object): _description_
            mod_name (str): _description_

        Returns:
            bool: _description_
        """

        for idx, dep in enumerate(self._mods):
            if dep.__name__ == mod_name:
                return self._mods[idx]

        return None

    def create_deps(self: object, *mods: List[str]) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        try:
            for mod in mods:
                self._mods.append(import_module(mod))
        except ModuleNotFoundError:
            pass
        
    # @staticmethod
    # def mainify_mod(obj: object) -> None:
    #     """_summary_

    #     Args:
    #         obj (object): _description_
    #     """

        # if obj.__module__ != '__main__':
        #     import __main__

    def execute(self: object) -> Any:
        """_summary_

        Args:
            self (object): _description_

        Returns:
            Any: _description_
        """

        pass

# class ScreenshotCommand(Command):
#     """_summary_

#     Args:
#         Command (_type_): _description_
#     """

#     def __init__(self: object) -> None:
#         """_summary_

#         Args:
#             self (object): _description_

#         Returns:
#             Any: _description_
#         """

#         # Initialise from Command parent.
#         super().__init__()

#         # Create list of imported dependencies.
#         self.create_deps('PIL.ImageGrab')

#     def execute(self: object) -> bytes:
#         """_summary_

#         Args:
#             self (object): _description_

#         Returns:
#             Any: _description_
#         """

#         # Create bytearray to store bytes for
#         # screen capture.
#         img_bytes = BytesIO()

#         # Create image capture, in PNG format.
#         img_capture = getattr(self.get_dep('PIL.ImageGrab'),'grab')(all_screens=True)
#         img_capture.save(img_bytes, 'PNG')

#         # Return bytes in byte array.
#         return img_bytes.getvalue()
