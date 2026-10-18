"""
Python variables, strings, and containers.

Level: Beginner.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Build and inspect a small telemetry record collection
# Practice the Python data structures used by later datasets.
# Step 1: Normalize hostname strings.
# Step 2: Use a tuple for a coordinate-like pair and a set for distinct roles.
# Step 3: Copy a list before appending.
# Step 4: Assert required dictionary fields and shared-reference behavior.
if __name__ == "__main__":
    hostname = " EDGE-01 ".strip().lower()
    record = {"hostname": hostname, "latency_ms": 12.5, "role": "edge"}
    records = [record, {"hostname": "core-01", "latency_ms": 4.0, "role": "core"}]
    coordinates = (1, 2)
    roles = {row["role"] for row in records}
    alias = records
    separate = list(records)
    separate.append({"hostname": "lab-01", "latency_ms": 1.0, "role": "lab"})
    assert alias is records and separate is not records
    assert len(records) == 2 and len(separate) == 3
    assert coordinates[0] == 1 and hostname == "edge-01"
    print(f"{record['hostname']}: {record['latency_ms']:.1f} ms")
    print("roles:", sorted(roles))
