"""
Fairness, privacy, and responsible AI evaluation.

Level: Intermediate to advanced.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Expose a subgroup failure hidden by one total
# Compute denominators and rates transparently.
# Step 1: Create synthetic outcomes for two sites.
# Step 2: Calculate per-site recall only where positive examples exist.
# Step 3: Retain group counts.
# Step 4: Assert the unequal rates and avoid labeling the model compliant.
if __name__ == "__main__":
    import numpy as np

    truth = np.array([1, 1, 0, 0, 1, 1, 0, 0])
    prediction = np.array([1, 1, 0, 0, 1, 0, 0, 0])
    sites = np.array(["a"] * 4 + ["b"] * 4)
    report = {}
    for site in sorted(set(sites)):
        mask = sites == site
        positives = int(((truth == 1) & mask).sum())
        true_positives = int(((truth == 1) & (prediction == 1) & mask).sum())
        recall = None if positives == 0 else true_positives / positives
        report[site] = {"samples": int(mask.sum()), "actual_positives": positives, "recall": recall}
    assert report["a"]["recall"] == 1.0 and report["b"]["recall"] == 0.5
    print("overall accuracy:", float((truth == prediction).mean()))
    print("subgroup evidence:", report)
