"""
Inference, temperature, top-p, and generation.

Level: Intermediate to advanced.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Stable temperature scaling and correct nucleus selection
# Test the top-p boundary explicitly.
# Step 1: Convert logits with a stable softmax.
# Step 2: Sort probabilities in descending order.
# Step 3: Keep the boundary token needed to reach p.
# Step 4: Sample with a seeded RNG and assert membership only in the retained set.
if __name__ == "__main__":
    import numpy as np

    def distribution(logits, temperature):
        if temperature <= 0:
            raise ValueError("positive temperature required; use argmax for greedy")
        scaled = np.asarray(logits, dtype=float) / temperature
        values = np.exp(scaled - scaled.max())
        return values / values.sum()

    def nucleus(probabilities, p):
        if not 0 < p <= 1:
            raise ValueError("p must be in (0, 1]")
        order = np.argsort(-probabilities)
        count = min(len(order), int(np.searchsorted(np.cumsum(probabilities[order]), p)) + 1)
        kept = order[:count]
        weights = probabilities[kept] / probabilities[kept].sum()
        return kept, weights

    probabilities = np.array([0.6, 0.3, 0.1])
    kept, weights = nucleus(probabilities, 0.7)
    assert kept.tolist() == [0, 1]
    assert distribution([2, 1, 0], 0.5).max() > distribution([2, 1, 0], 2).max()
    samples = np.random.default_rng(42).choice(kept, size=10, p=weights)
    assert set(samples).issubset({0, 1})
    print("top-p retained:", kept.tolist(), "renormalized:", np.round(weights, 3).tolist())
    print("sampled token IDs:", samples.tolist())
