"""
Q-learning, states, and discounted returns.

Level: Intermediate to advanced.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Learn a route through a tiny safe state space
# Implement a bounded tabular learning loop.
# Step 1: Use states 0..3 with 3 terminal and actions left/right.
# Step 2: Explore during bounded episodes.
# Step 3: Apply a terminal-aware Bellman update.
# Step 4: Execute the resulting greedy policy and assert it reaches the goal.
if __name__ == "__main__":
    import numpy as np

    rng = np.random.default_rng(42)
    Q = np.zeros((4, 2))
    for episode in range(350):
        state = 0
        for _ in range(25):
            action = int(rng.integers(2)) if rng.random() < 0.25 else int(np.argmax(Q[state]))
            next_state = max(0, state - 1) if action == 0 else min(3, state + 1)
            terminal = next_state == 3
            reward = 1.0 if terminal else -0.02
            target = reward + (0.0 if terminal else 0.95 * Q[next_state].max())
            Q[state, action] += 0.3 * (target - Q[state, action])
            state = next_state
            if terminal:
                break
    state, path = 0, [0]
    for _ in range(6):
        action = int(np.argmax(Q[state]))
        state = max(0, state - 1) if action == 0 else min(3, state + 1)
        path.append(state)
        if state == 3:
            break
    assert path == [0, 1, 2, 3]
    print("greedy path:", path)
    print("state-zero Q:", np.round(Q[0], 3).tolist())
