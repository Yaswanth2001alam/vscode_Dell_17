import pytest

from network_pytest.checks import lacp_member


pytestmark = [pytest.mark.offline, pytest.mark.layer2]


def test_healthy_lacp_member(healthy_lacp_flags):
    assert lacp_member(healthy_lacp_flags).passed


@pytest.mark.parametrize("bad_flag", ["synchronized", "collecting", "distributing"])
def test_lacp_required_forwarding_flag_failure(healthy_lacp_flags, bad_flag):
    healthy_lacp_flags[bad_flag] = False
    assert not lacp_member(healthy_lacp_flags).passed

