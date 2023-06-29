# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 25/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
...
"""

# Built-in/Generic Imports.
from typing import Any, Dict, List, Union
from pathlib import Path
from functools import partial

# External Imports.
from customtkinter import (
    CTkFrame,
    CTkTabview,
    CTkOptionMenu,
    CTkButton,
    CTkImage,
    CTkScrollableFrame,
    StringVar)
from PIL import Image # pylint: disable=import-error

# Modules.
from .buttons import DefaultButton # pylint: disable=relative-beyond-top-level
from ..commands.network import ( # pylint: disable=relative-beyond-top-level
    get_ifas,
    option_change_ifa,
    btn_collect_ipv4s
)

class TopLeftFrame(CTkFrame): # pylint: disable=too-many-ancestors
    """_summary_

    Args:
        CTkFrame (_type_): _description_
    """

    def __init__(
        self: object,
        master: Any,
        assets_dir: Path,
        **kwargs: Dict[Any, Any]
    ) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        super().__init__(master, **kwargs)

        self.grid_rowconfigure((0, 1), weight=0)
        self.grid_columnconfigure((0, 1, 2, 3), weight=0)

        # Comprises Path to assets directory.
        self._assets_dir = assets_dir

        # Icons.
        # Desktop icon.
        self._desktop_img_path: Union[None, CTkImage] = None
        # File icon.
        self._file_img_path: Union[None, CTkImage] = None
        # Keycap icon.
        self._keyboard_img_path: Union[None, CTkImage] = None
        # Command icon.
        self._cmd_img_path: Union[None, CTkImage] = None

        # Icons for buttons.
        self._render_icons()

        # Button widgets.
        self.btn_1: Union[None, CTkButton] = None
        self.btn_2: Union[None, CTkButton] = None
        self.btn_3: Union[None, CTkButton] = None
        self.btn_4: Union[None, CTkButton] = None

        # Render button widgets.
        self._create_widgets()
        self._position_widgets()

    def _create_widgets(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        # '' button.
        self.btn_1 = DefaultButton(
            self,
            state='disabled',
            image=self._desktop_img_path,
        )

        # '' button.
        self.btn_2 = DefaultButton(
            self,
            state='disabled',
            image=self._file_img_path
        )

        # '' button.
        self.btn_3 = DefaultButton(
            self,
            state='disabled',
            image=self._keyboard_img_path
        )

        # '' button.
        self.btn_4 = DefaultButton(
            self,
            state='disabled',
            image=self._cmd_img_path
        )

    def _position_widgets(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        self.btn_1.grid(row=0, column=0, padx=0, pady=0)
        self.btn_1.place(in_=self, relx=0.05, rely=0.17)

        self.btn_2.grid(row=0, column=1, padx=0, pady=0)
        self.btn_2.place(in_=self, relx=0.275, rely=0.17)

        self.btn_3.grid(row=0, column=2, padx=0, pady=0)
        self.btn_3.place(in_=self, relx=0.5, rely=0.17)

        self.btn_4.grid(row=0, column=3, padx=0, pady=0)
        self.btn_4.place(in_=self, relx=0.73, rely=0.17)

    def _render_icons(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        self._desktop_img_path = CTkImage(
            dark_image=Image.open(
                str(self._assets_dir) + '/desktop_img.png'
            ),
            size=(30, 30)
        )

        self._file_img_path = CTkImage(
            dark_image=Image.open(
                str(self._assets_dir) + '/files_img.png'
            ),
            size=(25, 30)
        )

        self._keyboard_img_path = CTkImage(
            dark_image=Image.open(
                str(self._assets_dir) + '/keycap_img.png'
            ),
            size=(30, 30)
        )

        self._cmd_img_path = CTkImage(
            dark_image=Image.open(
                str(self._assets_dir) + '/cmd_img.png'
            ),
            size=(30, 30)
        )

class LeftMiddleFrame(CTkFrame): # pylint: disable=too-many-ancestors
    """_summary_

    Args:
        CTkFrame (_type_): _description_
    """

    def __init__(
        self: object,
        master: Any,
        assets_dir: Path,
        **kwargs: Dict[Any, Any]
    ) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        super().__init__(master, **kwargs)

        self.grid_rowconfigure((0, 1), weight=0)
        self.grid_columnconfigure((0, 1, 2, 3), weight=0)

        # Comprises Path to assets directory.
        self._assets_dir = assets_dir

        # Icons for buttons.
        self._collect_img_path: Union[None, CTkImage] = None
        self._connect_img_path: Union[None, CTkImage] = None
        self._ping_img_path: Union[None, CTkImage] = None
        self._disconnect_img_path: Union[None, CTkImage] = None

        # Icons for buttons.
        self._render_icons()

        # Button widgets.
        self.btn_1: Union[None, CTkButton] = None
        self.btn_2: Union[None, CTkButton] = None
        self.btn_3: Union[None, CTkButton] = None
        self.btn_4: Union[None, CTkButton] = None

        self._create_widgets()
        self._position_widgets()

    def _create_widgets(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        # '' button.
        self.btn_1 = DefaultButton(
            self,
            state='normal',
            image=self._collect_img_path,
            command=partial(
                btn_collect_ipv4s,
                self.winfo_toplevel()
            )
        )

        # '' button.
        self.btn_2 = DefaultButton(
            self,
            state='disabled',
            image=self._connect_img_path,
        )

        # '' button.
        self.btn_3 = DefaultButton(
            self,
            state='disabled',
            image=self._ping_img_path
        )

        # '' button.
        self.btn_4 = DefaultButton(
            self,
            state='disabled',
            image=self._disconnect_img_path
        )

    def _position_widgets(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        self.btn_1.grid(row=0, column=0, padx=0, pady=0)
        self.btn_1.place(in_=self, relx=0.05, rely=0.17)

        self.btn_2.grid(row=0, column=0, padx=0, pady=0)
        self.btn_2.place(in_=self, relx=0.275, rely=0.17)

        self.btn_3.grid(row=0, column=1, padx=0, pady=0)
        self.btn_3.place(in_=self, relx=0.5, rely=0.17)

        self.btn_4.grid(row=0, column=2, padx=0, pady=0)
        self.btn_4.place(in_=self, relx=0.73, rely=0.17)

    def _render_icons(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        img_size = (30, 30)

        self._collect_img_path = CTkImage(
            dark_image=Image.open(
                str(self._assets_dir) + '/collect_img.png'
            ),
            size=img_size
        )

        self._connect_img_path = CTkImage(
            dark_image=Image.open(
                str(self._assets_dir) + '/connect_img.png'
            ),
            size=img_size
        )

        self._ping_img_path = CTkImage(
            dark_image=Image.open(
                str(self._assets_dir) + '/ping_img.png'
            ),
            size=img_size
        )

        self._disconnect_img_path = CTkImage(
            dark_image=Image.open(
                str(self._assets_dir) + '/disconnect_img.png'
            ),
            size=img_size
        )

class TopRightFrame(CTkScrollableFrame): # pylint: disable=too-many-ancestors
    """_summary_

    Credit: https://github.com/TomSchimansky/"""

    def __init__(self: object, master, command=None, **kwargs):
        """_summary_

        Args:
            master (_type_): _description_
            command (_type_, optional): _description_. Defaults to None.
        """

        super().__init__(master, **kwargs)

        # Grid configuration.
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = StringVar()
        self.button_list: List[Union[None, CTkButton]] = []

    def _create_btn_widget(self: object, text: str) -> CTkButton:
        """_summary_

        Args:
            self (object): _description_

        Returns:
            CTkButton: _description_
        """

        return CTkButton(
            master=self,
            text=text,
            width=300,
            height=24,
            fg_color="transparent",
            compound="left",
            anchor="w"
        )

    def add_item(self: object, item) -> None:
        """_summary_

        Args:
            self (object): _description_
            item (_type_): _description_
        """

        btn: CTkButton = self._create_btn_widget(item)

        if self.command is not None:
            btn.configure(command=lambda: self.command(item))

        btn.grid(row=len(self.button_list), column=0, pady=(0, 10), sticky="w")
        self.button_list.append(btn)

    def remove_item(self: object, item) -> None:
        """_summary_

        Args:
            item (_type_): _description_
        """

        for button in self.button_list:
            if item == button.cget("text"):
                button.destroy()
                self.button_list.remove(button)
                return

