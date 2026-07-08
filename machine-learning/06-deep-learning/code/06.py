"""06.06 - Perceptron / MLP: Dense layers and training from scratch"""

import numpy as np
import matplotlib.pyplot as plt


def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -100, 100)))

def sigmoid_deriv(x):
    s = sigmoid(x)
    return s * (1 - s)


class MLP:
    def __init__(self, layer_dims):
        self.params = []
        for i in range(len(layer_dims) - 1):
            W = np.random.randn(layer_dims[i], layer_dims[i+1]) * np.sqrt(2.0 / layer_dims[i])
            b = np.zeros((1, layer_dims[i+1]))
            self.params.append((W, b))

    def forward(self, X):
        self.cache = [(X,)]
        h = X
        for W, b in self.params[:-1]:
            h = sigmoid(h @ W + b)
            self.cache.append((h, W, b))
        W, b = self.params[-1]
        y = h @ W + b
        self.cache.append((y, W, b))
        return y

    def backward(self, dout):
        d = dout
        for i in range(len(self.params) - 1, -1, -1):
            h_act, W, b = self.cache[i+1]
            if i == len(self.params) - 1:
                dz = d
            else:
                dz = d * h_act * (1 - h_act)
            db = dz.sum(axis=0, keepdims=True)
            dW = self.cache[i][0].T @ dz
            if i > 0:
                d = dz @ W.T
            self.params[i] = (W - 0.1 * dW, b - 0.1 * db)

    def train(self, X, y, epochs=1000, lr=0.1):
        losses = []
        for epoch in range(epochs):
            logits = self.forward(X)
            loss = np.mean((logits - y) ** 2)
            dout = 2 * (logits - y) / X.shape[0]
            self.backward(dout)
            losses.append(loss)
            if epoch % 200 == 0:
                print(f"Epoch {epoch}, loss = {loss:.6f}")
        return losses


if __name__ == "__main__":
    np.random.seed(42)
    X = np.random.randn(200, 2)
    y = (X[:, 0] ** 2 + X[:, 1] ** 2 < 1.5).astype(float).reshape(-1, 1)

    mlp = MLP([2, 16, 8, 1])
    losses = mlp.train(X, y, epochs=1000, lr=0.5)
    acc = np.mean((mlp.forward(X) > 0.5).astype(float) == y)
    print(f"\nFinal accuracy: {acc*100:.1f}%")

    plt.plot(losses)
    plt.xlabel("Epoch")
    plt.ylabel("MSE Loss")
    plt.title("MLP Training Convergence")
    plt.savefig("../../assets/phase06/mlp_training.png")
    plt.close()
    print("MLP training complete. Plot saved.")
