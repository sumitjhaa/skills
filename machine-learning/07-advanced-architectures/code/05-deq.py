"""
07.05 DEQ: Deep Equilibrium Model with fixed-point iteration.
"""
import numpy as np
import matplotlib.pyplot as plt


class DEQLayer:
    """z = f(z, x) using fixed-point iteration."""
    def __init__(self, dim=32):
        self.W_z = np.random.randn(dim, dim) * 0.01
        self.W_x = np.random.randn(dim, dim) * 0.01
        self.b = np.zeros(dim)

    def forward(self, x, max_iter=50, tol=1e-4):
        z = np.zeros_like(x)
        for i in range(max_iter):
            z_next = np.tanh(z @ self.W_z + x @ self.W_x + self.b)
            if np.max(np.abs(z_next - z)) < tol:
                break
            z = z_next
        return z


class DEQ:
    def __init__(self, dim=32):
        self.layer = DEQLayer(dim)
        self.W_out = np.random.randn(dim, 1) * 0.01
        self.b_out = np.zeros(1)

    def forward(self, x):
        z = self.layer.forward(x)
        return z @ self.W_out + self.b_out


if __name__ == "__main__":
    np.random.seed(42)
    model = DEQ(32)
    X = np.random.randn(200, 32)
    y = np.sin(X[:, 0:1]) + 0.1 * np.random.randn(200, 1)
    lr = 0.001
    losses = []
    for epoch in range(500):
        y_pred = model.forward(X)
        loss = np.mean((y_pred - y) ** 2)
        losses.append(loss)
        grad = 2 * (y_pred - y) / len(X)
        model.W_out -= lr * (model.layer.forward(X).T @ grad)
        model.b_out -= lr * grad.sum(axis=0)
        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {loss:.6f}")

    plt.plot(losses)
    plt.yscale('log')
    plt.title('DEQ Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('MSE')
    plt.savefig('../../assets/phase07/deq.png')
    plt.close()
    print("Saved deq.png")
