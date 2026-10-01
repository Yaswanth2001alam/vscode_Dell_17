"""
Draft BGP neighbor validator with an explicit raw-output fallback.

This module is intentionally separate from bgp_neighbor_validator.py so it can
be reviewed before replacing the existing implementation.

The fallback supports the tabular output produced by:
    show ip bgp summary

If Genie parsing fails and the raw output cannot be interpreted reliably, the
result contains a validation error instead of reporting a misleading zero
neighbor count.
"""

import ipaddress
import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


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
        """Return whether the BGP session is established."""

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
    warnings: List[str] = field(default_factory=list)
    raw_output: Optional[str] = None
    collection_method: Optional[str] = None

    @property
    def validation_succeeded(self) -> bool:
        """Return whether the device state was determined reliably."""

        return not self.errors and self.collection_method is not None

    def get_status_summary(self) -> str:
        """Return a human-readable status summary."""

        if not self.validation_succeeded:
            return (
                f"BGP validation failed for {self.device_name}/{self.vrf}: "
                f"{'; '.join(self.errors) or 'state could not be determined'}"
            )

        return (
            f"BGP Summary for {self.device_name}/{self.vrf}: "
            f"Total={self.total_neighbors}, "
            f"Established={self.established_count}, "
            f"Down={self.down_count}, "
            f"Error={self.error_neighbors}, "
            f"Source={self.collection_method}"
        )

    def get_unhealthy_neighbors(self) -> List[BGPNeighbor]:
        """Return all neighbors that are not established."""

        return [neighbor for neighbor in self.neighbors if not neighbor.is_healthy()]

    def to_dict(self) -> dict:
        """Convert the result to a JSON-serializable dictionary."""

        return {
            "device_name": self.device_name,
            "vrf": self.vrf,
            "validation_succeeded": self.validation_succeeded,
            "collection_method": self.collection_method,
            "total_neighbors": self.total_neighbors,
            "established": self.established_count,
            "down": self.down_count,
            "errors": self.error_neighbors,
            "neighbors": [
                {
                    "ip_address": neighbor.ip_address,
                    "remote_as": neighbor.remote_as,
                    "state": neighbor.state.value,
                    "prefixes_received": neighbor.prefixes_received,
                    "prefixes_advertised": neighbor.prefixes_advertised,
                    "uptime": neighbor.uptime,
                    "vrf": neighbor.vrf,
                }
                for neighbor in self.neighbors
            ],
            "validation_errors": self.errors,
            "validation_warnings": self.warnings,
        }


