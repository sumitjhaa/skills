"""
09.13 Pruning — Magnitude Pruning & Wanda-Style with analysis.
"""
import numpy as np
import matplotlib.pyplot as plt

class MagnitudePruner:
    def __call__(self, weights, sparsity=0.5):
        mask = np.ones_like(weights, dtype=np.float32)
        thresh = np.percentile(np.abs(weights), sparsity * 100)
        mask[np.abs(weights) < thresh] = 0.0
        return weights * mask, mask

class WandaPruner:
    def __call__(self, weights, inputs, sparsity=0.5):
        act_norms = np.linalg.norm(inputs, axis=0)
        importance = np.abs(weights) * act_norms[None, :]
        mask = np.ones_like(weights, dtype=np.float32)
        for i in range(weights.shape[0]):
            thresh = np.percentile(importance[i], sparsity * 100)
            mask[i, importance[i] < thresh] = 0.0
        return weights * mask, mask

class RandomPruner:
    def __call__(self, weights, sparsity=0.5):
        mask = np.ones_like(weights, dtype=np.float32)
        n_prune = int(weights.size * sparsity)
        idx = np.random.choice(weights.size, n_prune, replace=False)
        mask.ravel()[idx] = 0.0
        return weights * mask, mask

def evaluate_pruning(weights, inputs, targets, pruner, sparsity):
    if isinstance(pruner, WandaPruner):
        pruned_w, mask = pruner(weights, inputs, sparsity)
    else:
        pruned_w, mask = pruner(weights, sparsity)
    error = np.mean((inputs @ pruned_w.T - targets) ** 2)
    actual_sparsity = 1.0 - np.count_nonzero(mask) / mask.size
    return error, actual_sparsity, mask

def layerwise_sparsity_profile(weights, sparsity=0.5):
    profiles = {}
    for name, w in weights.items():
        mag = MagnitudePruner()
        _, mask = mag(w, sparsity)
        sp = 1.0 - np.count_nonzero(mask) / mask.size
        profiles[name] = sp
    return profiles

