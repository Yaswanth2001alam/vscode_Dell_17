"""
Vectors, probability, losses, and optimization.

Level: Beginner to intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Optimize a scalar and verify a probability vector
# Trace parameter updates with independently checkable arithmetic.
# Step 1: Start away from the known optimum.
# Step 2: Apply repeated gradient descent updates.
# Step 3: Compare initial and final loss.
# Step 4: Compute a stable softmax and verify normalization.
if __name__ == "__main__":
    import numpy as np

    weight, rate = 0.0, 0.2
    initial = (weight - 3) ** 2
    for _ in range(40):
        gradient = 2 * (weight - 3)
        weight -= rate * gradient
    final = (weight - 3) ** 2
    assert final < initial and abs(weight - 3) < 1e-6
    logits = np.array([1001., 1002., 1003.])
    exp_values = np.exp(logits - logits.max())
    probabilities = exp_values / exp_values.sum()
    assert np.isclose(probabilities.sum(), 1) and (probabilities > 0).all()
    print("optimized weight:", round(weight, 6), "loss decreased:", final < initial)
    print("probabilities:", np.round(probabilities, 3).tolist())
