from __future__ import annotations

import subprocess
import sys
from pathlib import Path


LAB_DIR = Path(__file__).resolve().parent


def run_lab(*args: str) -> int:
    command = [sys.executable, str(LAB_DIR / "lab_automation.py"), *args]
    result = subprocess.run(
        command,
        cwd=LAB_DIR,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode
