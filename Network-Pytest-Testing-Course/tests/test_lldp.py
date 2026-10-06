import pytest

from network_pytest.checks import exact_set


pytestmark = [pytest.mark.offline, pytest.mark.layer2]


def test_exact_lldp_neighbor_set():
    result = exact_set("LLDP", {"leaf02", "spine01"}, {"spine01", "leaf02"})
    assert result.passed


def test_missing_and_unexpected_lldp_neighbor_fails():
    result = exact_set("LLDP", {"leaf02"}, {"unknown-switch"})
    assert not result.passed
    assert "missing=['leaf02']" in result.detail
    assert "unexpected=['unknown-switch']" in result.detail

