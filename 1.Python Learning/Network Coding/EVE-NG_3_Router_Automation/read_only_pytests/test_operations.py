from __future__ import annotations

import re

import pytest


@pytest.mark.live
def test_cdp_sees_expected_transit_peers(router_name, inventory, show):
    output = show("show cdp neighbors")
    for link in inventory[router_name]["links"]:
        assert link["peer"] in output


@pytest.mark.live
def test_cpu_is_below_95_percent(show):
    output = show("show processes cpu | include CPU utilization")
    match = re.search(r"five seconds:\s*(\d+)%", output)
    assert match, "Could not parse five-second CPU utilization"
    assert int(match.group(1)) < 95


@pytest.mark.live
def test_memory_command_returns_statistics(show):
    output = show("show memory statistics")
    assert "% Invalid input" not in output
    assert "Processor" in output


@pytest.mark.live
def test_no_active_interfaces_are_line_protocol_down(show):
    output = show("show ip interface brief")
    bad_rows = [
        line
        for line in output.splitlines()
        if "administratively down" not in line
        and line.split()
        and line.split()[-2:] in (["up", "down"], ["down", "down"])
    ]
    assert not bad_rows, f"Unexpected interface state: {bad_rows}"


@pytest.mark.live
def test_recent_logs_have_no_critical_failure(show):
    output = show("show logging | last 100")
    critical_patterns = (
        "%SYS-2-",
        "%OSPF-3-",
        "%BGP-3-",
        "Traceback",
        "System returned to ROM",
    )
    found = [pattern for pattern in critical_patterns if pattern in output]
    assert not found, f"Critical log patterns found: {found}"
