import pytest
from typer.testing import CliRunner

from python_learning_agent.cli import app
from python_learning_agent.config import Settings
from python_learning_agent.orchestrator import LearningAgent

runner = CliRunner()


@pytest.mark.parametrize(
    "arguments,expected",
    [
        (["learn", "variables"], "Memory Fundamentals"),
        (["explain", "variables"], "Memory Fundamentals"),
        (["explore", "variables"], "Memory Fundamentals"),
        (["practice", "variables"], "Exercise 1"),
        (["practice", "variables", "--solutions"], "Copy first"),
        (["progress"], "No progress yet"),
        (["next-topic"], "variables"),
        (["roadmap"], "capstone (planned)"),
        (["revise"], "No revision"),
        (["revise", "variables"], "Memory Fundamentals"),
    ],
)
def test_commands(arguments: list[str], expected: str) -> None:
    result = runner.invoke(app, arguments, terminal_width=120)
    assert result.exit_code == 0, result.output
    assert expected in result.output


def test_quiz_is_graded_and_persisted() -> None:
    result = runner.invoke(app, ["quiz", "variables"], input="wrong\na\nb\nc\nb\nc\nb\n")
    assert result.exit_code == 0, result.output
    assert "Choose one" in result.output
    assert "Score: 100%" in result.output
    tracker = LearningAgent(Settings.from_environment()).progress
    assert tracker.records()[0]["best_score"] == 100
    assert tracker.records()[0]["status"] == "started"


def test_failed_quiz_schedules_revision() -> None:
    result = runner.invoke(app, ["quiz", "variables"], input="b\na\na\na\na\na\n")
    assert result.exit_code == 0, result.output
    assert "Score: 0%" in result.output
    assert "variables" in runner.invoke(app, ["revise"]).output


def test_progress_completion_and_difficulty() -> None:
    result = runner.invoke(app, ["progress", "--difficult", "variables"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["progress", "--complete", "variables"])
    assert result.exit_code == 0
    assert "completed" in result.output
    assert "operators" in runner.invoke(app, ["next-topic"]).output


@pytest.mark.parametrize(
    "arguments",
    [
        ["learn", "unknown"],
        ["learn", "decorators"],
        ["progress", "--complete", ""],
        ["progress", "--complete", "variables", "--difficult", "variables"],
    ],
)
def test_errors_are_actionable(arguments: list[str]) -> None:
    result = runner.invoke(app, arguments)
    assert result.exit_code == 1
    assert "Error:" in result.output


def test_aborted_quiz_does_not_record_a_score() -> None:
    result = runner.invoke(app, ["quiz", "variables"], input="a\n")
    assert result.exit_code != 0
    assert LearningAgent(Settings.from_environment()).progress.records() == []
