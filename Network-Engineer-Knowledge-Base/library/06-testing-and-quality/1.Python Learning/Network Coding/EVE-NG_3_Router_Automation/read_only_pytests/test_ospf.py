from __future__ import annotations

import pytest


@pytest.mark.live
def test_expected_ospf_neighbors_are_full(router_name, inventory, show):
    output = show("show ip ospf neighbor")
    expected_peers = inventory[router_name]["links"]
    full_rows = [line for line in output.splitlines() if "FULL/" in line]
    assert len(full_rows) == len(expected_peers)
    for link in expected_peers:
        peer_router_id = inventory[link["peer"]]["router_id"]
        assert any(peer_router_id in line and "FULL/" in line for line in full_rows)


@pytest.mark.live
def test_ospf_router_id(router_name, inventory, show):
    output = show("show ip ospf")
    expected = inventory[router_name]["router_id"]
    assert f"Routing Process \"ospf 1\" with ID {expected}" in output


@pytest.mark.live
def test_ospf_transit_interfaces_are_point_to_point(
    router_name, inventory, show
):
    for link in inventory[router_name]["links"]:
        output = show(f"show ip ospf interface {link['interface']}")
        assert "Network Type POINT_TO_POINT" in output
        assert "State POINT_TO_POINT" in output


@pytest.mark.live
def test_ospf_database_contains_all_router_ids(inventory, show):
    output = show("show ip ospf database router")
    for router in inventory.values():
        assert router["router_id"] in output
