"""10.05 Function Approximation: DQN with numpy."""
import numpy as np

HIDDEN = 32
LR = 1e-3
GAMMA = 0.99
BATCH = 16
BUFFER = 5000
EPISODES = 150
STEPS_PER_EP = 50


class MLP:
    def __init__(self, din, dout, h=HIDDEN):
        self.W1 = np.random.randn(din, h) * 0.1
        self.b1 = np.zeros((1, h))
        self.W2 = np.random.randn(h, dout) * 0.1
        self.b2 = np.zeros((1, dout))

    def forward(self, x):
        self.x = x
        self.h = np.maximum(0, x @ self.W1 + self.b1)
        return self.h @ self.W2 + self.b2

    def sgd(self, lr, dout):
        dh = dout @ self.W2.T
        dh[self.h <= 0] = 0
        self.W2 -= lr * self.h.T @ dout
        self.b2 -= lr * dout.sum(axis=0, keepdims=True)
        self.W1 -= lr * self.x.T @ dh
        self.b1 -= lr * dh.sum(axis=0, keepdims=True)


online = MLP(2, 4)
target = MLP(2, 4)
buffer = []
step = 0

for ep in range(EPISODES):
    s = np.random.randn(2)
    total_r = 0
    for t in range(STEPS_PER_EP):
        eps = max(0.05, 1.0 - ep / 100)
        if np.random.rand() < eps:
            a = np.random.randint(4)
        else:
            a = np.argmax(online.forward(s.reshape(1, -1)))
        ns = s + np.random.randn(2) * 0.1
        dist = np.linalg.norm(ns)
        r = 1.0 if dist < 0.5 else -0.01
        done = 1.0 if dist < 0.5 else 0.0
        buffer.append((s.copy(), a, r, ns.copy(), done))
        if len(buffer) > BUFFER:
            buffer.pop(0)
        s = ns
        total_r += r
        if len(buffer) >= BATCH:
            idx = np.random.choice(len(buffer), BATCH, replace=False)
            b = [buffer[i] for i in idx]
            bs = np.array([x[0] for x in b])
            ba = np.array([x[1] for x in b])
            br = np.array([x[2] for x in b])
            bns = np.array([x[3] for x in b])
            bd = np.array([x[4] for x in b])
            qn = target.forward(bns)
            max_qn = np.max(qn, axis=1)
            y = br + GAMMA * max_qn * (1 - bd)
            q = online.forward(bs)
            grad = np.zeros_like(q)
            for i in range(BATCH):
                grad[i, ba[i]] = q[i, ba[i]] - y[i]
            online.sgd(LR, grad / BATCH)
        if done:
            break
    if ep % 50 == 0:
        print(f"Ep {ep}, reward: {total_r:.3f}")

print("DQN complete.")
