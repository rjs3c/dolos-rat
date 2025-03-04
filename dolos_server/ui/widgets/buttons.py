# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 24/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
# pylint: disable=too-many-ancestors
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
from typing import Any, Dict

# External Imports.
from customtkinter import CTkButton

class DefaultButton(CTkButton):
    """Represents a custom-styled CTkButton."""

    def __init__(
        self: object,
        master: Any,
        **kwargs: Dict[Any, Any]
    ) -> None:
        """Initialises 'DefaultButton'."""

        super().__init__(
            master,
            text='',
            corner_radius=10,
            border_width=1,
            border_color='#3d3f40',
            width=60,
            height=60,
            anchor='center',
            **kwargs,
        )

        if self.cget('state') == 'disabled':
            self.disable_btn()
        else:
            self.enable_btn()

    def enable_btn(self: object) -> None:
        """Enables the button, making this interactive."""

        self.configure(
            state='normal',
            fg_color='#106A43',
            hover_color='#17472E'
        )

    def disable_btn(self: object) -> None:
        """Renders the button inactive and greyed-out."""

        self.configure(
            state='disabled',
            fg_color='#181A1B'
        )

class DefaultButtonThin(CTkButton):
    """'DefaultButtonThin'"""

    def __init__(
        self: object,
        master: Any,
        **kwargs: Dict[Any, Any]
    ) -> None:
        """Initialises 'DefaultButtonThin'."""

        super().__init__(
            master,
            text='',
            corner_radius=10,
            border_width=1,
            border_color='#3d3f40',
            width=30,
            height=30,
            **kwargs,
        )

        if self.cget('state') == 'disabled':
            self.disable_btn()
        else:
            self.enable_btn()

    def enable_btn(self: object) -> None:
        """Enables button."""

        self.configure(
            state='normal',
            fg_color='#106A43',
            hover_color='#17472E'
        )

    def disable_btn(self: object) -> None:
        """Disables button."""

        self.configure(
            state='disabled',
            fg_color='#181A1B'
        )

class ListButton(CTkButton):
    """'ListButton'."""

    def __init__(
        self: object,
        master: Any,
        **kwargs: Dict[Any, Any]
    ) -> None:
        """Initialises 'ListButton'."""

        super().__init__(
            master,
            width=300,
            height=24,
            fg_color="transparent",
            compound="left",
            anchor="w",
            **kwargs
        )
