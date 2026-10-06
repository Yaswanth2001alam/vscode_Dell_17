"""Offline RESTCONF normalized-state validation.

Run the healthy teaching sample:
    python restconf.py

Validate collected observations:
    python restconf.py --input observation.json

This is a policy example, not a protocol implementation or live collector.
Expected values are illustrative intent, not universal vendor defaults.
Collect real device/API/packet observations separately and normalize their
field names and types before using this validator. No network I/O or device
changes are performed. See the adjacent Markdown file for protocol theory.
"""

from __future__ import annotations

import argparse
import copy
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

PROTOCOL = 'RESTCONF'
OSI_LAYERS = (7,)
PURPOSE = 'Manages YANG data using HTTP resources'
TRANSPORT = 'HTTPS'
DEFAULT_PORTS = (443,)
EXPECTED = {'status': 200,
 'media type': 'application/yang-data+json',
 'schema': 'valid',
 'ETag': 'matched'}
SAMPLE_OBSERVATION = {'status': 200,
 'media type': 'application/yang-data+json',
 'schema': 'valid',
 'ETag': 'matched'}


@dataclass(frozen=True)
class ValidationResult:
    field: str
    passed: bool
    expected: Any
    observed: Any
    detail: str = ""


def _matches(expected: Any, observed: Any) -> bool:
    if not isinstance(expected, dict):
        return type(observed) is type(expected) and observed == expected
    if "allowed" in expected:
        if not any(
            type(observed) is type(value) and observed == value
            for value in expected["allowed"]
        ):
            return False
    if "minimum" in expected or "maximum" in expected:
        if type(observed) not in (int, float):
            return False
        if isinstance(observed, float) and not math.isfinite(observed):
            return False
        if expected.get("integer") and type(observed) is not int:
            return False
        if "minimum" in expected and observed < expected["minimum"]:
            return False
        if "maximum" in expected and observed > expected["maximum"]:
            return False
    return True


def validate(observation: Mapping[str, Any]) -> list[ValidationResult]:
    """Validate teaching intent against already-collected, normalized state."""

    results: list[ValidationResult] = []
    for field, expected in EXPECTED.items():
        present = field in observation
        observed = observation.get(field)
        passed = present and _matches(expected, observed)
        detail = ""
        if not present:
            detail = f"Missing required field: {field}"
        elif not passed:
            detail = f"{field} does not satisfy policy"
        results.append(ValidationResult(field, passed, expected, observed, detail))
    return results


def _reject_constant(value: str) -> None:
    raise ValueError(f"Non-finite JSON value is not permitted: {value}")


def load_observation(path: Path | None) -> dict[str, Any]:
    if path is None:
        return copy.deepcopy(SAMPLE_OBSERVATION)
    data = json.loads(
        path.read_text(encoding="utf-8"),
        parse_constant=_reject_constant,
    )
    if not isinstance(data, dict):
        raise ValueError("Observation JSON must contain an object")
    return data


def report(observation: Mapping[str, Any]) -> dict[str, Any]:
    results = validate(observation)
    return {
        "protocol": PROTOCOL,
        "osi_layers": OSI_LAYERS,
        "purpose": PURPOSE,
        "transport": TRANSPORT,
        "default_ports": DEFAULT_PORTS,
        "mode": "offline-normalized-state-validation",
        "passed": bool(results) and all(result.passed for result in results),
        "checks": [asdict(result) for result in results],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="Normalized JSON observation")
    args = parser.parse_args(argv)
    output = report(load_observation(args.input))
    print(json.dumps(output, indent=2, allow_nan=False))
    return 0 if output["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
