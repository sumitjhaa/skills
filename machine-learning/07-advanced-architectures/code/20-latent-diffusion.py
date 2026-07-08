"""
07.20 Latent Diffusion: Autoencoder + diffusion in latent space.
"""
import numpy as np
import matplotlib.pyplot as plt


class SimpleAE:
    """Simple autoencoder for latent representation."""
    def __init__(self, in_dim=8, latent_dim=2):
        self.enc_W1 = np.random.randn(in_dim, 16) * 0.1
        self.enc_b1 = np.zeros(16)
        self.enc_W2 = np.random.randn(16, latent_dim) * 0.1
        self.enc_b2 = np.zeros(latent_dim)
        self.dec_W1 = np.random.randn(latent_dim, 16) * 0.1
        self.dec_b1 = np.zeros(16)
        self.dec_W2 = np.random.randn(16, in_dim) * 0.1
        self.dec_b2 = np.zeros(in_dim)

    def encode(self, x):
        h = np.tanh(x @ self.enc_W1 + self.enc_b1)
        return h @ self.enc_W2 + self.enc_b2

    def decode(self, z):
        h = np.tanh(z @ self.dec_W1 + self.dec_b1)
        return h @ self.dec_W2 + self.dec_b2


class LatentDiffusion:
    """DDPM in latent space."""
    def __init__(self, latent_dim=2, T=50):
        self.latent_dim = latent_dim
        self.T = T
        self.betas = np.linspace(1e-4, 0.02, T)
        self.alphas = 1 - self.betas
        self.alpha_bar = np.cumprod(self.alphas)
        self.W1 = np.random.randn(latent_dim, 64) * 0.1
        self.b1 = np.zeros(64)
        self.W2 = np.random.randn(64, 64) * 0.1
        self.b2 = np.zeros(64)
        self.W3 = np.random.randn(64, latent_dim) * 0.1
        self.b3 = np.zeros(latent_dim)

    def noise_pred(self, z, t):
        h = np.tanh(z @ self.W1 + self.b1 + t.reshape(-1, 1) * 0.01)
        h = np.tanh(h @ self.W2 + self.b2)
        return h @ self.W3 + self.b3

    def sample(self, n=100):
        z = np.random.randn(n, self.latent_dim)
        for t in reversed(range(self.T)):
            eps = np.random.randn(n, self.latent_dim) if t > 0 else 0
            eps_pred = self.noise_pred(z, np.full(n, t))
            z = (1 / np.sqrt(self.alphas[t])) * (z - (self.betas[t] / np.sqrt(1 - self.alpha_bar[t])) * eps_pred) + np.sqrt(self.betas[t]) * eps
        return z


if __name__ == "__main__":
    np.random.seed(42)
    ae = SimpleAE(in_dim=8, latent_dim=2)
    data = np.random.randn(500, 8)
    latents = ae.encode(data)
    recon = ae.decode(latents)
    print(f"AE recon error: {np.mean((data - recon)**2):.6f}")

    ldm = LatentDiffusion(latent_dim=2, T=30)
    for epoch in range(300):
        t = np.random.randint(0, ldm.T, len(latents))
        eps = np.random.randn(*latents.shape)
        zt = np.sqrt(ldm.alpha_bar[t]) * latents + np.sqrt(1 - ldm.alpha_bar[t]) * eps
        eps_pred = ldm.noise_pred(zt, t)
        loss = np.mean((eps - eps_pred) ** 2)
        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {loss:.6f}")

    z_new = ldm.sample(200)
    x_new = ae.decode(z_new)

    plt.figure(figsize=(12, 4))
    plt.subplot(131)
    plt.scatter(latents[:, 0], latents[:, 1], alpha=0.5)
    plt.title('Original latents')
    plt.subplot(132)
    plt.scatter(z_new[:, 0], z_new[:, 1], alpha=0.5)
    plt.title('Generated latents')
    plt.subplot(133)
    plt.plot(x_new.T, alpha=0.3)
    plt.title('Generated data (decoded)')
    plt.tight_layout()
    plt.savefig('../../assets/phase07/latent_diffusion.png')
    plt.close()
    print("Saved latent_diffusion.png")
