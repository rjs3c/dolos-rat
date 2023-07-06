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
from customtkinter import CTkTabview, CTkLabel

class TabView(CTkTabview):
    """_summary_

    Args:
        CTkTabview (_type_): _description_
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

        # Establish application tabs.
        self.add('Tab 1')
        self.add('Tab 2')

        # Set default tab.
        self.set('Tab 1')

        # Add labelling widget to tabs.
        self.label = CTkLabel(master=self.tab('Tab 1'))
        self.label.grid(row=0, column=0, padx=20, pady=10)
