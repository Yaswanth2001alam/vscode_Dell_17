import pytest

from network_pytest.checks import macsec_health


pytestmark = [pytest.mark.offline, pytest.mark.layer2, pytest.mark.security]


@pytest.mark.parametrize(
    ("secured", "protected", "invalid_icv", "replay", "passed"),
    [
        (True, 1000, 0, 0, True),
        (False, 0, 0, 0, False),
        (True, 0, 0, 0, False),
        (True, 1000, 1, 0, False),
        (True, 1000, 0, 1, False),
    ],
)
def test_macsec_health(secured, protected, invalid_icv, replay, passed):
    assert macsec_health(secured, protected, invalid_icv, replay).passed is passed

