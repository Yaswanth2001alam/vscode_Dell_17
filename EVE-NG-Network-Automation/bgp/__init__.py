"""
BGP Neighbor Validation Automation Module

Provides utilities for validating and monitoring BGP neighbor relationships
on Cisco IOS/IOS-XE devices using Genie/pyATS.
"""

from .bgp_neighbor_validator import (
    BGPNeighborValidator,
    BGPNeighborState,
    BGPValidationResult,
)

__all__ = [
    "BGPNeighborValidator",
    "BGPNeighborState",
    "BGPValidationResult",
]
