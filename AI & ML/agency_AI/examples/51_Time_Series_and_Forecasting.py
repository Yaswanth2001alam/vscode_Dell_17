"""
Time-series forecasting without future leakage.

Level: Intermediate to advanced.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Chronological one-step regression with a baseline
# Make time availability explicit.
# Step 1: Create a synthetic autoregressive series.
# Step 2: Build targets only from prior lag values.
# Step 3: Train on the earlier partition and evaluate later observations.
# Step 4: Report MAE for both model and persistence without selecting on test.
if __name__ == "__main__":
    import numpy as np
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error

    rng = np.random.default_rng(42)
    series = np.zeros(240)
    for index in range(1, len(series)):
        series[index] = 0.8 * series[index-1] + rng.normal(0, 0.2)
    X, y = series[:-1, None], series[1:]
    cutoff = 170
    model = LinearRegression().fit(X[:cutoff], y[:cutoff])
    predicted = model.predict(X[cutoff:])
    model_error = mean_absolute_error(y[cutoff:], predicted)
    baseline_error = mean_absolute_error(y[cutoff:], X[cutoff:, 0])
    assert predicted.shape == y[cutoff:].shape
    assert model_error < 0.4 and baseline_error < 0.4
    print("one-step test MAE:", round(model_error, 3))
    print("persistence MAE:", round(baseline_error, 3))
