"""03.20 ANOVA: One-way ANOVA with F-test and multiple comparisons."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import f_oneway, f as f_dist, tukey_hsd

np.random.seed(42)
k = 4
n_per_group = 25
group_means = [0, 0.5, 1.5, 3.0]
sigma = 1.0

data = [np.random.normal(m, sigma, n_per_group) for m in group_means]
all_data = np.concatenate(data)
group_labels = np.repeat(range(k), n_per_group)

grand_mean = np.mean(all_data)
group_means_obs = [np.mean(g) for g in data]

SSB = sum(n_per_group * (gm - grand_mean)**2 for gm in group_means_obs)
SSW = sum(np.sum((g - gm)**2) for g, gm in zip(data, group_means_obs))
SST = np.sum((all_data - grand_mean)**2)

dfb = k - 1
dfw = len(all_data) - k
MSB = SSB / dfb
MSW = SSW / dfw
F_stat = MSB / MSW
p_val = 1 - f_dist.cdf(F_stat, dfb, dfw)

eta_sq = SSB / SST
omega_sq = (SSB - dfb * MSW) / (SST + MSW)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

bp = axes[0, 0].boxplot(data, labels=[f"Group {i+1}\n(μ={group_means[i]})" for i in range(k)],
                         patch_artist=True)
colors_box = plt.cm.viridis(np.linspace(0.2, 0.8, k))
for patch, color in zip(bp['boxes'], colors_box):
    patch.set_facecolor(color)
positions = np.repeat(range(k), n_per_group)
jitter = np.random.normal(0, 0.05, len(all_data))
axes[0, 0].scatter(positions + jitter, all_data, alpha=0.4, s=15, color='black', zorder=5)
axes[0, 0].axhline(grand_mean, color='r', linestyle='--', lw=2, label=f"Grand mean = {grand_mean:.2f}")
axes[0, 0].set_ylabel("Value")
axes[0, 0].set_title(f"One-Way ANOVA: F={F_stat:.2f}, p={p_val:.6f}")
axes[0, 0].legend(fontsize=8)
axes[0, 0].grid(True, axis='y', alpha=0.3)

group_vars = [np.var(g, ddof=1) for g in data]
axes[0, 1].bar(range(k), group_means_obs, color=colors_box, alpha=0.7, yerr=group_vars,
               capsize=5, label="Group means ± var")
axes[0, 1].axhline(grand_mean, color='r', ls='--', label=f"Grand mean = {grand_mean:.2f}")
axes[0, 1].set_xticks(range(k))
axes[0, 1].set_xticklabels([f"G{i+1}" for i in range(k)])
axes[0, 1].set_ylabel("Mean")
axes[0, 1].set_title("Group Means with Variance")
axes[0, 1].legend(fontsize=8)
axes[0, 1].grid(True, axis='y', alpha=0.3)

f_dist_plot = np.linspace(0, 5, 200)
f_pdf = f_dist.pdf(f_dist_plot, dfb, dfw)
axes[0, 2].plot(f_dist_plot, f_pdf, 'b-', lw=2, label=f"F({dfb},{dfw})")
axes[0, 2].fill_between(f_dist_plot, 0, f_pdf,
                         where=(f_dist_plot >= F_stat), alpha=0.3, color='red')
axes[0, 2].axvline(F_stat, color='r', lw=2, ls='--', label=f"F={F_stat:.2f}")
crit_val = f_dist.ppf(0.95, dfb, dfw)
axes[0, 2].axvline(crit_val, color='g', lw=2, ls=':', label=f"F*={crit_val:.2f}")
axes[0, 2].set_xlabel("F-statistic")
axes[0, 2].set_ylabel("Density")
axes[0, 2].set_title("F-Distribution and Observed F")
axes[0, 2].legend(fontsize=8)
axes[0, 2].grid(True, alpha=0.3)

residuals_group = [g - gm for g, gm in zip(data, group_means_obs)]
all_residuals = np.concatenate(residuals_group)
ax = axes[1, 0]
for i in range(k):
    ax.scatter(np.ones(n_per_group) * i, residuals_group[i], alpha=0.6, s=15,
              color=colors_box[i])
ax.axhline(0, color='k', lw=1)
ax.set_xticks(range(k))
ax.set_xticklabels([f"G{i+1}" for i in range(k)])
ax.set_xlabel("Group")
ax.set_ylabel("Residuals")
ax.set_title("Residuals by Group")
ax.grid(True, alpha=0.3)

ax2 = axes[1, 1]
ax2.hist(all_residuals, bins=20, density=True, alpha=0.6, color='steelblue')
x_r = np.linspace(-3, 3, 200)
ax2.plot(x_r, 1/np.sqrt(2*np.pi)*np.exp(-x_r**2/2), 'r-', lw=2, label="N(0,1)")
ax2.set_xlabel("Residual")
ax2.set_ylabel("Density")
ax2.set_title("Residual Distribution")
ax2.legend()
ax2.grid(True, alpha=0.3)

from scipy.stats import probplot
probplot(all_residuals, dist="norm", plot=axes[1, 2])
axes[1, 2].set_title("Q-Q Plot of Residuals")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/20-anova.png")
plt.close()

print("=" * 60)
print("ONE-WAY ANOVA RESULTS")
print("=" * 60)
print(f"\n{'Source':<12s} {'SS':>8s} {'df':>4s} {'MS':>8s} {'F':>8s} {'p':>8s}")
print("-" * 52)
print(f"{'Between':<12s} {SSB:>8.3f} {dfb:>4d} {MSB:>8.3f} {F_stat:>8.3f} {p_val:>8.5f}")
print(f"{'Within':<12s} {SSW:>8.3f} {dfw:>4d} {MSW:>8.3f}")
print(f"{'Total':<12s} {SST:>8.3f} {dfb+dfw:>4d}")
print(f"\nSST = SSB + SSW: {np.isclose(SST, SSB+SSW)}")
print(f"Eta-squared (η²): {eta_sq:.4f} ({eta_sq*100:.1f}% variance explained)")
print(f"Omega-squared (ω²): {omega_sq:.4f}")

print(f"\nGroup means:")
for i, gm in enumerate(group_means_obs):
    print(f"  Group {i+1}: observed={gm:.3f}, true={group_means[i]:.3f}")

print(f"\nPairwise comparisons:")
from itertools import combinations
for i, j in combinations(range(k), 2):
    diff = group_means_obs[i] - group_means_obs[j]
    se_diff = np.sqrt(MSW * (1/n_per_group + 1/n_per_group))
    t_stat = diff / se_diff
    p_pair = 2 * (1 - f_dist.cdf(t_stat**2, 1, dfw))
    print(f"  G{i+1} - G{j+1}: diff={diff:.3f}, SE={se_diff:.3f}, t={t_stat:.3f}, p={p_pair:.4f}")

print(f"\nANOVA assumptions:")
print(f"  Homogeneity of variance (max/min = {max(group_vars)/min(group_vars):.2f})")
print("  (Rule of thumb: ratio < 3 is acceptable)")
