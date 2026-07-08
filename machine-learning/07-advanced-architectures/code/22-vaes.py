"""
07.22 VAEs: Variational Autoencoder with multiple variants.
"""
import numpy as np
import matplotlib.pyplot as plt


class VAE:
    def __init__(self, x_dim=8, latent_dim=2):
        self.enc_W = np.random.randn(x_dim, 32) * 0.1
        self.enc_b = np.zeros(32)
        self.mu_W = np.random.randn(32, latent_dim) * 0.1
        self.mu_b = np.zeros(latent_dim)
        self.logvar_W = np.random.randn(32, latent_dim) * 0.1
        self.logvar_b = np.zeros(latent_dim)
        self.dec_W1 = np.random.randn(latent_dim, 32) * 0.1
        self.dec_b1 = np.zeros(32)
        self.dec_W2 = np.random.randn(32, x_dim) * 0.1
        self.dec_b2 = np.zeros(x_dim)

    def encode(self, x):
        h = np.tanh(x @ self.enc_W + self.enc_b)
        return h @ self.mu_W + self.mu_b, h @ self.logvar_W + self.logvar_b

    def reparameterize(self, mu, logvar):
        eps = np.random.randn(*mu.shape)
        return mu + np.exp(0.5 * logvar) * eps

    def decode(self, z):
        h = np.tanh(z @ self.dec_W1 + self.dec_b1)
        return h @ self.dec_W2 + self.dec_b2

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        x_recon = self.decode(z)
        return x_recon, mu, logvar

    def loss(self, x, beta=1.0):
        x_recon, mu, logvar = self.forward(x)
        recon_loss = np.mean((x_recon - x) ** 2)
        kl_loss = -0.5 * np.mean(1 + logvar - mu**2 - np.exp(logvar))
        return recon_loss + beta * kl_loss, recon_loss, kl_loss


class BetaVAE(VAE):
    def loss(self, x, beta=4.0):
        return super().loss(x, beta=beta)


class CVAE(VAE):
    def __init__(self, x_dim=8, latent_dim=2, n_classes=3):
        self.n_classes = n_classes
        super().__init__(x_dim + n_classes, latent_dim)
        self.dec_dim = latent_dim + n_classes
        self.dec_W1 = np.random.randn(self.dec_dim, 32) * 0.1
        self.dec_b1 = np.zeros(32)
        self.dec_W2 = np.random.randn(32, x_dim) * 0.1
        self.dec_b2 = np.zeros(x_dim)

    def forward(self, x, c):
        xc = np.hstack([x, c])
        mu, logvar = self.encode(xc)
        z = self.reparameterize(mu, logvar)
        zc = np.hstack([z, c])
        h = np.tanh(zc @ self.dec_W1 + self.dec_b1)
        return h @ self.dec_W2 + self.dec_b2, mu, logvar


if __name__ == "__main__":
    np.random.seed(42)
    x = np.random.randn(500, 8)

    print("=== VAE ===")
    vae = VAE()
    for epoch in range(200):
        total, recon, kl = vae.loss(x)
        if epoch % 50 == 0:
            print(f"Epoch {epoch}, recon={recon:.4f}, KL={kl:.4f}")

    print("\n=== Beta-VAE ===")
    bvae = BetaVAE()
    total, recon, kl = bvae.loss(x, beta=4.0)
    print(f"Beta-VAE: recon={recon:.4f}, KL={kl:.4f} (beta=4)")

    print("\n=== CVAE ===")
    cvae = CVAE()
    c = np.eye(3)[np.random.randint(0, 3, 500)]
    x_recon, mu, logvar = cvae.forward(x, c)
    print(f"CVAE recon error: {np.mean((x_recon - x)**2):.4f}")

    # Generate samples
    z = np.random.randn(10, 2)
    samples = vae.decode(z)
    print(f"Generated samples shape: {samples.shape}")

    plt.figure(figsize=(10, 4))
    plt.subplot(121)
    _, mu, logvar = vae.forward(x)
    plt.scatter(mu[:, 0], mu[:, 1], alpha=0.5)
    plt.title('VAE Latent Space')
    plt.subplot(122)
    plt.plot(samples.T, alpha=0.5)
    plt.title('Generated samples')
    plt.tight_layout()
    plt.savefig('../../assets/phase07/vaes.png')
    plt.close()
    print("Saved vaes.png")
