from __future__ import annotations

import os

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("network safety")
    group.addoption(
        "--run-live",
        action="store_true",
        default=False,
        help="Run read-only live network tests",
    )
    group.addoption(
        "--run-disruptive",
        action="store_true",
        default=False,
        help="Run explicitly implemented disruptive lab tests",
    )


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    run_live = config.getoption("--run-live")
    run_disruptive = config.getoption("--run-disruptive")
    skip_live = pytest.mark.skip(reason="requires --run-live and an authorized lab")
    skip_disruptive = pytest.mark.skip(
        reason="requires --run-live --run-disruptive and an isolated lab"
    )
    for item in items:
        if "disruptive" in item.keywords and not (run_live and run_disruptive):
            item.add_marker(skip_disruptive)
        elif "live" in item.keywords and not run_live:
            item.add_marker(skip_live)


@pytest.fixture
def inventory() -> dict[str, dict[str, object]]:
    return {
        "leaf01": {
            "host": "192.0.2.11",
            "platform": "nxos",
            "role": "leaf",
            "site": "lab",
            "port": 22,
        },
        "leaf02": {
            "host": "192.0.2.12",
            "platform": "nxos",
            "role": "leaf",
            "site": "lab",
            "port": 22,
        },
    }


@pytest.fixture
def healthy_lacp_flags() -> dict[str, bool]:
    return {
        "synchronized": True,
        "collecting": True,
        "distributing": True,
        "defaulted": False,
        "expired": False,
    }


@pytest.fixture
def live_target() -> str:
    target = os.getenv("NETWORK_TEST_TARGET")
    if not target:
        pytest.skip("set NETWORK_TEST_TARGET to one authorized lab hostname or IP")
    return target

