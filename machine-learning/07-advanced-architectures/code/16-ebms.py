"""
07.16 EBMs: Energy-Based Models with Contrastive Divergence.
"""
import numpy as np
import matplotlib.pyplot as plt


class RBM:
    """Restricted Boltzmann Machine."""
    def __init__(self, n_visible=6, n_hidden=4):
        self.W = np.random.randn(n_visible, n_hidden) * 0.1
        self.b = np.zeros(n_visible)
        self.c = np.zeros(n_hidden)

    def sample_h(self, v):
        p = 1 / (1 + np.exp(-(v @ self.W + self.c)))
        return p, np.random.binomial(1, p)

    def sample_v(self, h):
        p = 1 / (1 + np.exp(-(h @ self.W.T + self.b)))
        return p, np.random.binomial(1, p)

    def energy(self, v, h):
        return -v @ self.b - h @ self.c - (v @ self.W * h).sum()


class EBM:
    """Simple energy-based model with Langevin sampling."""
    def __init__(self, dim=2, hidden=64):
        self.W1 = np.random.randn(dim, hidden) * 0.1
        self.b1 = np.zeros(hidden)
        self.W2 = np.random.randn(hidden, 1) * 0.1
        self.b2 = np.zeros(1)

    def energy(self, x):
        h = np.tanh(x @ self.W1 + self.b1)
        return (h @ self.W2 + self.b2).squeeze(-1)

    def langevin_sample(self, x_init, n_steps=100, eps=0.1):
        x = x_init.copy()
        for _ in range(n_steps):
            eps_ = np.random.randn(*x.shape) * np.sqrt(2 * eps)
            grad_x = self._grad_energy(x)
            x = x - eps * grad_x + eps_
        return x

    def _grad_energy(self, x):
        eps_fd = 1e-4
        grad = np.zeros_like(x)
        for i in range(x.shape[-1]):
            xp = x.copy()
            xm = x.copy()
            xp[..., i] += eps_fd
            xm[..., i] -= eps_fd
            grad[..., i] = (self.energy(xp) - self.energy(xm)) / (2 * eps_fd)
        return grad


if __name__ == "__main__":
    np.random.seed(42)
    print("=== RBM ===")
    rbm = RBM(6, 4)
    v = np.random.binomial(1, 0.5, (10, 6))
    _, h = rbm.sample_h(v)
    _, v_recon = rbm.sample_v(h)
    print(f"Reconstruction error: {np.abs(v - v_recon).mean():.4f}")

    print("\n=== EBM Langevin Sampling ===")
    ebm = EBM(dim=2)
    x_init = np.random.randn(20, 2)
    x_samples = ebm.langevin_sample(x_init, n_steps=50)

    plt.figure(figsize=(10, 4))
    plt.subplot(121)
    plt.scatter(x_init[:, 0], x_init[:, 1], alpha=0.5, label='Initial')
    plt.scatter(x_samples[:, 0], x_samples[:, 1], alpha=0.5, label='After Langevin')
    plt.legend()
    plt.title('EBM: Langevin sampling')
    plt.subplot(122)
    grid = np.mgrid[-3:3:30j, -3:3:30j].reshape(2, -1).T
    energies = ebm.energy(grid).reshape(30, 30)
    plt.contourf(np.linspace(-3, 3, 30), np.linspace(-3, 3, 30), energies, levels=20)
    plt.colorbar(label='Energy')
    plt.title('Learned Energy Landscape')
    plt.tight_layout()
    plt.savefig('../../assets/phase07/ebm.png')
    plt.close()
    print("Saved ebm.png")
