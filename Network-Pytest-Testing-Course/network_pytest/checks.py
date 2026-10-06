from __future__ import annotations

import ipaddress
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class CheckResult:
    passed: bool
    expected: Any
    observed: Any
    detail: str = ""


def inventory_errors(inventory: Mapping[str, Mapping[str, Any]]) -> list[str]:
    errors: list[str] = []
    required = {"host", "platform", "role", "site"}
    endpoints: dict[tuple[str, int], str] = {}
    for name, device in inventory.items():
        missing = sorted(required - device.keys())
        if missing:
            errors.append(f"{name}: missing {missing}")
            continue
        try:
            ipaddress.ip_address(str(device["host"]))
        except ValueError:
            errors.append(f"{name}: invalid host {device['host']!r}")
        port = int(device.get("port", 22))
        if not 1 <= port <= 65535:
            errors.append(f"{name}: invalid port {port}")
        endpoint = (str(device["host"]), port)
        if endpoint in endpoints:
            errors.append(f"{name}: duplicate endpoint with {endpoints[endpoint]}")
        endpoints[endpoint] = name
    return errors


def interface_health(
    admin_up: bool,
    oper_up: bool,
    expected_speed_mbps: int,
    observed_speed_mbps: int,
    input_errors: int,
    output_errors: int,
) -> CheckResult:
    values = (expected_speed_mbps, observed_speed_mbps, input_errors, output_errors)
    if any(value < 0 for value in values):
        raise ValueError("Interface speeds and counters cannot be negative")
    passed = (
        admin_up
        and oper_up
        and observed_speed_mbps == expected_speed_mbps
        and input_errors == 0
        and output_errors == 0
    )
    return CheckResult(
        passed,
        {
            "admin_up": True,
            "oper_up": True,
            "speed_mbps": expected_speed_mbps,
            "input_errors": 0,
            "output_errors": 0,
        },
        {
            "admin_up": admin_up,
            "oper_up": oper_up,
            "speed_mbps": observed_speed_mbps,
            "input_errors": input_errors,
            "output_errors": output_errors,
        },
    )


def counter_rate(before: int, after: int, seconds: float) -> float:
    if before < 0 or after < 0:
        raise ValueError("Counters cannot be negative")
    if seconds <= 0:
        raise ValueError("Sample interval must be greater than zero")
    if after < before:
        raise ValueError("Counter decreased; rollover or reset must be handled")
    return (after - before) / seconds


def exact_set(name: str, expected: Iterable[str], observed: Iterable[str]) -> CheckResult:
    expected_set = frozenset(expected)
    observed_set = frozenset(observed)
    missing = sorted(expected_set - observed_set)
    unexpected = sorted(observed_set - expected_set)
    return CheckResult(
        not missing and not unexpected,
        sorted(expected_set),
        sorted(observed_set),
        f"{name}: missing={missing}; unexpected={unexpected}",
    )


def vlan_policy(
    mode: str,
    expected_mode: str,
    access_vlan: int | None,
    expected_access_vlan: int | None,
    allowed_vlans: Iterable[int],
    expected_allowed_vlans: Iterable[int],
) -> CheckResult:
    observed = {
        "mode": mode.casefold(),
        "access_vlan": access_vlan,
        "allowed_vlans": sorted(set(allowed_vlans)),
    }
    expected = {
        "mode": expected_mode.casefold(),
        "access_vlan": expected_access_vlan,
        "allowed_vlans": sorted(set(expected_allowed_vlans)),
    }
    return CheckResult(observed == expected, expected, observed)


def lacp_member(flags: Mapping[str, bool]) -> CheckResult:
    expected = {
        "synchronized": True,
        "collecting": True,
        "distributing": True,
        "defaulted": False,
        "expired": False,
    }
    observed = {name: bool(flags.get(name, False)) for name in expected}
    return CheckResult(observed == expected, expected, observed)


def stp_root(expected_root: str, observed_root: str, topology_changes: int) -> CheckResult:
    if topology_changes < 0:
        raise ValueError("Topology-change count cannot be negative")
    passed = expected_root.casefold() == observed_root.casefold()
    return CheckResult(
        passed,
        expected_root,
        observed_root,
        f"topology_changes={topology_changes}",
    )


def adjacency(
    protocol: str,
    peer: str,
    state: str,
    ready_states: Iterable[str],
) -> CheckResult:
    allowed = {item.casefold() for item in ready_states}
    return CheckResult(
        state.casefold() in allowed,
        sorted(allowed),
        state,
        f"{protocol} peer {peer}",
    )


