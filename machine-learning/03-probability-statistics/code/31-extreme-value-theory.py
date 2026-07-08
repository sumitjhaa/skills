"""03.31 Extreme Value Theory: GEV fitting and return level plot."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import genextreme as gev, norm

np.random.seed(42)
n_blocks = 1000
block_size = 100

data = np.random.standard_t(df=3, size=(n_blocks, block_size))
block_max = np.max(data, axis=1)

params = gev.fit(block_max)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

x_gev = np.linspace(block_max.min() - 1, block_max.max() + 1, 200)
axes[0, 0].hist(block_max, bins=50, density=True, alpha=0.6, color='steelblue', edgecolor='white')
axes[0, 0].plot(x_gev, gev.pdf(x_gev, *params), 'r-', lw=2, label="GEV fit")
axes[0, 0].set_xlabel("Block maximum")
axes[0, 0].set_ylabel("Density")
axes[0, 0].set_title(f"GEV Fit to Block Maxima\nξ={params[0]:.3f}, μ={params[1]:.3f}, σ={params[2]:.3f}")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

return_periods = np.array([2, 5, 10, 20, 50, 100, 200, 500, 1000])
return_levels = gev.ppf(1 - 1/return_periods, *params)
empirical_levels = [np.percentile(block_max, 100 * (1 - 1/rp)) for rp in return_periods]

axes[0, 1].semilogx(return_periods, return_levels, 'o-', lw=2, markersize=6, label="GEV fit")
axes[0, 1].semilogx(return_periods[:5], empirical_levels[:5], 's--', lw=1, markersize=6,
                    label="Empirical", color='green')
axes[0, 1].set_xlabel("Return period")
axes[0, 1].set_ylabel("Return level")
axes[0, 1].set_title("Return Level Plot")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

block_sizes = [50, 100, 200, 500]
gev_shapes = []
for bs in block_sizes:
    block_max_bs = np.max(np.random.standard_t(df=3, size=(200, bs)), axis=1)
    p_bs = gev.fit(block_max_bs)
    gev_shapes.append(p_bs[0])

axes[0, 2].plot(block_sizes, gev_shapes, 'o-', lw=2)
axes[0, 2].axhline(1/3, color='r', ls='--', label=f"True ξ (t(3) = {1/3:.3f})")
axes[0, 2].set_xlabel("Block size")
axes[0, 2].set_ylabel("Estimated ξ (shape)")
axes[0, 2].set_title("GEV Shape Parameter vs Block Size")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

n_bootstrap = 500
bootstrap_params = np.zeros((n_bootstrap, 3))
for b in range(n_bootstrap):
    boot_sample = np.random.choice(block_max, n_blocks, replace=True)
    try:
        bootstrap_params[b] = gev.fit(boot_sample)
    except Exception:
        bootstrap_params[b] = params

axes[1, 0].hist(bootstrap_params[:, 0], bins=30, density=True, alpha=0.6, color='coral', edgecolor='white')
axes[1, 0].axvline(params[0], color='r', lw=2, ls='--', label=f"ξ={params[0]:.3f}")
axes[1, 0].set_xlabel("ξ")
axes[1, 0].set_ylabel("Density")
axes[1, 0].set_title(f"Bootstrap Distribution of ξ\nSE={np.std(bootstrap_params[:, 0]):.4f}")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].hist(bootstrap_params[:, 1], bins=30, density=True, alpha=0.6, color='steelblue', edgecolor='white')
axes[1, 1].axvline(params[1], color='r', lw=2, ls='--', label=f"μ={params[1]:.3f}")
axes[1, 1].set_xlabel("μ")
axes[1, 1].set_ylabel("Density")
axes[1, 1].set_title(f"Bootstrap Distribution of μ\nSE={np.std(bootstrap_params[:, 1]):.4f}")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

axes[1, 2].hist(bootstrap_params[:, 2], bins=30, density=True, alpha=0.6, color='green', edgecolor='white')
axes[1, 2].axvline(params[2], color='r', lw=2, ls='--', label=f"σ={params[2]:.3f}")
axes[1, 2].set_xlabel("σ")
axes[1, 2].set_ylabel("Density")
axes[1, 2].set_title(f"Bootstrap Distribution of σ\nSE={np.std(bootstrap_params[:, 2]):.4f}")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/31-extreme-value-theory.png")
plt.close()

print("=" * 60)
print("EXTREME VALUE THEORY: GEV ANALYSIS")
print("=" * 60)
print(f"\nData: t-distribution (df=3), {n_blocks} blocks of size {block_size}")
print(f"\nGEV fit parameters:")
print(f"  Shape (ξ) = {params[0]:.4f}  {'⇒ Fréchet type' if params[0] > 0 else '⇒ Weibull type' if params[0] < 0 else '⇒ Gumbel type'}")
print(f"  Location = {params[1]:.4f}")
print(f"  Scale = {params[2]:.4f}")
print(f"  For t(3), ξ should be ≈ 1/3 = {1/3:.4f} (Fréchet)")

print(f"\nReturn levels:")
print(f"{'Return Period':>15s} {'Return Level':>15s} {'Empirical':>15s}")
print("-" * 45)
for rp, rl, el in zip(return_periods, return_levels, empirical_levels):
    print(f"{rp:>10d}-year {rl:>15.3f} {el:>15.3f}")

print(f"\nBootstrap SE:")
print(f"  ξ: {np.std(bootstrap_params[:, 0]):.4f}")
print(f"  μ: {np.std(bootstrap_params[:, 1]):.4f}")
print(f"  σ: {np.std(bootstrap_params[:, 2]):.4f}")

print(f"\nThe three types of extreme value distributions:")
print(f"  ξ > 0: Fréchet (heavy tail, e.g., t, Pareto)")
print(f"  ξ = 0: Gumbel (exponential tail, e.g., normal, exp)")
print(f"  ξ < 0: Weibull (bounded tail, e.g., uniform, beta)")
