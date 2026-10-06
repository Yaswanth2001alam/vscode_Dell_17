import pytest

from network_pytest.checks import adjacency


pytestmark = [
    pytest.mark.offline,
    pytest.mark.layer3,
    pytest.mark.routing,
    pytest.mark.ospf,
]


@pytest.mark.parametrize(
    ("state", "ready"),
    [
        ("FULL", True),
        ("full", True),
        ("2WAY", False),
        ("EXSTART", False),
        ("DOWN", False),
    ],
)
def test_ospf_point_to_point_neighbor_state(state, ready):
    result = adjacency("OSPF", "192.0.2.2", state, {"FULL"})
    assert result.passed is ready

