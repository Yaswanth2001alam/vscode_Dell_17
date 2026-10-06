"""Offline regression coverage for every individual protocol Python example."""

import copy
import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "protocols"


class ProtocolPythonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paths = sorted(ROOT.glob("layer-*/*.py"))
        cls.modules = {
            path: runpy.run_path(str(path), run_name=f"protocol_{path.stem}")
            for path in cls.paths
        }

    def test_exact_markdown_python_parity_for_all_seven_layers(self):
        expected = {path.with_suffix(".py") for path in ROOT.glob("layer-*/*.md")}
        self.assertEqual(expected, set(self.paths))
        self.assertEqual(len(self.paths), 44)
        self.assertEqual(
            {path.parent.name for path in self.paths},
            {f"layer-{layer}" for layer in range(1, 8)},
        )

    def test_every_sample_passes_and_missing_fields_fail(self):
        for path, module in self.modules.items():
            with self.subTest(protocol=path.stem):
                sample = module["load_observation"](None)
                self.assertTrue(module["report"](sample)["passed"])
                self.assertFalse(module["report"]({})["passed"])
                for field in module["EXPECTED"]:
                    missing = dict(sample)
                    del missing[field]
                    self.assertFalse(module["report"](missing)["passed"])

    def test_numeric_boundaries_and_invalid_types(self):
        for path, module in self.modules.items():
            for field, policy in module["EXPECTED"].items():
                if not isinstance(policy, dict):
                    continue
                if "minimum" not in policy and "maximum" not in policy:
                    continue
                matches = module["_matches"]
                with self.subTest(protocol=path.stem, field=field):
                    for invalid in (True, False, None, "5", float("nan"), float("inf")):
                        self.assertFalse(matches(policy, invalid))
                    if "minimum" in policy:
                        self.assertTrue(matches(policy, policy["minimum"]))
                        self.assertFalse(matches(policy, policy["minimum"] - 1))
                    if "maximum" in policy:
                        self.assertTrue(matches(policy, policy["maximum"]))
                        self.assertFalse(matches(policy, policy["maximum"] + 1))
                    if policy.get("integer"):
                        self.assertFalse(matches(policy, 1.5))

    def test_scalar_types_and_allowed_membership_are_strict(self):
        for path, module in self.modules.items():
            with self.subTest(protocol=path.stem):
                matches = module["_matches"]
                self.assertFalse(matches(True, 1))
                self.assertFalse(matches(0, False))
                self.assertTrue(matches({"allowed": [1, 6, 11]}, 6))
                self.assertFalse(matches({"allowed": [1, 6, 11]}, True))
                self.assertFalse(matches({"allowed": [1, 6, 11]}, 9))

    def test_sample_loads_are_independent(self):
        for path, module in self.modules.items():
            with self.subTest(protocol=path.stem):
                sample = module["load_observation"](None)
                original = copy.deepcopy(module["SAMPLE_OBSERVATION"])
                for value in sample.values():
                    if isinstance(value, list):
                        value.append("mutation")
                self.assertEqual(module["SAMPLE_OBSERVATION"], original)

    def test_every_cli_returns_json_and_failure_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "observation.json"
            input_path.write_text("{}", encoding="utf-8")
            for path in self.paths:
                with self.subTest(protocol=path.stem):
                    healthy = subprocess.run(
                        [sys.executable, "-B", str(path)],
                        capture_output=True, text=True, timeout=10,
                    )
                    self.assertEqual(healthy.returncode, 0, healthy.stderr)
                    self.assertTrue(json.loads(healthy.stdout)["passed"])
                    missing = subprocess.run(
                        [sys.executable, "-B", str(path), "--input", str(input_path)],
                        capture_output=True, text=True, timeout=10,
                    )
                    self.assertEqual(missing.returncode, 1, missing.stderr)
                    self.assertFalse(json.loads(missing.stdout)["passed"])

    def test_malformed_and_non_object_json_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "observation.json"
            for text in ('{', '[]', '{"counter": NaN}', '{"counter": Infinity}'):
                path.write_text(text, encoding="utf-8")
                for module in self.modules.values():
                    with self.subTest(protocol=module["PROTOCOL"], text=text):
                        with self.assertRaises(ValueError):
                            module["load_observation"](path)


if __name__ == "__main__":
    unittest.main()
