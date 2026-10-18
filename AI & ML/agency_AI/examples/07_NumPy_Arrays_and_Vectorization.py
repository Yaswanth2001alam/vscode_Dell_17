"""
NumPy arrays, shapes, broadcasting, and vectorization.

Level: Beginner.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Batch predictions and column standardization
# Make array dimensions and standardization visible.
# Step 1: Create a 3x2 feature matrix.
# Step 2: Compute one prediction per row with matrix multiplication.
# Step 3: Center and scale columns using training data statistics.
# Step 4: Assert shapes, arithmetic, and centered columns.
if __name__ == "__main__":
    import numpy as np

    X = np.array([[10., 1.], [20., 2.], [30., 4.]])
    weights = np.array([0.5, 2.0])
    predictions = X @ weights + 1.0
    assert predictions.shape == (3,)
    np.testing.assert_allclose(predictions, [8., 15., 24.])
    means, scales = X.mean(axis=0), X.std(axis=0)
    standardized = (X - means) / scales
    np.testing.assert_allclose(standardized.mean(axis=0), [0., 0.], atol=1e-12)
    independent = X[:1].copy()
    independent[0, 0] = 999
    assert X[0, 0] == 10
    print("shape:", X.shape, "predictions:", predictions.tolist())
    print("column means after scaling:", np.round(standardized.mean(axis=0), 6).tolist())
