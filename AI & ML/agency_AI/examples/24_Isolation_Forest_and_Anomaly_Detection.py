"""
Isolation Forest and anomaly detection.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Fit a reference and score new observations
# Use explicit inlier/outlier semantics.
# Step 1: Generate a compact historical reference distribution.
# Step 2: Fit a bounded Isolation Forest.
# Step 3: Score a typical point and a distant new observation.
# Step 4: Check both the score ordering and labels.
if __name__ == "__main__":
    import numpy as np
    from sklearn.ensemble import IsolationForest

    rng = np.random.default_rng(42)
    historical = rng.normal(0, 0.3, (200, 2))
    detector = IsolationForest(n_estimators=50, contamination=0.05, random_state=42, n_jobs=1)
    detector.fit(historical)
    new = np.array([[0., 0.], [8., 8.]])
    scores = detector.decision_function(new)
    labels = detector.predict(new)
    assert scores[1] < scores[0] and labels.tolist() == [1, -1]
    print("decision scores:", np.round(scores, 3).tolist())
    print("inlier/outlier labels:", labels.tolist())
