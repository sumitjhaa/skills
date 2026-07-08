"""03.18 Confidence Intervals: Frequentist and Bootstrap."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, t as t_dist

np.random.seed(42)
n = 50
data = np.random.lognormal(mean=0, sigma=0.5, size=n)
log_data = np.log(data)
mu_hat = np.mean(log_data)
se_hat = np.std(log_data, ddof=1) / np.sqrt(n)

ci_normal = (mu_hat - 1.96 * se_hat, mu_hat + 1.96 * se_hat)
ci_t = t_dist.interval(0.95, df=n-1, loc=mu_hat, scale=se_hat)

B = 10000
boot_means = np.zeros(B)
boot_stds = np.zeros(B)
for b in range(B):
    boot_sample = np.random.choice(log_data, n, replace=True)
    boot_means[b] = np.mean(boot_sample)
    boot_stds[b] = np.std(boot_sample, ddof=1)

ci_percentile = np.percentile(boot_means, [2.5, 97.5])
ci_basic = (2 * mu_hat - ci_percentile[1], 2 * mu_hat - ci_percentile[0])
bias = np.mean(boot_means) - mu_hat
ci_bca_adjusted = np.percentile(boot_means, [2.5, 97.5]) - bias

boot_t = np.zeros(B)
for b in range(B):
    boot_sample = np.random.choice(log_data, n, replace=True)
    boot_t[b] = (np.mean(boot_sample) - mu_hat) / (np.std(boot_sample, ddof=1) / np.sqrt(n))
t_crit_upper = np.percentile(boot_t, 97.5)
t_crit_lower = np.percentile(boot_t, 2.5)
ci_bootstrap_t = (mu_hat - t_crit_upper * se_hat, mu_hat - t_crit_lower * se_hat)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes[0, 0].hist(boot_means, bins=60, density=True, alpha=0.6, color='lightblue', edgecolor='white')
for ci, label, color in [
    (ci_normal, "Normal", "blue"),
    (ci_t, "t-dist", "green"),
    (ci_percentile, "Bootstrap\npercentile", "red"),
    (ci_basic, "Bootstrap\nbasic", "purple"),
    (ci_bootstrap_t, "Bootstrap\nt", "orange"),
]:
    y_max = axes[0, 0].get_ylim()[1] * 0.9
    axes[0, 0].plot([ci[0], ci[1]], [y_max, y_max], 'o-', color=color, lw=2, label=label)
    axes[0, 0].axvline(ci[0], color=color, linestyle='--', alpha=0.5)
    axes[0, 0].axvline(ci[1], color=color, linestyle='--', alpha=0.5)
axes[0, 0].axvline(mu_hat, color='k', lw=2, ls='-', label=f"Observed μ̂={mu_hat:.3f}")
axes[0, 0].set_xlabel("Mean (log scale)")
axes[0, 0].set_ylabel("Density")
axes[0, 0].set_title("Confidence Intervals Comparison (n=50)")
axes[0, 0].legend(fontsize=8, loc='upper left')
axes[0, 0].grid(True, alpha=0.3)

ci_types = ["Normal", "t", "Percentile", "Basic", "Bootstrap-t"]
ci_lowers = [ci_normal[0], ci_t[0], ci_percentile[0], ci_basic[0], ci_bootstrap_t[0]]
ci_uppers = [ci_normal[1], ci_t[1], ci_percentile[1], ci_basic[1], ci_bootstrap_t[1]]
ci_widths = [u - l for l, u in zip(ci_lowers, ci_uppers)]
colors_bar = plt.cm.viridis(np.linspace(0.2, 0.8, 5))
axes[0, 1].barh(ci_types, ci_widths, color=colors_bar)
axes[0, 1].set_xlabel("CI Width")
axes[0, 1].set_title("Confidence Interval Width")
axes[0, 1].grid(True, axis='x', alpha=0.3)

ns_sim = [10, 30, 50, 100]
coverages = []
for ni in ns_sim:
    cov_count = 0
    nrep = 500
    for _ in range(nrep):
        d = np.random.lognormal(0, 0.5, ni)
        ld = np.log(d)
        mh = np.mean(ld)
        se = np.std(ld, ddof=1) / np.sqrt(ni)
        ci = t_dist.interval(0.95, df=ni-1, loc=mh, scale=se)
        if ci[0] <= 0 <= ci[1]:
            cov_count += 1
    coverages.append(cov_count / nrep)
    print(f"  n={ni}: t-CI coverage={cov_count/nrep:.3f}")

axes[1, 0].plot(ns_sim, coverages, 'o-', lw=2)
axes[1, 0].axhline(0.95, color='r', ls='--', label="Nominal 95%")
axes[1, 0].set_xlabel("n")
axes[1, 0].set_ylabel("Coverage")
axes[1, 0].set_title("t-CI Coverage vs Sample Size")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].hist(boot_means, bins=40, density=True, alpha=0.5, color='gray', label="Bootstrap means")
x_fit = np.linspace(boot_means.min(), boot_means.max(), 200)
axes[1, 1].plot(x_fit, norm.pdf(x_fit, loc=mu_hat, scale=se_hat), 'r-', lw=2, label="Normal approx")
axes[1, 1].set_xlabel("Mean (log scale)")
axes[1, 1].set_ylabel("Density")
axes[1, 1].set_title("Bootstrap vs Normal Approximation")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/18-confidence-intervals.png")
plt.close()

print("=" * 60)
print("CONFIDENCE INTERVALS (95%)")
print("=" * 60)
print(f"\nData: n={n}, log-normal(μ=0, σ=0.5)")
print(f"Observed log-mean: {mu_hat:.4f}")
print(f"\n{'Method':<25s} {'Lower':>8s} {'Upper':>8s} {'Width':>8s}")
print("-" * 55)
for label, low, high, width in zip(ci_types, ci_lowers, ci_uppers, ci_widths):
    print(f"{label:<25s} {low:>8.4f} {high:>8.4f} {width:>8.4f}")

print(f"\nBootstrap diagnostics:")
print(f"  Bias = {bias:.4f}")
print(f"  Bootstrap SE = {np.std(boot_means, ddof=1):.4f} vs analytic SE = {se_hat:.4f}")
print(f"\nThe t-interval is widest (accounts for uncertainty in σ)")
print("The bootstrap percentile interval is non-parametric.")