class BGPNeighborValidator:
    """Validate BGP neighbor states using Genie or raw IOS/IOS-XE output."""

    _RAW_NEIGHBOR_PATTERN = re.compile(
        r"^(?P<neighbor>\S+)\s+"
        r"(?P<version>\d+)\s+"
        r"(?P<remote_as>\d+)\s+"
        r"(?P<messages_received>\d+)\s+"
        r"(?P<messages_sent>\d+)\s+"
        r"(?P<table_version>\d+)\s+"
        r"(?P<input_queue>\d+)\s+"
        r"(?P<output_queue>\d+)\s+"
        r"(?P<uptime>\S+)\s+"
        r"(?P<state_or_prefixes>.+?)\s*$"
    )

    def __init__(self, device, vrf: str = "default", logger_obj=None):
        """
        Initialize the validator.

        Args:
            device: Connected Genie/pyATS device object.
            vrf: VRF to validate.
            logger_obj: Optional logger instance.
        """

        self.device = device
        self.vrf = vrf
        self.logger = logger_obj or logger

    def validate_neighbors(self) -> BGPValidationResult:
        """
        Validate all BGP neighbors.

        Genie parsing is attempted first. If it fails, raw command output is
        parsed. An unparseable fallback is returned as a validation error.
        """

        result = BGPValidationResult(device_name=self.device.name, vrf=self.vrf)

        try:
            parsed_bgp = self.device.parse("show ip bgp summary")
        except Exception as parse_error:
            self.logger.warning(
                "Genie failed to parse BGP summary on %s: %s",
                self.device.name,
                parse_error,
            )
            return self._validate_from_raw_output(result, parse_error)

        try:
            vrf_found = self._extract_neighbors(parsed_bgp, result)
        except (AttributeError, TypeError, ValueError) as extraction_error:
            message = (
                "Genie returned an unsupported BGP data structure: "
                f"{extraction_error}"
            )
            self.logger.error(message)
            result.errors.append(message)
            return result

        if not vrf_found:
            result.errors.append(
                f"VRF '{self.vrf}' was not present in the parsed BGP summary"
            )
            return result

        result.collection_method = "genie"
        self._calculate_metrics(result)
        self.logger.info(result.get_status_summary())
        return result

    def validate_specific_neighbor(self, neighbor_ip: str) -> Optional[BGPNeighbor]:
        """Validate and return one neighbor, or None if it is not present."""

        try:
            normalized_ip = str(ipaddress.ip_address(neighbor_ip))
        except ValueError:
            self.logger.error("Invalid neighbor IP address: %s", neighbor_ip)
            return None

        result = self.validate_neighbors()
        if not result.validation_succeeded:
            return None

        for neighbor in result.neighbors:
            if neighbor.ip_address == normalized_ip:
                return neighbor

        return None

    def _validate_from_raw_output(
        self,
        result: BGPValidationResult,
        parse_error: Exception,
    ) -> BGPValidationResult:
        """Execute and parse raw output after Genie parser failure."""

        try:
            raw_output = self.device.execute("show ip bgp summary")
        except Exception as execution_error:
            message = (
                "Unable to validate BGP neighbors: Genie parsing failed "
                f"({parse_error}) and raw command execution failed "
                f"({execution_error})"
            )
            self.logger.error(message)
            result.errors.append(message)
            return result

        result.raw_output = raw_output

        if not isinstance(raw_output, str) or not raw_output.strip():
            result.errors.append(
                "Unable to validate BGP neighbors: Genie parsing failed and "
                "the raw command returned no output"
            )
            return result

        neighbors, header_found = self._parse_raw_bgp_summary(raw_output)

        if not header_found:
            result.errors.append(
                "Unable to validate BGP neighbors: Genie parsing failed and "
                "the raw output did not contain a recognized IOS/IOS-XE BGP "
                "summary header"
            )
            return result

        if not neighbors:
            result.errors.append(
                "Unable to validate BGP neighbors: a BGP summary header was "
                "found, but no neighbor rows could be parsed reliably"
            )
            return result

        result.neighbors.extend(neighbors)
        result.collection_method = "raw_ios_summary"
        result.warnings.append(
            "Genie parsing failed; values were collected from raw IOS/IOS-XE "
            "summary output. Prefixes advertised are unavailable in this view."
        )
        self._calculate_metrics(result)
        self.logger.info(result.get_status_summary())
        return result

    def _parse_raw_bgp_summary(
        self,
        raw_output: str,
    ) -> Tuple[List[BGPNeighbor], bool]:
        """Parse IOS/IOS-XE BGP summary table rows."""

        neighbors: List[BGPNeighbor] = []
        header_found = False

        for raw_line in raw_output.splitlines():
            line = raw_line.strip()
            normalized_header = " ".join(line.lower().split())

            if (
                normalized_header.startswith("neighbor ")
                and "state/pfxrcd" in normalized_header
            ):
                header_found = True
                continue

            if not header_found or not line:
                continue

            match = self._RAW_NEIGHBOR_PATTERN.match(line)
            if not match:
                continue

            neighbor_ip = match.group("neighbor")
            try:
                neighbor_ip = str(ipaddress.ip_address(neighbor_ip))
            except ValueError:
                continue

            state_field = match.group("state_or_prefixes").strip()
            state, prefixes_received = self._parse_raw_state(state_field)

            neighbors.append(
                BGPNeighbor(
                    ip_address=neighbor_ip,
                    remote_as=int(match.group("remote_as")),
                    state=state,
                    prefixes_received=prefixes_received,
                    prefixes_advertised=0,
                    uptime=match.group("uptime"),
                    vrf=self.vrf,
                )
            )

        return neighbors, header_found

    def _parse_raw_state(
        self,
        state_or_prefixes: str,
    ) -> Tuple[BGPNeighborState, int]:
        """
        Interpret the final BGP summary column.

        A numeric value means the session is established and represents the
        number of received prefixes. Text represents a BGP session state.
        """

        compact_value = state_or_prefixes.replace(",", "")
        if compact_value.isdigit():
            return BGPNeighborState.ESTABLISHED, int(compact_value)

        state_name = state_or_prefixes.split(maxsplit=1)[0]
        return self._parse_state(state_name), 0

    def _extract_neighbors(
        self,
        parsed_bgp: Dict,
        result: BGPValidationResult,
    ) -> bool:
        """Extract neighbors and report whether the requested VRF was found."""

        if not isinstance(parsed_bgp, dict):
            raise TypeError("top-level parser output is not a dictionary")

        instance_data = parsed_bgp.get("instance")
        if not isinstance(instance_data, dict):
            raise ValueError("missing or invalid 'instance' section")

        vrf_found = False

        for instance in instance_data.values():
            if not isinstance(instance, dict):
                continue

            vrfs = instance.get("vrf", {})
            if not isinstance(vrfs, dict):
                continue

            if self.vrf not in vrfs:
                continue

            vrf_found = True
            vrf_data = vrfs[self.vrf]
            if not isinstance(vrf_data, dict):
                raise TypeError(f"VRF '{self.vrf}' data is not a dictionary")

            neighbors = vrf_data.get("neighbor", {})
            if not isinstance(neighbors, dict):
                raise TypeError(
                    f"VRF '{self.vrf}' neighbor data is not a dictionary"
                )

            for neighbor_ip, neighbor_data in neighbors.items():
                neighbor = self._parse_neighbor_data(neighbor_ip, neighbor_data)
                result.neighbors.append(neighbor)

        return vrf_found

    def _parse_neighbor_data(
        self,
        neighbor_ip: str,
        neighbor_data: Dict,
    ) -> BGPNeighbor:
        """Convert one Genie neighbor dictionary to a BGPNeighbor."""

        if not isinstance(neighbor_data, dict):
            raise TypeError(f"neighbor '{neighbor_ip}' data is not a dictionary")

        try:
            normalized_ip = str(ipaddress.ip_address(neighbor_ip))
        except ValueError as error:
            raise ValueError(
                f"neighbor '{neighbor_ip}' is not a valid IP address"
            ) from error

        prefixes = neighbor_data.get("prefixes", {})
        if not isinstance(prefixes, dict):
            prefixes = {}

        received = prefixes.get("received", {})
        sent = prefixes.get("sent", {})

        return BGPNeighbor(
            ip_address=normalized_ip,
            remote_as=int(neighbor_data.get("remote_as", 0)),
            state=self._parse_state(
                str(neighbor_data.get("session_state", "Unknown"))
            ),
            prefixes_received=self._read_prefix_count(received),
            prefixes_advertised=self._read_prefix_count(sent),
            uptime=neighbor_data.get("up_down"),
            vrf=self.vrf,
        )

    @staticmethod
    def _read_prefix_count(prefix_data) -> int:
        """Read a total_entries value without accepting invalid types."""

        if not isinstance(prefix_data, dict):
            return 0

        value = prefix_data.get("total_entries", 0)
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _parse_state(state_value: str) -> BGPNeighborState:
        """Convert parser or CLI state text to a known enum value."""

        normalized = state_value.strip().lower().replace("_", "")
        aliases = {
            "established": BGPNeighborState.ESTABLISHED,
            "active": BGPNeighborState.ACTIVE,
            "connect": BGPNeighborState.CONNECT,
            "openconfirm": BGPNeighborState.OPENCONFIRM,
            "opensent": BGPNeighborState.OPENSENT,
            "idle": BGPNeighborState.IDLE,
            "down": BGPNeighborState.DOWN,
            "shutdown": BGPNeighborState.DOWN,
            "admin": BGPNeighborState.DOWN,
        }
        return aliases.get(normalized, BGPNeighborState.UNKNOWN)

    @staticmethod
    def _calculate_metrics(result: BGPValidationResult) -> None:
        """Calculate summary metrics from the collected neighbors."""

        result.total_neighbors = len(result.neighbors)
        result.established_count = sum(
            neighbor.is_healthy() for neighbor in result.neighbors
        )
        result.down_count = sum(
            neighbor.state == BGPNeighborState.DOWN
            for neighbor in result.neighbors
        )
        result.error_neighbors = (
            result.total_neighbors
            - result.established_count
            - result.down_count
        )
