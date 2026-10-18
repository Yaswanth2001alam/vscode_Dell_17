"""
K-nearest neighbors and support vector machines.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Compare two nonlinear classifiers on the same split
# Keep preprocessing and evaluation conditions consistent.
# Step 1: Generate two-moon data with a fixed seed.
# Step 2: Reserve a stratified test set.
# Step 3: Use a separate scaling pipeline for each classifier.
# Step 4: Check held-out scores without selecting a winner from the test set.
if __name__ == "__main__":
    from sklearn.datasets import make_moons
    from sklearn.model_selection import train_test_split
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.svm import SVC

    X, y = make_moons(n_samples=240, noise=0.12, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)
    estimators = {"knn": KNeighborsClassifier(n_neighbors=5), "svm": SVC(C=2, gamma="scale")}
    scores = {}
    for name, estimator in estimators.items():
        model = make_pipeline(StandardScaler(), estimator).fit(X_train, y_train)
        scores[name] = round(model.score(X_test, y_test), 3)
    assert all(score > 0.8 for score in scores.values())
    print("held-out accuracies:", scores)
