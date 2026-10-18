"""
Accuracy, precision, recall, F1, and calibration.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Hand-check metrics and threshold tradeoffs
# Verify formulas with counts, not just library output.
# Step 1: Construct fixed binary truth and score vectors.
# Step 2: Threshold scores at 0.5.
# Step 3: Compute confusion counts and known metrics.
# Step 4: Lower the threshold and verify recall cannot decrease on these fixed scores.
if __name__ == "__main__":
    import numpy as np
    from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score

    truth = np.array([1, 1, 1, 0, 0, 0])
    scores = np.array([0.9, 0.8, 0.2, 0.7, 0.1, 0.05])
    predicted = (scores >= 0.5).astype(int)
    matrix = confusion_matrix(truth, predicted)
    assert matrix.tolist() == [[2, 1], [1, 2]]
    assert np.isclose(precision_score(truth, predicted), 2/3)
    assert np.isclose(recall_score(truth, predicted), 2/3)
    assert np.isclose(f1_score(truth, predicted), 2/3)
    lower = (scores >= 0.2).astype(int)
    assert recall_score(truth, lower) >= recall_score(truth, predicted)
    print("confusion matrix:", matrix.tolist())
    print("accuracy/precision/recall/F1:", [round(fn(truth, predicted), 3)
          for fn in [accuracy_score, precision_score, recall_score, f1_score]])

# %% Worked example: Expose an imbalanced accuracy trap
# Show why a high accuracy can coexist with zero incident recall.
# Step 1: Create 100 examples with one positive.
# Step 2: Predict the majority class for all rows.
# Step 3: Report accuracy together with recall and F1.
if __name__ == "__main__":
    from sklearn.metrics import accuracy_score, f1_score, recall_score

    truth = [0] * 99 + [1]
    predicted = [0] * 100
    accuracy = accuracy_score(truth, predicted)
    recall = recall_score(truth, predicted)
    f1 = f1_score(truth, predicted, zero_division=0)
    assert accuracy == 0.99 and recall == 0 and f1 == 0
    print("accuracy:", accuracy, "incident recall:", recall, "incident F1:", f1)