class BottomFrame(CTkTabview): # pylint: disable=abstract-method
    """_summary_

    Args:
        CTkFrame (_type_): _description_
    """

    def __init__(
        self: object,
        master: Any,
        **kwargs: Dict[Any, Any]
    ) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        super().__init__(master, **kwargs)

        # Tab configuration.
        self.add('Hex View')
        self.add('Text View')
        self.add('Natural View')

        # Frame 1 'Hex View'
        self.frame_1: Union[None, CTkFrame] = None
        # Frame 2 'Text View'
        self.frame_2: Union[None, CTkFrame] = None
        # Frame 3 'Natural View'
        self.frame_3: Union[None, CTkFrame] = None

        self._create_tab_frames()

    def _create_tab_frames(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        self.frame_1 = CTkFrame(master=self.tab('Hex View'))

class BottomInterfaceFrame(CTkFrame): # pylint: disable=too-many-ancestors
    """_summary_

    Args:
        CTkFrame (_type_): _description_
    """

    def __init__(
        self: object,
        master: Any,
        **kwargs: Dict[Any, Any]
    ) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        super().__init__(master, **kwargs)

        # Interface drop-down.
        self._interface_option: Union[None, CTkOptionMenu] = None

        self._create_widgets()
        self._position_widgets()

    def _create_widgets(self: object) -> None:
        """_summary_
        """

        self.interface_option = CTkOptionMenu(
            master=self,
            fg_color="#181A1B",
            values=get_ifas(),
            command=option_change_ifa
        )

    def _position_widgets(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        self.interface_option.grid(row=0, column=0)
