"""
Gradient boosting on tabular data.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Fit a nonlinear numeric relationship
# See boosting outperform a constant baseline on held-out data.
# Step 1: Generate a deterministic nonlinear target plus noise.
# Step 2: Split before fitting.
# Step 3: Fit a small bounded ensemble.
# Step 4: Compare test MAE against a training-mean baseline.
if __name__ == "__main__":
    import numpy as np
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.metrics import mean_absolute_error
    from sklearn.model_selection import train_test_split

    rng = np.random.default_rng(42)
    X = rng.uniform(-2, 2, (240, 2))
    y = X[:, 0] ** 2 + np.sin(X[:, 1]) + rng.normal(0, 0.1, 240)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    model = GradientBoostingRegressor(n_estimators=70, max_depth=2, random_state=42)
    model.fit(X_train, y_train)
    error = mean_absolute_error(y_test, model.predict(X_test))
    baseline = mean_absolute_error(y_test, np.full_like(y_test, y_train.mean()))
    assert error < baseline
    print("test MAE:", round(error, 3), "baseline:", round(baseline, 3))
