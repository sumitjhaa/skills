"""
07.19 Diffusion: DDPM on 2D data.
"""
import numpy as np
import matplotlib.pyplot as plt


class DDPM:
    """Denoising Diffusion Probabilistic Model on 2D."""
    def __init__(self, T=100, beta_start=1e-4, beta_end=0.02):
        self.T = T
        self.betas = np.linspace(beta_start, beta_end, T)
        self.alphas = 1 - self.betas
        self.alpha_bar = np.cumprod(self.alphas)
        self.W1 = np.random.randn(2, 128) * 0.1
        self.b1 = np.zeros(128)
        self.W2 = np.random.randn(128, 128) * 0.1
        self.b2 = np.zeros(128)
        self.W3 = np.random.randn(128, 2) * 0.1
        self.b3 = np.zeros(2)

    def forward_diffusion(self, x0, t):
        eps = np.random.randn(*x0.shape)
        alpha_t = self.alpha_bar[t]
        xt = np.sqrt(alpha_t) * x0 + np.sqrt(1 - alpha_t) * eps
        return xt, eps

    def noise_pred(self, xt, t):
        h = np.tanh(xt @ self.W1 + self.b1 + t.reshape(-1, 1) * 0.01)
        h = np.tanh(h @ self.W2 + self.b2)
        return h @ self.W3 + self.b3

    def sample(self, n=100):
        x = np.random.randn(n, 2)
        for t in reversed(range(self.T)):
            z = np.random.randn(n, 2) if t > 0 else 0
            t_batch = np.full(n, t)
            eps_pred = self.noise_pred(x, t_batch)
            alpha_t = self.alphas[t]
            alpha_bar_t = self.alpha_bar[t]
            beta_t = self.betas[t]
            coef1 = 1 / np.sqrt(alpha_t)
            coef2 = beta_t / np.sqrt(1 - alpha_bar_t)
            x = coef1 * (x - coef2 * eps_pred) + np.sqrt(beta_t) * z
        return x


if __name__ == "__main__":
    np.random.seed(42)
    ddpm = DDPM(T=50)
    # Generate data from 2D mixture
    x0 = np.random.randn(500, 2)
    x0[:250] += np.array([3, 0])
    x0[250:] += np.array([-3, 0])

    # Train
    lr = 0.001
    for epoch in range(500):
        t = np.random.randint(0, ddpm.T, len(x0))
        xt, eps = ddpm.forward_diffusion(x0, t)
        eps_pred = ddpm.noise_pred(xt, t)
        loss = np.mean((eps - eps_pred) ** 2)
        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {loss:.6f}")
        grad = 2 * (eps_pred - eps) / len(x0)
        ddpm.W1 -= lr * (xt.T @ (grad @ ddpm.W3.T * (1 - np.tanh(xt @ ddpm.W1 + ddpm.b1 + t.reshape(-1, 1) * 0.01)**2))) * 0.01
        ddpm.W3 -= lr * (np.tanh(xt @ ddpm.W1 + ddpm.b1 + t.reshape(-1, 1) * 0.01).T @ grad)
        ddpm.b3 -= lr * grad.mean(axis=0)

    samples = ddpm.sample(500)
    x_noisy, _ = ddpm.forward_diffusion(x0, 40)

    plt.figure(figsize=(12, 4))
    plt.subplot(131)
    plt.scatter(x0[:, 0], x0[:, 1], alpha=0.5)
    plt.title('Original data')
    plt.subplot(132)
    plt.scatter(x_noisy[:, 0], x_noisy[:, 1], alpha=0.5)
    plt.title('Noisy (t=40)')
    plt.subplot(133)
    plt.scatter(samples[:, 0], samples[:, 1], alpha=0.5)
    plt.title('Generated (DDPM)')
    plt.tight_layout()
    plt.savefig('../../assets/phase07/diffusion.png')
    plt.close()
    print("Saved diffusion.png")
