"""
Retrieval-augmented generation and evidence.

Level: Intermediate to advanced.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Retrieve with source IDs and abstain on no overlap
# Keep evidence provenance visible.
# Step 1: Fit a local document index.
# Step 2: Score a query using normalized sparse vectors.
# Step 3: Return a source-backed extract rather than inventing a generated answer.
# Step 4: Assert a relevant source and an unsupported-query abstention.
if __name__ == "__main__":
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer

    documents = [
        {"id": "mtu-policy", "text": "The lab interface MTU is 1500 bytes."},
        {"id": "dns-policy", "text": "The lab DNS resolver is 192.0.2.53."},
        {"id": "backup-policy", "text": "Configuration backups run every day."},
    ]
    vectorizer = TfidfVectorizer()
    index = vectorizer.fit_transform([item["text"] for item in documents])
    def retrieve(query):
        scores = (index @ vectorizer.transform([query]).T).toarray().ravel()
        best = int(np.argmax(scores))
        if scores[best] == 0:
            return {"answer": "unknown", "sources": []}
        document = documents[best]
        return {"answer": document["text"], "sources": [document["id"]]}
    result = retrieve("interface MTU bytes")
    assert result["sources"] == ["mtu-policy"] and "1500" in result["answer"]
    assert retrieve("penguins Antarctica") == {"answer": "unknown", "sources": []}
    print(result)
    print(retrieve("penguins Antarctica"))
