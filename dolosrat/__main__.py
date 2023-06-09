# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 06/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
DolosRAT provides a GUI-based RAT client and server, purposed for demonstrating
techniques frequently used within scammer take-down operations. Please note that
the use of this tool is for educational purposes only.
"""

# Built-in/Generic Imports.
import sys

(__appname__,
 __author__,
 __licence__,
 __version__) = 'DolosRAT', 'Ryan I.', 'MIT License', '1.0'

__copyright__ = f""""
{__licence__}

Copyright (c) 2023 {__author__}.

Permission is hereby granted, free of charge, to any person obtaining a copy
import typing
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Initial class housing primary DolosRAT logic.
class DolosRAT(object):
    """Houses the logic pertinent to the running
    application. This is responsible for initialising
    the neccessary, internal modules of the application
    and interfacing between each of these.
    """

    def __init__(self: object) -> None: 
        """Initialises DolosRAT class.

        Configures other, internal modules of DolosRAT.
        """
        ...
        
    def __del__(self: object) -> None:
        """Destructs DolosRAT class.

        The purpose of this is to destroy existing handles
        to modules and release other resources.
        """
        ...

if __name__ == '__main__':
    # Application entry-point.
    DolosRAT()
    
    # Gracefully exit.
    sys.exit(0)