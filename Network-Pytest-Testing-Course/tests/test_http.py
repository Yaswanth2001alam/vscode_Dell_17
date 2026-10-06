import pytest

from network_pytest.checks import http_response


pytestmark = [pytest.mark.offline, pytest.mark.layer7, pytest.mark.services]


@pytest.mark.parametrize(
    ("status", "content_type", "passed"),
    [
        (200, "application/json", True),
        (200, "application/json; charset=utf-8", True),
        (201, "application/json", True),
        (204, None, False),
        (404, "application/json", False),
        (500, "application/json", False),
        (200, "text/html", False),
    ],
    ids=[
        "ok-json",
        "json-with-charset",
        "created-json",
        "missing-content-type",
        "not-found",
        "server-error",
        "wrong-media-type",
    ],
)
def test_http_status_and_content_type(status, content_type, passed):
    result = http_response(
        status,
        content_type,
        allowed_statuses={200, 201},
        expected_content_type="application/json",
    )
    assert result.passed is passed

