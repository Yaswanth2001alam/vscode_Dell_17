"""
Bag-of-words, TF-IDF, and text classification.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Build a sparse TF-IDF classification pipeline
# Train text representation and classifier together.
# Step 1: Keep vocabulary learning inside the pipeline.
# Step 2: Use unigrams and bigrams.
# Step 3: Fit a linear classifier on synthetic sentiment labels.
# Step 4: Check vocabulary behavior and toy predictions.
if __name__ == "__main__":
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline

    texts = ["good stable service", "excellent good connection", "happy reliable service",
             "bad unstable service", "terrible bad connection", "unhappy broken service"]
    labels = [1, 1, 1, 0, 0, 0]
    model = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), LogisticRegression(C=10))
    model.fit(texts, labels)
    predicted = model.predict(["good reliable connection", "bad broken connection"])
    assert predicted.tolist() == [1, 0]
    vectorizer = model.steps[0][1]
    matrix = vectorizer.transform(texts)
    assert matrix.shape[0] == 6 and "never-seen-token" not in vectorizer.vocabulary_
    print("toy sentiment labels:", predicted.tolist())
    print("sparse feature shape:", matrix.shape)
