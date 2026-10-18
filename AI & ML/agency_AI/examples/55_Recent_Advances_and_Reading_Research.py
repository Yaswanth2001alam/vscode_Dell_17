"""
Recent advances and how to evaluate new AI claims.

Level: Advanced.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Budgeted candidate verification and a simple MoE router
# Inspect two modern mechanisms without claiming to reproduce a frontier model.
# Step 1: Evaluate candidate answers with a deterministic verifier.
# Step 2: Stop at a hard candidate budget.
# Step 3: Route a tiny vector to the highest-scoring synthetic expert.
# Step 4: Assert verified correctness and route choice, not general reasoning ability.
if __name__ == "__main__":
    import numpy as np

    candidates = [18, 20, 21]
    budget, checked, accepted = 3, 0, None
    for candidate in candidates[:budget]:
        checked += 1
        if candidate == 3 * 7:
            accepted = candidate
            break
    if accepted is None:
        raise RuntimeError("no verified candidate within budget")
    assert accepted == 21 and checked <= budget
    gate_logits = np.array([0.1, 2.0, -0.5])
    expert = int(np.argmax(gate_logits))
    experts = [lambda x: x, lambda x: 2*x, lambda x: -x]
    output = experts[expert](np.array([1., 2.]))
    assert expert == 1 and output.tolist() == [2., 4.]
    print("verified answer:", accepted, "candidates checked:", checked)
    print("toy selected expert:", expert, "output:", output.tolist())
