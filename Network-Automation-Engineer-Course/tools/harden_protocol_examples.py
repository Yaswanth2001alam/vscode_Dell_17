"""Regenerate the course's standalone protocol validators without touching notes.

The existing companion modules supply their protocol metadata and teaching
policies. This tool updates only those Python companions, never their Markdown
notes, indexes, configuration, or other course modules.
"""

from __future__ import annotations

import ast
from pathlib import Path
from pprint import pformat


ROOT = Path(__file__).resolve().parents[1] / "protocols"
CONSTANTS = (
    "PROTOCOL",
    "OSI_LAYERS",
    "PURPOSE",
    "TRANSPORT",
    "DEFAULT_PORTS",
    "EXPECTED",
    "SAMPLE_OBSERVATION",
)
INTEGER_FIELDS = {
    "speed", "TTL", "hop limit", "prefixes", "priority", "window",
    "retransmission", "counter", "stratum", "reach", "errors", "FCS",
    "retries", "age", "MTU", "port", "access VLAN", "native VLAN",
}


def metadata(path: Path) -> dict[str, object]:
    values = {}
    for node in ast.parse(path.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and target.id in CONSTANTS:
                values[target.id] = ast.literal_eval(node.value)
        elif isinstance(node, ast.AnnAssign):
            target = node.target
            if isinstance(target, ast.Name) and target.id in CONSTANTS:
                values[target.id] = ast.literal_eval(node.value)
    missing = set(CONSTANTS) - values.keys()
    if missing:
        raise ValueError(f"{path}: missing metadata {sorted(missing)}")
    return values


BODY = '''

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
'''


def render(path: Path) -> str:
    values = metadata(path)
    expected = values["EXPECTED"]
    sample = values["SAMPLE_OBSERVATION"]
    for field, policy in expected.items():
        if isinstance(policy, dict) and field in INTEGER_FIELDS:
            policy["integer"] = True
            sample[field] = int(sample[field])

    if values["PROTOCOL"] == "DNS":
        expected["TTL"] = {"minimum": 0, "maximum": 2_147_483_647, "integer": True}
        expected["answer"] = ["192.0.2.10"]
        sample["answer"] = ["192.0.2.10"]
        sample["TTL"] = 3600
    elif values["PROTOCOL"] == "MPLS":
        expected["FEC"] = "203.0.113.0/24"
        sample["FEC"] = "203.0.113.0/24"
    elif values["PROTOCOL"] == "PIM":
        expected["neighbor"] = "up"
        sample["neighbor"] = "up"

    header = f'''"""Offline {values["PROTOCOL"]} normalized-state validation.

Run the healthy teaching sample:
    python {path.name}

Validate collected observations:
    python {path.name} --input observation.json

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

'''
    assignments = "\n".join(
        f"{name} = {pformat(values[name], width=88, sort_dicts=False)}"
        for name in CONSTANTS
    )
    return header + assignments + "\n" + BODY


def main() -> int:
    paths = sorted(ROOT.glob("layer-*/*.py"))
    if not paths:
        raise RuntimeError("No protocol Python companions found")
    rendered = {path: render(path) for path in paths}
    for path, content in rendered.items():
        compile(content, str(path), "exec")
    for path, content in rendered.items():
        path.write_text(content, encoding="utf-8")
    print(f"Updated {len(paths)} protocol Python companions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
