"""Fixtures keep all test progress outside the learner's actual database."""

from pathlib import Path

import pytest

from python_learning_agent.config import Settings
from python_learning_agent.orchestrator import LearningAgent

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def agent(tmp_path: Path) -> LearningAgent:
    return LearningAgent(Settings(ROOT, tmp_path / "data"))


@pytest.fixture(autouse=True)
def isolated_cli(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("PYTHON_LEARNING_ROOT", str(ROOT))
    monkeypatch.setenv("PYTHON_LEARNING_DATA_DIR", str(tmp_path / "cli-data"))
