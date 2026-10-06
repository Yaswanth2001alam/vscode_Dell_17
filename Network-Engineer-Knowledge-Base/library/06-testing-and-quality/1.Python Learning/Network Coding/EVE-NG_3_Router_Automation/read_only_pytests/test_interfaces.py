from __future__ import annotations

import pytest


def interface_row(output: str, interface: str) -> list[str]:
    for line in output.splitlines():
        fields = line.split()
        if fields and fields[0].lower() == interface.lower():
            return fields
    return []


@pytest.mark.live
def test_management_interface_is_up(router_name, inventory, show):
    output = show("show ip interface brief")
    host = inventory[router_name]["host"]
    matching_rows = [
        line for line in output.splitlines() if host in line and " up " in f" {line} "
    ]
    assert matching_rows, f"No up management interface found with {host}"
    assert matching_rows[0].split()[-2:] == ["up", "up"]


@pytest.mark.live
def test_transit_interfaces_are_up(router_name, inventory, show):
    output = show("show ip interface brief")
    for link in inventory[router_name]["links"]:
        row = interface_row(output, link["interface"])
        assert row, f"{link['interface']} missing from show output"
        assert row[1] == link["address"].split("/")[0]
        assert row[-2:] == ["up", "up"]


@pytest.mark.live
def test_loopback_is_up(router_name, inventory, show):
    output = show("show ip interface brief")
    row = interface_row(output, "Loopback0")
    assert row
    assert row[1] == inventory[router_name]["router_id"]
    assert row[-2:] == ["up", "up"]


@pytest.mark.live
def test_transit_interface_descriptions(router_name, inventory, show):
    output = show("show interfaces description")
    for link in inventory[router_name]["links"]:
        assert link["interface"].replace("Ethernet", "Et") in output
        assert link["description"] in output


@pytest.mark.live
def test_transit_interfaces_have_no_input_or_crc_errors(
    router_name, inventory, show
):
    for link in inventory[router_name]["links"]:
        output = show(f"show interfaces {link['interface']}")
        assert "line protocol is up" in output
        assert "0 input errors" in output
        assert "0 CRC" in output
