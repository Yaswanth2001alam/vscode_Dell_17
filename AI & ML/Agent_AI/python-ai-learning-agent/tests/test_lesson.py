"""Set LEARNING_EXERCISE_FILE only for code you have reviewed and trust.

This harness imports Python code into the test process. It is NOT a sandbox.
Default execution loads the authored reference solution.
"""

import importlib.util
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
LESSON = ROOT / "lessons" / "beginner" / "01_variables"


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("lesson_under_test", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def solution():
    return load_module(Path(os.environ.get("LEARNING_EXERCISE_FILE", LESSON / "solutions.py")))


def test_device_label(solution) -> None:
    assert solution.device_label("r1", 24) == "r1: 24 interfaces"
    assert solution.device_label("r0", 0) == "r0: 0 interfaces"
    with pytest.raises(ValueError):
        solution.device_label("r1", -1)


@pytest.mark.parametrize("text,expected", [("24", 24), (" 0 ", 0), ("+5", 5)])
def test_parse_count(solution, text: str, expected: int) -> None:
    assert solution.parse_count(text) == expected


@pytest.mark.parametrize("text", ["abc", "-1", "2.4", ""])
def test_parse_count_errors(solution, text: str) -> None:
    with pytest.raises(ValueError):
        solution.parse_count(text)


def test_type_names(solution) -> None:
    assert solution.type_names([1, 1.5, "r1", True, None]) == [
        "int",
        "float",
        "str",
        "bool",
        "NoneType",
    ]
    assert solution.type_names([]) == []


def test_add_device_without_mutation(solution) -> None:
    original = ["r1"]
    result = solution.add_device(original, "r2")
    assert result == ["r1", "r2"]
    assert original == ["r1"]
    assert result is not original
    assert solution.add_device([], "r0") == ["r0"]


def test_compare_lists(solution) -> None:
    left = [1]
    assert solution.compare_lists(left, [1]) == (True, False)
    assert solution.compare_lists(left, left) == (True, True)
    assert solution.compare_lists(left, [2]) == (False, False)


@pytest.mark.parametrize("celsius,expected", [(0, 32), (100, 212), (-40, -40)])
def test_fahrenheit(solution, celsius: float, expected: float) -> None:
    assert solution.fahrenheit(celsius) == pytest.approx(expected)


def test_example_output(capsys: pytest.CaptureFixture[str]) -> None:
    load_module(LESSON / "examples.py").main()
    assert capsys.readouterr().out.splitlines() == [
        "1. Rebinding: 4 3",
        "2. Types: ['int', 'float', 'str', 'bool', 'NoneType']",
        "3. Conversion: 25",
        "4. Shared list: ['r1', 'r2']",
        "5. Copied list: ['r1'] ['r1', 'r2']",
        "6. Equality and identity: True False",
        "7. Invalid input: Count must be an integer written as text.",
    ]
