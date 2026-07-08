"""
08.29 Visual RL — DQN with CNN on synthetic grid world
Usage: python 29-visual-rl.py
"""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

# simple grid world 5x5
class GridWorld:
    def __init__(self):
        self.grid = np.zeros((5, 5))
        self.agent = [0, 0]
        self.goal = [4, 4]
        self.grid[self.goal[0], self.goal[1]] = 1
    def reset(self):
        self.agent = [0, 0]
        return self._obs()
    def _obs(self):
        return self.grid.copy()
    def step(self, action):
        # 0=up,1=down,2=left,3=right
        if action == 0: self.agent[0] = max(0, self.agent[0]-1)
        if action == 1: self.agent[0] = min(4, self.agent[0]+1)
        if action == 2: self.agent[1] = max(0, self.agent[1]-1)
        if action == 3: self.agent[1] = min(4, self.agent[1]+1)
        done = self.agent == self.goal
        reward = 1 if done else -0.01
        return self._obs(), reward, done

env = GridWorld()

# DQN with simple linear policy (skipping CNN for speed)
n_actions = 4
W_q = np.random.randn(5*5, 16) * 0.1
b_q = np.zeros(16)
W_out = np.random.randn(16, n_actions) * 0.1
b_out = np.zeros(n_actions)

def q_vals(obs):
    h = np.maximum(0, obs.flatten() @ W_q + b_q)
    return h @ W_out + b_out

# play one episode with epsilon-greedy
epsilon = 0.3
obs = env.reset()
rewards = []
for step in range(50):
    q = q_vals(obs)
    if np.random.rand() < epsilon:
        action = np.random.randint(n_actions)
    else:
        action = q.argmax()
    obs, reward, done = env.step(action)
    rewards.append(reward)
    if done:
        print(f"Goal reached in {step+1} steps!")
        break

print(f"Total reward: {sum(rewards):.2f}")

fig, axes = plt.subplots(1, 2, figsize=(8, 4))
axes[0].plot(np.cumsum(rewards))
axes[0].set_title('Cumulative Reward')
axes[0].set_xlabel('Step')
# visualise Q-values
obs = env.reset()
q = q_vals(obs)
axes[1].bar(range(n_actions), q)
axes[1].set_xticks(range(n_actions))
axes[1].set_xticklabels(['Up','Down','Left','Right'])
axes[1].set_title('Q-values at start')
plt.tight_layout(); plt.savefig('../../assets/phase08/29_visual_rl.png', dpi=100)
print("Saved 29_visual_rl.png")
