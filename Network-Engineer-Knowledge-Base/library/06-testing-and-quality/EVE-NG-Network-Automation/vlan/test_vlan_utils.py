# test_vlan_utils.py

import pytest
from vlan_utils import add_vlan

# ----------------------
# VALID VLAN TESTS
# ----------------------

def test_valid_vlan():
    result = add_vlan(10, "users")
    assert result["status"] == "created"
    assert result["vlan_id"] == 10


# ----------------------
# INVALID VLAN ID TESTS
# ----------------------

@pytest.mark.parametrize("vlan_id", [-1, 0, 4095, 5000])
def test_invalid_vlan_id_range(vlan_id):
    with pytest.raises(ValueError):
        add_vlan(vlan_id, "test_vlan")


@pytest.mark.parametrize("vlan_id", ["10", None, 10.5])
def test_invalid_vlan_id_type(vlan_id):
    with pytest.raises(TypeError):
        add_vlan(vlan_id, "test_vlan")


# ----------------------
# INVALID VLAN NAME TESTS
# ----------------------

@pytest.mark.parametrize("vlan_name", ["", None, 123])
def test_invalid_vlan_name(vlan_name):
    with pytest.raises(ValueError):
        add_vlan(20, vlan_name)
