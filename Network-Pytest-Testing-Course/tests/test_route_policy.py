import pytest

from network_pytest.checks import route_policy


pytestmark = [pytest.mark.offline, pytest.mark.layer3, pytest.mark.routing]


@pytest.mark.bgp
def test_required_route_and_forbidden_default_route():
    required, forbidden = route_policy(
        observed=["203.0.113.1/24"],
        required=["203.0.113.0/24"],
        forbidden=["0.0.0.0/0", "10.0.0.0/8"],
    )
    assert required.passed
    assert forbidden.passed


@pytest.mark.bgp
def test_route_leak_is_detected():
    required, forbidden = route_policy(
        observed=["203.0.113.0/24", "10.0.0.0/8"],
        required=["203.0.113.0/24"],
        forbidden=["10.0.0.0/8"],
    )
    assert required.passed
    assert not forbidden.passed
    assert forbidden.observed == ["10.0.0.0/8"]


@pytest.mark.ipv6
def test_ipv6_required_and_forbidden_routes():
    required, forbidden = route_policy(
        observed=["2001:db8:100::1/48"],
        required=["2001:db8:100::/48"],
        forbidden=["::/0"],
    )
    assert required.passed
    assert forbidden.passed

