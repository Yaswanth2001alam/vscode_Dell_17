"""
Files, JSON, and explicit data boundaries.

Level: Beginner.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Safely write, read, and reject a malformed record
# Practice a temporary file plus schema checks.
# Step 1: Validate the exact required field set.
# Step 2: Write UTF-8 JSON inside a temporary folder.
# Step 3: Read the content back using a context manager.
# Step 4: Reject a negative latency instead of silently fixing it.
if __name__ == "__main__":
    import json
    from pathlib import Path
    from tempfile import TemporaryDirectory

    def validate(record):
        if not isinstance(record, dict) or set(record) != {"hostname", "latency_ms"}:
            raise ValueError("unexpected record fields")
        latency = record["latency_ms"]
        if not isinstance(record["hostname"], str) or not record["hostname"].strip():
            raise ValueError("hostname must be nonempty")
        if type(latency) not in (int, float) or not 0 <= latency < float("inf"):
            raise ValueError("finite nonnegative latency required")
        return record

    original = validate({"hostname": "edge-01", "latency_ms": 12.5})
    with TemporaryDirectory() as folder:
        path = Path(folder) / "sample.json"
        with path.open("w", encoding="utf-8") as handle:
            json.dump(original, handle)
        with path.open(encoding="utf-8") as handle:
            restored = validate(json.load(handle))
        assert restored == original
    try:
        validate({"hostname": "edge-01", "latency_ms": -1})
    except ValueError:
        print("invalid record rejected")
    else:
        raise AssertionError("negative value accepted")
    print(restored)
