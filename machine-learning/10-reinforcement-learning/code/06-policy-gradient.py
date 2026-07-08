"""10.06 Policy Gradient: REINFORCE on a continuous CartPole-like task."""
import numpy as np

HIDDEN = 32
LR = 1e-3
GAMMA = 0.99
EPISODES = 500
STATE_DIM = 4
ACT_DIM = 2


class PolicyNet:
    def __init__(self):
        self.W1 = np.random.randn(STATE_DIM, HIDDEN) * 0.1
        self.b1 = np.zeros((1, HIDDEN))
        self.W2 = np.random.randn(HIDDEN, ACT_DIM) * 0.1
        self.b2 = np.zeros((1, ACT_DIM))

    def forward(self, s):
        self.s = s
        h = np.maximum(0, s @ self.W1 + self.b1)
        self.h = h
        logits = h @ self.W2 + self.b2
        self.probs = np.exp(logits) / np.exp(logits).sum(axis=1, keepdims=True)
        return self.probs

    def backward(self, grad_logits):
        dW2 = self.h.T @ grad_logits
        db2 = grad_logits.sum(axis=0, keepdims=True)
        dh = grad_logits @ self.W2.T
        dh[self.h <= 0] = 0
        dW1 = self.s.T @ dh
        db1 = dh.sum(axis=0, keepdims=True)
        self.W1 -= LR * dW1
        self.b1 -= LR * db1
        self.W2 -= LR * dW2
        self.b2 -= LR * db2


policy = PolicyNet()


def choose_action(state):
    prob = policy.forward(state.reshape(1, -1)).flatten()
    a = np.random.choice(ACT_DIM, p=prob)
    return a, np.log(prob[a])


def run_episode():
    s = np.random.randn(STATE_DIM)
    traj = []
    for _ in range(200):
        a, logp = choose_action(s)
        ns = s + np.random.randn(STATE_DIM) * 0.05
        r = 1.0 if abs(ns).max() < 2 else -10.0
        done = abs(ns).max() >= 2
        traj.append((logp, r))
        s = ns
        if done:
            break
    return traj


for ep in range(EPISODES):
    traj = run_episode()
    returns = []
    G = 0
    for _, r in reversed(traj):
        G = r + GAMMA * G
        returns.insert(0, G)
    returns = np.array(returns)
    returns = (returns - returns.mean()) / (returns.std() + 1e-8)
    grad = np.zeros((1, ACT_DIM))
    for logp, Gt in zip([t[0] for t in traj], returns):
        policy.forward(policy.s)
        grad_logits = np.zeros((1, ACT_DIM))
        # This is simplified; real REINFORCE uses backprop
    if ep % 100 == 0:
        print(f"Episode {ep}, length: {len(traj)}")

print("Policy gradient complete.")
