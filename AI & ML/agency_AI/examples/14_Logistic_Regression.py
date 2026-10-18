"""
Logistic regression and classification probabilities.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Train and inspect probabilities on a held-out set
# See the difference between scores and decisions.
# Step 1: Generate binary labels and split with stratification.
# Step 2: Scale inside a training pipeline.
# Step 3: Fit logistic regression and inspect class-1 probabilities.
# Step 4: Check normalization and nontrivial held-out accuracy.
if __name__ == "__main__":
    import numpy as np
    from sklearn.datasets import make_classification
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    X, y = make_classification(n_samples=300, n_features=6, n_informative=4,
                               class_sep=1.5, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=300))
    model.fit(X_train, y_train)
    probabilities = model.predict_proba(X_test)
    labels = (probabilities[:, 1] >= 0.5).astype(int)
    score = accuracy_score(y_test, labels)
    assert score > 0.75
    np.testing.assert_allclose(probabilities.sum(axis=1), 1)
    print("first probabilities:", np.round(probabilities[:3, 1], 3).tolist())
    print("held-out accuracy:", round(score, 3))

# %% Worked example: Check sigmoid confidence and class threshold
# Inspect probabilities without interpreting them as guaranteed correctness.
# Step 1: Compute stable sigmoid values for fixed scores.
# Step 2: Threshold into decisions.
# Step 3: Verify symmetry and the exact zero-score boundary.
if __name__ == "__main__":
    import numpy as np

    scores = np.array([-2., 0., 2.])
    probabilities = 1 / (1 + np.exp(-scores))
    labels = (probabilities >= 0.5).astype(int)
    assert labels.tolist() == [0, 1, 1]
    assert np.isclose(probabilities[0] + probabilities[2], 1)
    assert probabilities[1] == 0.5
    print("probabilities:", np.round(probabilities, 3).tolist(), "labels:", labels.tolist())
