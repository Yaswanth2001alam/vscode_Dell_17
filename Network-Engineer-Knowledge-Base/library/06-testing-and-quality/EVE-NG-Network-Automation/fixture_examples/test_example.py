import pytest

# Fixture to prepare test data
@pytest.fixture
def sample_numbers():
    # This is the "setup" part: preparing data for tests
    return [1, 2, 3, 4, 5]

# A simple test that uses the fixture
def test_sum(sample_numbers):
    # "sample_numbers" gets automatically injected by pytest
    assert sum(sample_numbers) == 15

# Another test using the same fixture
def test_max(sample_numbers):
    assert max(sample_numbers) == 5