if __name__ == "__main__":
    np.random.seed(42)
    print("=== Network Pruning ===\n")

    d_out, d_in = 32, 64
    weights = np.random.randn(d_out, d_in) * 0.5
    inputs = np.random.randn(200, d_in)
    targets = inputs @ weights.T + 0.1 * np.random.randn(200, d_out)

    magnitude_pruner = MagnitudePruner()
    wanda_pruner = WandaPruner()
    random_pruner = RandomPruner()

    # Sparsity sweep
    sparsities = [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99]
    results = {'magnitude': [], 'wanda': [], 'random': []}

    for sparsity in sparsities:
        err_mag, actual_mag, _ = evaluate_pruning(
            weights, inputs, targets, magnitude_pruner, sparsity)
        err_wanda, actual_wanda, _ = evaluate_pruning(
            weights, inputs, targets, wanda_pruner, sparsity)
        err_rand, actual_rand, _ = evaluate_pruning(
            weights, inputs, targets, random_pruner, sparsity)
        results['magnitude'].append((actual_mag, err_mag))
        results['wanda'].append((actual_wanda, err_wanda))
        results['random'].append((actual_rand, err_rand))

        print(f"Sparsity {sparsity:.0%}: "
              f"Mag MSE={err_mag:.4f}, Wanda MSE={err_wanda:.4f}, "
              f"Random MSE={err_rand:.4f}")

    # Weight distribution
    print(f"\nWeight stats:")
    print(f"  Mean={weights.mean():.4f}, Std={weights.std():.4f}")
    print(f"  Min={weights.min():.4f}, Max={weights.max():.4f}")

    # Layer-wise analysis
    print("\nLayer-wise pruning profile:")
    layer_weights = {
        'layer1': np.random.randn(64, 128) * 0.3,
        'layer2': np.random.randn(32, 64) * 0.5,
        'layer3': np.random.randn(16, 32) * 0.7,
    }
    for sp in [0.3, 0.5, 0.7]:
        prof = layerwise_sparsity_profile(layer_weights, sp)
        print(f"  Target {sp:.0%}: "
              f"{', '.join(f'{k}={v:.1%}' for k, v in prof.items())}")

    # Output error analysis
    w_mag, mask_mag = magnitude_pruner(weights, 0.7)
    w_wanda, mask_wanda = wanda_pruner(weights, inputs, 0.7)
    diff_mag = (w_mag - weights).ravel()
    diff_wanda = (w_wanda - weights).ravel()
    print(f"\nPruning error distribution (sparsity=70%):")
    print(f"  Magnitude: mean={diff_mag.mean():.4f}, std={diff_mag.std():.4f}")
    print(f"  Wanda:     mean={diff_wanda.mean():.4f}, std={diff_wanda.std():.4f}")

    # Seed the random pruner for reproducibility
    np.random.seed(42)

    # Visualization
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # MSE vs sparsity
    for label, color, marker in [('magnitude', 'C0', 'o'),
                                  ('wanda', 'C1', 's'),
                                  ('random', 'C2', '^')]:
        sp_vals = [r[0] for r in results[label]]
        mse_vals = [r[1] for r in results[label]]
        axes[0, 0].semilogy(sp_vals, mse_vals, f'{marker}-',
                            color=color, label=label, lw=2)
    axes[0, 0].axvline(0.7, color='gray', ls='--', alpha=0.5, label='70% sparsity')
    axes[0, 0].set_xlabel("Actual sparsity")
    axes[0, 0].set_ylabel("MSE")
    axes[0, 0].set_title("Pruning: Sparsity vs Error")
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Weight distribution before/after
    axes[0, 1].hist(weights.ravel(), bins=40, alpha=0.5, label='Original')
    axes[0, 1].hist(w_mag.ravel(), bins=40, alpha=0.5, label='Magnitude-pruned')
    axes[0, 1].set_xlabel("Weight value")
    axes[0, 1].set_ylabel("Count")
    axes[0, 1].set_title("Weight Distribution (70% sparsity)")
    axes[0, 1].legend()
    axes[0, 1].grid(True, axis='y', alpha=0.3)

    # Importance score heatmap
    wanda_importance = np.abs(weights) * np.linalg.norm(inputs, axis=0)[None, :]
    im = axes[0, 2].imshow(wanda_importance[:8, :16], aspect='auto', cmap='hot')
    axes[0, 2].set_xlabel("Input dimension")
    axes[0, 2].set_ylabel("Output dimension")
    axes[0, 2].set_title("Wanda Importance Scores (subset)")
    plt.colorbar(im, ax=axes[0, 2])

    # Pruning mask visualization
    axes[1, 0].imshow(mask_mag[:8, :16], cmap='gray', aspect='auto')
    axes[1, 0].set_title(f"Magnitude Mask (live={mask_mag.mean():.1%})")
    axes[1, 0].set_xlabel("Input"); axes[1, 0].set_ylabel("Output")

    axes[1, 1].imshow(mask_wanda[:8, :16], cmap='gray', aspect='auto')
    axes[1, 1].set_title(f"Wanda Mask (live={mask_wanda.mean():.1%})")
    axes[1, 1].set_xlabel("Input"); axes[1, 1].set_ylabel("Output")

    # Per-row sparsity
    row_sparsity_mag = 1.0 - mask_mag.mean(axis=1)
    row_sparsity_wanda = 1.0 - mask_wanda.mean(axis=1)
    axes[1, 2].hist(row_sparsity_mag, bins=15, alpha=0.5, label='Magnitude')
    axes[1, 2].hist(row_sparsity_wanda, bins=15, alpha=0.5, label='Wanda')
    axes[1, 2].set_xlabel("Per-output sparsity")
    axes[1, 2].set_ylabel("Count")
    axes[1, 2].set_title("Sparsity Distribution Across Outputs")
    axes[1, 2].legend()
    axes[1, 2].grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig("../../assets/phase09/pruning.png")
    plt.close()
    print("\nFigure saved to pruning.png")

    # Edge cases
    print("\n=== Edge Cases ===")
    w_small = np.array([[0.0, 1.0], [0.01, 100.0]])
    i_small = np.random.randn(10, 2)
    mag = MagnitudePruner()
    wanda = WandaPruner()
    w_sm, m_sm = mag(w_small, 0.5)
    w_sw, m_sw = wanda(w_small, i_small, 0.5)
    print(f"  Small matrix mag mask: {m_sm}")
    print(f"  Small matrix wanda mask: {m_sw}")

    w_zero = np.zeros((4, 8))
    w_z, m_z = mag(w_zero, 0.5)
    print(f"  Zero weights mask: unique={np.unique(m_z)}")

    np.random.seed(42)
    w_uniform = np.ones((5, 5)) * 0.5
    w_u, m_u = mag(w_uniform, 0.3)
    print(f"  Uniform weights: sparsity={1.0 - m_u.mean():.1%}")
