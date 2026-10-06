import pytest

from network_pytest.checks import forbidden_config


pytestmark = [pytest.mark.offline, pytest.mark.unit, pytest.mark.security]


@pytest.mark.parametrize(
    "pattern",
    ["password 0", "snmp-server community public", "transport input telnet"],
)
def test_forbidden_insecure_configuration_is_detected(pattern):
    config = f"hostname lab\n{pattern}\n"
    result = forbidden_config(
        config,
        ["password 0", "snmp-server community public", "transport input telnet"],
    )
    assert not result.passed
    assert pattern in result.observed


def test_secure_configuration_passes_forbidden_pattern_check():
    result = forbidden_config(
        "hostname lab\ntransport input ssh\n",
        ["password 0", "transport input telnet"],
    )
    assert result.passed

