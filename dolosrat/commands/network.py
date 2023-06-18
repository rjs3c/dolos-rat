# !/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Creator : Ryan I.
# Created Date: 18/06/2023
# version ='1.0'
# ---------------------------------------------------------------------------
"""
...
"""

# Built-in/Generic Imports.
from typing import Set, Optional, Union
from ipaddress import IPv4Address

# Modules.
from utils.network import Ifa
from utils.validator import validate_ipv4_addr

# External Imports.
from pyshark import LiveCapture
from pyshark.packet.packet import Packet

class IPv4Capture:
    """_summary_
    """

    def __init__(
        self: object,
        ifa: Ifa,
        timeout: Optional[int] = 15,
        capture_filter: Optional[str] = 'ip and tcp'
    ) -> None:
        """Initialises IPv4Capture.

        Args:
            ifa (Ifa): Represents a single interface 
            (Ifa dataclass).
            timeout (Optional[int], optional): Timeout for the frame capture. 
            Defaults to 15.
            capture_filter (Optional[str], optional): Represents the Tshark filter
            by which to filter captured frames. Defaults to 'ip and tcp'.
        """
        # Input network interface.
        # Comprises ifa_name and ifa_addrs fields.
        self._ifa = ifa

        # Timeout parameter passed into .sniff()
        # PyShark method.
        self._timeout = timeout

        # Filter to reduce capture overhead.
        self._filter = capture_filter

        # Handle to LiveCapture.
        self._capture: Union[None, LiveCapture] = None

        # List comprising the extracted, and parsed,
        # IPv4 addresses.
        self._ipv4_addrs: Set[Union[str, IPv4Address]] = set()

        # Create LiveCapture handler.
        self._init_handler()

    def __del__(self: object) -> None:
        """Destroys the LiveCapture handle
        and releases resources."""
        self._capture = None
        del self

    def _init_handler(self: object) -> None:
        """Creates a LiveCapture instance and assigns
        to _capture for simple access."""
        # Checks if 'Ifa' is set; otherwise
        # ifa_name cannot be read.
        if self._ifa:
            # Creates LiveCapture instance.
            self._capture = LiveCapture(
                # Interface name.
                interface=self._ifa.ifa_name,
                # Filter to reduce processing
                # overhead of unneccessary frames.
                # i.e., UDP (for now), etc.
                bpf_filter=self._filter
            )

    def _extract_ipv4_addr(self: object, packet: Packet) -> None:
        """In each packet captured by PyShark,
        the callback _extract_ipv4_addr is applied. This
        extracts each IPv4 address, and adds this to a set.

        Args:
            packet (Packet): Comprises the Packet object
            created by the PyShark LiveCapture.
        """
        # As IPv4Address is hashable, this
        # can be added to a set to ensure that
        # no hashes match.
        self._ipv4_addrs.add(
            # Converts src IPv4 address (str)
            # to hashable IPv4Address.
            validate_ipv4_addr(packet.ip.src)
        )

    def _sniff_packets(self: object) -> None:
        """Captures all packets in the LiveCapture
        and applies a callbacl to each incoming packet."""
        try:
            # Sniff, and apply callback to
            # extract IPv4 addresses from packets.
            self._capture.apply_on_packets(
                self._extract_ipv4_addr,
                timeout=self._timeout
            )
        # Raised by PyShark - therefore
        # caught and ignored.
        except TimeoutError:
            pass

    def capture(self: object) -> None:
        """Provides a public means to initiate
        the LiveCapture and extract IPv4 addresses."""
        # Initialises capturing of packets
        # on selected interface.
        self._sniff_packets()

def get_ipv4_capture(ifa: Ifa) -> IPv4Capture:
    """Returns an instantiated IPv4Capture.

    Returns:
        IPv4Capture: Instantiated form of IPv4Capture.
    """
    return IPv4Capture(ifa.ifa_name)
