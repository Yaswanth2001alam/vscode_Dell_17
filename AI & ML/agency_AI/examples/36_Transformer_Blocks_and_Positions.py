"""
Transformer blocks and positional information.

Level: Advanced.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Check multi-head block causality with a perturbation
# Demonstrate learned projections and positional embeddings.
# Step 1: Build token plus position embeddings.
# Step 2: Create a two-head transformer layer with dropout zero.
# Step 3: Apply an upper-triangular causal mask.
# Step 4: Change the last token and assert earlier outputs remain unchanged.
if __name__ == "__main__":
    import torch
    from torch import nn

    torch.set_num_threads(1)
    torch.manual_seed(42)
    token_embedding, position_embedding = nn.Embedding(12, 8), nn.Embedding(5, 8)
    tokens = torch.tensor([[1, 2, 3, 4, 5]])
    positions = torch.arange(tokens.shape[1])
    layer = nn.TransformerEncoderLayer(d_model=8, nhead=2, dim_feedforward=16,
                                       dropout=0.0, batch_first=True)
    layer.eval()
    mask = torch.triu(torch.ones(5, 5, dtype=torch.bool), diagonal=1)
    with torch.inference_mode():
        original = token_embedding(tokens) + position_embedding(positions)
        output = layer(original, src_mask=mask)
        changed_tokens = tokens.clone()
        changed_tokens[0, -1] = 9
        changed = token_embedding(changed_tokens) + position_embedding(positions)
        perturbed = layer(changed, src_mask=mask)
    assert output.shape == (1, 5, 8)
    torch.testing.assert_close(output[:, :-1], perturbed[:, :-1], atol=1e-6, rtol=1e-5)
    assert not torch.allclose(output[:, -1], perturbed[:, -1])
    print("block shape:", tuple(output.shape), "earlier positions unchanged")
