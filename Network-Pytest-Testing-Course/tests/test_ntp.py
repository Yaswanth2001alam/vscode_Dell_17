import pytest

from network_pytest.checks import ntp_health


pytestmark = [pytest.mark.offline, pytest.mark.layer7, pytest.mark.services]


@pytest.mark.parametrize(
    ("synchronized", "offset", "passed"),
    [
        (True, 0.0, True),
        (True, 49.9, True),
        (True, -50.0, True),
        (True, 50.1, False),
        (False, 0.0, False),
    ],
)
def test_ntp_sync_and_offset(synchronized, offset, passed):
    assert ntp_health(synchronized, offset, 50).passed is passed


def test_negative_ntp_threshold_is_rejected():
    with pytest.raises(ValueError, match="cannot be negative"):
        ntp_health(True, 0, -1)

