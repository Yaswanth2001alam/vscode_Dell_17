"""
Random forests and bagging.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: A bounded forest with held-out permutation importance
# Train an ensemble without using all CPU cores.
# Step 1: Create a controlled dataset and held-out split.
# Step 2: Fit a modest n_jobs=1 forest.
# Step 3: Evaluate accuracy and compute permutation importance.
# Step 4: Check importance shape and finite values.
if __name__ == "__main__":
    import numpy as np
    from sklearn.datasets import make_classification
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.inspection import permutation_importance
    from sklearn.model_selection import train_test_split

    X, y = make_classification(n_samples=300, n_features=5, n_informative=3,
                               class_sep=1.5, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)
    model = RandomForestClassifier(n_estimators=40, min_samples_leaf=2, n_jobs=1, random_state=42)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    importance = permutation_importance(model, X_test, y_test, n_repeats=3, random_state=42, n_jobs=1)
    assert score > 0.75 and importance.importances_mean.shape == (5,)
    assert np.isfinite(importance.importances_mean).all()
    print("held-out accuracy:", round(score, 3))
    print("permutation importance:", np.round(importance.importances_mean, 3).tolist())
