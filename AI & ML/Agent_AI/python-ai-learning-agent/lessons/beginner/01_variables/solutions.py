"""Explained solutions. Run: python solutions.py. Expected output: Solutions checked."""


def device_label(name: str, interfaces: int) -> str:
    """Validate the count, then insert the two values into an f-string."""
    if interfaces < 0:
        raise ValueError("Interface count must not be negative.")
    return f"{name}: {interfaces} interfaces"


def parse_count(raw_count: str) -> int:
    """int parses text; a separate comparison rejects negative counts."""
    try:
        count = int(raw_count)
    except ValueError:
        raise ValueError("Count must be an integer written as text.") from None
    if count < 0:
        raise ValueError("Count must not be negative.")
    return count


def type_names(values: list[object]) -> list[str]:
    """Visit values one at a time; __name__ makes type objects readable."""
    names = []
    for value in values:
        names.append(type(value).__name__)
    return names


def add_device(devices: list[str], name: str) -> list[str]:
    """Copy first so append mutates a new outer list, not the caller's list."""
    independent = devices.copy()
    independent.append(name)
    return independent


def compare_lists(left: list[int], right: list[int]) -> tuple[bool, bool]:
    """== compares list values; is checks whether both names share one list."""
    return left == right, left is right


def fahrenheit(celsius: float) -> float:
    """Multiply by the scale ratio before adding the temperature offset."""
    return celsius * 9 / 5 + 32


if __name__ == "__main__":
    assert device_label("r1", 24) == "r1: 24 interfaces"
    assert parse_count("24") == 24
    assert type_names([1, "r1"]) == ["int", "str"]
    original = ["r1"]
    assert add_device(original, "r2") == ["r1", "r2"]
    assert original == ["r1"]
    assert compare_lists([1], [1]) == (True, False)
    assert fahrenheit(0.0) == 32.0
    print("Solutions checked.")
