"""06.08 - Initialization Methods: Xavier, He, Orthogonal, LeCun"""

import numpy as np
import matplotlib.pyplot as plt


def xavier_uniform(fan_in, fan_out):
    limit = np.sqrt(6 / (fan_in + fan_out))
    return np.random.uniform(-limit, limit, (fan_in, fan_out))

def xavier_normal(fan_in, fan_out):
    std = np.sqrt(2 / (fan_in + fan_out))
    return np.random.randn(fan_in, fan_out) * std

def he_uniform(fan_in, fan_out):
    limit = np.sqrt(6 / fan_in)
    return np.random.uniform(-limit, limit, (fan_in, fan_out))

def he_normal(fan_in, fan_out):
    std = np.sqrt(2 / fan_in)
    return np.random.randn(fan_in, fan_out) * std

def orthogonal(fan_in, fan_out):
    W = np.random.randn(fan_in, fan_out)
    U, _, Vt = np.linalg.svd(W, full_matrices=False)
    W_orth = U if W.shape[0] <= W.shape[1] else Vt.T
    return W_orth[:fan_in, :fan_out] if W_orth.shape != (fan_in, fan_out) else W_orth

def lecun_normal(fan_in, fan_out):
    std = np.sqrt(1 / fan_in)
    return np.random.randn(fan_in, fan_out) * std


def forward_propagation(fan_in, fan_out, init_fn, n_layers=10, n_samples=1000):
    x = np.random.randn(n_samples, fan_in)
    activations = [x]
    for _ in range(n_layers):
        W = init_fn(activations[-1].shape[1], fan_out)
        x = np.maximum(0, x @ W)
        activations.append(x)
        if x.shape[1] != fan_out:
            break
    return np.array([a.mean() for a in activations]), np.array([a.std() for a in activations])


if __name__ == "__main__":
    init_methods = {
        "Xavier Uniform": lambda fi, fo: xavier_uniform(fi, fo),
        "Xavier Normal": lambda fi, fo: xavier_normal(fi, fo),
        "He Uniform": lambda fi, fo: he_uniform(fi, fo),
        "He Normal": lambda fi, fo: he_normal(fi, fo),
        "Orthogonal": lambda fi, fo: orthogonal(fi, fo),
        "LeCun Normal": lambda fi, fo: lecun_normal(fi, fo),
    }

    fan_in, fan_out = 128, 128
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    for idx, (name, init_fn) in enumerate(init_methods.items()):
        W = init_fn(fan_in, fan_out)
        means, stds = forward_propagation(fan_in, fan_out, init_fn, n_layers=15, n_samples=2000)

        ax = axes[idx]
        ax.hist(W.flatten(), bins=50, alpha=0.7, density=True)
        ax.set_title(f"{name}\nstd={W.std():.3f}")
        ax.set_xlabel("Weight value")
        ax.set_ylabel("Density")

        print(f"{name:20s}: weight std={W.std():.4f}, "
              f"final act mean={means[-1]:.4f}, std={stds[-1]:.4f}")

    plt.tight_layout()
    plt.savefig("../../assets/phase06/initialization.png")
    plt.close()
    print("\nAll initialization methods validated.")
