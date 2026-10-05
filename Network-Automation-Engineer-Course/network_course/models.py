from __future__ import annotations

import ipaddress
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Mapping


class CheckStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    ERROR = "ERROR"
    SKIP = "SKIP"


@dataclass(frozen=True)
class CheckResult:
    """One independently reportable intent check."""

    name: str
    status: CheckStatus
    expected: Any
    observed: Any
    detail: str = ""

    @property
    def passed(self) -> bool:
        return self.status is CheckStatus.PASS

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["status"] = self.status.value
        return result


@dataclass(frozen=True)
class Device:
    name: str
    host: str
    platform: str
    role: str
    site: str
    port: int = 22
    tags: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Device name cannot be empty")
        try:
            ipaddress.ip_address(self.host)
        except ValueError as error:
            raise ValueError(f"{self.name} has invalid host {self.host!r}") from error
        if not 1 <= self.port <= 65535:
            raise ValueError(f"{self.name} has invalid TCP port {self.port}")
        for field_name in ("platform", "role", "site"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{self.name} has empty {field_name}")

    @classmethod
    def from_mapping(cls, name: str, data: Mapping[str, Any]) -> "Device":
        required = {"host", "platform", "role", "site"}
        missing = required - data.keys()
        unknown = data.keys() - required - {"port", "tags"}
        if missing:
            raise ValueError(f"{name} is missing fields: {sorted(missing)}")
        if unknown:
            raise ValueError(f"{name} has unknown fields: {sorted(unknown)}")
        raw_tags = data.get("tags", ())
        if isinstance(raw_tags, str) or not isinstance(raw_tags, (list, tuple)):
            raise ValueError(f"{name} tags must be a list")
        return cls(
            name=name,
            host=str(data["host"]),
            platform=str(data["platform"]),
            role=str(data["role"]),
            site=str(data["site"]),
            port=int(data.get("port", 22)),
            tags=tuple(str(tag) for tag in raw_tags),
        )


@dataclass(frozen=True)
class NeighborExpectation:
    protocol: str
    local_interface: str
    peer: str
    peer_interface: str | None = None
    peer_as: int | None = None

    def __post_init__(self) -> None:
        supported = {"lldp", "lacp", "ospf", "isis", "bgp"}
        protocol = self.protocol.lower()
        if protocol not in supported:
            raise ValueError(
                f"Unsupported protocol {self.protocol!r}; expected one of "
                f"{sorted(supported)}"
            )
        object.__setattr__(self, "protocol", protocol)
        if not self.local_interface or not self.peer:
            raise ValueError("Neighbor interface and peer are required")
        if self.peer_as is not None and not 1 <= self.peer_as <= 4_294_967_295:
            raise ValueError(f"Invalid BGP autonomous system {self.peer_as}")


def load_devices(data: Mapping[str, Any]) -> dict[str, Device]:
    """Validate a normalized inventory mapping and reject duplicate endpoints."""

    if data.get("schema_version") != 1:
        raise ValueError("Inventory schema_version must be 1")
    raw_devices = data.get("devices")
    if not isinstance(raw_devices, Mapping) or not raw_devices:
        raise ValueError("Inventory devices must be a non-empty mapping")

    devices = {
        str(name): Device.from_mapping(str(name), raw)
        for name, raw in raw_devices.items()
        if isinstance(raw, Mapping)
    }
    if len(devices) != len(raw_devices):
        raise ValueError("Every inventory device must be a mapping")

    endpoints: dict[tuple[str, int], str] = {}
    for device in devices.values():
        endpoint = (device.host, device.port)
        if endpoint in endpoints:
            raise ValueError(
                f"{device.name} and {endpoints[endpoint]} share endpoint "
                f"{device.host}:{device.port}"
            )
        endpoints[endpoint] = device.name
    return devices

