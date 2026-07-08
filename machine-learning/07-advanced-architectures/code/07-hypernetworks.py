"""
07.07 Hypernetworks: Generate weights of a target network.
"""
import numpy as np
import matplotlib.pyplot as plt


class Hypernetwork:
    """Generates weights for a small target MLP."""
    def __init__(self, embed_dim=8, target_sizes=[2, 16, 1]):
        self.embed_dim = embed_dim
        self.W1 = np.random.randn(embed_dim, 32) * 0.1
        self.b1 = np.zeros(32)
        self.W2 = np.random.randn(32, 64) * 0.1
        self.b2 = np.zeros(64)
        self.num_target_params = sum((target_sizes[i] * target_sizes[i+1] +
                                       target_sizes[i+1]) for i in range(len(target_sizes)-1))
        self.W_out = np.random.randn(64, self.num_target_params) * 0.1
        self.b_out = np.zeros(self.num_target_params)

    def forward(self, embedding):
        h = np.tanh(embedding @ self.W1 + self.b1)
        h = np.tanh(h @ self.W2 + self.b2)
        params = h @ self.W_out + self.b_out
        return params

    def generate_target_params(self, embedding, target_sizes):
        flat = self.forward(embedding)
        params = []
        idx = 0
        for i in range(len(target_sizes)-1):
            n_w = target_sizes[i] * target_sizes[i+1]
            n_b = target_sizes[i+1]
            W = flat[0, idx:idx+n_w].reshape(target_sizes[i], target_sizes[i+1])
            idx += n_w
            b = flat[0, idx:idx+n_b].reshape(1, target_sizes[i+1])
            idx += n_b
            params.extend([W, b])
        return params


def target_forward(params, x):
    h = x
    for i in range(0, len(params)-2, 2):
        W, b = params[i], params[i+1]
        h = np.tanh(h @ W + b)
    W, b = params[-2], params[-1]
    return h @ W + b


if __name__ == "__main__":
    np.random.seed(42)
    hyper = Hypernetwork()
    target_sizes = [2, 16, 1]
    embedding = np.random.randn(1, 8)
    params = hyper.generate_target_params(embedding, target_sizes)
    x = np.random.randn(100, 2)
    y = np.sin(x[:, 0:1] + x[:, 1:2]) + 0.1 * np.random.randn(100, 1)
    y_pred = target_forward(params, x)
    loss = np.mean((y_pred - y) ** 2)
    print(f"Initial loss: {loss:.6f}")
    print(f"Generated {len(params)} parameter tensors for target network")
    print("Hypernetwork demo complete.")
