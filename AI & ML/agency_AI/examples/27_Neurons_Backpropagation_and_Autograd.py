"""
Neurons, backpropagation, and autograd.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Check an automatic gradient and reduce loss
# Make one learning update mathematically transparent.
# Step 1: Create a trainable scalar tensor.
# Step 2: Build an explicit prediction and squared loss.
# Step 3: Compare backward's gradient to the analytical answer.
# Step 4: Update without recording the update itself and verify lower loss.
if __name__ == "__main__":
    import torch

    torch.set_num_threads(1)
    weight = torch.tensor(0.0, requires_grad=True)
    x, target = torch.tensor(2.0), torch.tensor(6.0)
    loss = (weight * x - target) ** 2
    loss.backward()
    assert weight.grad.item() == -24.0
    before = loss.item()
    with torch.no_grad():
        weight -= 0.1 * weight.grad
    weight.grad = None
    after = ((weight * x - target) ** 2).item()
    assert after < before
    print("gradient:", -24.0, "loss before/after:", round(before, 3), round(after, 3))
