"""
Linear regression and numerical prediction.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Held-out regression versus a constant baseline
# Fit an actual estimator and evaluate it on unseen synthetic rows.
# Step 1: Generate a noisy linear target with a fixed seed.
# Step 2: Fit only the training partition.
# Step 3: Compute MAE on untouched test rows.
# Step 4: Require improvement over a training-mean baseline.
if __name__ == "__main__":
    import numpy as np
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error
    from sklearn.model_selection import train_test_split

    rng = np.random.default_rng(42)
    X = rng.uniform(0, 100, (240, 2))
    y = 5 + X @ np.array([0.3, 0.1]) + rng.normal(0, 1, 240)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    model = LinearRegression().fit(X_train, y_train)
    error = mean_absolute_error(y_test, model.predict(X_test))
    baseline = mean_absolute_error(y_test, np.full_like(y_test, y_train.mean()))
    assert error < baseline and error < 2
    print("coefficients:", np.round(model.coef_, 3).tolist())
    print("test MAE:", round(error, 3), "baseline MAE:", round(baseline, 3))

# %% Worked example: Learn a slope with gradient descent
# Connect the library estimator to a transparent optimization algorithm.
# Step 1: Generate a known linear relationship.
# Step 2: Calculate the analytical batch gradient.
# Step 3: Apply bounded updates and verify the learned slope against the known value.
if __name__ == "__main__":
    import numpy as np

    X = np.array([0., 0.25, 0.5, 0.75, 1.])
    y = 3 * X
    weight = 0.0
    initial = np.mean((weight * X - y) ** 2)
    for _ in range(160):
        gradient = 2 * np.mean(X * (weight * X - y))
        weight -= 0.2 * gradient
    final = np.mean((weight * X - y) ** 2)
    assert final < initial and abs(weight - 3) < 1e-6
    print("learned slope:", round(weight, 6), "loss decreased:", final < initial)
