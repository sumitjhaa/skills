"""
07.17 Normalizing Flows: Real NVP affine coupling layers.
"""
import numpy as np
import matplotlib.pyplot as plt


class AffineCoupling:
    """Real NVP affine coupling layer."""
    def __init__(self, dim, mask):
        self.dim = dim
        self.mask = mask
        self.s_W = np.random.randn(dim, dim) * 0.1
        self.s_b = np.zeros(dim)
        self.t_W = np.random.randn(dim, dim) * 0.1
        self.t_b = np.zeros(dim)

    def forward(self, x):
        x1 = x * self.mask
        x2 = x * (1 - self.mask)
        s = np.tanh(x1 @ self.s_W + self.s_b) * (1 - self.mask)
        t = (x1 @ self.t_W + self.t_b) * (1 - self.mask)
        y = x1 + (1 - self.mask) * (x2 * np.exp(s) + t)
        log_det = np.sum(s, axis=-1)
        return y, log_det

    def inverse(self, y):
        y1 = y * self.mask
        y2 = y * (1 - self.mask)
        s = np.tanh(y1 @ self.s_W + self.s_b) * (1 - self.mask)
        t = (y1 @ self.t_W + self.t_b) * (1 - self.mask)
        x = y1 + (1 - self.mask) * ((y2 - t) * np.exp(-s))
        return x


class NormalizingFlow:
    def __init__(self, dim=2, n_layers=4):
        self.layers = []
        for i in range(n_layers):
            mask = np.array([1 if (j + i) % 2 == 0 else 0 for j in range(dim)])
            self.layers.append(AffineCoupling(dim, mask))

    def forward(self, x):
        log_det_sum = 0
        z = x
        for layer in self.layers:
            z, ld = layer.forward(z)
            log_det_sum += ld
        return z, log_det_sum

    def inverse(self, z):
        x = z
        for layer in reversed(self.layers):
            x = layer.inverse(x)
        return x

    def sample(self, n, dim=2):
        z = np.random.randn(n, dim)
        return self.inverse(z)


if __name__ == "__main__":
    np.random.seed(42)
    flow = NormalizingFlow(dim=2, n_layers=4)
    nf = NormalizingFlow(dim=2, n_layers=4)

    # Test forward/inverse
    x = np.random.randn(100, 2)
    z, ld = flow.forward(x)
    x_recon = flow.inverse(z)
    print(f"Forward/backward error: {np.abs(x - x_recon).max():.6f}")

    # Sample from learned distribution
    samples = nf.sample(500)

    plt.figure(figsize=(12, 4))
    plt.subplot(131)
    plt.scatter(x[:, 0], x[:, 1], alpha=0.5, label='Original')
    plt.legend()
    plt.title('Original (Gaussian)')
    plt.subplot(132)
    plt.scatter(z[:, 0], z[:, 1], alpha=0.5, label='Transformed')
    plt.legend()
    plt.title('Flow: transformed')
    plt.subplot(133)
    plt.scatter(samples[:, 0], samples[:, 1], alpha=0.5, label='Generated')
    plt.legend()
    plt.title('Flow: generated samples')
    plt.tight_layout()
    plt.savefig('../../assets/phase07/normalizing_flows.png')
    plt.close()
    print("Saved normalizing_flows.png")
