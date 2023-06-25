# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 24/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
...
"""

# Built-in/Generic Imports.
from typing import Any, Dict

# External Imports.
from tksvg import SvgImage
from customtkinter import CTkFrame, CTkLabel, CTkFont, CTkButton

class Frame:
    """_summary_
    """

    def __init__(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        pass

    def get_svg(self: object, svg_path: str) -> SvgImage:
        """_summary_

        Args:
            self (object): _description_
            svg_path (str): _description_

        Returns:
            SvgImage: _description_
        """

        return SvgImage(file=svg_path)

class TopLeftFrame(CTkFrame):
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

        # SVGs for buttons.
        self._desktop_img_path = 'dolosrat/assets/desktop.svg'
        self.file_img_path = 'dolosrat/assets/files.svg'
        self._keyboard_typing_img_path = 'dolosrat/assets/keyboard-typing.svg'

        # Addition of widgets.
        self.label_1 = CTkLabel(
            self,
            text="Victim Commands",
            font=CTkFont(
                family='Segoe UI',
                size=14,
                weight='bold',
            ),
        )
        self.label_1.grid(row=0, column=0, padx=10, sticky='N')

        # '' button.
        self.btn_1 = CTkButton(
            self, text='Test',
            state='disabled',
            corner_radius=5,
            fg_color="#181A1B",
            width=100,
            height=23
        )
        self.btn_1.grid(row=0, column=1, padx=0, pady=0)
        self.btn_1.place(in_=self, relx=0.02, rely=0.20)

        # '' button.
        self.btn_2 = CTkButton(
            self,
            text='Test 2',
            state='disabled',
            corner_radius=5,
            fg_color="#181A1B",
            width=100,
            height=23
        )
        self.btn_2.grid(row=0, column=1, padx=0, pady=0)
        self.btn_2.place(in_=self, relx=0.35, rely=0.20)

        # '' button.
        self.btn_3 = CTkButton(
            self,
            text='Test 3',
            state='disabled',
            corner_radius=5,
            fg_color="#181A1B",
            width=100,
            height=23
        )
        self.btn_3.grid(row=0, column=1, padx=0, pady=0)
        self.btn_3.place(in_=self, relx=0.68, rely=0.20)

        # '' button.
        self.btn_4 = CTkButton(
            self,
            text='Test',
            state='disabled',
            corner_radius=5,
            fg_color="#181A1B",
            width=100,
            height=23
        )
        self.btn_4.grid(row=0, column=1, padx=0, pady=0)
        self.btn_4.place(in_=self, relx=0.02, rely=0.37)

        # '' button.
        self.btn_5 = CTkButton(
            self,
            text='Test 2',
            state='disabled',
            corner_radius=5,
            fg_color="#181A1B",
            width=100,
            height=23
        )
        self.btn_5.grid(row=0, column=1, padx=0, pady=0)
        self.btn_5.place(in_=self, relx=0.35, rely=0.37)

        # '' button.
        self.btn_6 = CTkButton(
            self,
            text='Test 3',
            state='disabled',
            corner_radius=5,
            fg_color="#181A1B",
            width=100,
            height=23
        )
        self.btn_6.grid(row=0, column=1, padx=0, pady=0)
        self.btn_6.place(in_=self, relx=0.68, rely=0.37)

class LeftMiddleFrame(CTkFrame):
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

        # Addition of widgets.
        self.label_1 = CTkLabel(
            self,
            text="Victim Actions",
            font=CTkFont(
                family='Segoe UI',
                size=14,
                weight='bold',
            ),
            # fg_color='blue'
            # width=300,
            # height=30,
            # bg_color='5A5A5A',
            # corner_radius=10
        )
        self.label_1.grid(row=0, column=0, padx=10, sticky='N')

class TopRightFrame(CTkFrame):
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

        # Addition of widgets.
        self.label_1 = CTkLabel(self, text="Victim Actions")
        self.label_1.grid(row=0, column=0, sticky='NE')

class BottomFrame(CTkFrame):
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

        # Addition of widgets.
        self.label_1 = CTkLabel(self, text="Victim Actions")
        self.label_1.grid(row=0, column=0, sticky='NE')
