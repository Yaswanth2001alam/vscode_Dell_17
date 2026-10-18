"""
Language models, pretraining, and next-token prediction.

Level: Advanced.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Train a tiny neural bigram from scratch
# Shift targets and optimize next-token loss without downloading weights.
# Step 1: Encode a deliberately simple repeated token stream.
# Step 2: Construct one-token input and next-token targets.
# Step 3: Train an embedding table of next-token logits.
# Step 4: Verify loss decreases and learned next-token transitions fit the training pattern.
if __name__ == "__main__":
    import torch
    from torch import nn

    torch.set_num_threads(1)
    torch.manual_seed(42)
    text = "abc" * 60
    vocabulary = sorted(set(text))
    token_to_id = {token: index for index, token in enumerate(vocabulary)}
    ids = torch.tensor([token_to_id[token] for token in text])
    inputs, targets = ids[:-1], ids[1:]
    model = nn.Embedding(len(vocabulary), len(vocabulary))
    optimizer, criterion = torch.optim.Adam(model.parameters(), lr=0.1), nn.CrossEntropyLoss()
    initial = criterion(model(inputs), targets).item()
    for _ in range(90):
        optimizer.zero_grad()
        loss = criterion(model(inputs), targets)
        loss.backward()
        optimizer.step()
    assert loss.item() < initial and loss.item() < 0.05
    next_ids = model(torch.arange(3)).argmax(dim=1).tolist()
    assert next_ids == [token_to_id["b"], token_to_id["c"], token_to_id["a"]]
    print("training loss:", round(initial, 3), "->", round(loss.item(), 3))
    print("learned transitions:", {token: vocabulary[next_ids[index]] for index, token in enumerate(vocabulary)})

# %% Worked example: Train a miniature causal transformer
# Combine embeddings, positions, a causal attention block, and next-token cross-entropy in a real tiny training run.
# Step 1: Encode a repeated synthetic pattern with shifted targets.
# Step 2: Create learned token/position embeddings and a masked block.
# Step 3: Train the vocabulary head end-to-end.
# Step 4: Verify decreasing training loss without claiming held-out language ability.
if __name__ == "__main__":
    import torch
    from torch import nn

    torch.set_num_threads(1)
    torch.manual_seed(42)

    class TinyCausalModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.tokens, self.positions = nn.Embedding(4, 8), nn.Embedding(6, 8)
            self.block = nn.TransformerEncoderLayer(8, 2, 16, dropout=0.0, batch_first=True)
            self.head = nn.Linear(8, 4)

        def forward(self, ids):
            length = ids.shape[1]
            hidden = self.tokens(ids) + self.positions(torch.arange(length))
            mask = torch.triu(torch.ones(length, length, dtype=torch.bool), diagonal=1)
            return self.head(self.block(hidden, src_mask=mask))

    ids = torch.tensor([[0, 1, 2, 3, 0, 1], [1, 2, 3, 0, 1, 2]])
    targets = (ids + 1) % 4
    model = TinyCausalModel()
    optimizer, criterion = torch.optim.Adam(model.parameters(), lr=0.03), nn.CrossEntropyLoss()
    initial = criterion(model(ids).reshape(-1, 4), targets.reshape(-1)).item()
    for _ in range(90):
        optimizer.zero_grad()
        loss = criterion(model(ids).reshape(-1, 4), targets.reshape(-1))
        loss.backward()
        optimizer.step()
    assert loss.item() < initial and loss.item() < 0.1
    print("tiny transformer's training loss:", round(initial, 3), "->", round(loss.item(), 3))
    print("trained on a repeating synthetic pattern, not natural language")
