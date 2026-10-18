"""
Conditions, loops, functions, lambda, and OOP.

Level: Beginner.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Reusable rule object with explicit validation
# Follow an input through a method, branch, returned label, and rejection path.
# Step 1: Store a threshold on one instance.
# Step 2: Validate input before comparing.
# Step 3: Use a function and loop to score records.
# Step 4: Sort with lambda and prove invalid input raises without a fake result.
if __name__ == "__main__":
    class LatencyRule:
        def __init__(self, threshold):
            self.threshold = threshold

        def predict(self, latency_ms):
            if not isinstance(latency_ms, (int, float)) or isinstance(latency_ms, bool):
                raise TypeError("numeric latency required")
            if latency_ms < 0:
                raise ValueError("latency cannot be negative")
            return int(latency_ms >= self.threshold)

    def score(values, rule):
        return [rule.predict(value) for value in values]

    rule = LatencyRule(20)
    assert score([5, 20, 30], rule) == [0, 1, 1]
    ranked = sorted([{"ms": 20}, {"ms": 5}], key=lambda row: row["ms"])
    try:
        rule.predict(-1)
    except ValueError as error:
        print(str(error))
    else:
        raise AssertionError("invalid input accepted")
    print("sorted:", ranked, "labels:", score([5, 20, 30], rule))

# %% Worked example: Compose a predictor and a reporting service
# Use dependency injection rather than a large inheritance hierarchy.
# Step 1: Define a small public prediction contract.
# Step 2: Inject a fake into a service.
# Step 3: Verify the same service can use a different compatible collaborator.
if __name__ == "__main__":
    class ConstantPredictor:
        def __init__(self, label):
            self.label = label
        def predict(self, features):
            return self.label

    class ReportService:
        def __init__(self, predictor):
            self.predictor = predictor
        def report(self, features):
            return {"prediction": self.predictor.predict(features)}

    normal = ReportService(ConstantPredictor("normal"))
    alert = ReportService(ConstantPredictor("alert"))
    assert normal.report([10, 0]) == {"prediction": "normal"}
    assert alert.report([10, 0]) == {"prediction": "alert"}
    print("same service, independently injected policies")
