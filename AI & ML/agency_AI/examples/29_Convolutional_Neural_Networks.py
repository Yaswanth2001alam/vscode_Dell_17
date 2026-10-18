"""
Convolutional neural networks and image features.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Inspect a convolution's geometry and parameter sharing
# Apply one known kernel to a synthetic image.
# Step 1: Construct a 1x1x5x5 tensor with a vertical stripe.
# Step 2: Install a hand-written 3x3 kernel without gradient updates.
# Step 3: Run convolution and pooling.
# Step 4: Assert output shapes and nonzero response.
if __name__ == "__main__":
    import torch
    from torch import nn

    torch.set_num_threads(1)
    image = torch.zeros(1, 1, 5, 5)
    image[:, :, :, 2] = 1
    convolution = nn.Conv2d(1, 1, kernel_size=3, bias=False)
    kernel = torch.tensor([[-1., 0., 1.], [-1., 0., 1.], [-1., 0., 1.]])
    with torch.no_grad():
        convolution.weight.copy_(kernel.reshape(1, 1, 3, 3))
    features = convolution(image)
    pooled = nn.MaxPool2d(2)(features.abs())
    assert features.shape == (1, 1, 3, 3) and pooled.shape == (1, 1, 1, 1)
    assert torch.count_nonzero(features).item() > 0
    assert sum(parameter.numel() for parameter in convolution.parameters()) == 9
    print("feature shape:", tuple(features.shape), "pooled response:", pooled.item())

# %% Worked example: Train a CNN on synthetic stripe images
# Move from a fixed kernel to actual learned visual classification on a held-out set.
# Step 1: Generate noisy horizontal and vertical stripe examples locally.
# Step 2: Split before training.
# Step 3: Train a small CNN on CPU.
# Step 4: Assert reduced training loss and held-out accuracy.
if __name__ == "__main__":
    import numpy as np
    import torch
    from torch import nn
    from sklearn.model_selection import train_test_split

    torch.set_num_threads(1)
    torch.manual_seed(42)
    rng = np.random.default_rng(42)
    images = rng.normal(0, 0.08, (160, 1, 8, 8)).astype(np.float32)
    labels = np.arange(160) % 2
    for index, label in enumerate(labels):
        position = int(rng.integers(2, 6))
        if label == 0:
            images[index, 0, :, position] += 1
        else:
            images[index, 0, position, :] += 1
    train_ids, test_ids = train_test_split(np.arange(160), stratify=labels, random_state=42)
    train_X, test_X = torch.tensor(images[train_ids]), torch.tensor(images[test_ids])
    train_y = torch.tensor(labels[train_ids], dtype=torch.long)
    model = nn.Sequential(nn.Conv2d(1, 4, 3), nn.ReLU(), nn.Flatten(), nn.Linear(4*6*6, 2))
    optimizer, criterion = torch.optim.Adam(model.parameters(), lr=0.02), nn.CrossEntropyLoss()
    initial = criterion(model(train_X), train_y).item()
    for _ in range(65):
        optimizer.zero_grad()
        loss = criterion(model(train_X), train_y)
        loss.backward()
        optimizer.step()
    model.eval()
    with torch.inference_mode():
        accuracy = float((model(test_X).argmax(1).numpy() == labels[test_ids]).mean())
    assert loss.item() < initial and accuracy > 0.9
    print("synthetic stripe held-out accuracy:", round(accuracy, 3))
