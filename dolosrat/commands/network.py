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
from typing import Set, Union

# Modules.
from config.network import NetworkConfig
from utils.network import IPv4Host
from utils.wrapper import BaseWrapper
from utils.validator import validate_ipv4_addr

# External Imports.
from pyshark import LiveCapture
from pyshark.packet.packet import Packet

class IPv4CaptureWrapper(BaseWrapper):
    """_summary_
    """

    def __init__(self: object, config: NetworkConfig,
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

        super().__init__()

        # Houses saved network configuration.
        self.conf = config

        # Amends filter to focus upon specific
        # IPv4Host.
        if self.conf._conf['selected_host']:
            self._sel_ipv4_addr_filter()

        # Handle to LiveCapture.
        self._capture: Union[None, LiveCapture] = None

        # List comprising the extracted, and parsed,
        # IPv4 addresses.
        self._ipv4_addrs: Set[Union[None, IPv4Host]] = set()

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
        if self.conf._conf['selected_ifa']:
            # Creates LiveCapture instance.
            self._register_handle(LiveCapture(
                # Interface name.
                interface=self.conf._conf['selected_ifa'].ifa_name,
                # Filter to reduce processing
                # overhead of unneccessary frames.
                # i.e., UDP (for now), etc.
                bpf_filter=self.conf._conf['capture_filter']
            ))

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
            IPv4Host(
                validate_ipv4_addr(packet.ip.src),
                packet.tcp.dstport
            )
        )

    def _sniff_packets(self: object) -> None:
        """Captures all packets in the LiveCapture
        and applies a callback to each incoming packet."""

        try:
            # Sniff, and apply callback to
            # extract IPv4 addresses from packets.
            self._get_handle('LiveCapture').apply_on_packets(
                self._extract_ipv4_addr,
                timeout=self.conf._conf['timeout']
            )
        # Raised by PyShark - therefore
        # caught and returned.
        except TimeoutError:
            return

    def _sel_ipv4_addr_filter(self: object) -> None:
        """_summary_

        Args:
            self (object): _description_
        """

        # Apply BPF filter for specific src IPv4 address.
        self.conf._conf['capture_filter'] = 'ip and tcp and src host ' \
            f'{self.conf._conf["selected_host"].ipv4_addr}'

    def get_ipv4_addrs(self: object) -> Set[Union[None, IPv4Host]]:
        """Returns the collected IPv4 addresses for processing, 
        displaying, etc.

        Returns:
            Set[Union[None, IPv4Address]]: A set comprising all
            collected IPv4 addresses of type IPv4Address.
        """

        return self._ipv4_addrs

    def capture(self: object) -> None:
        """Provides a public means to initiate
        the LiveCapture and extract IPv4 addresses."""

        # Initialises capturing of packets
        # on selected interface.
        self._sniff_packets()

def get_ipv4_capture(network_config: NetworkConfig) -> IPv4CaptureWrapper:
    """Returns an instantiated IPv4Capture.

    Returns:
        IPv4Capture: Instantiated form of IPv4Capture.
    """

    return IPv4CaptureWrapper(network_config)
