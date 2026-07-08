"""
07.27 NAS: Neural Architecture Search (DARTS-style cell search).
"""
import numpy as np
import matplotlib.pyplot as plt


class NASCell:
    """Search cell with candidate operations (simplified DARTS)."""
    OPS = ['identity', 'tanh', 'relu', 'sigmoid']

    def __init__(self, in_dim=8, out_dim=8):
        self.in_dim = in_dim
        self.out_dim = out_dim
        self.alphas = np.random.randn(len(self.OPS)) * 0.1  # architecture weights
        self.W = {op: np.random.randn(in_dim, out_dim) * 0.1 for op in self.OPS}
        self.b = {op: np.zeros(out_dim) for op in self.OPS}

    def forward(self, x):
        weights = np.exp(self.alphas) / np.sum(np.exp(self.alphas))
        out = np.zeros((x.shape[0], self.out_dim))
        for i, op in enumerate(self.OPS):
            if op == 'identity':
                h = x @ np.eye(self.in_dim, self.out_dim) + self.b[op]
            elif op == 'tanh':
                h = np.tanh(x @ self.W[op] + self.b[op])
            elif op == 'relu':
                h = np.maximum(x @ self.W[op] + self.b[op], 0)
            elif op == 'sigmoid':
                h = 1 / (1 + np.exp(-(x @ self.W[op] + self.b[op])))
            out += weights[i] * h
        return out

    def discretize(self):
        return self.OPS[np.argmax(self.alphas)]


class DARTS:
    """Differentiable Architecture Search (simplified)."""
    def __init__(self, n_cells=4, in_dim=8, out_dim=1):
        self.cells = [NASCell(in_dim, in_dim) for _ in range(n_cells)]
        self.head_W = np.random.randn(in_dim, out_dim) * 0.1
        self.head_b = np.zeros(out_dim)

    def forward(self, x):
        h = x
        for cell in self.cells:
            h = cell.forward(h)
        return h @ self.head_W + self.head_b

    def get_arch(self):
        return [c.discretize() for c in self.cells]


if __name__ == "__main__":
    np.random.seed(42)
    darts = DARTS()
    X = np.random.randn(200, 8)
    y = np.sin(X[:, 0:1]) + 0.1 * np.random.randn(200, 1)
    lr = 0.001
    losses = []
    for epoch in range(300):
        y_pred = darts.forward(X)
        loss = np.mean((y_pred - y) ** 2)
        losses.append(loss)
        grad = 2 * (y_pred - y) / len(X)
        # Simplified gradient step
        for cell in darts.cells:
            cell.alphas -= lr * np.random.randn(*cell.alphas.shape) * loss * 0.01
        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {loss:.6f}")
            print(f"  Architecture: {darts.get_arch()}")

    arch = darts.get_arch()
    print(f"\nDiscovered architecture: {arch}")

    plt.figure(figsize=(10, 4))
    plt.subplot(121)
    plt.plot(losses)
    plt.yscale('log')
    plt.title('NAS Training Loss')
    plt.subplot(122)
    alphas = np.array([cell.alphas for cell in darts.cells])
    plt.imshow(alphas, aspect='auto', cmap='YlOrRd')
    plt.yticks(range(len(darts.cells)), [f'Cell {i}' for i in range(len(darts.cells))])
    plt.xticks(range(len(NASCell.OPS)), NASCell.OPS)
    plt.colorbar(label='Alpha')
    plt.title('Architecture weights')
    plt.tight_layout()
    plt.savefig('../../assets/phase07/nas.png')
    plt.close()
    print("Saved nas.png")
