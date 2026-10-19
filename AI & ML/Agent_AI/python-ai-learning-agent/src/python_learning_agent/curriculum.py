"""Load a validated, prerequisite-aware roadmap from local YAML."""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

IDENTIFIER = re.compile(r"[a-z][a-z0-9_-]*")


@dataclass(frozen=True)
class Topic:
    id: str
    title: str
    level: str
    prerequisites: tuple[str, ...]
    lesson: str | None = None
    capstone: str = ""


class Curriculum:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.topics: dict[str, Topic] = {}
        for path in sorted((self.root / "curriculum").glob("*.yaml")):
            with path.open(encoding="utf-8") as stream:
                payload = yaml.safe_load(stream)
            self._load(payload, path)
        if not self.topics:
            raise ValueError("Curriculum contains no topics.")
        self._validate_graph()

    def _load(self, payload: Any, path: Path) -> None:
        if not isinstance(payload, dict) or not isinstance(payload.get("topics"), list):
            raise ValueError(f"Invalid curriculum document: {path.name}")
        level = payload.get("level")
        if not isinstance(level, str) or not level:
            raise ValueError(f"Missing curriculum level: {path.name}")
        capstone = payload.get("capstone", "")
        if not isinstance(capstone, str):
            raise ValueError(f"Invalid capstone: {path.name}")
        previous: str | None = None
        for entry in payload["topics"]:
            if not isinstance(entry, dict):
                raise ValueError(f"Invalid topic in {path.name}")
            topic_id, title = entry.get("id"), entry.get("title")
            if not isinstance(topic_id, str) or not IDENTIFIER.fullmatch(topic_id):
                raise ValueError(f"Invalid topic identifier in {path.name}")
            if topic_id in self.topics:
                raise ValueError(f"Duplicate topic: {topic_id}")
            if not isinstance(title, str) or not title:
                raise ValueError(f"Missing title for {topic_id}")
            # A track is progressive by default; explicit prerequisites allow branches.
            prerequisites = entry.get("prerequisites", [previous] if previous else [])
            if not isinstance(prerequisites, list) or not all(
                isinstance(item, str) for item in prerequisites
            ):
                raise ValueError(f"Invalid prerequisites for {topic_id}")
            lesson = entry.get("lesson")
            if lesson is not None and not isinstance(lesson, str):
                raise ValueError(f"Invalid lesson path for {topic_id}")
            topic = Topic(topic_id, title, level, tuple(prerequisites), lesson, capstone)
            if lesson is not None:
                self.lesson_path(topic)
            self.topics[topic_id] = topic
            previous = topic_id

    def _validate_graph(self) -> None:
        visited: set[str] = set()
        active: set[str] = set()

        def visit(topic_id: str) -> None:
            if topic_id in active:
                raise ValueError(f"Prerequisite cycle at {topic_id}")
            if topic_id in visited:
                return
            if topic_id not in self.topics:
                raise ValueError(f"Unknown prerequisite: {topic_id}")
            active.add(topic_id)
            for prerequisite in self.topics[topic_id].prerequisites:
                visit(prerequisite)
            active.remove(topic_id)
            visited.add(topic_id)

        for topic_id in self.topics:
            visit(topic_id)

    def get(self, topic_id: str) -> Topic:
        try:
            return self.topics[topic_id.strip().lower()]
        except KeyError:
            raise ValueError(f"Unknown topic '{topic_id}'. Run roadmap for valid IDs.") from None

    def lesson_path(self, topic: Topic) -> Path:
        if topic.lesson is None:
            raise ValueError(
                f"'{topic.id}' is planned, not implemented in Phase 1. Try 'learn variables'."
            )
        path = (self.root / topic.lesson).resolve()
        if not path.is_relative_to(self.root / "lessons") or not (path / "notes.md").is_file():
            raise ValueError(f"Invalid or missing lesson content for {topic.id}")
        return path

    def ordered(self) -> list[Topic]:
        """Stable topological ordering independent of YAML file names."""
        result: list[Topic] = []
        visited: set[str] = set()

        def add(topic: Topic) -> None:
            if topic.id in visited:
                return
            for prerequisite in topic.prerequisites:
                add(self.topics[prerequisite])
            visited.add(topic.id)
            result.append(topic)

        for topic in self.topics.values():
            add(topic)
        return result