def prefix_count(peer: str, observed: int, minimum: int, maximum: int) -> CheckResult:
    if minimum < 0 or maximum < minimum:
        raise ValueError("Require 0 <= minimum <= maximum")
    return CheckResult(
        minimum <= observed <= maximum,
        {"minimum": minimum, "maximum": maximum},
        observed,
        f"BGP peer {peer}",
    )


def route_policy(
    observed: Iterable[str],
    required: Iterable[str],
    forbidden: Iterable[str],
) -> list[CheckResult]:
    normalize = lambda items: {
        str(ipaddress.ip_network(item, strict=False)) for item in items
    }
    observed_set = normalize(observed)
    required_set = normalize(required)
    forbidden_set = normalize(forbidden)
    missing = sorted(required_set - observed_set)
    leaked = sorted(forbidden_set & observed_set)
    return [
        CheckResult(not missing, sorted(required_set), sorted(observed_set), f"missing={missing}"),
        CheckResult(not leaked, [], leaked, f"forbidden={leaked}"),
    ]


def probe_quality(
    sent: int,
    received: int,
    average_latency_ms: float,
    maximum_loss_percent: float,
    maximum_latency_ms: float,
) -> CheckResult:
    if sent <= 0 or received < 0 or received > sent:
        raise ValueError("Invalid probe packet counts")
    if min(average_latency_ms, maximum_loss_percent, maximum_latency_ms) < 0:
        raise ValueError("Latency and loss thresholds cannot be negative")
    loss = ((sent - received) / sent) * 100
    return CheckResult(
        loss <= maximum_loss_percent and average_latency_ms <= maximum_latency_ms,
        {
            "maximum_loss_percent": maximum_loss_percent,
            "maximum_latency_ms": maximum_latency_ms,
        },
        {"loss_percent": loss, "average_latency_ms": average_latency_ms},
    )


def certificate_health(
    hostname_matches: bool,
    not_after: datetime,
    minimum_days_remaining: int,
    now: datetime | None = None,
) -> CheckResult:
    if minimum_days_remaining < 0:
        raise ValueError("Minimum remaining days cannot be negative")
    reference = now or datetime.now(timezone.utc)
    if reference.tzinfo is None or not_after.tzinfo is None:
        raise ValueError("Certificate times must be timezone-aware")
    days = (not_after - reference).total_seconds() / 86400
    return CheckResult(
        hostname_matches and days >= minimum_days_remaining,
        {"hostname_matches": True, "minimum_days_remaining": minimum_days_remaining},
        {"hostname_matches": hostname_matches, "days_remaining": days},
    )


def http_response(
    status: int,
    content_type: str | None,
    allowed_statuses: Iterable[int],
    expected_content_type: str,
) -> CheckResult:
    allowed = set(allowed_statuses)
    observed_type = (content_type or "").split(";", 1)[0].strip().casefold()
    expected_type = expected_content_type.casefold()
    return CheckResult(
        status in allowed and observed_type == expected_type,
        {"statuses": sorted(allowed), "content_type": expected_type},
        {"status": status, "content_type": observed_type},
    )


def ntp_health(synchronized: bool, offset_ms: float, maximum_absolute_offset_ms: float) -> CheckResult:
    if maximum_absolute_offset_ms < 0:
        raise ValueError("Maximum NTP offset cannot be negative")
    return CheckResult(
        synchronized and abs(offset_ms) <= maximum_absolute_offset_ms,
        {"synchronized": True, "maximum_absolute_offset_ms": maximum_absolute_offset_ms},
        {"synchronized": synchronized, "offset_ms": offset_ms},
    )


def forbidden_config(config: str, forbidden_patterns: Iterable[str]) -> CheckResult:
    lowered = config.casefold()
    found = sorted(pattern for pattern in forbidden_patterns if pattern.casefold() in lowered)
    return CheckResult(not found, [], found, f"forbidden patterns={found}")


def macsec_health(
    secured: bool,
    protected_packets: int,
    invalid_icv: int,
    replay_drops: int,
) -> CheckResult:
    if min(protected_packets, invalid_icv, replay_drops) < 0:
        raise ValueError("MACsec counters cannot be negative")
    return CheckResult(
        secured and protected_packets > 0 and invalid_icv == 0 and replay_drops == 0,
        {"secured": True, "protected_packets": ">0", "invalid_icv": 0, "replay_drops": 0},
        {
            "secured": secured,
            "protected_packets": protected_packets,
            "invalid_icv": invalid_icv,
            "replay_drops": replay_drops,
        },
    )
