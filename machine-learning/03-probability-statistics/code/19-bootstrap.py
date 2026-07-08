"""03.19 Bootstrap: Nonparametric bootstrap for mean and median."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, bootstrap

np.random.seed(42)
n = 100
data = np.random.exponential(scale=3, size=n)

B = 10000
boot_means = np.zeros(B)
boot_medians = np.zeros(B)
boot_mads = np.zeros(B)

for b in range(B):
    idx = np.random.randint(0, n, n)
    boot_means[b] = np.mean(data[idx])
    boot_medians[b] = np.median(data[idx])
    boot_mads[b] = np.median(np.abs(data[idx] - np.median(data[idx])))

se_mean = np.std(boot_means, ddof=1)
se_median = np.std(boot_medians, ddof=1)
se_mad = np.std(boot_mads, ddof=1)

bias_mean = np.mean(boot_means) - np.mean(data)
bias_median = np.mean(boot_medians) - np.median(data)
bias_mad = np.mean(boot_mads) - np.median(np.abs(data - np.median(data)))

ci_mean = np.percentile(boot_means, [2.5, 97.5])
ci_median = np.percentile(boot_medians, [2.5, 97.5])
ci_mad = np.percentile(boot_mads, [2.5, 97.5])

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].hist(boot_means, bins=60, density=True, alpha=0.6, color='steelblue', edgecolor='white')
axes[0, 0].axvline(np.mean(data), color='r', lw=2, label=f"Observed mean={np.mean(data):.2f}")
axes[0, 0].axvline(ci_mean[0], color='k', ls='--', alpha=0.5)
axes[0, 0].axvline(ci_mean[1], color='k', ls='--', alpha=0.5)
axes[0, 0].set_title(f"Bootstrap Distribution of Mean\nSE={se_mean:.3f}, Bias={bias_mean:.3f}")
axes[0, 0].set_xlabel("Mean")
axes[0, 0].legend(fontsize=8)
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].hist(boot_medians, bins=60, density=True, alpha=0.6, color='orange', edgecolor='white')
axes[0, 1].axvline(np.median(data), color='r', lw=2, label=f"Observed median={np.median(data):.2f}")
axes[0, 1].axvline(ci_median[0], color='k', ls='--', alpha=0.5)
axes[0, 1].axvline(ci_median[1], color='k', ls='--', alpha=0.5)
axes[0, 1].set_title(f"Bootstrap Distribution of Median\nSE={se_median:.3f}, Bias={bias_median:.3f}")
axes[0, 1].set_xlabel("Median")
axes[0, 1].legend(fontsize=8)
axes[0, 1].grid(True, alpha=0.3)

axes[0, 2].hist(boot_mads, bins=60, density=True, alpha=0.6, color='green', edgecolor='white')
axes[0, 2].axvline(np.median(np.abs(data - np.median(data))), color='r', lw=2,
                   label=f"Observed MAD={np.median(np.abs(data - np.median(data))):.2f}")
axes[0, 2].axvline(ci_mad[0], color='k', ls='--', alpha=0.5)
axes[0, 2].axvline(ci_mad[1], color='k', ls='--', alpha=0.5)
axes[0, 2].set_title(f"Bootstrap Distribution of MAD\nSE={se_mad:.3f}, Bias={bias_mad:.3f}")
axes[0, 2].set_xlabel("MAD")
axes[0, 2].legend(fontsize=8)
axes[0, 2].grid(True, alpha=0.3)

ns_boot = [10, 25, 50, 100, 250, 500]
se_means = []
se_medians = []
for ni in ns_boot:
    di = np.random.exponential(3, ni)
    bmeans = np.array([np.mean(di[np.random.randint(0, ni, ni)]) for _ in range(2000)])
    bmedians = np.array([np.median(di[np.random.randint(0, ni, ni)]) for _ in range(2000)])
    se_means.append(np.std(bmeans, ddof=1))
    se_medians.append(np.std(bmedians, ddof=1))

axes[1, 0].loglog(ns_boot, se_means, 'o-', label="Mean SE", lw=2)
axes[1, 0].loglog(ns_boot, se_medians, 's-', label="Median SE", lw=2)
axes[1, 0].loglog(ns_boot, [3/np.sqrt(ni) for ni in ns_boot], '--', label="O(1/√n)")
axes[1, 0].set_xlabel("n")
axes[1, 0].set_ylabel("Bootstrap SE")
axes[1, 0].set_title("Standard Error vs Sample Size")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

jackknife = np.zeros(n)
for i in range(n):
    jackknife[i] = np.mean(np.delete(data, i))
jack_mean = np.mean(jackknife)
jack_se = np.sqrt((n-1)/n * np.sum((jackknife - jack_mean)**2))

bar_data = [np.std(boot_means, ddof=1), jack_se,
            3 / np.sqrt(n), np.std(boot_medians, ddof=1)]
bar_labels = ['Bootstrap\nMean SE', 'Jackknife\nMean SE', 'Analytic\nMean SE', 'Bootstrap\nMedian SE']
axes[1, 1].bar(range(4), bar_data, color=['steelblue', 'coral', 'green', 'orange'])
axes[1, 1].set_xticks(range(4))
axes[1, 1].set_xticklabels(bar_labels, fontsize=8)
axes[1, 1].set_ylabel("Standard Error")
axes[1, 1].set_title("SE Comparison: Bootstrap vs Jackknife vs Analytic")
axes[1, 1].grid(True, axis='y', alpha=0.3)

x_fit = np.linspace(boot_means.min(), boot_means.max(), 200)
axes[1, 2].hist(boot_means, bins=50, density=True, alpha=0.5, color='lightblue', label="Bootstrap")
axes[1, 2].plot(x_fit, norm.pdf(x_fit, loc=np.mean(data), scale=se_mean), 'r-', lw=2, label="Normal approx")
axes[1, 2].set_xlabel("Mean")
axes[1, 2].set_ylabel("Density")
axes[1, 2].set_title("Bootstrap vs Normal Approximation")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/19-bootstrap.png")
plt.close()

print("=" * 60)
print("BOOTSTRAP RESULTS")
print("=" * 60)
print(f"\nOriginal data (n={n}):")
print(f"  Mean:   {np.mean(data):.4f}")
print(f"  Median: {np.median(data):.4f}")
print(f"  MAD:    {np.median(np.abs(data - np.median(data))):.4f}")

print(f"\n{'Statistic':<15s} {'Estimate':>10s} {'SE':>8s} {'Bias':>8s} {'95% CI':>20s}")
print("-" * 65)
print(f"{'Mean':<15s} {np.mean(data):>10.3f} {se_mean:>8.3f} {bias_mean:>8.3f} [{ci_mean[0]:.3f}, {ci_mean[1]:.3f}]")
print(f"{'Median':<15s} {np.median(data):>10.3f} {se_median:>8.3f} {bias_median:>8.3f} [{ci_median[0]:.3f}, {ci_median[1]:.3f}]")
print(f"{'MAD':<15s} {np.median(np.abs(data - np.median(data))):>10.3f} {se_mad:>8.3f} {bias_mad:>8.3f} [{ci_mad[0]:.3f}, {ci_mad[1]:.3f}]")

print(f"\nJackknife SE (mean): {jack_se:.4f}")
print(f"Bootstrap SE (mean):  {se_mean:.4f}")
print(f"Jackknife bias:       {np.mean(jackknife) - np.mean(data):.4f}")
print("\nBootstrap plot saved.")
