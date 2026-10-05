from __future__ import annotations

import json
from collections.abc import Iterable

from .models import CheckResult
from .validators import (
    adjacency_state,
    all_passed,
    bgp_prefix_count,
    exact_neighbor_set,
    lacp_member,
    macsec_health,
    required_and_forbidden_prefixes,
)


def demo_checks() -> list[CheckResult]:
    """Return healthy, offline examples for several protocol contracts."""

    results = [
        exact_neighbor_set("lldp", ["leaf02"], ["leaf02"]),
        lacp_member(
            "Ethernet1",
            {
                "synchronized": True,
                "collecting": True,
                "distributing": True,
                "defaulted": False,
                "expired": False,
            },
        ),
        adjacency_state("ospf", "192.0.2.2", "FULL", {"FULL"}),
        adjacency_state("isis", "0000.0000.0002", "UP", {"UP"}),
        adjacency_state("bgp", "198.51.100.2", "ESTABLISHED", {"ESTABLISHED"}),
        bgp_prefix_count("198.51.100.2", observed=42, minimum=1, maximum=100),
    ]
    results.extend(
        required_and_forbidden_prefixes(
            "edge-routes",
            observed=["203.0.113.0/24"],
            required=["203.0.113.0/24"],
            forbidden=["0.0.0.0/0", "10.0.0.0/8"],
        )
    )
    results.extend(
        macsec_health(
            "Ethernet1",
            secured=True,
            encrypted_packets=10_000,
            invalid_icv_packets=0,
            replay_drops=0,
        )
    )
    return results


def report(results: Iterable[CheckResult]) -> dict[str, object]:
    result_list = list(results)
    return {
        "passed": all_passed(result_list),
        "summary": {
            status: sum(result.status.value == status for result in result_list)
            for status in ("PASS", "FAIL", "ERROR", "SKIP")
        },
        "checks": [result.to_dict() for result in result_list],
    }


def main() -> int:
    output = report(demo_checks())
    print(json.dumps(output, indent=2))
    return 0 if output["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

