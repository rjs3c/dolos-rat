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
from customtkinter import CTkButton

class DefaultButton(CTkButton): # pylint: disable=too-many-ancestors
    """_summary_
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

        super().__init__(
            master,
            text='',
            corner_radius=10,
            # fg_color='#181A1B',
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
        """_summary_

        Args:
            self (object): _description_
        """

        self.configure(
            state='normal',
            fg_color='#106A43',
            hover_color='#17472E'
        )

    def disable_btn(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        self.configure(
            state='disabled',
            fg_color='#181A1B'
        )
