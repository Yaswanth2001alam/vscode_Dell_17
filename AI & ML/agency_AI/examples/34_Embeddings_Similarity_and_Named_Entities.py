"""
Embeddings, semantic similarity, and named entities.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Vector similarity and constrained entity spans
# Inspect geometry and extraction without hidden downloads.
# Step 1: Normalize small handcrafted vectors.
# Step 2: Rank a query by cosine similarity.
# Step 3: Extract only the declared hostname pattern.
# Step 4: Check exact matched spans rather than inferring general language understanding.
if __name__ == "__main__":
    import re
    import numpy as np

    vectors = np.array([[1., 0.], [0.95, 0.1], [0., 1.]])
    names = ["router", "switch", "flower"]
    normalized = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
    similarities = normalized @ normalized[0]
    ranking = np.argsort(-similarities)
    assert [names[index] for index in ranking] == ["router", "switch", "flower"]
    text = "edge-01 reported loss near core-02."
    entities = [(match.group(), match.start(), match.end())
                for match in re.finditer(r"\b(?:edge|core)-\d{2}\b", text)]
    assert [item[0] for item in entities] == ["edge-01", "core-02"]
    print("handcrafted similarities:", np.round(similarities, 3).tolist())
    print("pattern-based entities:", entities)

# %% Worked example: Learn lexical latent embeddings from a local corpus
# Distinguish fitted latent semantic representations from handcrafted vectors and pretrained contextual embeddings.
# Step 1: Fit TF-IDF on a tiny local corpus.
# Step 2: Learn a low-rank SVD representation.
# Step 3: Normalize document embeddings and inspect similarity.
# Step 4: Verify shape and finite values without claiming broad semantic understanding.
if __name__ == "__main__":
    import numpy as np
    from sklearn.decomposition import TruncatedSVD
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import normalize

    corpus = ["router packet forwarding network", "switch packet network port",
              "router switch network", "garden flower plant soil",
              "flower garden leaf plant", "soil garden growing plant"]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    model = TruncatedSVD(n_components=2, random_state=42)
    embeddings = normalize(model.fit_transform(X))
    similarities = embeddings @ embeddings.T
    assert embeddings.shape == (6, 2) and np.isfinite(embeddings).all()
    assert similarities[0, 1] > similarities[0, 3]
    print("learned lexical embedding shape:", embeddings.shape)
    print("router-switch / router-garden similarity:", round(similarities[0, 1], 3), round(similarities[0, 3], 3))

# %% Worked example: Train a constrained token-level entity classifier
# Practice supervised entity labels without pretending a regex is a learned NER model.
# Step 1: Represent tokens by explicit lexical shape features.
# Step 2: Train a token classifier on synthetic labels.
# Step 3: Evaluate previously unseen host IDs and ordinary words.
# Step 4: State that there is no general NER or span-context capability here.
if __name__ == "__main__":
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline

    def features(token):
        return {"has_dash": "-" in token, "has_digit": any(char.isdigit() for char in token),
                "prefix": token.split("-")[0] if "-" in token else "ordinary"}
    train_tokens = ["edge-01", "edge-02", "core-01", "core-02", "lab-01", "lab-02",
                    "router", "status", "up", "down", "traffic", "failed"]
    targets = ["HOST"] * 6 + ["O"] * 6
    model = make_pipeline(DictVectorizer(), LogisticRegression(C=10))
    model.fit([features(token) for token in train_tokens], targets)
    tokens = ["edge-99", "reported", "core-88"]
    predicted = model.predict([features(token) for token in tokens]).tolist()
    assert predicted == ["HOST", "O", "HOST"]
    print("synthetic token entity labels:", list(zip(tokens, predicted)))
