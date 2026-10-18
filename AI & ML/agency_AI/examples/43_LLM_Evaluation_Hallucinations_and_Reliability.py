"""
Hallucinations, reasoning checks, and LLM evaluation.

Level: Advanced.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Evaluate correctness and evidence separately
# Catch valid-looking but unsupported output.
# Step 1: Declare expected values and supporting source IDs.
# Step 2: Score mock outputs against both dimensions.
# Step 3: Keep per-case failure reasons.
# Step 4: Assert the fabricated value fails even though it has JSON structure.
if __name__ == "__main__":
    cases = [
        {"id": "known", "expected": "1500", "allowed_source": "mtu-policy"},
        {"id": "unknown", "expected": "unknown", "allowed_source": None},
    ]
    mock_outputs = {
        "known": {"answer": "9000", "source": "made-up"},
        "unknown": {"answer": "unknown", "source": None},
    }
    results = []
    for case in cases:
        output = mock_outputs[case["id"]]
        correct = output["answer"] == case["expected"]
        grounded = output["source"] == case["allowed_source"]
        results.append({"id": case["id"], "correct": correct, "grounded": grounded,
                        "passed": correct and grounded})
    assert results[0]["passed"] is False and results[1]["passed"] is True
    pass_rate = sum(item["passed"] for item in results) / len(results)
    assert pass_rate == 0.5
    print("per-case evaluation:", results)
    print("mock-output pass rate:", pass_rate)
