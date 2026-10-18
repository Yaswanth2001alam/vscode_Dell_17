"""
Naive Bayes and text classification.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Classify synthetic operational messages
# Train a vocabulary and probabilistic classifier together.
# Step 1: Create training messages and labels.
# Step 2: Fit CountVectorizer inside a Pipeline.
# Step 3: Predict on separate messages.
# Step 4: Assert expected toy outcomes and probability normalization.
if __name__ == "__main__":
    import numpy as np
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.pipeline import make_pipeline

    messages = ["link down outage", "router failed down", "packet loss outage",
                "link healthy stable", "router healthy normal", "traffic stable normal"]
    labels = [1, 1, 1, 0, 0, 0]
    model = make_pipeline(CountVectorizer(), MultinomialNB(alpha=1.0))
    model.fit(messages, labels)
    test = ["link down failed", "healthy stable traffic"]
    predictions = model.predict(test)
    probabilities = model.predict_proba(test)
    assert predictions.tolist() == [1, 0]
    np.testing.assert_allclose(probabilities.sum(axis=1), 1)
    print("labels:", predictions.tolist())
    print("probabilities:", np.round(probabilities, 3).tolist())
