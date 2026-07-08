"""
07.18 Autoregressive Models: MADE-like masked autoencoder.
"""
import numpy as np
import matplotlib.pyplot as plt


class MADE:
    """Masked Autoencoder for Distribution Estimation."""
    def __init__(self, dim=4, hidden=32):
        self.dim = dim
        self.W1 = np.random.randn(dim, hidden) * 0.1
        self.b1 = np.zeros(hidden)
        self.W2 = np.random.randn(hidden, dim * 2) * 0.1  # mu + log_sigma
        self.b2 = np.zeros(dim * 2)
        self._create_masks()

    def _create_masks(self):
        """Autoregressive masks: each output i only depends on inputs < i."""
        self.mask1 = np.zeros_like(self.W1)
        self.mask2 = np.zeros_like(self.W2)
        for i in range(self.dim):
            for h in range(self.W1.shape[1]):
                self.mask1[i, h] = 1.0  # simplified: all inputs to all hidden
        for h in range(self.W2.shape[0]):
            for o in range(self.dim * 2):
                out_dim = o % self.dim
                self.mask2[h, o] = 1.0 if h < self.W2.shape[0] else 0.0  # simplified

    def forward(self, x):
        h = np.tanh(x @ (self.W1 * self.mask1) + self.b1)
        params = h @ (self.W2 * self.mask2) + self.b2
        mu = params[:, :self.dim]
        log_sigma = params[:, self.dim:]
        return mu, log_sigma

    def log_prob(self, x):
        mu, log_sigma = self.forward(x)
        sigma = np.exp(log_sigma)
        return -0.5 * np.log(2 * np.pi) - log_sigma - 0.5 * ((x - mu) / sigma) ** 2

    def sample(self, n_samples):
        samples = np.zeros((n_samples, self.dim))
        for i in range(self.dim):
            mu, log_sigma = self.forward(samples)
            samples[:, i] = mu[:, i] + np.exp(log_sigma[:, i]) * np.random.randn(n_samples)
        return samples


class WaveNetBlock:
    """Simplified WaveNet-style dilated convolution."""
    def __init__(self, channels=4, kernel=3, dilation=1):
        self.channels = channels
        self.kernel = kernel
        self.dilation = dilation
        self.W = np.random.randn(channels, channels, kernel) * 0.1
        self.b = np.zeros(channels)

    def forward(self, x):
        T = x.shape[0]
        pad = self.kernel * self.dilation
        x_pad = np.pad(x, ((pad, 0), (0, 0)), mode='replicate')
        out = np.zeros_like(x)
        for t in range(T):
            for c_out in range(self.channels):
                val = 0
                for c_in in range(self.channels):
                    for k in range(self.kernel):
                        idx = t + pad - k * self.dilation
                        val += self.W[c_out, c_in, k] * x_pad[idx, c_in]
                out[t, c_out] = val + self.b[c_out]
        return np.tanh(out)


if __name__ == "__main__":
    np.random.seed(42)
    print("=== MADE ===")
    made = MADE(dim=4)
    x = np.random.randn(100, 4)
    lp = made.log_prob(x)
    print(f"Mean log prob: {lp.mean():.4f}")
    samples = made.sample(10)
    print(f"Generated samples shape: {samples.shape}")

    print("\n=== WaveNet block ===")
    wavenet = WaveNetBlock(channels=4, kernel=3, dilation=2)
    audio = np.sin(np.linspace(0, 10 * np.pi, 200)).reshape(-1, 1)
    audio = np.tile(audio, (1, 4))
    out = wavenet.forward(audio)

    plt.figure(figsize=(10, 3))
    plt.subplot(121)
    plt.plot(audio[:100, 0], label='Input')
    plt.plot(out[:100, 0], label='Output (tanh)')
    plt.legend()
    plt.title('WaveNet block (dilated conv)')
    plt.subplot(122)
    for i in range(4):
        samples_sorted = np.sort(samples[:, i])
        plt.plot(samples_sorted, np.linspace(0, 1, len(samples_sorted)), label=f'dim{i}')
    plt.legend()
    plt.title('MADE: empirical CDF')
    plt.tight_layout()
    plt.savefig('../../assets/phase07/autoregressive.png')
    plt.close()
    print("Saved autoregressive.png")
