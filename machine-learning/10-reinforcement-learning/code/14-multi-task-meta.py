"""10.14 Multi-Task & Meta-RL: MAML-inspired few-shot adaptation."""
import numpy as np

N_TASKS = 10
HIDDEN = 16
INNER_LR = 0.1
OUTER_LR = 0.01
EPOCHS = 50
K_SHOT = 5


class Net:
    def __init__(self):
        self.W1 = np.random.randn(2, HIDDEN) * 0.1
        self.b1 = np.zeros((1, HIDDEN))
        self.W2 = np.random.randn(HIDDEN, 2) * 0.1
        self.b2 = np.zeros((1, 2))

    def forward(self, x):
        h = np.maximum(0, x @ self.W1 + self.b1)
        return h @ self.W2 + self.b2


def task_loss(theta, inputs, targets):
    h = np.maximum(0, inputs @ theta['W1'] + theta['b1'])
    out = h @ theta['W2'] + theta['b2']
    probs = np.exp(out) / np.exp(out).sum(axis=1, keepdims=True)
    return -np.mean(np.log(probs[np.arange(len(targets)), targets] + 1e-8))


meta_params = Net()

for ep in range(EPOCHS):
    meta_grad = {'W1': 0, 'b1': 0, 'W2': 0, 'b2': 0}
    for _ in range(N_TASKS):
        # Sample a task — binary classification with different decision boundary
        theta = {'W1': meta_params.W1.copy(), 'b1': meta_params.b1.copy(),
                 'W2': meta_params.W2.copy(), 'b2': meta_params.b2.copy()}
        xs = np.random.randn(K_SHOT, 2)
        ys = (xs[:, 0] + xs[:, 1] > np.random.randn()).astype(int)
        # Inner loop 1 step
        grad = {}
        h = np.maximum(0, xs @ theta['W1'] + theta['b1'])
        out = h @ theta['W2'] + theta['b2']
        probs = np.exp(out) / np.exp(out).sum(axis=1, keepdims=True)
        dout = probs.copy()
        dout[np.arange(K_SHOT), ys] -= 1
        dout /= K_SHOT
        grad['W2'] = h.T @ dout
        grad['b2'] = dout.sum(axis=0, keepdims=True)
        dh = dout @ theta['W2'].T
        dh[h <= 0] = 0
        grad['W1'] = xs.T @ dh
        grad['b1'] = dh.sum(axis=0, keepdims=True)
        for k in theta:
            theta[k] -= INNER_LR * grad[k]
        # Outer loss on new batch
        xs2 = np.random.randn(K_SHOT, 2)
        ys2 = (xs2[:, 0] + xs2[:, 1] > np.random.randn()).astype(int)
        loss = task_loss(theta, xs2, ys2)
        # Outer gradient (simplified - second-order approx)
        for k in meta_grad:
            meta_grad[k] += grad[k] * loss
    for k in meta_grad:
        meta_params.__dict__[k] -= OUTER_LR * meta_grad[k] / N_TASKS
    if ep % 20 == 0:
        print(f"Meta epoch {ep}")

print("Meta-RL (MAML-style) complete.")
