"""
System/user prompts, context, and model boundaries.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Build an evidence-oriented request with explicit boundaries
# Separate instructions from untrusted source text.
# Step 1: Define a system task contract.
# Step 2: Keep user intent and retrieved evidence in separate fields.
# Step 3: Set a finite output budget.
# Step 4: Verify structure without claiming the prompt enforces security by itself.
if __name__ == "__main__":
    import json

    request = {
        "messages": [
            {"role": "system", "content": "Answer from supplied evidence. If unsupported, say unknown. Return a concise answer and source IDs."},
            {"role": "user", "content": "What MTU does the lab policy require?"},
        ],
        "evidence": [{"id": "lab-policy-1", "text": "The simulated lab interface MTU is 1500 bytes."}],
        "max_output_tokens": 100,
    }
    assert request["messages"][0]["role"] == "system"
    assert request["evidence"][0]["id"] == "lab-policy-1"
    assert 0 < request["max_output_tokens"] <= 100
    encoded = json.dumps(request, sort_keys=True)
    assert json.loads(encoded) == request
    print("request constructed; no model called")
    print("evidence IDs:", [item["id"] for item in request["evidence"]])
