"""
Multimodal models and contrastive representations.

Level: Advanced.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Learn alignment between two synthetic modalities
# Train and verify the matching objective directly.
# Step 1: Create independent trainable embedding tables for paired IDs.
# Step 2: Normalize both before similarity.
# Step 3: Train a symmetric contrastive loss.
# Step 4: Assert diagonal retrieval after optimization.
if __name__ == "__main__":
    import torch
    from torch import nn
    from torch.nn import functional as F

    torch.set_num_threads(1)
    torch.manual_seed(42)
    image_ids = nn.Parameter(torch.randn(4, 8))
    text_ids = nn.Parameter(torch.randn(4, 8))
    optimizer = torch.optim.Adam([image_ids, text_ids], lr=0.05)
    labels = torch.arange(4)
    for _ in range(100):
        optimizer.zero_grad()
        similarities = F.normalize(image_ids, dim=1) @ F.normalize(text_ids, dim=1).T / 0.1
        loss = (F.cross_entropy(similarities, labels) + F.cross_entropy(similarities.T, labels)) / 2
        loss.backward()
        optimizer.step()
    assert similarities.argmax(1).tolist() == [0, 1, 2, 3]
    print("synthetic matched pair IDs:", similarities.argmax(1).tolist())
    print("contrastive loss:", round(loss.item(), 4))
