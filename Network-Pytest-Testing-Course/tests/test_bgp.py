import pytest

from network_pytest.checks import adjacency, prefix_count


pytestmark = [
    pytest.mark.offline,
    pytest.mark.layer3,
    pytest.mark.routing,
    pytest.mark.bgp,
]


@pytest.mark.parametrize(
    ("state", "ready"),
    [
        ("ESTABLISHED", True),
        ("Established", True),
        ("IDLE", False),
        ("CONNECT", False),
        ("ACTIVE", False),
        ("OPENSENT", False),
        ("OPENCONFIRM", False),
    ],
)
def test_bgp_fsm_state(state, ready):
    result = adjacency("BGP", "198.51.100.2", state, {"ESTABLISHED"})
    assert result.passed is ready


@pytest.mark.parametrize(
    ("count", "passed"),
    [(0, False), (1, True), (500, True), (501, False)],
    ids=["below-minimum", "minimum", "maximum", "above-maximum"],
)
def test_bgp_prefix_count_boundaries(count, passed):
    assert prefix_count("198.51.100.2", count, 1, 500).passed is passed


def test_invalid_bgp_prefix_threshold_is_rejected():
    with pytest.raises(ValueError, match="minimum"):
        prefix_count("198.51.100.2", 5, 100, 10)

