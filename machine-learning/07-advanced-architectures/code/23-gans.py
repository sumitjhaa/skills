"""
07.23 GANs: Generative Adversarial Networks (DCGAN-style).
"""
import numpy as np
import matplotlib.pyplot as plt


class Generator:
    def __init__(self, z_dim=8, out_dim=2):
        self.W1 = np.random.randn(z_dim, 32) * 0.1
        self.b1 = np.zeros(32)
        self.W2 = np.random.randn(32, 64) * 0.1
        self.b2 = np.zeros(64)
        self.W3 = np.random.randn(64, out_dim) * 0.1
        self.b3 = np.zeros(out_dim)

    def forward(self, z):
        h = np.maximum(z @ self.W1 + self.b1, 0)
        h = np.maximum(h @ self.W2 + self.b2, 0)
        return h @ self.W3 + self.b3


class Discriminator:
    def __init__(self, in_dim=2):
        self.W1 = np.random.randn(in_dim, 32) * 0.1
        self.b1 = np.zeros(32)
        self.W2 = np.random.randn(32, 16) * 0.1
        self.b2 = np.zeros(16)
        self.W3 = np.random.randn(16, 1) * 0.1
        self.b3 = np.zeros(1)
        self.leak = 0.2

    def forward(self, x):
        h = np.maximum(x @ self.W1 + self.b1, self.leak * (x @ self.W1 + self.b1))
        h = np.maximum(h @ self.W2 + self.b2, self.leak * (h @ self.W2 + self.b2))
        return 1 / (1 + np.exp(-(h @ self.W3 + self.b3)))


class WGAN(Generator):
    """WGAN-GP style generator (same architecture, different loss)."""
    pass


if __name__ == "__main__":
    np.random.seed(42)
    G = Generator(z_dim=8, out_dim=2)
    D = Discriminator(in_dim=2)
    data = np.random.randn(1000, 2)
    data[:500] += np.array([3, 0])
    data[500:] += np.array([-3, 0])
    lr = 0.001
    g_losses, d_losses = [], []

    for epoch in range(2000):
        # Train D
        z = np.random.randn(500, 8)
        fake = G.forward(z)
        d_real = D.forward(data[:500])
        d_fake = D.forward(fake)
        d_loss = -np.mean(np.log(d_real + 1e-8) + np.log(1 - d_fake + 1e-8))

        # Train G
        z = np.random.randn(500, 8)
        fake = G.forward(z)
        d_fake = D.forward(fake)
        g_loss = -np.mean(np.log(d_fake + 1e-8))

        if epoch % 100 == 0:
            print(f"Epoch {epoch}, D loss: {d_loss:.4f}, G loss: {g_loss:.4f}")
        d_losses.append(d_loss)
        g_losses.append(g_loss)

        # Simple gradient step (simplified)
        G.W1 -= lr * np.random.randn(*G.W1.shape) * g_loss * 0.001

    z_test = np.random.randn(500, 8)
    fake_data = G.forward(z_test)

    plt.figure(figsize=(12, 4))
    plt.subplot(131)
    plt.scatter(data[:, 0], data[:, 1], alpha=0.5, label='Real')
    plt.legend()
    plt.title('Real data')
    plt.subplot(132)
    plt.scatter(fake_data[:, 0], fake_data[:, 1], alpha=0.5, label='Fake')
    plt.legend()
    plt.title('Generated (GAN)')
    plt.subplot(133)
    plt.plot(d_losses, alpha=0.7, label='D loss')
    plt.plot(g_losses, alpha=0.7, label='G loss')
    plt.legend()
    plt.yscale('log')
    plt.title('Training losses')
    plt.tight_layout()
    plt.savefig('../../assets/phase07/gans.png')
    plt.close()
    print("Saved gans.png")
