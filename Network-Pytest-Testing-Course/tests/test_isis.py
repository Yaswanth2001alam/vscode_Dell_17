import pytest

from network_pytest.checks import adjacency


pytestmark = [
    pytest.mark.offline,
    pytest.mark.layer3,
    pytest.mark.routing,
    pytest.mark.isis,
]


@pytest.mark.parametrize(
    ("state", "ready"),
    [("UP", True), ("up", True), ("INITIALIZING", False), ("DOWN", False)],
)
def test_isis_neighbor_state(state, ready):
    result = adjacency("IS-IS", "0000.0000.0002", state, {"UP"})
    assert result.passed is ready

