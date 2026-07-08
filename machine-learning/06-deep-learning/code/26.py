"""06.26 - Normalization Alternatives: RMSNorm, ScaleNorm, AdaptiveNorm"""

import numpy as np


class RMSNorm:
    def __init__(self, dim, eps=1e-6):
        self.gamma = np.ones(dim)
        self.eps = eps

    def forward(self, x):
        rms = np.sqrt(np.mean(x ** 2, axis=-1, keepdims=True) + self.eps)
        return self.gamma * x / rms


class ScaleNorm:
    def __init__(self, dim, eps=1e-6):
        self.g = np.ones(1)
        self.eps = eps

    def forward(self, x):
        norm = np.linalg.norm(x, axis=-1, keepdims=True) + self.eps
        return self.g * x / norm


class AdaptiveNorm:
    def __init__(self, dim):
        self.dim = dim
        self.W_gamma = np.random.randn(dim, dim) * 0.01
        self.W_beta = np.random.randn(dim, dim) * 0.01

    def forward(self, x, cond):
        gamma = 1 + x @ self.W_gamma + cond @ self.W_gamma * 0.1
        beta = x @ self.W_beta + cond @ self.W_beta * 0.1
        mu = x.mean(axis=-1, keepdims=True)
        var = x.var(axis=-1, keepdims=True)
        x_norm = (x - mu) / np.sqrt(var + 1e-5)
        return gamma * x_norm + beta


class WeightNormLinear:
    def __init__(self, in_features, out_features):
        self.v = np.random.randn(in_features, out_features) * 0.01
        self.g = np.ones(out_features)
        self.b = np.zeros(out_features)

    @property
    def W(self):
        return self.g * self.v / np.linalg.norm(self.v, axis=0, keepdims=True)

    def forward(self, x):
        return x @ self.W + self.b


class SpectralNormLinear:
    def __init__(self, in_features, out_features, n_power_iter=1):
        self.W = np.random.randn(in_features, out_features) * 0.01
        self.u = np.random.randn(out_features)
        self.n_power_iter = n_power_iter

    @property
    def W_bar(self):
        u = self.u.copy()
        v = np.random.randn(self.W.shape[0])
        for _ in range(self.n_power_iter):
            v = (self.W @ u) / np.linalg.norm(self.W @ u)
            u = (self.W.T @ v) / np.linalg.norm(self.W.T @ v)
        sigma = v @ self.W @ u
        return self.W / sigma

    def forward(self, x):
        return x @ self.W_bar


if __name__ == "__main__":
    np.random.seed(42)
    x = np.random.randn(4, 32)

    rms = RMSNorm(32)
    out_rms = rms.forward(x)
    rms_val = np.sqrt(np.mean(out_rms ** 2, axis=-1))
    print(f"RMSNorm:   output shape {out_rms.shape}, RMS = {rms_val}")
    print(f"  All RMS values ~1: {np.allclose(rms_val, 1.0, atol=1e-4)}")

    sc = ScaleNorm(32)
    out_sc = sc.forward(x)
    norms = np.linalg.norm(out_sc, axis=-1)
    print(f"\nScaleNorm: output shape {out_sc.shape}, norms = {norms}")
    print(f"  All norms = g ({sc.g[0]:.1f}): {np.allclose(norms, sc.g[0])}")

    adn = AdaptiveNorm(32)
    cond = np.random.randn(4, 32)
    out_adn = adn.forward(x, cond)
    print(f"\nAdaptiveNorm: output shape {out_adn.shape}")

    wn = WeightNormLinear(32, 16)
    out_wn = wn.forward(x)
    print(f"\nWeightNorm Linear: input (4,32) -> output {out_wn.shape}")
    W_norms = np.linalg.norm(wn.W, axis=0)
    print(f"  Weight column norms = {np.round(W_norms, 4)} (should be |g| = {wn.g[0]})")

    sn = SpectralNormLinear(32, 16)
    out_sn = sn.forward(x)
    U, S, Vt = np.linalg.svd(sn.W_bar, full_matrices=False)
    print(f"\nSpectralNorm Linear: input (4,32) -> output {out_sn.shape}")
    print(f"  Spectral norm (max singular value) = {S[0]:.4f} (~1.0)")

    print("\nAll normalization alternatives implemented.")
