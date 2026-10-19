from pathlib import Path

import pytest

from python_learning_agent.config import Settings
from python_learning_agent.orchestrator import LearningAgent


def test_progress_persists_and_does_not_repeat_completed(
    agent: LearningAgent,
) -> None:
    agent.progress.mark("variables")
    agent.progress.mark("variables", complete=True)
    agent.progress.mark("variables")
    reopened = LearningAgent(agent.settings)
    assert reopened.progress.completed() == {"variables"}
    topic, reason = reopened.progress.next_topic()
    assert topic is not None and topic.id == "operators"
    assert "not implemented" in reason
    assert reopened.progress.records()[0]["last_study"].endswith("+00:00")


def test_quiz_revision_and_history(agent: LearningAgent) -> None:
    agent.progress.record_quiz("variables", 50)
    topic, reason = agent.progress.next_topic()
    assert topic is not None and topic.id == "variables"
    assert reason == "Revision recommended"
    agent.progress.record_quiz("variables", 100)
    row = agent.progress.records()[0]
    assert row["best_score"] == 100
    assert not row["revision_required"]
    with agent.progress.storage.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM quiz_attempts").fetchone()[0] == 2


@pytest.mark.parametrize("score", [-1, 101, float("nan")])
def test_rejects_invalid_score(agent: LearningAgent, score: float) -> None:
    with pytest.raises(ValueError, match="between"):
        agent.progress.record_quiz("variables", score)
    assert agent.progress.records() == []


def test_difficulty_and_explicit_revision_completion(agent: LearningAgent) -> None:
    agent.progress.mark("variables", difficult=True)
    assert agent.progress.records()[0]["revision_required"]
    agent.progress.mark("variables", complete=True)
    assert not agent.progress.records()[0]["revision_required"]
    assert agent.progress.records()[0]["difficult"]


def test_no_planned_topic_progress(agent: LearningAgent) -> None:
    with pytest.raises(ValueError, match="planned"):
        agent.progress.mark("operators", complete=True)
    assert not agent.progress.records()


def test_prerequisites_block_completion(tmp_path: Path) -> None:
    (tmp_path / "curriculum").mkdir()
    lesson_path = tmp_path / "lessons" / "demo"
    lesson_path.mkdir(parents=True)
    (lesson_path / "notes.md").write_text("Demo lesson", encoding="utf-8")
    (tmp_path / "curriculum" / "test.yaml").write_text(
        "level: test\n"
        "topics:\n"
        "  - {id: first, title: First, lesson: lessons/demo}\n"
        "  - {id: second, title: Second, lesson: lessons/demo}\n",
        encoding="utf-8",
    )
    tracker = LearningAgent(Settings(tmp_path, tmp_path / "data")).progress
    with pytest.raises(ValueError, match="Complete prerequisites first"):
        tracker.mark("second", complete=True)
    assert tracker.records() == []
    tracker.mark("first", complete=True)
    tracker.mark("second", complete=True)
    assert tracker.completed() == {"first", "second"}


def test_invalid_root_is_reported(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("PYTHON_LEARNING_ROOT", str(tmp_path / "missing"))
    with pytest.raises(ValueError, match="Content root"):
        Settings.from_environment()
