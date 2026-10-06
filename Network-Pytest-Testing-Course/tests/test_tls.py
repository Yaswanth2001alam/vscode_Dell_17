from datetime import datetime, timedelta, timezone

import pytest

from network_pytest.checks import certificate_health


pytestmark = [pytest.mark.offline, pytest.mark.layer6, pytest.mark.security]


@pytest.mark.parametrize(
    ("hostname_matches", "days", "minimum", "passed"),
    [
        (True, 90, 30, True),
        (True, 30, 30, True),
        (True, 29, 30, False),
        (False, 90, 30, False),
        (True, -1, 0, False),
    ],
    ids=["healthy", "expiry-boundary", "expires-soon", "hostname-mismatch", "expired"],
)
def test_tls_certificate_policy(hostname_matches, days, minimum, passed):
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    result = certificate_health(
        hostname_matches,
        now + timedelta(days=days),
        minimum,
        now=now,
    )
    assert result.passed is passed


def test_certificate_requires_timezone_aware_values():
    with pytest.raises(ValueError, match="timezone-aware"):
        certificate_health(
            True,
            datetime(2026, 2, 1),
            30,
            now=datetime(2026, 1, 1),
        )

