"""
Generative models: autoencoders, GANs, and diffusion.

Level: Advanced.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Inspect the forward diffusion equation
# Understand signal/noise mixing before training a model.
# Step 1: Create a small clean signal and seeded Gaussian noise.
# Step 2: Mix with an explicit alpha_bar.
# Step 3: Invert using the known injected noise.
# Step 4: Assert exact reconstruction within numerical tolerance and state the oracle limitation.
if __name__ == "__main__":
    import numpy as np

    clean = np.linspace(-1, 1, 12)
    noise = np.random.default_rng(42).normal(size=clean.shape)
    alpha_bar = 0.4
    noisy = np.sqrt(alpha_bar) * clean + np.sqrt(1 - alpha_bar) * noise
    oracle_reconstruction = (noisy - np.sqrt(1 - alpha_bar) * noise) / np.sqrt(alpha_bar)
    np.testing.assert_allclose(oracle_reconstruction, clean, atol=1e-12)
    assert not np.allclose(noisy, clean)
    print("clean shape:", clean.shape, "noisy differs:", not np.allclose(noisy, clean))
    print("oracle reconstruction error:", round(float(np.abs(oracle_reconstruction - clean).max()), 12))

# %% Worked example: Train a denoising network on synthetic signals
# Distinguish a learned denoiser from the oracle inversion example.
# Step 1: Generate low-dimensional clean signals embedded in a larger vector.
# Step 2: Add independent Gaussian noise.
# Step 3: Train a small network using only the training split.
# Step 4: Compare held-out reconstruction MSE against the noisy-input baseline.
if __name__ == "__main__":
    import torch
    from torch import nn

    torch.set_num_threads(1)
    torch.manual_seed(42)
    latent = torch.randn(300, 1)
    clean = latent @ torch.tensor([[1., 0.5, -0.5, -1.]])
    noisy = clean + 0.5 * torch.randn_like(clean)
    model = nn.Sequential(nn.Linear(4, 8), nn.Tanh(), nn.Linear(8, 4))
    optimizer = torch.optim.Adam(model.parameters(), lr=0.02)
    for _ in range(140):
        optimizer.zero_grad()
        loss = ((model(noisy[:220]) - clean[:220]) ** 2).mean()
        loss.backward()
        optimizer.step()
    model.eval()
    with torch.inference_mode():
        error = ((model(noisy[220:]) - clean[220:]) ** 2).mean().item()
        baseline = ((noisy[220:] - clean[220:]) ** 2).mean().item()
    assert error < baseline
    print("held-out denoising MSE:", round(error, 4), "noisy baseline:", round(baseline, 4))
    print("a learned denoiser, not a complete diffusion sampler")
