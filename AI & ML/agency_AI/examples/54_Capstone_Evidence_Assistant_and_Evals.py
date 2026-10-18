"""
Capstone: an evidence assistant with regression tests.

Level: Advanced.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Build and test a local evidence contract
# Return only supported extracts or explicit unknown.
# Step 1: Define a validated output record.
# Step 2: Index a small synthetic policy set.
# Step 3: Use a deterministic overlap threshold and source IDs.
# Step 4: Run known and unsupported evaluation cases.
if __name__ == "__main__":
    import numpy as np
    from pydantic import BaseModel, ConfigDict
    from sklearn.feature_extraction.text import TfidfVectorizer

    class Answer(BaseModel):
        model_config = ConfigDict(extra="forbid", strict=True)
        text: str
        source_ids: list[str]

    docs = {"mtu": "Lab interface MTU is 1500 bytes.",
            "backup": "Configuration backup frequency is daily.",
            "dns": "Lab DNS resolver is 192.0.2.53."}
    ids = list(docs)
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(docs.values())
    def answer(query):
        scores = (matrix @ vectorizer.transform([query]).T).toarray().ravel()
        best = int(np.argmax(scores))
        if scores[best] < 0.15:
            return Answer(text="unknown", source_ids=[])
        return Answer(text=docs[ids[best]], source_ids=[ids[best]])
    tests = [("MTU interface bytes", "mtu"), ("backup frequency", "backup"),
             ("penguin habitat", None)]
    for query, expected_id in tests:
        result = answer(query)
        assert result.source_ids == ([] if expected_id is None else [expected_id])
        assert result.text == ("unknown" if expected_id is None else docs[expected_id])
    print("passed evidence cases:", len(tests))
    print(answer("MTU interface bytes").model_dump())
