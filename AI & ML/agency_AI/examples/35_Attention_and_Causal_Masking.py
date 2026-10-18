"""
Attention, self-attention, and causal masking.

Level: Intermediate to advanced.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Compute masked scaled dot-product attention
# Verify both the math and the no-future-information invariant.
# Step 1: Create Q, K, V from one small sequence.
# Step 2: Compute scaled scores.
# Step 3: Mask future key positions before stable softmax.
# Step 4: Check row sums and exact zero future weights.
if __name__ == "__main__":
    import numpy as np

    X = np.array([[1., 0.], [0., 1.], [1., 1.]])
    Q, K, V = X.copy(), X.copy(), X.copy()
    scores = Q @ K.T / np.sqrt(K.shape[1])
    future = np.triu(np.ones((3, 3), dtype=bool), k=1)
    scores[future] = -np.inf
    weights = np.exp(scores - scores.max(axis=1, keepdims=True))
    weights /= weights.sum(axis=1, keepdims=True)
    output = weights @ V
    np.testing.assert_allclose(weights.sum(axis=1), 1)
    assert np.all(weights[future] == 0)
    np.testing.assert_allclose(output[0], V[0])
    print("attention weights:", np.round(weights, 3).tolist())
    print("output shape:", output.shape)
