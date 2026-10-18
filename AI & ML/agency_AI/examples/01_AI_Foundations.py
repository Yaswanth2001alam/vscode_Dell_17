"""
What AI is: AI, ML, deep learning, and generative AI.

Level: Beginner.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Fit a tiny numerical model, then use it
# Distinguish data, learned parameters, and a new prediction without needing an ML library.
# Step 1: Separate observed input values and labels.
# Step 2: Estimate the slope and intercept from two consistent observations.
# Step 3: Predict for a previously unseen input.
# Step 4: Assert a known answer and inspect the learned parameters.
if __name__ == "__main__":
    utilization = [0.2, 0.4, 0.6]
    latency_ms = [12.0, 14.0, 16.0]
    weight = (latency_ms[-1] - latency_ms[0]) / (utilization[-1] - utilization[0])
    bias = latency_ms[0] - weight * utilization[0]
    prediction = weight * 0.5 + bias
    assert abs(prediction - 15.0) < 1e-9
    print("learned parameters:", round(weight, 2), round(bias, 2))
    print("inference latency_ms:", round(prediction, 2))

# %% Worked example: Contrast classification, regression, and generated text
# Make output types explicit without confusing rule-based examples with learned models.
# Step 1: Define three different output contracts.
# Step 2: Check a class label and a numeric prediction separately.
# Step 3: Generate a templated sentence and label it as templating, not generative learning.
if __name__ == "__main__":
    def classify_latency(value):
        return "high" if value >= 20 else "normal"
    def predict_linear_latency(utilization):
        return 5.0 + 0.2 * utilization
    def render_template(hostname, label):
        return f"{hostname} has {label} latency."
    label = classify_latency(25)
    numeric = predict_linear_latency(50)
    text = render_template("edge-01", label)
    assert label == "high" and numeric == 15.0
    assert text == "edge-01 has high latency."
    print("category:", label, "numeric:", numeric)
    print("template, not a learned generator:", text)
