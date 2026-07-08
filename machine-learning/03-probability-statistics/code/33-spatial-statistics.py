"""03.33 Spatial Statistics: Variogram and Kriging for 1D spatial data."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform

np.random.seed(42)
n_locs = 50
locs = np.random.uniform(0, 10, n_locs)

sigma2, phi = 1.0, 2.0
dist = np.abs(locs[:, None] - locs[None, :])
C = sigma2 * np.exp(-dist / phi) + 1e-6 * np.eye(n_locs)
z = np.random.multivariate_normal(np.zeros(n_locs), C)

pairs = [(i, j) for i in range(n_locs) for j in range(i+1, n_locs)]
dists_pairs = [dist[i, j] for i, j in pairs]
gammas = [0.5 * (z[i] - z[j])**2 for i, j in pairs]

bins = np.linspace(0, 10, 20)
bin_centers = (bins[:-1] + bins[1:]) / 2
bin_means = []
for k in range(len(bins)-1):
    mask = [(d >= bins[k]) & (d < bins[k+1]) for d in dists_pairs]
    vals = [g for g, m in zip(gammas, mask) if m]
    bin_means.append(np.mean(vals) if vals else np.nan)

x_vario = np.linspace(0, 10, 200)
true_vario = sigma2 * (1 - np.exp(-x_vario / phi))

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].scatter(locs, z, c='k', s=30)
axes[0, 0].set_xlabel("Location")
axes[0, 0].set_ylabel("z")
axes[0, 0].set_title("Spatial Process")
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].scatter(dists_pairs, gammas, alpha=0.3, s=5, label="Point pairs")
axes[0, 1].plot(bin_centers, bin_means, 'o-', color='r', lw=2, markersize=6, label="Binned")
axes[0, 1].plot(x_vario, true_vario, 'k--', lw=2, label="True (exponential)")
axes[0, 1].set_xlabel("Distance h")
axes[0, 1].set_ylabel("γ(h)")
axes[0, 1].set_title("Variogram")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

n_krig = 20
locs_krig = np.linspace(0.5, 9.5, n_krig)
dist_pred = np.abs(locs[:, None] - locs_krig[None, :])
C_pred = sigma2 * np.exp(-dist_pred / phi) + 1e-6 * np.eye(n_locs, n_krig)
C_obs = sigma2 * np.exp(-dist / phi) + 1e-6 * np.eye(n_locs)
C_krig = sigma2 * np.exp(-np.abs(locs_krig[:, None] - locs_krig[None, :]) / phi) + 1e-6 * np.eye(n_krig)

weights = np.linalg.solve(C_obs, C_pred)
z_pred = weights.T @ z
krig_var = np.diag(C_krig - C_pred.T @ np.linalg.solve(C_obs, C_pred))

axes[0, 2].scatter(locs, z, c='k', s=30, label="Observed")
axes[0, 2].plot(locs_krig, z_pred, 'r-', lw=2, label="Kriging (BLUP)")
axes[0, 2].fill_between(locs_krig, z_pred - 2*np.sqrt(np.maximum(krig_var, 0)),
                         z_pred + 2*np.sqrt(np.maximum(krig_var, 0)),
                         alpha=0.3, color='r', label="95% CI")
axes[0, 2].set_xlabel("Location")
axes[0, 2].set_ylabel("z")
axes[0, 2].set_title("Kriging Predictions (Ordinary Kriging)")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

phi_vals = [0.5, 1.0, 2.0, 5.0]
for phi_i in phi_vals:
    vario_i = sigma2 * (1 - np.exp(-x_vario / phi_i))
    axes[1, 0].plot(x_vario, vario_i, lw=2, label=f"φ={phi_i}")

axes[1, 0].scatter(bin_centers, bin_means, color='k', s=30, zorder=5, label="Empirical")
axes[1, 0].set_xlabel("Distance h")
axes[1, 0].set_ylabel("γ(h)")
axes[1, 0].set_title("Variogram Sensitivity to Range φ")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

np.random.seed(123)
n_small = 15
locs_small = np.sort(np.random.uniform(0, 10, n_small))
dist_small = np.abs(locs_small[:, None] - locs_small[None, :])
C_small = sigma2 * np.exp(-dist_small / phi) + 1e-6 * np.eye(n_small)
z_small = np.random.multivariate_normal(np.zeros(n_small), C_small)
dist_pred_small = np.abs(locs_small[:, None] - locs_krig[None, :])
C_pred_small = sigma2 * np.exp(-dist_pred_small / phi)
weights_small = np.linalg.solve(C_small, C_pred_small)
z_pred_small = weights_small.T @ z_small

axes[1, 1].scatter(locs_small, z_small, c='k', s=50, label="Observed (n=15)")
axes[1, 1].plot(locs_krig, z_pred_small, 'b-', lw=2, label="Kriging")
axes[1, 1].plot(locs_krig, np.zeros_like(locs_krig), 'g--', lw=2, label="True E[z]=0")
axes[1, 1].set_xlabel("Location")
axes[1, 1].set_ylabel("z")
axes[1, 1].set_title("Kriging with Fewer Observations")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

bins_2d = 15
h_grid = np.linspace(0, 10, bins_2d)
counts_2d, _, _ = np.histogram2d(dists_pairs, gammas, bins=[h_grid, np.linspace(0, 2, bins_2d)])
axes[1, 2].imshow(counts_2d.T, origin='lower', aspect='auto',
                  extent=[0, 10, 0, 2], cmap='YlOrRd')
axes[1, 2].plot(x_vario, true_vario, 'b-', lw=2, label="True variogram")
axes[1, 2].set_xlabel("Distance h")
axes[1, 2].set_ylabel("γ(h)")
axes[1, 2].set_title("Variogram Cloud (2D histogram)")
axes[1, 2].legend()
plt.colorbar(axes[1, 2].images[0], ax=axes[1, 2], label="Count")

plt.tight_layout()
plt.savefig("../../assets/phase03/33-spatial-statistics.png")
plt.close()

print("=" * 60)
print("SPATIAL STATISTICS")
print("=" * 60)
print(f"\nData: {n_locs} locations, exponential covariance")
print(f"  Sill σ² = {sigma2}, Range φ = {phi}")
print(f"\nEmpirical variogram shows increasing spatial variance with distance.")
print(f"Kriging provides Best Linear Unbiased Prediction (BLUP).")

rmse = np.sqrt(np.mean((z_pred - 0)**2))
print(f"\nKriging RMSE (prediction of zero-mean process): {rmse:.4f}")
print(f"Average kriging variance: {np.mean(krig_var):.4f}")
