# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 24/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
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
        self.label_1 = CTkLabel(master=self.tab('Tab 1'))
        self.label_1.grid(row=0, column=0, padx=20, pady=10)
        
        self.label_2 = CTkLabel(master=self.tab('Tab 2'))
        self.label_2.grid(row=0, column=0, padx=20, pady=10)
