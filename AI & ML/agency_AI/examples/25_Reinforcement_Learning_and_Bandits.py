"""
Reinforcement learning and exploration with bandits.

Level: Intermediate.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: Learn which simulated action has the highest reward
# Implement epsilon-greedy value estimates from scratch.
# Step 1: Define fixed reward probabilities for three safe simulated actions.
# Step 2: Explore occasionally and exploit otherwise.
# Step 3: Update only the chosen action's empirical value.
# Step 4: Check that the best estimated action matches the known simulated optimum.
if __name__ == "__main__":
    import numpy as np

    rng = np.random.default_rng(42)
    reward_probabilities = np.array([0.2, 0.5, 0.8])
    estimates, counts = np.zeros(3), np.zeros(3, dtype=int)
    rewards = []
    for _ in range(1800):
        action = int(rng.integers(3)) if rng.random() < 0.15 else int(np.argmax(estimates))
        reward = float(rng.random() < reward_probabilities[action])
        counts[action] += 1
        estimates[action] += (reward - estimates[action]) / counts[action]
        rewards.append(reward)
    assert counts.sum() == 1800 and (counts > 0).all()
    assert int(np.argmax(estimates)) == 2
    print("value estimates:", np.round(estimates, 3).tolist())
    print("action counts:", counts.tolist(), "mean reward:", round(float(np.mean(rewards)), 3))

# %% Worked example: Check discounted rewards by hand
# Understand why immediate reward and cumulative return are different objectives.
# Step 1: Specify a finite reward sequence and discount factor.
# Step 2: Compute its discounted sum.
# Step 3: Compare against a delayed alternative with different gamma values.
if __name__ == "__main__":
    def discounted_return(rewards, gamma):
        if not 0 <= gamma <= 1:
            raise ValueError("gamma must be in [0, 1]")
        return sum((gamma ** index) * reward for index, reward in enumerate(rewards))
    immediate, delayed = [1., 0., 0.], [0., 0., 2.]
    assert discounted_return(immediate, 0.5) > discounted_return(delayed, 0.5)
    assert discounted_return(immediate, 0.9) < discounted_return(delayed, 0.9)
    print("immediate gamma=.9:", discounted_return(immediate, 0.9))
    print("delayed gamma=.9:", round(discounted_return(delayed, 0.9), 3))
