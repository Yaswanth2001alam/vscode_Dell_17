"""
Fine-tuning, LoRA, distillation, and preference learning.

Level: Advanced.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Train a low-rank update while preserving the base
# Implement and test the central LoRA mechanism.
# Step 1: Create a frozen base matrix and a known rank-one target change.
# Step 2: Optimize only A and B.
# Step 3: Compare initial and final reconstruction losses.
# Step 4: Assert the base stayed unchanged and adapter parameter count is smaller.
if __name__ == "__main__":
    import torch

    torch.set_num_threads(1)
    torch.manual_seed(42)
    base = torch.randn(6, 8)
    saved = base.clone()
    X = torch.randn(100, 8)
    true_update = torch.randn(6, 1) @ torch.randn(1, 8)
    targets = X @ (base + true_update).T
    A = torch.nn.Parameter(torch.randn(1, 8) * 0.1)
    B = torch.nn.Parameter(torch.zeros(6, 1))
    optimizer = torch.optim.Adam([A, B], lr=0.05)
    initial = ((X @ base.T - targets) ** 2).mean().item()
    for _ in range(180):
        optimizer.zero_grad()
        predictions = X @ (base + B @ A).T
        loss = ((predictions - targets) ** 2).mean()
        loss.backward()
        optimizer.step()
    torch.testing.assert_close(base, saved)
    assert loss.item() < initial * 0.01
    assert A.numel() + B.numel() < base.numel()
    print("base/adapter parameters:", base.numel(), A.numel() + B.numel())
    print("loss:", round(initial, 4), "->", round(loss.item(), 4))

# %% Worked example: Distill soft targets into a small student
# Actually optimize a student against teacher distributions instead of using distillation only as vocabulary.
# Step 1: Define a frozen synthetic teacher mapping.
# Step 2: Calculate temperature-softened target probabilities.
# Step 3: Train a smaller student's logits with KL divergence.
# Step 4: Assert matching loss decreases and teacher state is unchanged.
if __name__ == "__main__":
    import torch
    from torch import nn
    from torch.nn import functional as F

    torch.set_num_threads(1)
    torch.manual_seed(42)
    X = torch.randn(100, 3)
    teacher_weights = torch.tensor([[2., -1., 0.5], [-1., 2., -0.5]])
    with torch.no_grad():
        teacher_logits = X @ teacher_weights.T
    temperature = 2.0
    teacher_probabilities = F.softmax(teacher_logits / temperature, dim=1)
    student = nn.Linear(3, 2)
    optimizer = torch.optim.Adam(student.parameters(), lr=0.05)
    def distillation_loss():
        return F.kl_div(F.log_softmax(student(X) / temperature, dim=1),
                        teacher_probabilities, reduction="batchmean") * temperature**2
    initial = distillation_loss().item()
    for _ in range(100):
        optimizer.zero_grad()
        loss = distillation_loss()
        loss.backward()
        optimizer.step()
    assert loss.item() < initial * 0.02
    print("synthetic teacher/student KL loss:", round(initial, 4), "->", round(loss.item(), 4))

# %% Worked example: Inspect a pairwise preference objective
# Connect chosen/rejected probabilities to a simplified DPO loss calculation without claiming a full preference-training pipeline.
# Step 1: Compute a policy chosen-minus-rejected log-probability ratio.
# Step 2: Subtract the frozen reference ratio.
# Step 3: Apply a stable negative log-sigmoid with a beta scale.
# Step 4: Check the loss is lower for a better preference margin.
if __name__ == "__main__":
    import numpy as np

    def pairwise_loss(policy_chosen, policy_rejected, reference_chosen, reference_rejected, beta=0.1):
        margin = beta * ((policy_chosen - policy_rejected) -
                         (reference_chosen - reference_rejected))
        return float(np.logaddexp(0., -margin))
    weak = pairwise_loss(-3., -2., -2., -2.)
    improved = pairwise_loss(-1., -3., -2., -2.)
    assert improved < weak
    assert np.isclose(pairwise_loss(-2., -2., -2., -2.), np.log(2))
    print("weak/improved pairwise loss:", round(weak, 4), round(improved, 4))
