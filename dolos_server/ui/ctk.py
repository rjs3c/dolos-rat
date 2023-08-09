# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 25/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
from typing import Union

# Modules.
from config.ctkinter import CTkinterConfig # pylint: disable=import-error
from .widgets.frames import (
    TopLeftFrame,
    TopRightFrame,
    LeftMiddleFrame,
    BottomFrame,
    BottomInterfaceFrame
)

# External Imports.
import customtkinter # pylint: disable=wrong-import-order

# Global configurations for CTK application
# appearance.
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

class App(customtkinter.CTk):
    """_summary_
    """

    def __init__(
        self: object,
        ctkinter_conf: CTkinterConfig
    ) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        super().__init__()

        # Houses CTkinterConfig.
        self.conf = ctkinter_conf

        # Sets the sizing of the window.
        self.geometry(self.conf.conf['app_geometry'])

        # No fullscreen.
        self.resizable(False, False)

        # Sets the title of the window.
        self.title(self.conf.conf['app_title'])

        # Grid layout.
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1), weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)

        # Tabbing.
        # self.tab_view = TabView(master=self)
        # self.tab_view.grid(row=0, column=0, padx=20, pady=20)

        # Top-left frame.
        self.top_col_frame_1: Union[None, TopLeftFrame] = None
        self._add_frame1_widget()

        # Top-right frame.
        self.top_col_frame_2: Union[None, LeftMiddleFrame] = None
        self._add_frame2_widget()

        # Left-middle frame.
        self.top_col_frame_3: Union[None, TopRightFrame] = None
        self._add_frame3_widget()

        # Bottom frame.
        self.bottom_col_frame: Union[None, TopRightFrame] = None
        self._add_frame4_widget()

        # Bottom interface frame
        self.bottom_int_frame: Union[None, TopRightFrame] = None
        self._add_frame5_widget()

    def _add_frame1_widget(self: object) -> None:
        """_summary_
        """

        # Top-left frame.
        self.top_col_frame_1 = TopLeftFrame(
            master=self,
            height=20,
            border_width=1,
            border_color='black',
            assets_dir=self.conf._conf['app_assets_dir'],
            corner_radius=10,
        )
        self.top_col_frame_1.grid(
            row=0, column=0, columnspan=1, padx=20, pady=(20, 0), sticky="nsew"
            )
        self.top_col_frame_1.grid_rowconfigure(0, weight=0)

    def _add_frame2_widget(self: object) -> None:
        """_summary_
        """

        self.top_col_frame_2 = LeftMiddleFrame(
            master=self,
            height=20,
            border_width=1,
            border_color='black',
            assets_dir=self.conf._conf['app_assets_dir'],
            corner_radius=10
        )
        self.top_col_frame_2.grid(
            row=1, column=0, columnspan=1, padx=20, pady=(20, 0), sticky="nsew"
        )
        self.top_col_frame_2.grid_rowconfigure(0, weight=1)

    def _add_frame3_widget(self: object) -> None:
        """_summary_
        """

        self.top_col_frame_3 = TopRightFrame(
            self,
            border_width=1,
            border_color='black',
            corner_radius=10
        )
        self.top_col_frame_3.grid(
            row=0, column=1, columnspan=1, rowspan=2, padx=20, pady=(20, 0), sticky="nsew"
        )
        self.top_col_frame_3.grid_rowconfigure(0, weight=1)

    def _add_frame4_widget(self: object) -> None:
        """_summary_
        """

        self.bottom_col_frame = BottomFrame(
            self,
            height=200,
            border_width=1,
            border_color='black',
            segmented_button_selected_color="#181A1B",
            segmented_button_selected_hover_color="#181A1B",
            corner_radius=10
        )
        self.bottom_col_frame.grid(
            row=2, column=0, columnspan=2, padx=20, pady=(0, 15), sticky="nsew"
        )
        self.bottom_col_frame.grid_rowconfigure(0, weight=1)

    def _add_frame5_widget(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        self.bottom_int_frame = BottomInterfaceFrame(
            self,
            height=30,
            corner_radius=10
        )
        self.bottom_int_frame.grid(
            row=3, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="nsew"
        )
        self.bottom_int_frame.grid_rowconfigure(0, weight=0)

def get_ctkinter_app(ctkinter_conf: CTkinterConfig) -> None:
    """_summary_

    Args:
        tkinter_conf (_type_): _description_
    """

    return App(
        ctkinter_conf
    )
