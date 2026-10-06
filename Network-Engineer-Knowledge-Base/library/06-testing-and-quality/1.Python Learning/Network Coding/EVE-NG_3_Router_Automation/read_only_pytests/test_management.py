from __future__ import annotations

import socket

import pytest

from conftest import ROUTERS


@pytest.mark.live
@pytest.mark.parametrize("name", ROUTERS)
def test_management_ssh_port_is_reachable(name, inventory, selected_router_names):
    if name not in selected_router_names:
        pytest.skip(f"{name} not selected")
    router = inventory[name]
    with socket.create_connection((router["host"], router["port"]), timeout=5):
        pass


@pytest.mark.live
def test_expected_hostname_is_configured(router_name, show):
    output = show("show running-config | include ^hostname")
    assert f"hostname {router_name}" in output


@pytest.mark.live
def test_ssh_is_enabled(show):
    output = show("show ip ssh")
    assert "% Invalid input" not in output
    assert "SSH Enabled" in output
