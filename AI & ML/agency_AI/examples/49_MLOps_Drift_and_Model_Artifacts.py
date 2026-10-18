"""
MLOps, drift, reproducibility, and model artifacts.

Level: Advanced.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Version a simple artifact and flag a shifted batch
# Keep provenance and monitoring separate from model inference.
# Step 1: Serialize a small allowlisted model record.
# Step 2: Hash its canonical bytes.
# Step 3: Compare reference and new batch means using reference scale.
# Step 4: Assert that the synthetic large shift triggers an explicit flag.
if __name__ == "__main__":
    import hashlib
    import json
    import numpy as np

    artifact = {"schema_version": 1, "model_version": "linear-v1",
                "feature_names": ["utilization"], "weights": [0.3], "bias": 5.0}
    encoded = json.dumps(artifact, sort_keys=True, separators=(",", ":")).encode()
    fingerprint = hashlib.sha256(encoded).hexdigest()
    rng = np.random.default_rng(42)
    reference = rng.normal(0, 1, 500)
    new = rng.normal(4, 1, 200)
    shift = abs(new.mean() - reference.mean()) / reference.std()
    alert = {"feature": "utilization", "standardized_mean_shift": float(shift), "flagged": bool(shift > 2)}
    assert len(fingerprint) == 64 and alert["flagged"]
    assert json.loads(encoded)["feature_names"] == ["utilization"]
    print("artifact SHA-256:", fingerprint)
    print("synthetic drift flag:", alert["flagged"], "shift:", round(shift, 3))
