"""Small transactional SQLite store; no external service or credentials."""

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


class Storage:
    def __init__(self, data_dir: Path) -> None:
        data_dir.mkdir(parents=True, exist_ok=True)
        self.path = data_dir / "progress.sqlite3"
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS topics (
                    topic_id TEXT PRIMARY KEY,
                    status TEXT NOT NULL CHECK(status IN ('started', 'completed')),
                    difficult INTEGER NOT NULL DEFAULT 0,
                    revision_required INTEGER NOT NULL DEFAULT 0,
                    last_study TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS quiz_attempts (
                    id INTEGER PRIMARY KEY,
                    topic_id TEXT NOT NULL,
                    score REAL NOT NULL CHECK(score >= 0 AND score <= 100),
                    attempted_at TEXT NOT NULL
                );
                """
            )

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        """Commit on success, roll back on error, and always release the connection."""
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        try:
            with connection:
                yield connection
        finally:
            connection.close()
