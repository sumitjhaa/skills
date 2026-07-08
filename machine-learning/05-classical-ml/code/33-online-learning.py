"""Online Learning (Perceptron, PA, OGD) from scratch."""
import numpy as np
from sklearn.datasets import make_classification

class Perceptron:
    def __init__(self):
        self.w = None; self.b = 0

    def partial_fit(self, x, y):
        if self.w is None:
            self.w = np.zeros(len(x))
        if y * (self.w @ x + self.b) <= 0:
            self.w += y * x
            self.b += y

    def predict(self, X):
        return np.sign(X @ self.w + self.b).astype(int)

class PassiveAggressive:
    def __init__(self, C=1.0):
        self.w = None; self.b = 0; self.C = C

    def partial_fit(self, x, y):
        if self.w is None:
            self.w = np.zeros(len(x))
        loss = max(0, 1 - y * (self.w @ x + self.b))
        if loss > 0:
            tau = min(self.C, loss / (np.linalg.norm(x)**2 + 1e-10))
            self.w += tau * y * x
            self.b += tau * y

    def predict(self, X):
        return np.sign(X @ self.w + self.b).astype(int)

class OGD:
    def __init__(self, lr=0.01):
        self.w = None; self.b = 0; self.lr = lr

    def partial_fit(self, x, y):
        if self.w is None:
            self.w = np.zeros(len(x))
        loss_grad = -y * x / (1 + np.exp(y * (self.w @ x + self.b)))
        self.w -= self.lr * loss_grad
        self.b += self.lr * y / (1 + np.exp(y * (self.w @ x + self.b)))

    def predict(self, X):
        return np.sign(X @ self.w + self.b).astype(int)

if __name__ == "__main__":
    X, y = make_classification(n_samples=500, n_features=10, random_state=42)
    y = y.astype(float) * 2 - 1

    perm = np.random.permutation(len(X))
    X, y = X[perm], y[perm]
    split = len(X) // 2

    models = [Perceptron(), PassiveAggressive(C=1.0), OGD(lr=0.01)]
    for m in models:
        for i in range(split):
            m.partial_fit(X[i], y[i])
        preds = m.predict(X[split:])
        acc = np.mean(preds == y[split:])
        print(f"{type(m).__name__} test accuracy: {acc:.4f}")
