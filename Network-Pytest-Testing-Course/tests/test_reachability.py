import pytest

from network_pytest.checks import probe_quality


pytestmark = [pytest.mark.offline, pytest.mark.layer4]


@pytest.mark.parametrize(
    ("received", "latency", "passed"),
    [
        (10, 10.0, True),
        (9, 10.0, True),
        (8, 10.0, False),
        (10, 50.0, True),
        (10, 50.1, False),
    ],
    ids=["no-loss", "loss-boundary", "excess-loss", "latency-boundary", "excess-latency"],
)
def test_probe_loss_and_latency_boundaries(received, latency, passed):
    result = probe_quality(
        sent=10,
        received=received,
        average_latency_ms=latency,
        maximum_loss_percent=10,
        maximum_latency_ms=50,
    )
    assert result.passed is passed


def test_invalid_probe_counts_are_rejected():
    with pytest.raises(ValueError, match="packet counts"):
        probe_quality(10, 11, 1, 0, 10)

