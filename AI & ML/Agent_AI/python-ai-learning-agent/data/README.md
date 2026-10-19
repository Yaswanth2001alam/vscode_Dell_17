# Local learning state

The application creates `progress.sqlite3` here on first progress-related command.
The database contains local topic status, UTC study timestamps, quiz history,
difficulty flags, and revision flags. It is excluded from Git and is not encrypted.
Use `PYTHON_LEARNING_DATA_DIR` to select a different directory.

Tests always use temporary databases. The Phase 1 terminal demonstration uses
`reports\phase1-demo-data`, not your personal progress database.
