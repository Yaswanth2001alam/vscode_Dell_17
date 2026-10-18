"""
Pandas tables and exploratory data analysis.

Level: Beginner.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Inspect and summarize a telemetry table
# Practice missingness, filtering, and grouped aggregation.
# Step 1: Construct a DataFrame from local records.
# Step 2: Count missing measurements explicitly.
# Step 3: Group valid latency values by site.
# Step 4: Verify the values and keep labels separate from features.
if __name__ == "__main__":
    import pandas as pd

    frame = pd.DataFrame({
        "site": ["a", "a", "b", "b"],
        "latency_ms": [10., 20., 40., None],
        "outage": [0, 0, 1, 1],
    })
    assert frame.shape == (4, 3)
    assert frame["latency_ms"].isna().sum() == 1
    summary = frame.groupby("site")["latency_ms"].mean()
    assert summary.to_dict() == {"a": 15.0, "b": 40.0}
    X = frame[["latency_ms"]].copy()
    y = frame["outage"].copy()
    assert X.shape == (4, 1) and y.shape == (4,)
    print("missing:", frame.isna().sum().to_dict())
    print("site means:", summary.to_dict())
