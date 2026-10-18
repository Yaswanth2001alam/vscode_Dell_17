"""
Preprocessing and leakage-safe pipelines.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Mixed numeric and categorical preprocessing
# Fit transform state only through the training pipeline.
# Step 1: Select numeric and site columns by name.
# Step 2: Impute missing latency and standardize it.
# Step 3: Encode site values and fit logistic regression.
# Step 4: Predict an unseen site and verify finite probabilities.
if __name__ == "__main__":
    import numpy as np
    import pandas as pd
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    train = pd.DataFrame({"latency": [1., 2., np.nan, 8., 9., 10.],
                          "site": ["a", "a", "b", "b", "a", "b"]})
    y = [0, 0, 0, 1, 1, 1]
    numeric = make_pipeline(SimpleImputer(strategy="median"), StandardScaler())
    preprocessing = ColumnTransformer([
        ("numeric", numeric, ["latency"]),
        ("site", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["site"]),
    ])
    model = make_pipeline(preprocessing, LogisticRegression())
    model.fit(train, y)
    new = pd.DataFrame({"latency": [9.], "site": ["new-site"]})
    probabilities = model.predict_proba(new)
    assert probabilities.shape == (1, 2) and np.isfinite(probabilities).all()
    assert np.isclose(probabilities.sum(), 1)
    print("new-site probabilities:", np.round(probabilities, 3).tolist())
