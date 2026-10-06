import pytest

from network_pytest.checks import inventory_errors


pytestmark = [pytest.mark.offline, pytest.mark.unit]


def test_valid_inventory_has_no_errors(inventory):
    assert inventory_errors(inventory) == []


@pytest.mark.parametrize(
    ("field", "value", "expected_error"),
    [
        ("host", "999.1.1.1", "invalid host"),
        ("port", 0, "invalid port"),
        ("port", 65536, "invalid port"),
    ],
    ids=["invalid-ip", "port-too-low", "port-too-high"],
)
def test_invalid_inventory_values_are_rejected(inventory, field, value, expected_error):
    inventory["leaf01"][field] = value
    assert any(expected_error in error for error in inventory_errors(inventory))


def test_missing_required_inventory_field_is_reported(inventory):
    del inventory["leaf01"]["platform"]
    assert any("missing" in error for error in inventory_errors(inventory))


def test_duplicate_management_endpoint_is_reported(inventory):
    inventory["leaf02"]["host"] = inventory["leaf01"]["host"]
    assert any("duplicate endpoint" in error for error in inventory_errors(inventory))
