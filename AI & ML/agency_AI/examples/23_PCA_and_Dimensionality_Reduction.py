"""
PCA and dimensionality reduction.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Compress and reconstruct correlated features
# Inspect retained variance and reconstruction error.
# Step 1: Generate a shared latent factor plus small noise.
# Step 2: Standardize before PCA.
# Step 3: Keep one component.
# Step 4: Check dimensions and compare reconstruction error with the standardized variance scale.
if __name__ == "__main__":
    import numpy as np
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler

    rng = np.random.default_rng(42)
    latent = rng.normal(size=(160, 1))
    X = latent @ np.array([[1., 2., -1.]]) + rng.normal(0, 0.05, (160, 3))
    standardized = StandardScaler().fit_transform(X)
    pca = PCA(n_components=1).fit(standardized)
    Z = pca.transform(standardized)
    reconstruction = pca.inverse_transform(Z)
    error = np.mean((standardized - reconstruction) ** 2)
    assert Z.shape == (160, 1) and pca.explained_variance_ratio_[0] > 0.95
    assert error < 0.05
    print("retained variance:", round(float(pca.explained_variance_ratio_[0]), 4))
    print("reconstruction MSE:", round(float(error), 4))
