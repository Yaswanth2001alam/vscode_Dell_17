from __future__ import annotations

import ipaddress
from collections.abc import Iterable, Mapping
from typing import Any

from .models import CheckResult, CheckStatus


def _result(
    name: str,
    condition: bool,
    expected: Any,
    observed: Any,
    detail: str = "",
) -> CheckResult:
    return CheckResult(
        name=name,
        status=CheckStatus.PASS if condition else CheckStatus.FAIL,
        expected=expected,
        observed=observed,
        detail=detail,
    )


def exact_neighbor_set(
    protocol: str,
    expected: Iterable[str],
    observed: Iterable[str],
) -> CheckResult:
    """Require every expected neighbor and reject unexpected neighbors."""

    expected_set = frozenset(expected)
    observed_set = frozenset(observed)
    missing = sorted(expected_set - observed_set)
    unexpected = sorted(observed_set - expected_set)
    detail_parts = []
    if missing:
        detail_parts.append(f"missing={missing}")
    if unexpected:
        detail_parts.append(f"unexpected={unexpected}")
    return _result(
        name=f"{protocol.lower()}-neighbor-set",
        condition=expected_set == observed_set,
        expected=sorted(expected_set),
        observed=sorted(observed_set),
        detail="; ".join(detail_parts),
    )


def adjacency_state(
    protocol: str,
    peer: str,
    observed_state: str,
    allowed_states: Iterable[str],
) -> CheckResult:
    allowed = {state.casefold() for state in allowed_states}
    normalized = observed_state.strip().casefold()
    return _result(
        name=f"{protocol.lower()}-adjacency-{peer}",
        condition=normalized in allowed,
        expected=sorted(allowed),
        observed=observed_state,
        detail=f"{peer} must be in a protocol-ready state",
    )


def bgp_prefix_count(
    peer: str,
    observed: int,
    minimum: int,
    maximum: int,
) -> CheckResult:
    if minimum < 0 or maximum < minimum:
        raise ValueError("Prefix thresholds must satisfy 0 <= minimum <= maximum")
    return _result(
        name=f"bgp-prefix-count-{peer}",
        condition=minimum <= observed <= maximum,
        expected={"minimum": minimum, "maximum": maximum},
        observed=observed,
        detail="Accepted prefixes must remain inside the approved range",
    )


def required_and_forbidden_prefixes(
    name: str,
    observed: Iterable[str],
    required: Iterable[str],
    forbidden: Iterable[str],
) -> list[CheckResult]:
    observed_set = {
        str(ipaddress.ip_network(prefix, strict=False)) for prefix in observed
    }
    required_set = {
        str(ipaddress.ip_network(prefix, strict=False)) for prefix in required
    }
    forbidden_set = {
        str(ipaddress.ip_network(prefix, strict=False)) for prefix in forbidden
    }

    missing = sorted(required_set - observed_set)
    leaked = sorted(forbidden_set & observed_set)
    return [
        _result(
            name=f"{name}-required-prefixes",
            condition=not missing,
            expected=sorted(required_set),
            observed=sorted(observed_set),
            detail=f"missing={missing}" if missing else "",
        ),
        _result(
            name=f"{name}-forbidden-prefixes",
            condition=not leaked,
            expected=[],
            observed=leaked,
            detail=f"forbidden routes present={leaked}" if leaked else "",
        ),
    ]


def lacp_member(
    interface: str,
    flags: Mapping[str, bool],
) -> CheckResult:
    required = ("synchronized", "collecting", "distributing")
    missing = [flag for flag in required if not flags.get(flag, False)]
    unsafe = [
        flag for flag in ("defaulted", "expired") if flags.get(flag, False)
    ]
    return _result(
        name=f"lacp-member-{interface}",
        condition=not missing and not unsafe,
        expected={
            "synchronized": True,
            "collecting": True,
            "distributing": True,
            "defaulted": False,
            "expired": False,
        },
        observed=dict(flags),
        detail=f"missing={missing}; unsafe={unsafe}" if missing or unsafe else "",
    )


def counter_delta(
    name: str,
    before: int,
    after: int,
    maximum_increase: int = 0,
) -> CheckResult:
    if min(before, after, maximum_increase) < 0:
        raise ValueError("Counters and maximum increase cannot be negative")
    if after < before:
        return CheckResult(
            name=name,
            status=CheckStatus.ERROR,
            expected=f"increase <= {maximum_increase}",
            observed={"before": before, "after": after},
            detail="Counter decreased; device reset, rollover, or bad sample",
        )
    increase = after - before
    return _result(
        name=name,
        condition=increase <= maximum_increase,
        expected=f"increase <= {maximum_increase}",
        observed=increase,
        detail="Counter increase exceeded policy" if increase > maximum_increase else "",
    )


def macsec_health(
    interface: str,
    secured: bool,
    encrypted_packets: int,
    invalid_icv_packets: int,
    replay_drops: int,
) -> list[CheckResult]:
    if min(encrypted_packets, invalid_icv_packets, replay_drops) < 0:
        raise ValueError("MACsec counters cannot be negative")
    return [
        _result(
            name=f"macsec-secured-{interface}",
            condition=secured,
            expected=True,
            observed=secured,
        ),
        _result(
            name=f"macsec-protected-traffic-{interface}",
            condition=encrypted_packets > 0,
            expected="greater than 0",
            observed=encrypted_packets,
        ),
        _result(
            name=f"macsec-integrity-{interface}",
            condition=invalid_icv_packets == 0 and replay_drops == 0,
            expected={"invalid_icv_packets": 0, "replay_drops": 0},
            observed={
                "invalid_icv_packets": invalid_icv_packets,
                "replay_drops": replay_drops,
            },
        ),
    ]


def all_passed(results: Iterable[CheckResult]) -> bool:
    result_list = list(results)
    return bool(result_list) and all(result.passed for result in result_list)
