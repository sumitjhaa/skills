"""03.09 Sums of RVs & CLT: Convolution and CLT demonstration."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, gamma, chi2, t as t_dist

np.random.seed(42)
n_sims = 50000

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

for n in [1, 2, 5, 30, 100]:
    sample_means = np.mean(np.random.exponential(1, size=(n_sims, n)), axis=1)
    axes[0, 0].hist(sample_means, bins=80, density=True, alpha=0.5, label=f"n={n}")

x_clt = np.linspace(0, 2, 200)
axes[0, 0].plot(x_clt, norm.pdf(x_clt, loc=1, scale=1/np.sqrt(100)), 'k-', lw=2, label="CLT: N(1, 1/n)")
axes[0, 0].set_xlabel("Sample Mean")
axes[0, 0].set_ylabel("Density")
axes[0, 0].set_title("CLT: Exp(1) Sample Means → Normal")
axes[0, 0].legend(fontsize=8)
axes[0, 0].grid(True, alpha=0.3)

U1 = np.random.uniform(0, 1, 100000)
U2 = np.random.uniform(0, 1, 100000)
S = U1 + U2

axes[0, 1].hist(S, bins=60, density=True, alpha=0.7, label="U(0,1)+U(0,1)", color='steelblue')
x_tri = np.linspace(0, 2, 200)
triangular = np.where(x_tri < 1, x_tri, 2 - x_tri)
axes[0, 1].plot(x_tri, triangular, 'r-', lw=2, label="Triangular")
axes[0, 1].set_xlabel("Sum")
axes[0, 1].set_ylabel("Density")
axes[0, 1].set_title("Convolution: Sum of Two Uniforms")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

n_sums = [2, 3, 5, 10]
for ns in n_sums:
    U_many = np.sum([np.random.uniform(0, 1, (n_sims)) for _ in range(ns)], axis=0)
    axes[0, 2].hist(U_many, bins=80, density=True, alpha=0.4, label=f"n={ns}")
mean_sum = ns / 2
var_sum = ns / 12
x_irwin = np.linspace(0, ns, 200)
axes[0, 2].plot(x_irwin, norm.pdf(x_irwin, loc=mean_sum, scale=np.sqrt(var_sum)), 'k--', lw=2)
axes[0, 2].set_xlabel("Sum")
axes[0, 2].set_ylabel("Density")
axes[0, 2].set_title("Sum of n Uniforms → Normal")
axes[0, 2].legend(fontsize=8)
axes[0, 2].grid(True, alpha=0.3)

n_chi = [2, 5, 20, 50]
for df in n_chi:
    chi_samples = np.sum(np.random.randn(n_sims, df)**2, axis=1)
    axes[1, 0].hist(chi_samples, bins=80, density=True, alpha=0.4, label=f"df={df}")
x_chi = np.linspace(0, 80, 200)
for df in [20, 50]:
    axes[1, 0].plot(x_chi, norm.pdf(x_chi, loc=df, scale=np.sqrt(2*df)), '--', lw=1)
axes[1, 0].set_xlabel("Chi-squared")
axes[1, 0].set_ylabel("Density")
axes[1, 0].set_title("Chi-Squared Sums → Normal")
axes[1, 0].legend(fontsize=8)
axes[1, 0].grid(True, alpha=0.3)

ns_plot = [1, 5, 30, 100]
means_data = {}
for n in ns_plot:
    sample_means = np.mean(np.random.exponential(1, size=(n_sims, n)), axis=1)
    standardized = (sample_means - 1) * np.sqrt(n)
    means_data[n] = standardized

for n in ns_plot:
    axes[1, 1].hist(means_data[n], bins=80, density=True, alpha=0.4, label=f"n={n}")
x_std = np.linspace(-4, 4, 200)
axes[1, 1].plot(x_std, norm.pdf(x_std, 0, 1), 'k--', lw=2, label="N(0,1)")
axes[1, 1].set_xlabel("Standardized mean")
axes[1, 1].set_ylabel("Density")
axes[1, 1].set_title("CLT: Standardized Exp(1) Means")
axes[1, 1].legend(fontsize=8)
axes[1, 1].grid(True, alpha=0.3)

from scipy import stats
ns_berry = [5, 10, 30, 100, 500]
ks_results = []
for n in ns_berry:
    means_b = np.mean(np.random.exponential(1, size=(10000, n)), axis=1)
    std_b = (means_b - 1) * np.sqrt(n)
    ks = np.max(np.abs(np.sort(std_b) - norm.cdf(np.sort(std_b), 0, 1)))
    ks_results.append(ks)
    print(f"  Berry-Esseen n={n:4d}: KS stat = {ks:.4f}")

axes[1, 2].plot(ns_berry, ks_results, 'o-', lw=2, markersize=8)
axes[1, 2].set_xlabel("n")
axes[1, 2].set_ylabel("KS Statistic (max CDF error)")
axes[1, 2].set_title("Berry-Esseen: CLT Convergence Rate")
axes[1, 2].set_xscale('log')
axes[1, 2].set_yscale('log')
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/09-sums-clt.png")
plt.close()

print("=" * 60)
print("SUMS OF RVs & CENTRAL LIMIT THEOREM")
print("=" * 60)
print("\nCLT for Exponential(1):")
for n in ns_plot:
    m = means_data[n]
    print(f"  n={n:4d}: mean={m.mean():.4f}, var={m.var():.4f} (expected: 0, 1)")

print("\nConvolution of Uniforms:")
print(f"  U(0,1)+U(0,1): mean={np.mean(S):.4f}, var={np.var(S):.4f}")
print(f"  Expected: mean=1.0, var=1/6={1/6:.4f}")

print("\nBerry-Esseen (convergence rate):")
for n, ks in zip(ns_berry, ks_results):
    print(f"  n={n:4d}: KS={ks:.4f}")
print("\nCLT and convolution plots saved.")
