
import pytest
from app import add, divide

# A simple fixture that provides reusable test data
@pytest.fixture
def numbers():
    return {"a": 6, "b": 7}

def test_add_works(numbers):
    assert add(numbers["a"], numbers["b"]) == 13

def test_divide_works():
    assert divide(10, 2) == 5

def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
