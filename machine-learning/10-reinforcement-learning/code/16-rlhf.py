"""10.16 RLHF: Preference-based reward learning."""
import numpy as np

STATE_DIM = 4
HIDDEN = 16
LR = 0.01
EPOCHS = 100


class RewardModel:
    def __init__(self):
        self.W1 = np.random.randn(STATE_DIM, HIDDEN) * 0.1
        self.b1 = np.zeros((1, HIDDEN))
        self.W2 = np.random.randn(HIDDEN, 1) * 0.1
        self.b2 = np.zeros((1, 1))

    def forward(self, s):
        s = s.reshape(1, -1)
        h = np.maximum(0, s @ self.W1 + self.b1)
        return (h @ self.W2 + self.b2).item()

    def train_step(self, s1, s2, pref):
        h1 = np.maximum(0, s1.reshape(1, -1) @ self.W1 + self.b1)
        h2 = np.maximum(0, s2.reshape(1, -1) @ self.W1 + self.b1)
        r1 = (h1 @ self.W2 + self.b2).item()
        r2 = (h2 @ self.W2 + self.b2).item()
        prob = 1 / (1 + np.exp(-(r1 - r2)))
        grad = prob - pref
        d1 = grad * (h1 @ self.W2 + self.b2 > 0)
        d2 = -grad * (h2 @ self.W2 + self.b2 > 0)
        dr1 = h1.T * grad
        dr2 = h2.T * (-grad)
        self.W2 -= LR * (dr1 + dr2)
        self.b2 -= LR * np.array([[grad - grad]])
        self.W1 -= LR * (s1.reshape(1, -1).T @ (d1 @ self.W2.T) + s2.reshape(1, -1).T @ (d2 @ self.W2.T)) * 0.01
        return -np.log(prob + 1e-8) if pref > 0.5 else -np.log(1 - prob + 1e-8)


true_reward = lambda s: -np.linalg.norm(s)
model = RewardModel()

prefs = []
for _ in range(200):
    s1 = np.random.randn(STATE_DIM)
    s2 = np.random.randn(STATE_DIM)
    pref = 1.0 if true_reward(s1) > true_reward(s2) else 0.0
    prefs.append((s1, s2, pref))

for ep in range(EPOCHS):
    loss = 0.0
    for s1, s2, pref in prefs:
        loss += model.train_step(s1, s2, pref)
    if ep % 20 == 0:
        print(f"Epoch {ep}, loss: {loss:.3f}")

# Test
t1, t2 = np.random.randn(STATE_DIM), np.random.randn(STATE_DIM)
print(f"True: {true_reward(t1):.3f} vs {true_reward(t2):.3f}")
print(f"Model: {model.forward(t1):.3f} vs {model.forward(t2):.3f}")
print("RLHF reward modelling complete.")
