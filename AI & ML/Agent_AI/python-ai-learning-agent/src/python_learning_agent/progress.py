"""Persistent progress and prerequisite-based recommendations."""

from datetime import UTC, datetime
from typing import Any

from python_learning_agent.curriculum import Curriculum, Topic
from python_learning_agent.storage import Storage


class Progress:
    def __init__(self, storage: Storage, curriculum: Curriculum) -> None:
        self.storage = storage
        self.curriculum = curriculum

    def records(self) -> list[dict[str, Any]]:
        with self.storage.connect() as connection:
            return [
                dict(row)
                for row in connection.execute(
                    """SELECT topics.*, (SELECT MAX(score) FROM quiz_attempts
                       WHERE quiz_attempts.topic_id = topics.topic_id) AS best_score
                       FROM topics ORDER BY last_study DESC, topic_id"""
                )
            ]

    def completed(self) -> set[str]:
        return {row["topic_id"] for row in self.records() if row["status"] == "completed"}

    def mark(self, topic_id: str, *, complete: bool = False, difficult: bool = False) -> None:
        topic = self.curriculum.get(topic_id)
        self.curriculum.lesson_path(topic)
        if complete:
            missing = set(topic.prerequisites) - self.completed()
            if missing:
                raise ValueError(f"Complete prerequisites first: {', '.join(sorted(missing))}")
        now = datetime.now(UTC).isoformat()
        with self.storage.connect() as connection:
            connection.execute(
                """INSERT INTO topics
                   (topic_id, status, difficult, revision_required, last_study)
                   VALUES (?, ?, ?, ?, ?)
                   ON CONFLICT(topic_id) DO UPDATE SET
                   status = CASE WHEN excluded.status = 'completed' THEN 'completed'
                                 ELSE topics.status END,
                   difficult = MAX(topics.difficult, excluded.difficult),
                   revision_required = CASE WHEN excluded.status = 'completed' THEN 0
                       ELSE MAX(topics.revision_required, excluded.revision_required) END,
                   last_study = excluded.last_study""",
                (topic.id, "completed" if complete else "started", difficult, difficult, now),
            )

    def record_quiz(self, topic_id: str, score: float) -> None:
        if not 0 <= score <= 100:
            raise ValueError("Quiz score must be between 0 and 100.")
        self.mark(topic_id)
        topic = self.curriculum.get(topic_id)
        with self.storage.connect() as connection:
            connection.execute(
                "INSERT INTO quiz_attempts(topic_id, score, attempted_at) VALUES (?, ?, ?)",
                (topic.id, score, datetime.now(UTC).isoformat()),
            )
            connection.execute(
                "UPDATE topics SET revision_required = ? WHERE topic_id = ?",
                (score < 80, topic.id),
            )

    def next_topic(self) -> tuple[Topic | None, str]:
        for row in self.records():
            if row["revision_required"]:
                return self.curriculum.get(row["topic_id"]), "Revision recommended"
        completed = self.completed()
        for topic in self.curriculum.ordered():
            if (
                topic.lesson is not None
                and topic.id not in completed
                and set(topic.prerequisites) <= completed
            ):
                return topic, "Available lesson"
        for topic in self.curriculum.ordered():
            if topic.id not in completed and set(topic.prerequisites) <= completed:
                return topic, "Next roadmap topic (lesson not implemented)"
        return None, "Roadmap completed"
