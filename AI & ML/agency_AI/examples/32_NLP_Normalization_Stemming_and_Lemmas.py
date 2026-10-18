"""
NLP preprocessing, normalization, stemming, and lemmatization.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Compare minimal normalization with toy morphology
# Make every text transformation explicit.
# Step 1: Normalize case and tokenize while preserving hyphenated identifiers.
# Step 2: Apply a deliberately limited suffix rule.
# Step 3: Use a tiny explicit irregular lemma dictionary.
# Step 4: Assert that negation and host identity survive.
if __name__ == "__main__":
    import re

    text = "EDGE-01 devices were running, not failed."
    tokens = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text.lower())
    def toy_stem(token):
        return token[:-1] if token.endswith("s") and len(token) > 3 else token
    lemma_dictionary = {"were": "be", "running": "run", "devices": "device"}
    stems = [toy_stem(token) for token in tokens]
    lemmas = [lemma_dictionary.get(token, token) for token in tokens]
    assert "edge-01" in tokens and "not" in tokens
    assert "run" in lemmas and "running" in stems
    print("tokens:", tokens)
    print("toy stems:", stems)
    print("dictionary lemmas:", lemmas)
