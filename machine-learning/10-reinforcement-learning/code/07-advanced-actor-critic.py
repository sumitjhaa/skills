"""10.07 Advanced Actor-Critic: SAC on a simple continuous task."""
import numpy as np

HIDDEN = 32
LR_A = 1e-3
LR_C = 1e-3
GAMMA = 0.99
ALPHA = 0.2
TAU = 0.005
BATCH = 32
BUFFER = 50000
EPISODES = 200
STEPS = 50


class MLP:
    def __init__(self, din, dout):
        self.W1 = np.random.randn(din, HIDDEN) * 0.1
        self.b1 = np.zeros((1, HIDDEN))
        self.W2 = np.random.randn(HIDDEN, dout) * 0.1
        self.b2 = np.zeros((1, dout))

    def __call__(self, x):
        h = np.maximum(0, x @ self.W1 + self.b1)
        return h @ self.W2 + self.b2


actor = MLP(3, 1)
q1 = MLP(4, 1)
q2 = MLP(4, 1)
tq1 = MLP(4, 1)
tq2 = MLP(4, 1)
buffer = []


def soft_update(src, dst):
    dst.W1 = TAU * src.W1 + (1 - TAU) * dst.W1
    dst.b1 = TAU * src.b1 + (1 - TAU) * dst.b1
    dst.W2 = TAU * src.W2 + (1 - TAU) * dst.W2
    dst.b2 = TAU * src.b2 + (1 - TAU) * dst.b2


def get_action(s):
    mu = actor(s.reshape(1, -1))
    return np.tanh(mu + np.random.randn() * 0.1)


def train():
    if len(buffer) < BATCH:
        return
    idx = np.random.choice(len(buffer), BATCH, replace=False)
    s = np.array([buffer[i][0] for i in idx])
    a = np.array([buffer[i][1] for i in idx])
    r = np.array([buffer[i][2] for i in idx])
    ns = np.array([buffer[i][3] for i in idx])
    d = np.array([buffer[i][4] for i in idx])

    na = np.tanh(actor(ns) + np.random.randn(BATCH, 1) * 0.1)
    sa = np.concatenate([ns, na.reshape(-1, 1)], axis=1)
    q1t = tq1(sa).flatten()
    q2t = tq2(sa).flatten()
    y = r + GAMMA * (1 - d) * (np.minimum(q1t, q2t) - ALPHA * np.log(0.5))
    # simplified — just demonstrating structure
    return np.mean(y)


for ep in range(EPISODES):
    s = np.random.randn(3)
    total_r = 0
    for t in range(STEPS):
        a = get_action(s)[0, 0]
        ns = s + np.array([a, a * 0.5, -a * 0.3]) + np.random.randn(3) * 0.05
        r = -np.linalg.norm(ns) * 0.1
        done = 0.0 if np.linalg.norm(ns) < 2 else 1.0
        buffer.append((s.copy(), a, r, ns.copy(), done))
        s = ns
        total_r += r
        train()
        soft_update(q1, tq1)
        soft_update(q2, tq2)
        if len(buffer) > BUFFER:
            buffer.pop(0)
        if done:
            break
    if ep % 50 == 0:
        print(f"Ep {ep}, return: {total_r:.3f}")

print("SAC-style training complete.")
