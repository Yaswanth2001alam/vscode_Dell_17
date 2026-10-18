"""
Decision trees and rule-like decisions.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Train a shallow tree and inspect its rules
# Connect a fitted model to its branching structure.
# Step 1: Generate informative synthetic data.
# Step 2: Keep the test partition untouched during fitting.
# Step 3: Limit depth and leaf size.
# Step 4: Print a short rule listing and check basic held-out performance.
if __name__ == "__main__":
    from sklearn.datasets import make_classification
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeClassifier, export_text

    X, y = make_classification(n_samples=300, n_features=4, n_informative=3,
                               n_redundant=0, class_sep=1.6, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)
    model = DecisionTreeClassifier(max_depth=3, min_samples_leaf=5, random_state=42)
    model.fit(X_train, y_train)
    score = accuracy_score(y_test, model.predict(X_test))
    assert model.get_depth() <= 3 and score > 0.65
    print("held-out accuracy:", round(score, 3))
    print(export_text(model, max_depth=1).strip())
