import pytest

from network_pytest.checks import counter_rate, interface_health


pytestmark = [pytest.mark.offline, pytest.mark.layer1]


@pytest.mark.parametrize(
    ("admin", "oper", "speed", "input_errors", "output_errors", "expected"),
    [
        (True, True, 10000, 0, 0, True),
        (False, False, 10000, 0, 0, False),
        (True, False, 10000, 0, 0, False),
        (True, True, 1000, 0, 0, False),
        (True, True, 10000, 1, 0, False),
        (True, True, 10000, 0, 1, False),
    ],
    ids=[
        "healthy",
        "admin-down",
        "oper-down",
        "wrong-speed",
        "input-errors",
        "output-errors",
    ],
)
def test_interface_health(admin, oper, speed, input_errors, output_errors, expected):
    result = interface_health(admin, oper, 10000, speed, input_errors, output_errors)
    assert result.passed is expected


def test_counter_rate_calculation_and_reset_detection():
    assert counter_rate(100, 130, 10) == 3
    with pytest.raises(ValueError, match="decreased"):
        counter_rate(100, 5, 10)

