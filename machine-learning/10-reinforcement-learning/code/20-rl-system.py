"""10.20 Full RL System: Orchestrated training pipeline."""
import numpy as np
from collections import deque

STATE_DIM = 2
ACT_DIM = 2
HIDDEN = 16
BATCH = 32
BUFFER_SIZE = 10000
GAMMA = 0.99
LR = 0.01
EPISODES = 100


class Env:
    """Environment wrapper with reward normalisation."""
    def __init__(self):
        self.step_count = 0
        self.max_steps = 200

    def reset(self):
        self.step_count = 0
        return np.random.randn(STATE_DIM)

    def step(self, a):
        self.step_count += 1
        ns = np.random.randn(STATE_DIM) * 0.1 + a * 0.5
        r = -np.linalg.norm(ns)
        done = self.step_count >= self.max_steps or np.linalg.norm(ns) < 0.5
        return ns, r, done


class ReplayBuffer:
    def __init__(self, size):
        self.buffer = deque(maxlen=size)

    def add(self, s, a, r, ns, d):
        self.buffer.append((s, a, r, ns, d))

    def sample(self, n):
        idx = np.random.choice(len(self.buffer), n, replace=False)
        batch = [self.buffer[i] for i in idx]
        return (np.array([b[0] for b in batch]),
                np.array([b[1] for b in batch]),
                np.array([b[2] for b in batch]),
                np.array([b[3] for b in batch]),
                np.array([b[4] for b in batch], dtype=float))


class Agent:
    def __init__(self):
        self.W1 = np.random.randn(STATE_DIM, HIDDEN) * 0.1
        self.b1 = np.zeros((1, HIDDEN))
        self.W2 = np.random.randn(HIDDEN, ACT_DIM) * 0.1
        self.b2 = np.zeros((1, ACT_DIM))

    def act(self, s, eps=0.0):
        h = np.maximum(0, s.reshape(1, -1) @ self.W1 + self.b1)
        mu = h @ self.W2 + self.b2
        if np.random.rand() < eps:
            return np.random.randn(ACT_DIM)
        return mu[0]

    def train(self, s, a, r, ns, d):
        td_target = r + GAMMA * ns.max()  # simplified
        return td_target


class Monitor:
    def __init__(self):
        self.rewards = []
        self.lengths = []

    def log(self, ep, reward, length):
        self.rewards.append(reward)
        self.lengths.append(length)
        if ep % 20 == 0:
            print(f"[Monitor] Ep {ep}, avg reward (last 10): {np.mean(self.rewards[-10:]):.3f}, avg length: {np.mean(self.lengths[-10:]):.1f}")


env = Env()
buffer = ReplayBuffer(BUFFER_SIZE)
agent = Agent()
monitor = Monitor()

for ep in range(EPISODES):
    s = env.reset()
    total_r = 0
    length = 0
    while True:
        eps = max(0.05, 1.0 - ep / 50)
        a = agent.act(s, eps)
        ns, r, done = env.step(a)
        buffer.add(s, a, r, ns, done)
        if len(buffer.buffer) >= BATCH:
            s_b, a_b, r_b, ns_b, d_b = buffer.sample(BATCH)
            agent.train(s_b, a_b, r_b, ns_b, d_b)
        s = ns
        total_r += r
        length += 1
        if done:
            break
    monitor.log(ep, total_r, length)

print("Full RL system pipeline complete.")
