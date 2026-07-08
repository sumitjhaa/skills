"""
07.01 KAN: Kolmogorov-Arnold Network
Minimal B-spline based KAN implementation.
"""
import numpy as np
import matplotlib.pyplot as plt


class BSpline:
    """B-spline basis functions."""
    def __init__(self, num_grids=8, k=3):
        self.num_grids = num_grids
        self.k = k
        self.grid = np.linspace(-1, 1, num_grids)

    def basis(self, x):
        """Evaluate B-spline basis."""
        n = len(self.grid)
        knots = np.concatenate([
            np.full(self.k, self.grid[0]),
            self.grid,
            np.full(self.k, self.grid[-1])
        ])
        x = np.asarray(x)
        N = np.zeros((x.shape[0], n))
        for i in range(n - 1):
            idx = i + self.k
            N[:, i] = ((x >= knots[idx]) & (x < knots[idx + 1])).astype(float)
        for _ in range(1, self.k + 1):
            for i in range(n):
                idx = i + self.k - _
                left = (x - knots[idx]) / (knots[idx + _] - knots[idx] + 1e-10) if knots[idx + _] != knots[idx] else 0
                right = (knots[idx + _ + 1] - x) / (knots[idx + _ + 1] - knots[idx + 1] + 1e-10) if knots[idx + _ + 1] != knots[idx + 1] else 0
                if _ == 1:
                    N[:, i] = left * N[:, max(0, i-1)] + right * N[:, i]
                else:
                    if i > 0:
                        N[:, i] = left * N[:, i + _ - 1] + right * N[:, i] if i + _ - 1 < n else right * N[:, i]
        return N


class KAN:
    def __init__(self, in_features, out_features, num_grids=8, k=3):
        self.in_features = in_features
        self.out_features = out_features
        self.spline = BSpline(num_grids, k)
        self.num_basis = num_grids
        self.coeffs = np.random.randn(in_features, out_features, self.num_basis) * 0.1
        self.silu_weight = np.random.randn(in_features, out_features) * 0.1

    def silu(self, x):
        return x / (1 + np.exp(-x))

    def forward(self, x):
        batch = x.shape[0]
        basis_out = self.spline.basis(x.ravel()).reshape(batch, self.in_features, self.num_basis)
        spline_out = np.einsum('bik,ioj->bo', basis_out, self.coeffs) / self.num_basis
        siLU_out = self.silu(x) @ self.silu_weight
        return siLU_out + spline_out


if __name__ == "__main__":
    np.random.seed(42)
    model = KAN(1, 1)
    x = np.linspace(-1, 1, 100).reshape(-1, 1)
    y = np.sin(3 * x) + 0.1 * np.random.randn(100, 1)
    lr = 0.005
    losses = []
    for epoch in range(2000):
        y_pred = model.forward(x)
        loss = np.mean((y_pred - y) ** 2)
        losses.append(loss)
        grad = 2 * (y_pred - y) / len(x)
        # Simple gradient descent (no autograd needed for demo)
        for i in range(model.in_features):
            for o in range(model.out_features):
                basis_out = model.spline.basis(x.ravel()).reshape(100, model.in_features, model.num_basis)
                g_coeff = np.mean(grad[:, o:o+1] * basis_out[:, i, :], axis=0) / model.num_basis
                model.coeffs[i, o] -= lr * g_coeff
                g_silu = np.mean(grad[:, o:o+1] * model.silu(x), axis=0)[0]
                model.silu_weight[i, o] -= lr * g_silu
        if epoch % 400 == 0:
            print(f"Epoch {epoch}, Loss: {loss:.6f}")

    plt.figure(figsize=(10, 4))
    plt.subplot(121)
    plt.plot(losses)
    plt.yscale('log')
    plt.title('Training Loss')
    plt.subplot(122)
    plt.scatter(x, y, s=10, alpha=0.5, label='Data')
    plt.plot(x, model.forward(x), 'r-', label='KAN fit')
    plt.legend()
    plt.title('KAN Regression')
    plt.tight_layout()
    plt.savefig('../../assets/phase07/kan_demo.png')
    plt.close()
    print("Done. Saved kan_demo.png")
