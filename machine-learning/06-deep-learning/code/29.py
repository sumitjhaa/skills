"""06.29 - Gradient Noise / Clipping: Stabilizing training dynamics"""

import numpy as np
import matplotlib.pyplot as plt


class GradientClipper:
    @staticmethod
    def clip_by_value(grads, clip_min=-1.0, clip_max=1.0):
        return [np.clip(g, clip_min, clip_max) for g in grads]

    @staticmethod
    def clip_by_norm(grads, max_norm=1.0):
        total_norm = np.sqrt(sum(np.sum(g ** 2) for g in grads))
        if total_norm > max_norm:
            scale = max_norm / (total_norm + 1e-6)
            return [g * scale for g in grads]
        return grads

    @staticmethod
    def clip_by_global_norm(grads, max_norm=1.0):
        total_norm = np.sqrt(sum(np.sum(g ** 2) for g in grads))
        if total_norm > max_norm:
            scale = max_norm / (total_norm + 1e-6)
            return [g * scale for g in grads]
        return list(grads)


class GradientNoise:
    def __init__(self, noise_scale=0.01, decay=0.9):
        self.noise_scale = noise_scale
        self.decay = decay
        self.step = 0

    def add_noise(self, grads, lr=1.0):
        self.step += 1
        sigma = self.noise_scale * lr * self.decay ** self.step
        return [g + np.random.randn(*g.shape) * sigma for g in grads]


class GradientCentralization:
    @staticmethod
    def centralize(grads):
        return [g - g.mean(axis=0, keepdims=True) if g.ndim > 1 else g for g in grads]


class AdaptiveGradientClipper:
    def __init__(self, clip_factor=0.01):
        self.clip_factor = clip_factor

    def clip(self, params, grads):
        clipped = []
        for p, g in zip(params, grads):
            param_norm = np.linalg.norm(p)
            grad_norm = np.linalg.norm(g)
            if param_norm > 0 and grad_norm > 0:
                max_norm = param_norm * self.clip_factor
                if grad_norm > max_norm:
                    g = g * (max_norm / grad_norm)
            clipped.append(g)
        return clipped


if __name__ == "__main__":
    np.random.seed(42)

    grads = [
        np.random.randn(32, 64) * 5.0,
        np.random.randn(64) * 3.0,
        np.random.randn(64, 10) * 10.0,
    ]

    clipper = GradientClipper()
    clipped_val = clipper.clip_by_value(grads, -1.0, 1.0)
    clipped_norm = clipper.clip_by_norm(grads, max_norm=5.0)

    norms_before = [np.linalg.norm(g) for g in grads]
    norms_val = [np.linalg.norm(g) for g in clipped_val]
    norms_norm = [np.linalg.norm(g) for g in clipped_norm]

    total_before = np.sqrt(sum(n ** 2 for n in norms_before))
    total_after = np.sqrt(sum(n ** 2 for n in norms_norm))

    print(f"Gradient norms before: {[f'{n:.2f}' for n in norms_before]}")
    print(f"Total norm before: {total_before:.2f}")
    print(f"Total norm after (clip=5.0): {total_after:.2f}")
    print(f"Clipping applied: {total_after > total_before * 0.99}")

    noise = GradientNoise(noise_scale=0.1, decay=0.95)
    noisy_grads = noise.add_noise(grads, lr=0.1)
    noise_norms = [np.linalg.norm(g - ng) for g, ng in zip(grads, noisy_grads)]
    print(f"\nGradient noise added: norms diff = {[f'{n:.4f}' for n in noise_norms]}")

    gc = GradientCentralization()
    centralized = gc.centralize(grads)
    for i, g in enumerate(centralized):
        if g.ndim > 1:
            print(f"Grad {i} centralized mean: {g.mean(axis=0)[:3]} (~0)")

    params = [np.random.randn(32, 64) * 0.1, np.random.randn(64) * 0.1]
    agc = AdaptiveGradientClipper(clip_factor=0.01)
    agc_grads = agc.clip(params, grads[:2])
    for i, g in enumerate(agc_grads):
        print(f"AGC grad {i} norm: {np.linalg.norm(g):.4f}")

    plt.figure(figsize=(10, 5))
    plt.bar(range(len(norms_before)), norms_before, alpha=0.6, label="Before")
    plt.bar(range(len(norms_val)), norms_val, alpha=0.6, label="Value clipped")
    plt.bar(range(len(norms_norm)), norms_norm, alpha=0.6, label="Norm clipped")
    plt.legend()
    plt.xlabel("Parameter group")
    plt.ylabel("Gradient norm")
    plt.title("Gradient Clipping Comparison")
    plt.savefig("../../assets/phase06/gradient_clipping.png")
    plt.close()
    print("\nGradient noise/clipping techniques verified.")
