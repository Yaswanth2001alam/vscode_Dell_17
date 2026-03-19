from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import pytest


@dataclass
class WanDevice:
    name: str
    vendor: str
    site: str


PathInfo = Dict[str, Dict[str, List[WanDevice]]]


@pytest.fixture(scope="function")
def all_paths_info() -> List[PathInfo]:
    return [
        {
            "siteA-siteB": {   # ✅ dict here (NOT a list)
                "primary": [
                    WanDevice("r1", "cisco", "siteA"),
                    WanDevice("r2", "juniper", "siteB"),
                ],
                "backup": [
                    WanDevice("r3", "arista", "siteA"),
                ],
            }
        },
        {
            "siteA-siteC": {   # ✅ dict here (NOT a list)
                "primary": [
                    WanDevice("r4", "cisco", "siteA"),
                    WanDevice("r5", "juniper", "siteC"),
                ],
                "backup": [],
            }
        },
    ]