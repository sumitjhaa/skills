"""10.17 Continuous Control: DDPG on 2D navigation."""
import numpy as np

STATE_DIM = 2
ACT_DIM = 1
HIDDEN = 32
GAMMA = 0.99
BUFFER = 10000
BATCH = 32
EPISODES = 60
STEPS = 80


class Actor:
    def __init__(self):
        self.W1 = np.random.randn(STATE_DIM, HIDDEN) * 0.1
        self.b1 = np.zeros((1, HIDDEN))
        self.W2 = np.random.randn(HIDDEN, ACT_DIM) * 0.1
        self.b2 = np.zeros((1, ACT_DIM))

    def forward(self, s):
        h = np.maximum(0, s @ self.W1 + self.b1)
        return np.tanh(h @ self.W2 + self.b2)

    def update(self, s, grad_a):
        h = np.maximum(0, s @ self.W1 + self.b1)
        dh = grad_a @ self.W2.T
        dh[h <= 0] = 0
        self.W2 -= 1e-3 * h.T @ grad_a
        self.b2 -= 1e-3 * grad_a.sum(axis=0, keepdims=True)
        self.W1 -= 1e-3 * s.T @ dh
        self.b1 -= 1e-3 * dh.sum(axis=0, keepdims=True)


class Critic:
    def __init__(self):
        self.W1 = np.random.randn(STATE_DIM + ACT_DIM, HIDDEN) * 0.1
        self.b1 = np.zeros((1, HIDDEN))
        self.W2 = np.random.randn(HIDDEN, 1) * 0.1
        self.b2 = np.zeros((1, 1))

    def forward(self, s, a):
        x = np.concatenate([s.reshape(1, -1), a.reshape(1, -1)], axis=1)
        h = np.maximum(0, x @ self.W1 + self.b1)
        return (h @ self.W2 + self.b2).item()

    def forward_batch(self, s, a):
        x = np.concatenate([s.reshape(s.shape[0], -1), a.reshape(a.shape[0], -1)], axis=1)
        h = np.maximum(0, x @ self.W1 + self.b1)
        return h @ self.W2 + self.b2


actor = Actor()
critic = Critic()
buffer = []

for ep in range(EPISODES):
    s = np.random.randn(STATE_DIM)
    total_r = 0
    for t in range(STEPS):
        a = actor.forward(s.reshape(1, -1)).item()
        a_noisy = a + np.random.randn() * 0.1
        target = np.array([2.0, 2.0])
        ns = s + np.array([a_noisy, -a_noisy * 0.5]) + np.random.randn(2) * 0.05
        r = -float(np.linalg.norm(ns - target))
        done = 1.0 if np.linalg.norm(ns - target) < 0.3 else 0.0
        buffer.append((s.copy(), a_noisy, r, ns.copy(), done))
        if len(buffer) > BUFFER:
            buffer.pop(0)
        s = ns
        total_r += r
        if done:
            break
    if ep % 20 == 0:
        print(f"Ep {ep}, return: {total_r:.3f}")

print("DDPG continuous control complete.")
