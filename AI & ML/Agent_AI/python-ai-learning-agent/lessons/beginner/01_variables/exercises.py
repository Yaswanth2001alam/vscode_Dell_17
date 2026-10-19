"""Copy this file before editing. Run reviewed work with the local assessment tests.

These are intentionally unfinished practice functions, not application stubs.
Use only fictional device names. No device connections are made.
"""


def device_label(name: str, interfaces: int) -> str:
    """Return 'r1: 24 interfaces' for ('r1', 24); reject negative counts."""
    raise NotImplementedError("Exercise 1: validate the count and format the label.")


def parse_count(raw_count: str) -> int:
    """Return 24 for '24'; raise ValueError for 'abc' or '-1'."""
    raise NotImplementedError("Exercise 2: convert text and validate the result.")


def type_names(values: list[object]) -> list[str]:
    """Return ['int', 'str'] for [1, 'r1']; support an empty list."""
    raise NotImplementedError("Exercise 3: inspect each object's type.")


def add_device(devices: list[str], name: str) -> list[str]:
    """Return ['r1', 'r2'] for (['r1'], 'r2') without mutating the input."""
    raise NotImplementedError("Exercise 4: create an independent outer list.")


def compare_lists(left: list[int], right: list[int]) -> tuple[bool, bool]:
    """Return (True, False) for two distinct lists both containing [1]."""
    raise NotImplementedError("Exercise 5: return equality and identity.")


def fahrenheit(celsius: float) -> float:
    """Return 32.0 for 0.0 and 212.0 for 100.0."""
    raise NotImplementedError("Exercise 6: translate the formula into arithmetic.")
