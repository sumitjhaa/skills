"""
07.10 Capsule Networks: Dynamic routing between capsules with visualization.
"""
import numpy as np
import matplotlib.pyplot as plt

def squash(v):
    norm = np.linalg.norm(v, axis=-1, keepdims=True)
    return (norm ** 2 / (1 + norm ** 2)) * (v / (norm + 1e-8))

class CapsuleLayer:
    def __init__(self, in_caps, in_dim, out_caps, out_dim, num_routing=3):
        self.in_caps = in_caps
        self.in_dim = in_dim
        self.out_caps = out_caps
        self.out_dim = out_dim
        self.num_routing = num_routing
        self.W = np.random.randn(in_caps, out_caps, out_dim, in_dim) * 0.1

    def forward(self, u):
        batch = u.shape[0]
        u_exp = u[:, :, np.newaxis, np.newaxis, :]
        W_exp = self.W[np.newaxis, :, :, :, :]
        u_hat = np.sum(u_exp * W_exp, axis=-1)
        b = np.zeros((batch, self.in_caps, self.out_caps))
        routing_log = []
        for r in range(self.num_routing):
            c = np.exp(b) / np.sum(np.exp(b), axis=-1, keepdims=True)
            s = np.sum(u_hat * c[:, :, :, np.newaxis], axis=1)
            v = squash(s)
            routing_log.append(np.linalg.norm(v, axis=-1).mean(axis=0))
            if r < self.num_routing - 1:
                v_exp = v[:, np.newaxis, :, :]
                b += np.sum(u_hat * v_exp, axis=-1)
        return v, np.array(routing_log)

def test_capsule_forward():
    np.random.seed(42)
    layer = CapsuleLayer(in_caps=8, in_dim=16, out_caps=4, out_dim=8)
    batch = 32
    u = np.random.randn(batch, 8, 16)
    v, route_log = layer.forward(u)
    norms = np.linalg.norm(v, axis=-1)

    assert v.shape == (batch, 4, 8), f"Expected (32,4,8), got {v.shape}"
    assert np.all(norms <= 1.0), "Squash should keep norms <= 1"
    assert np.all(norms >= 0), "Norms should be non-negative"

    return v, route_log

def compare_routing_iterations():
    np.random.seed(42)
    batch = 16
    u = np.random.randn(batch, 8, 16)
    results = []
    for n_routing in [1, 2, 3, 5]:
        layer = CapsuleLayer(in_caps=8, in_dim=16, out_caps=4, out_dim=8,
                             num_routing=n_routing)
        v, _ = layer.forward(u)
        results.append((n_routing, v))
    return results

if __name__ == "__main__":
    np.random.seed(42)
    print("=== Capsule Networks ===\n")

    v, route_log = test_capsule_forward()
    print(f"Input:  (32, 8, 16)")
    print(f"Output: {v.shape}")
    print(f"Output capsule norms: {np.linalg.norm(v, axis=-1).mean(axis=0)}")

    # Routing iterations analysis
    print("\n=== Routing Iteration Comparison ===")
    results = compare_routing_iterations()
    for n_r, vr in results:
        norms_r = np.linalg.norm(vr, axis=-1)
        print(f"  Routing={n_r}: mean norm={norms_r.mean():.4f}, "
              f"max norm={norms_r.max():.4f}")

    # Weight visualization
    layer = CapsuleLayer(in_caps=8, in_dim=16, out_caps=4, out_dim=8)
    fig, axes = plt.subplots(2, 3, figsize=(14, 10))

    # Weight matrix overview
    im = axes[0, 0].imshow(layer.W.reshape(-1, layer.out_dim), aspect='auto', cmap='RdBu')
    axes[0, 0].set_xlabel("Output dimension")
    axes[0, 0].set_ylabel("Weight index (in_caps * out_caps)")
    axes[0, 0].set_title("Capsule Weight Matrix W")
    plt.colorbar(im, ax=axes[0, 0])

    # Routing evolution
    _, route_log_full = CapsuleLayer(8, 16, 4, 8, num_routing=5).forward(
        np.random.randn(32, 8, 16))
    for r in range(route_log_full.shape[0]):
        axes[0, 1].bar(np.arange(4) + r * 0.15, route_log_full[r],
                       width=0.15, label=f'Routing {r + 1}')
    axes[0, 1].set_xlabel("Output capsule")
    axes[0, 1].set_ylabel("Mean norm")
    axes[0, 1].set_title("Capsule Norms Across Routing Iterations")
    axes[0, 1].legend()
    axes[0, 1].grid(True, axis='y', alpha=0.3)

    # Routing weights (coupling coefficients) for one input
    layer_small = CapsuleLayer(8, 16, 4, 8, num_routing=3)
    u_one = np.random.randn(1, 8, 16)
    v_one, _ = layer_small.forward(u_one)
    axes[0, 2].bar(range(4), np.linalg.norm(v_one[0], axis=-1))
    axes[0, 2].set_xlabel("Output capsule")
    axes[0, 2].set_ylabel("Output norm")
    axes[0, 2].set_title("Single Input Capsule Output Norms")
    axes[0, 2].grid(True, axis='y', alpha=0.3)

    # Routing iterations vs norm spread
    for n_r in [1, 2, 3, 5]:
        layer_n = CapsuleLayer(8, 16, 4, 8, num_routing=n_r)
        v_n, _ = layer_n.forward(np.random.randn(32, 8, 16))
        norms_n = np.linalg.norm(v_n, axis=-1)
        axes[1, 0].plot(range(4), norms_n.mean(axis=0), 'o-', label=f'R={n_r}')
    axes[1, 0].set_xlabel("Output capsule")
    axes[1, 0].set_ylabel("Mean norm")
    axes[1, 0].set_title("Effect of Routing Iterations")
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # Capsule vector directions (first 2 dims)
    for i in range(4):
        axes[1, 1].quiver(0, 0, v_one[0, i, 0], v_one[0, i, 1],
                          angles='xy', scale_units='xy', scale=1,
                          label=f'Capsule {i}')
    axes[1, 1].set_xlim(-1, 1); axes[1, 1].set_ylim(-1, 1)
    axes[1, 1].set_aspect('equal')
    axes[1, 1].set_title("Capsule Vector Directions (2D)")
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    # Norm histogram
    axes[1, 2].hist(np.linalg.norm(v, axis=-1).ravel(), bins=20, alpha=0.7)
    axes[1, 2].set_xlabel("Capsule norm")
    axes[1, 2].set_ylabel("Count")
    axes[1, 2].set_title("Distribution of Capsule Norms")
    axes[1, 2].grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig("../../assets/phase07/10-capsule-networks.png")
    plt.close()
    print("\nFigure saved to 10-capsule-networks.png")

    # Edge cases
    print("\n=== Edge Cases ===")
    layer_zero = CapsuleLayer(4, 8, 2, 4, num_routing=1)
    u_zero = np.zeros((2, 4, 8))
    v_zero, _ = layer_zero.forward(u_zero)
    print(f"  Zero input: output norms={np.linalg.norm(v_zero, axis=-1).mean():.4f}")

    layer_large = CapsuleLayer(2, 4, 10, 8, num_routing=2)
    u_large = np.random.randn(1, 2, 4)
    v_large, _ = layer_large.forward(u_large)
    print(f"  More outputs than inputs: {v_large.shape}, norms={np.linalg.norm(v_large[0], axis=-1)[:5]}")

    # Routing weight convergence
    print(f"  Routing iterations: norm spread increases from "
          f"{route_log_full[0].std():.4f} to {route_log_full[-1].std():.4f}")
