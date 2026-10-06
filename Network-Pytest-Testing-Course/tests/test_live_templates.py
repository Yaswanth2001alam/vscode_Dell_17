import socket

import pytest

from network_pytest.probes import tcp_connect


@pytest.mark.live
@pytest.mark.layer4
def test_live_ssh_port_is_reachable(live_target):
    """Read-only example; enable only for one authorized lab target."""

    result = tcp_connect(live_target, 22, timeout=3)
    assert result.peer[1] == 22
    assert result.latency_ms < 3000


@pytest.mark.live
@pytest.mark.layer7
@pytest.mark.services
def test_live_target_resolves_when_hostname_is_used(live_target):
    """Resolution succeeds for hostnames and is harmless for IP literals."""

    addresses = {
        record[4][0]
        for record in socket.getaddrinfo(
            live_target,
            None,
            type=socket.SOCK_STREAM,
        )
    }
    assert addresses


@pytest.mark.live
@pytest.mark.disruptive
def test_disruptive_lab_template_requires_platform_implementation():
    pytest.skip(
        "template only: implement backup, fault injection, validation, rollback, "
        "and recovery for a specific isolated lab before removing this skip"
    )

