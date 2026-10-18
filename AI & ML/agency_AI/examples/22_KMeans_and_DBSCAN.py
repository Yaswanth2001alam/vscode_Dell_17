"""
Unsupervised clustering: K-means and DBSCAN.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Fit clusters and identify an explicit outlier
# Compare centroid grouping with density-based noise handling.
# Step 1: Generate separated blobs and fit K-means without labels.
# Step 2: Measure permutation-invariant agreement only afterward.
# Step 3: Add a distant point for DBSCAN.
# Step 4: Check that noise is -1 rather than pretending it is a normal class.
if __name__ == "__main__":
    import numpy as np
    from sklearn.cluster import DBSCAN, KMeans
    from sklearn.datasets import make_blobs
    from sklearn.metrics import adjusted_rand_score

    X, hidden_labels = make_blobs(n_samples=120, centers=[[-3, -3], [3, 3]],
                                 cluster_std=0.3, random_state=42)
    groups = KMeans(n_clusters=2, n_init=10, random_state=42).fit_predict(X)
    agreement = adjusted_rand_score(hidden_labels, groups)
    assert agreement > 0.9
    with_outlier = np.vstack([X, [20, 20]])
    density_groups = DBSCAN(eps=0.7, min_samples=4).fit_predict(with_outlier)
    assert density_groups[-1] == -1
    print("external synthetic agreement:", round(agreement, 3))
    print("DBSCAN noise points:", int((density_groups == -1).sum()))

# %% Worked example: Trace one K-means assignment/update step
# Understand the centroid arithmetic underneath the estimator.
# Step 1: Create two well-separated groups and two starting centroids.
# Step 2: Assign each row to its nearest centroid.
# Step 3: Update each centroid and compare with the manually known means.
if __name__ == "__main__":
    import numpy as np

    X = np.array([[0., 0.], [0., 2.], [10., 10.], [10., 12.]])
    centroids = np.array([[0., 0.], [10., 10.]])
    distances = ((X[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)
    assignments = distances.argmin(axis=1)
    updated = np.vstack([X[assignments == group].mean(axis=0) for group in range(2)])
    assert assignments.tolist() == [0, 0, 1, 1]
    np.testing.assert_allclose(updated, [[0., 1.], [10., 11.]])
    print("assignments:", assignments.tolist(), "updated centroids:", updated.tolist())
