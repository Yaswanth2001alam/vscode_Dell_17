from pathlib import Path

import pytest

from python_learning_agent.curriculum import Curriculum
from python_learning_agent.orchestrator import LearningAgent


def test_order_prerequisites_and_availability(agent: LearningAgent) -> None:
    ordered = agent.curriculum.ordered()
    seen: set[str] = set()
    for topic in ordered:
        assert set(topic.prerequisites) <= seen
        seen.add(topic.id)
    assert len({topic.level for topic in ordered}) == 6
    available = [topic.id for topic in ordered if topic.lesson]
    assert available == ["variables"]
    assert "Memory Fundamentals" in agent.content("variables")


@pytest.mark.parametrize(
    "document,message",
    [
        ("level: test\ntopics: [{id: x, title: X, prerequisites: [missing]}]", "Unknown"),
        ("level: test\ntopics: [{id: x, title: X, prerequisites: [x]}]", "cycle"),
        ("level: test\ntopics: [{id: x, title: X}, {id: x, title: X}]", "Duplicate"),
        ("level: test\ntopics: [{id: x, title: X, lesson: ../../escape}]", "Invalid"),
        ("level: test\ntopics: [{id: x, title: X, prerequisites: bad}]", "Invalid"),
        ("topics: []", "level"),
    ],
)
def test_rejects_invalid_curriculum(tmp_path: Path, document: str, message: str) -> None:
    (tmp_path / "curriculum").mkdir()
    (tmp_path / "curriculum" / "test.yaml").write_text(document, encoding="utf-8")
    with pytest.raises(ValueError, match=message):
        Curriculum(tmp_path)


def test_unknown_and_planned_topics_are_explicit(agent: LearningAgent) -> None:
    with pytest.raises(ValueError, match="Unknown"):
        agent.content("not-a-topic")
    with pytest.raises(ValueError, match="planned"):
        agent.content("decorators")
