"""
Transfer learning and frozen feature extractors.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Pretrain locally, freeze, and transfer
# Prove that the source encoder was trained and remains unchanged during target training.
# Step 1: Train a small encoder/head on a source regression task.
# Step 2: Snapshot and freeze encoder weights.
# Step 3: Train a new target head on extracted representations.
# Step 4: Assert encoder identity of values and reduced target loss.
if __name__ == "__main__":
    import torch
    from torch import nn

    torch.set_num_threads(1)
    torch.manual_seed(42)
    X = torch.randn(120, 2)
    source_y = (X[:, :1] + 0.5 * X[:, 1:])
    encoder = nn.Sequential(nn.Linear(2, 6), nn.Tanh())
    source_head = nn.Linear(6, 1)
    optimizer = torch.optim.Adam(list(encoder.parameters()) + list(source_head.parameters()), lr=0.03)
    for _ in range(100):
        optimizer.zero_grad()
        loss = ((source_head(encoder(X)) - source_y) ** 2).mean()
        loss.backward()
        optimizer.step()
    assert loss.item() < 0.1
    before = [parameter.detach().clone() for parameter in encoder.parameters()]
    encoder.requires_grad_(False)
    encoder.eval()
    features = encoder(X).detach()
    target_y = 2 * source_y + 1
    target_head = nn.Linear(6, 1)
    target_optimizer = torch.optim.Adam(target_head.parameters(), lr=0.05)
    initial = ((target_head(features) - target_y) ** 2).mean().item()
    for _ in range(100):
        target_optimizer.zero_grad()
        target_loss = ((target_head(features) - target_y) ** 2).mean()
        target_loss.backward()
        target_optimizer.step()
    assert target_loss.item() < initial
    for saved, parameter in zip(before, encoder.parameters()):
        torch.testing.assert_close(saved, parameter)
    print("source loss:", round(loss.item(), 3), "target loss:", round(target_loss.item(), 3))
    print("frozen encoder unchanged")
