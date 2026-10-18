"""
RNNs, sequence modeling, and encoder-decoder ideas.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Inspect recurrent output and hidden-state shapes
# Trace batch, sequence, and hidden dimensions.
# Step 1: Create a batch-first three-sequence input.
# Step 2: Run a small GRU encoder.
# Step 3: Map every timestep to vocabulary logits.
# Step 4: Verify that final hidden state matches the last valid timestep for equal-length inputs.
if __name__ == "__main__":
    import torch
    from torch import nn

    torch.set_num_threads(1)
    torch.manual_seed(42)
    inputs = torch.randn(3, 5, 4)
    encoder = nn.GRU(input_size=4, hidden_size=6, batch_first=True)
    outputs, hidden = encoder(inputs)
    projection = nn.Linear(6, 8)
    token_logits = projection(outputs)
    assert outputs.shape == (3, 5, 6)
    assert hidden.shape == (1, 3, 6) and token_logits.shape == (3, 5, 8)
    torch.testing.assert_close(hidden[0], outputs[:, -1])
    print("encoder:", tuple(outputs.shape), "hidden:", tuple(hidden.shape))
    print("per-position vocabulary logits:", tuple(token_logits.shape))
