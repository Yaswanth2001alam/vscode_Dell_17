"""
Bias, variance, overfitting, and model selection.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Tune a polynomial ridge model without leaking the test set
# Separate selection from final evaluation.
# Step 1: Generate noisy nonlinear data and reserve a test set.
# Step 2: Put transforms in a pipeline.
# Step 3: Search a tiny grid on training folds.
# Step 4: Evaluate the selected estimator on the untouched test partition.
if __name__ == "__main__":
    import numpy as np
    from sklearn.linear_model import Ridge
    from sklearn.metrics import mean_absolute_error
    from sklearn.model_selection import GridSearchCV, KFold, train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import PolynomialFeatures, StandardScaler

    rng = np.random.default_rng(42)
    X = rng.uniform(-2, 2, (120, 1))
    y = X[:, 0] ** 2 + rng.normal(0, 0.15, 120)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    pipeline = Pipeline([("poly", PolynomialFeatures(include_bias=False)),
                         ("scale", StandardScaler()), ("ridge", Ridge())])
    search = GridSearchCV(pipeline, {"poly__degree": [1, 2, 4], "ridge__alpha": [0.01, 1.]},
                          cv=KFold(3, shuffle=True, random_state=42),
                          scoring="neg_mean_absolute_error", n_jobs=1)
    search.fit(X_train, y_train)
    error = mean_absolute_error(y_test, search.predict(X_test))
    assert error < 0.5
    print("selected:", search.best_params_)
    print("test MAE:", round(error, 3))
