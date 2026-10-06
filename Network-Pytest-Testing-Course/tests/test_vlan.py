import pytest

from network_pytest.checks import vlan_policy


pytestmark = [pytest.mark.offline, pytest.mark.layer2]


@pytest.mark.parametrize(
    ("mode", "access_vlan", "allowed", "passed"),
    [
        ("access", 10, [], True),
        ("ACCESS", 10, [], True),
        ("access", 20, [], False),
        ("trunk", None, [10, 20], False),
    ],
)
def test_access_vlan_policy(mode, access_vlan, allowed, passed):
    result = vlan_policy(mode, "access", access_vlan, 10, allowed, [])
    assert result.passed is passed


def test_trunk_vlan_policy_requires_exact_allowed_set():
    assert vlan_policy("trunk", "trunk", None, None, [20, 10], [10, 20]).passed
    assert not vlan_policy(
        "trunk", "trunk", None, None, [10, 20, 999], [10, 20]
    ).passed

