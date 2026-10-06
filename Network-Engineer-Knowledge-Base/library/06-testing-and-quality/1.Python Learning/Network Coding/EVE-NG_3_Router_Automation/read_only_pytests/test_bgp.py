from __future__ import annotations

import re

import pytest


def bgp_neighbor_rows(output: str) -> list[list[str]]:
    return [
        line.split()
        for line in output.splitlines()
        if re.match(r"^\d+\.\d+\.\d+\.\d+\s+", line)
    ]


@pytest.mark.live
def test_local_bgp_as_and_router_id(router_name, inventory, show):
    output = show("show ip bgp summary")
    router = inventory[router_name]
    assert f"BGP router identifier {router['router_id']}" in output
    assert f"local AS number {router['asn']}" in output


@pytest.mark.live
def test_all_bgp_neighbors_are_established(router_name, inventory, show):
    output = show("show ip bgp summary")
    rows = bgp_neighbor_rows(output)
    assert len(rows) == len(inventory[router_name]["links"])
    for link in inventory[router_name]["links"]:
        row = next((fields for fields in rows if fields[0] == link["peer_address"]), None)
        assert row, f"Missing BGP neighbor {link['peer_address']}"
        assert row[-1].isdigit(), f"BGP neighbor {link['peer_address']} is {row[-1]}"


@pytest.mark.live
def test_bgp_table_contains_all_loopbacks(inventory, show):
    output = show("show ip bgp")
    for router in inventory.values():
        assert f"{router['router_id']}/32" in output


@pytest.mark.live
def test_bgp_learns_expected_remote_prefix_count(router_name, show):
    output = show("show ip bgp summary")
    rows = bgp_neighbor_rows(output)
    received = sum(int(row[-1]) for row in rows)
    expected = 2 if router_name in {"R1", "R3"} else 2
    assert received == expected
