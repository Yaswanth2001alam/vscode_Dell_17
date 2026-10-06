from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Callable

import pytest


TEST_DIR = Path(__file__).resolve().parent
LAB_DIR = TEST_DIR.parent
sys.path.insert(0, str(LAB_DIR))

import lab_automation as lab  # noqa: E402


ROUTERS = ("R1", "R2", "R3")


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--routers",
        nargs="+",
        choices=ROUTERS,
        default=list(ROUTERS),
        help="Routers to test; default: R1 R2 R3",
    )


@pytest.fixture(scope="session")
def inventory() -> dict:
    lab.load_env_file()
    return lab.load_inventory()


@pytest.fixture(scope="session")
def selected_router_names(pytestconfig: pytest.Config) -> list[str]:
    return pytestconfig.getoption("--routers")


@pytest.fixture(scope="session")
def report_dir() -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = TEST_DIR / "results" / timestamp
    path.mkdir(parents=True, exist_ok=True)
    return path


@pytest.fixture(params=ROUTERS)
def router_name(
    request: pytest.FixtureRequest, selected_router_names: list[str]
) -> str:
    if request.param not in selected_router_names:
        pytest.skip(f"{request.param} not selected")
    return request.param


@pytest.fixture(scope="session")
def connections(inventory: dict, selected_router_names: list[str]):
    active = {}
    try:
        for name in selected_router_names:
            active[name] = lab.connect(inventory[name])
        yield active
    finally:
        for connection in active.values():
            connection.disconnect()


@pytest.fixture
def device(router_name: str, connections: dict):
    return connections[router_name]


@pytest.fixture
def show(
    request: pytest.FixtureRequest,
    device,
    router_name: str,
    report_dir: Path,
) -> Callable[[str], str]:
    """Execute and record read-only IOS commands."""

    def execute(command: str) -> str:
        if not re.match(r"^(show|ping)\s", command, re.IGNORECASE):
            raise ValueError(f"Read-only test rejected command: {command}")
        output = device.send_command(command, read_timeout=90)
        safe_command = re.sub(r"[^a-zA-Z0-9_-]+", "_", command).strip("_")
        safe_test = re.sub(r"[^a-zA-Z0-9_-]+", "_", request.node.name).strip("_")
        path = report_dir / router_name
        path.mkdir(parents=True, exist_ok=True)
        artifact = {
            "test": request.node.nodeid,
            "device": router_name,
            "command": command,
            "output": output,
        }
        (path / f"{safe_test}__{safe_command}.json").write_text(
            json.dumps(artifact, indent=2), encoding="utf-8"
        )
        return output

    return execute


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    result_root = TEST_DIR / "results"
    result_root.mkdir(parents=True, exist_ok=True)
    summary = {
        "completed_at": datetime.now().isoformat(timespec="seconds"),
        "exit_status": exitstatus,
        "tests_collected": session.testscollected,
        "tests_failed": session.testsfailed,
    }
    (result_root / "latest_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
