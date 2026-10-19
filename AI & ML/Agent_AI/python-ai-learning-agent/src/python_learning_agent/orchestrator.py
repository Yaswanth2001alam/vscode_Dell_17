"""Route explicit offline learning requests without shell or model execution."""

import json
from pathlib import Path
from typing import Any

from python_learning_agent.config import Settings
from python_learning_agent.curriculum import Curriculum
from python_learning_agent.progress import Progress
from python_learning_agent.storage import Storage


class LearningAgent:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.curriculum = Curriculum(settings.root)

    @property
    def progress(self) -> Progress:
        return Progress(Storage(self.settings.data_dir), self.curriculum)

    def content(self, topic_id: str, filename: str = "notes.md") -> str:
        if filename not in {"notes.md", "exercises.py", "solutions.py"}:
            raise ValueError("Unsupported lesson resource.")
        topic = self.curriculum.get(topic_id)
        return (self.curriculum.lesson_path(topic) / filename).read_text(encoding="utf-8")

    def quiz(self, topic_id: str) -> list[dict[str, Any]]:
        path: Path = self.curriculum.lesson_path(self.curriculum.get(topic_id)) / "quiz.json"
        questions: Any = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(questions, list) or not questions:
            raise ValueError("Quiz must be a nonempty list.")
        for question in questions:
            if not isinstance(question, dict):
                raise ValueError("Quiz question must be an object.")
            if not all(isinstance(question.get(key), str) for key in ("prompt", "explanation")):
                raise ValueError("Quiz requires a prompt and explanation.")
            options = question.get("options")
            answer = question.get("answer")
            if (
                not isinstance(options, dict)
                or not options
                or not all(isinstance(k, str) and isinstance(v, str) for k, v in options.items())
                or not isinstance(answer, str)
                or answer not in options
            ):
                raise ValueError("Quiz requires labeled options and a valid answer.")
        return questions
