"""
Capstone: a leakage-safe telemetry classifier.

Level: Advanced.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Train, compare, and report a complete small model
# Combine earlier pieces without hidden downloads.
# Step 1: Generate synthetic features with explicit units.
# Step 2: Reserve a stratified test set.
# Step 3: Fit scaling plus logistic regression and a dummy baseline.
# Step 4: Assert improvement and print a classification report.
if __name__ == "__main__":
    import numpy as np
    from sklearn.dummy import DummyClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import classification_report, f1_score
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    rng = np.random.default_rng(42)
    X = np.column_stack([rng.uniform(0, 100, 500), rng.uniform(0, 5, 500), rng.uniform(1, 100, 500)])
    incident_score = 0.03*X[:, 0] + 0.7*X[:, 1] + 0.02*X[:, 2]
    y = (incident_score + rng.normal(0, 0.2, 500) > 4.7).astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=300)).fit(X_train, y_train)
    baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
    prediction = model.predict(X_test)
    score = f1_score(y_test, prediction)
    baseline_score = f1_score(y_test, baseline.predict(X_test), zero_division=0)
    assert score > baseline_score and score > 0.8
    print("test F1:", round(score, 3), "baseline F1:", round(baseline_score, 3))
    print(classification_report(y_test, prediction, zero_division=0))
