"""
Train a multilayer neural network with PyTorch.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Actually train and test a small nonlinear classifier
# Run a real CPU-sized training loop with held-out evaluation.
# Step 1: Split synthetic data and fit scaling on training only.
# Step 2: Create a two-layer network and optimizer.
# Step 3: Train with integer targets and raw logits.
# Step 4: Compare initial/final loss and assert useful held-out accuracy.
if __name__ == "__main__":
    import numpy as np
    import torch
    from torch import nn
    from sklearn.datasets import make_moons
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler

    torch.set_num_threads(1)
    torch.manual_seed(42)
    X, y = make_moons(n_samples=260, noise=0.12, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)
    scaler = StandardScaler().fit(X_train)
    train_X = torch.tensor(scaler.transform(X_train), dtype=torch.float32)
    test_X = torch.tensor(scaler.transform(X_test), dtype=torch.float32)
    train_y = torch.tensor(y_train, dtype=torch.long)
    model = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 2))
    optimizer, criterion = torch.optim.Adam(model.parameters(), lr=0.03), nn.CrossEntropyLoss()
    initial = criterion(model(train_X), train_y).item()
    model.train()
    for _ in range(140):
        optimizer.zero_grad()
        loss = criterion(model(train_X), train_y)
        loss.backward()
        optimizer.step()
    model.eval()
    with torch.inference_mode():
        accuracy = float((model(test_X).argmax(1).numpy() == y_test).mean())
        final = criterion(model(train_X), train_y).item()
    assert final < initial and accuracy > 0.85
    print("training loss:", round(initial, 3), "->", round(final, 3))
    print("held-out accuracy:", round(accuracy, 3))
