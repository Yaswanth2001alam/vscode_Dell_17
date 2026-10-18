"""
Datasets, supervision, and train/validation/test splits.

Level: Beginner to intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Disjoint stratified data partitions
# Track sample IDs to prove split isolation.
# Step 1: Generate labeled synthetic samples with a fixed seed.
# Step 2: Reserve test data first.
# Step 3: Split the remaining development data into train and validation.
# Step 4: Assert disjoint IDs and full coverage.
if __name__ == "__main__":
    import numpy as np
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split

    X, y = make_classification(n_samples=200, n_features=6, random_state=42)
    ids = np.arange(len(y))
    dev, test = train_test_split(ids, test_size=0.2, stratify=y, random_state=42)
    train, validation = train_test_split(dev, test_size=0.25, stratify=y[dev], random_state=42)
    assert [len(train), len(validation), len(test)] == [120, 40, 40]
    assert not (set(train) & set(validation) or set(train) & set(test) or set(validation) & set(test))
    assert set(train) | set(validation) | set(test) == set(ids)
    print("train/validation/test:", len(train), len(validation), len(test))
    print("feature shape:", X.shape, "target shape:", y.shape)
