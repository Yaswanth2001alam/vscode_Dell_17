"""
Matplotlib and visual reasoning.

Level: Beginner.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Render a labeled prediction plot in memory
# Create a reproducible image without external data.
# Step 1: Use the noninteractive Agg backend for script portability.
# Step 2: Plot observations and a linear predictor.
# Step 3: Set readable labels and a legend.
# Step 4: Verify a real PNG was generated and close the figure.
if __name__ == "__main__":
    from io import BytesIO
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    X = np.array([10, 20, 30, 40])
    y = np.array([5, 8, 10, 14])
    prediction = 0.3 * X + 2
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.scatter(X, y, label="observed")
    ax.plot(X, prediction, label="linear model")
    ax.set(xlabel="Utilization (%)", ylabel="Latency (ms)", title="Synthetic latency example")
    ax.legend()
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=90, bbox_inches="tight")
    assert buffer.getvalue().startswith(b"\x89PNG")
    assert len(ax.lines) == 1
    plt.close(fig)
    print("PNG generated in memory; MAE:", round(float(np.abs(y - prediction).mean()), 3))
