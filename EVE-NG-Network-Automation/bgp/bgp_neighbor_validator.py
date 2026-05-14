"""
BGP Neighbor Validator Module

Provides functionality to validate and monitor BGP neighbor states on Cisco
IOS/IOS-XE devices using Genie/pyATS parsing.

Usage:
    from bgp_neighbor_validator import BGPNeighborValidator
    
    validator = BGPNeighborValidator(device)
    result = validator.validate_neighbors()
    
    # Access results
    print(f"Total neighbors: {result.total_neighbors}")
    print(f"Established: {result.established_count}")
    print(f"Down: {result.down_count}")
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


logger = logging.getLogger(__name__)


class BGPNeighborState(str, Enum):
    """BGP neighbor session states."""
    ESTABLISHED = "Established"
    ACTIVE = "Active"
    CONNECT = "Connect"
    OPENCONFIRM = "OpenConfirm"
    OPENSENT = "OpenSent"
    IDLE = "Idle"
    DOWN = "Down"
    UNKNOWN = "Unknown"


@dataclass
class BGPNeighbor:
    """Represents a BGP neighbor."""
    ip_address: str
    remote_as: int
    state: BGPNeighborState
    prefixes_received: int = 0
    prefixes_advertised: int = 0
    uptime: Optional[str] = None
    vrf: str = "default"
    
    def is_healthy(self) -> bool:
        """Check if neighbor is in healthy state."""
        return self.state == BGPNeighborState.ESTABLISHED


@dataclass
class BGPValidationResult:
    """Result of BGP neighbor validation."""
    device_name: str
    vrf: str = "default"
    neighbors: List[BGPNeighbor] = field(default_factory=list)
    total_neighbors: int = 0
    established_count: int = 0
    down_count: int = 0
    error_neighbors: int = 0
    errors: List[str] = field(default_factory=list)
    raw_output: Optional[str] = None
    
    def get_status_summary(self) -> str:
        """Return human-readable status summary."""
        total = self.total_neighbors
        established = self.established_count
        down = self.down_count
        error = self.error_neighbors
        
        return (
            f"BGP Summary for {self.device_name}/{self.vrf}: "
            f"Total={total}, Established={established}, "
            f"Down={down}, Error={error}"
        )
    
    def get_unhealthy_neighbors(self) -> List[BGPNeighbor]:
        """Return list of unhealthy neighbors."""
        return [n for n in self.neighbors if not n.is_healthy()]
    
    def to_dict(self) -> dict:
        """Convert result to dictionary."""
        return {
            "device_name": self.device_name,
            "vrf": self.vrf,
            "total_neighbors": self.total_neighbors,
            "established": self.established_count,
            "down": self.down_count,
            "errors": self.error_neighbors,
            "neighbors": [
                {
                    "ip_address": n.ip_address,
                    "remote_as": n.remote_as,
                    "state": n.state.value,
                    "prefixes_received": n.prefixes_received,
                    "prefixes_advertised": n.prefixes_advertised,
                    "uptime": n.uptime,
                }
                for n in self.neighbors
            ],
            "validation_errors": self.errors,
        }


class BGPNeighborValidator:
    """Validates BGP neighbor states on network devices."""
    
    def __init__(self, device, vrf: str = "default", logger_obj=None):
        """
        Initialize BGP validator.
        
        Args:
            device: Genie/pyATS device object with active connection
            vrf: VRF name to validate (default: "default")
            logger_obj: Optional logger instance
        """
        self.device = device
        self.vrf = vrf
        self.logger = logger_obj or logger
    
    def validate_neighbors(self) -> BGPValidationResult:
        """
        Validate all BGP neighbors for the device.
        
        Returns:
            BGPValidationResult with neighbor states and validation metrics
        """
        result = BGPValidationResult(device_name=self.device.name, vrf=self.vrf)
        
        try:
            parsed_bgp = self._parse_bgp_summary()
            if not parsed_bgp:
                result.errors.append("Failed to parse BGP summary")
                return result
            
            self._extract_neighbors(parsed_bgp, result)
            self._calculate_metrics(result)
            
            self.logger.info(result.get_status_summary())
            
        except Exception as e:
            error_msg = f"Error validating BGP neighbors: {str(e)}"
            self.logger.error(error_msg)
            result.errors.append(error_msg)
        
        return result
    
    def validate_specific_neighbor(
        self, neighbor_ip: str
    ) -> Optional[BGPNeighbor]:
        """
        Validate a specific BGP neighbor by IP address.
        
        Args:
            neighbor_ip: IP address of the neighbor to validate
            
        Returns:
            BGPNeighbor object if found, None otherwise
        """
        try:
            parsed_bgp = self._parse_bgp_summary()
            if not parsed_bgp:
                self.logger.warning("Could not parse BGP summary")
                return None
            
            neighbor = self._find_neighbor(parsed_bgp, neighbor_ip)
            return neighbor
            
        except Exception as e:
            self.logger.error(f"Error validating neighbor {neighbor_ip}: {str(e)}")
            return None
    
    def _parse_bgp_summary(self) -> Optional[dict]:
        """
        Parse 'show ip bgp summary' output using Genie.
        
        Returns:
            Parsed BGP summary dictionary or None on failure
        """
        try:
            parsed = self.device.parse("show ip bgp summary")
            self.logger.debug("Successfully parsed BGP summary")
            return parsed
            
        except Exception as e:
            self.logger.warning(f"Failed to parse 'show ip bgp summary': {str(e)}")
            # Fallback: try raw execution
            try:
                raw_output = self.device.execute("show ip bgp summary")
                self.logger.debug("Retrieved raw BGP summary output")
                return {"raw_output": raw_output}
            except Exception as raw_e:
                self.logger.error(f"Could not retrieve BGP summary: {str(raw_e)}")
                return None
    
    def _extract_neighbors(self, parsed_bgp: dict, result: BGPValidationResult):
        """Extract individual neighbors from parsed BGP data."""
        try:
            # Handle Genie's nested structure for IOS-XE
            # Expected: instance -> vrf -> neighbor
            instance_data = parsed_bgp.get("instance", {})
            
            for inst_name, inst_data in instance_data.items():
                vrf_data = inst_data.get("vrf", {})
                
                for vrf_name, vrf_info in vrf_data.items():
                    if vrf_name != self.vrf:
                        continue
                    
                    neighbors = vrf_info.get("neighbor", {})
                    for nbr_ip, nbr_info in neighbors.items():
                        neighbor = self._parse_neighbor_data(nbr_ip, nbr_info)
                        if neighbor:
                            result.neighbors.append(neighbor)
        
        except Exception as e:
            self.logger.warning(f"Error extracting neighbors: {str(e)}")
    
    def _parse_neighbor_data(
        self, neighbor_ip: str, nbr_info: dict
    ) -> Optional[BGPNeighbor]:
        """Parse individual neighbor data."""
        try:
            state_str = nbr_info.get("session_state", "Unknown")
            state = self._parse_state(state_str)
            
            prefixes_info = nbr_info.get("prefixes", {})
            prefixes_rx = prefixes_info.get("received", {}).get("total_entries", 0)
            prefixes_tx = prefixes_info.get("sent", {}).get("total_entries", 0)
            
            remote_as = nbr_info.get("remote_as", 0)
            uptime = nbr_info.get("up_down", None)
            
            return BGPNeighbor(
                ip_address=neighbor_ip,
                remote_as=remote_as,
                state=state,
                prefixes_received=prefixes_rx,
                prefixes_advertised=prefixes_tx,
                uptime=uptime,
                vrf=self.vrf,
            )
        
        except Exception as e:
            self.logger.warning(f"Error parsing neighbor {neighbor_ip}: {str(e)}")
            return None
    
    def _find_neighbor(self, parsed_bgp: dict, neighbor_ip: str) -> Optional[BGPNeighbor]:
        """Find a specific neighbor in parsed BGP data."""
        result = BGPValidationResult(device_name=self.device.name, vrf=self.vrf)
        self._extract_neighbors(parsed_bgp, result)
        
        for neighbor in result.neighbors:
            if neighbor.ip_address == neighbor_ip:
                return neighbor
        
        return None
    
    def _parse_state(self, state_str: str) -> BGPNeighborState:
        """Convert state string to BGPNeighborState enum."""
        state_str = state_str.lower()
        
        for state in BGPNeighborState:
            if state_str == state.value.lower():
                return state
        
        return BGPNeighborState.UNKNOWN
    
    def _calculate_metrics(self, result: BGPValidationResult):
        """Calculate summary metrics."""
        result.total_neighbors = len(result.neighbors)
        
        for neighbor in result.neighbors:
            if neighbor.is_healthy():
                result.established_count += 1
            elif neighbor.state == BGPNeighborState.DOWN:
                result.down_count += 1
            else:
                result.error_neighbors += 1
