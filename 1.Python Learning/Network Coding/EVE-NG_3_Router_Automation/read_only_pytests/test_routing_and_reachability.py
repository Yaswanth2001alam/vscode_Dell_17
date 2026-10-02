from __future__ import annotations

import pytest


@pytest.mark.live
def test_all_loopbacks_are_reachable(inventory, show):
    for router in inventory.values():
        output = show(f"ping {router['router_id']} repeat 5 timeout 1")
        assert "Success rate is 100 percent" in output


@pytest.mark.live
def test_remote_loopbacks_have_routes(router_name, inventory, show):
    for name, router in inventory.items():
        if name == router_name:
            continue
        output = show(f"show ip route {router['router_id']}")
        assert f"Routing entry for {router['router_id']}/32" in output
        assert "Known via" in output


@pytest.mark.live
def test_direct_peer_addresses_are_reachable(router_name, inventory, show):
    for link in inventory[router_name]["links"]:
        output = show(f"ping {link['peer_address']} repeat 5 timeout 1")
        assert "Success rate is 100 percent" in output


@pytest.mark.live
def test_cef_is_running(show):
    output = show("show ip cef summary")
    assert "% Invalid input" not in output
    assert "CEF" in output
