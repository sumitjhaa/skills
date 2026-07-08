"""03.10 LLN & CLT: Convergence of sample mean and normal approximation."""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import norm

np.random.seed(42)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

ns = np.arange(1, 5001)
sample_means = np.cumsum(np.random.exponential(1, 5000)) / ns

axes[0, 0].plot(ns, sample_means, alpha=0.6, lw=0.5)
axes[0, 0].axhline(1.0, color='r', linestyle='--', lw=2, label="True mean")
axes[0, 0].set_xlabel("n")
axes[0, 0].set_ylabel("Sample Mean")
axes[0, 0].set_title("LLN: Sample Mean Converges to E[X]")
axes[0, 0].legend()
axes[0, 0].set_xscale('log')
axes[0, 0].grid(True, alpha=0.3)

n_sample = 1000
n_reps = 5000
means = np.mean(np.random.exponential(1, size=(n_reps, n_sample)), axis=1)
standardized = (means - 1) * np.sqrt(n_sample)

stats.probplot(standardized, dist="norm", plot=axes[0, 1])
axes[0, 1].set_title(f"CLT QQ-Plot (n={n_sample})")
axes[0, 1].grid(True, alpha=0.3)

axes[0, 2].hist(standardized, bins=80, density=True, alpha=0.6, color='steelblue', label="Standardized means")
x_s = np.linspace(-4, 4, 200)
axes[0, 2].plot(x_s, norm.pdf(x_s, 0, 1), 'r-', lw=2, label="N(0,1)")
axes[0, 2].set_xlabel("Standardized mean")
axes[0, 2].set_ylabel("Density")
axes[0, 2].set_title(f"CLT: Standardized Exp(1) Means (n={n_sample})")
axes[0, 2].legend(fontsize=8)
axes[0, 2].grid(True, alpha=0.3)

ns_lln = np.logspace(1, 4, 20, dtype=int)
lln_estimates = []
for ni in ns_lln:
    x = np.random.exponential(1, ni)
    lln_estimates.append(np.mean(x))

axes[1, 0].semilogx(ns_lln, np.abs(np.array(lln_estimates) - 1), 'o-')
axes[1, 0].axhline(0, color='r', ls='--')
axes[1, 0].set_xlabel("n")
axes[1, 0].set_ylabel("|Sample Mean - True Mean|")
axes[1, 0].set_title("LLN: Absolute Error Decays with n")
axes[1, 0].grid(True, alpha=0.3)

ns_berry = [5, 10, 30, 100, 500]
ks_result = []
for n in ns_berry:
    means_b = np.mean(np.random.exponential(1, size=(10000, n)), axis=1)
    std_b = (means_b - 1) * np.sqrt(n)
    ks_stat = np.max(np.abs(np.sort(std_b) - norm.cdf(np.sort(std_b), 0, 1)))
    ks_result.append(ks_stat)

axes[1, 1].plot(ns_berry, ks_result, 'o-', lw=2, markersize=8, color='green')
axes[1, 1].set_xlabel("n")
axes[1, 1].set_ylabel("KS Statistic")
axes[1, 1].set_title("Berry-Esseen: Convergence Rate")
axes[1, 1].set_xscale('log')
axes[1, 1].set_yscale('log')
axes[1, 1].grid(True, alpha=0.3)

logn_data = np.random.lognormal(0, 1, 5000)
logn_means = np.zeros(1000)
for i in range(1000):
    logn_means[i] = np.mean(np.random.choice(logn_data, 100))
axes[1, 2].hist(logn_means, bins=50, density=True, alpha=0.6, color='orange')
x_ln = np.linspace(logn_means.min(), logn_means.max(), 200)
axes[1, 2].plot(x_ln, norm.pdf(x_ln, loc=np.mean(logn_means), scale=np.std(logn_means)), 'r-', lw=2)
axes[1, 2].set_xlabel("Sample Mean")
axes[1, 2].set_ylabel("Density")
axes[1, 2].set_title("CLT for Lognormal Data\n(n=100, 1000 resamples)")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/10-lln-clt.png")
plt.close()

print("=" * 60)
print("LAW OF LARGE NUMBERS & CENTRAL LIMIT THEOREM")
print("=" * 60)
print(f"\nLLN: Final sample mean after n=5000: {sample_means[-1]:.4f} (true: 1.0)")
print(f"\nCLT (n={n_sample}):")
print(f"  Standardized mean: {np.mean(standardized):.4f} (expected: 0)")
print(f"  Standardized std:  {np.std(standardized):.4f} (expected: 1)")
print(f"  Skewness: {stats.skew(standardized):.4f}")
print(f"  Kurtosis: {stats.kurtosis(standardized):.4f}")

ks_stat, ks_p = stats.kstest(standardized, 'norm')
print(f"  KS test vs N(0,1): stat={ks_stat:.4f}, p={ks_p:.4f}")

print(f"\nBerry-Esseen Convergence:")
for n, ks in zip(ns_berry, ks_result):
    print(f"  n={n:4d}: KS = {ks:.4f}")

print("\nLLN and CLT plots saved.")
