"""
07.12 Set Functions: Deep Sets and permutation-invariant networks.
"""
import numpy as np
import matplotlib.pyplot as plt


class DeepSet:
    def __init__(self, x_dim=1, hidden_dim=32, out_dim=1):
        self.phi_W1 = np.random.randn(x_dim, hidden_dim) * 0.1
        self.phi_b1 = np.zeros(hidden_dim)
        self.phi_W2 = np.random.randn(hidden_dim, hidden_dim) * 0.1
        self.phi_b2 = np.zeros(hidden_dim)
        self.rho_W1 = np.random.randn(hidden_dim, hidden_dim) * 0.1
        self.rho_b1 = np.zeros(hidden_dim)
        self.rho_W2 = np.random.randn(hidden_dim, out_dim) * 0.1
        self.rho_b2 = np.zeros(out_dim)

    def forward(self, x_set):
        h = np.tanh(x_set @ self.phi_W1 + self.phi_b1)
        h = np.tanh(h @ self.phi_W2 + self.phi_b2)
        aggregated = np.mean(h, axis=1, keepdims=True)
        h = np.tanh(aggregated @ self.rho_W1 + self.rho_b1)
        out = h @ self.rho_W2 + self.rho_b2
        return out.squeeze(-1)


class PointNet:
    def __init__(self, x_dim=3, hidden_dim=64, out_dim=1):
        self.mlp_W1 = np.random.randn(x_dim, hidden_dim) * 0.1
        self.mlp_b1 = np.zeros(hidden_dim)
        self.mlp_W2 = np.random.randn(hidden_dim, hidden_dim) * 0.1
        self.mlp_b2 = np.zeros(hidden_dim)
        self.head_W1 = np.random.randn(hidden_dim, hidden_dim) * 0.1
        self.head_b1 = np.zeros(hidden_dim)
        self.head_W2 = np.random.randn(hidden_dim, out_dim) * 0.1
        self.head_b2 = np.zeros(out_dim)

    def forward(self, points):
        h = np.maximum(points @ self.mlp_W1 + self.mlp_b1, 0)
        h = np.maximum(h @ self.mlp_W2 + self.mlp_b2, 0)
        global_feat = np.max(h, axis=1)
        out = np.maximum(global_feat @ self.head_W1 + self.head_b1, 0)
        out = out @ self.head_W2 + self.head_b2
        return out


if __name__ == "__main__":
    np.random.seed(42)
    print("=== Deep Sets ===")
    ds = DeepSet()
    batch, set_size, x_dim = 16, 8, 1
    x = np.random.randn(batch, set_size, x_dim)
    permuted = x[:, np.random.permutation(set_size), :]
    out1 = ds.forward(x)
    out2 = ds.forward(permuted)
    print(f"Permutation invariant? {np.allclose(out1, out2, atol=1e-5)}")

    print("\n=== PointNet ===")
    pn = PointNet()
    pts = np.random.randn(4, 10, 3)
    out = pn.forward(pts)
    print(f"PointNet output shape: {out.shape}")

    plt.bar(range(len(out)), out.ravel())
    plt.title('PointNet: per-batch classification')
    plt.savefig('../../assets/phase07/set_functions.png')
    plt.close()
    print("Saved set_functions.png")
