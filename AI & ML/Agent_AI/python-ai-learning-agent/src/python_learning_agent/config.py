"""Resolve explicit local paths without reading secrets or changing the workspace."""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    root: Path
    data_dir: Path

    @classmethod
    def from_environment(cls) -> "Settings":
        """Use the editable source checkout unless a content root is supplied."""
        root = Path(
            os.environ.get("PYTHON_LEARNING_ROOT", Path(__file__).resolve().parents[2])
        ).resolve()
        if not (root / "curriculum").is_dir() or not (root / "lessons").is_dir():
            raise ValueError(
                "Content root is missing curriculum/ or lessons/. Use an editable install "
                "or set PYTHON_LEARNING_ROOT to the project directory."
            )
        data_dir = Path(os.environ.get("PYTHON_LEARNING_DATA_DIR", root / "data")).resolve()
        return cls(root=root, data_dir=data_dir)
