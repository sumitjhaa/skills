"""03.30 Empirical Processes: ECDF, DKW bands, KS test."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, kstest, uniform

np.random.seed(42)
n = 100
data = np.random.normal(0, 1, n)

x_grid = np.linspace(-3.5, 3.5, 500)
ecdf = np.array([np.mean(data <= x) for x in x_grid])
true_cdf = norm.cdf(x_grid)

alpha = 0.05
eps_n = np.sqrt(np.log(2/alpha) / (2 * n))
lower = np.maximum(ecdf - eps_n, 0)
upper = np.minimum(ecdf + eps_n, 1)

ks_stat, ks_p = kstest(data, 'norm')

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].step(np.sort(data), np.linspace(0, 1, n, endpoint=False), where='post', lw=2, label="ECDF")
axes[0, 0].plot(x_grid, true_cdf, 'r--', lw=2, label="True N(0,1) CDF")
axes[0, 0].fill_between(x_grid, lower, upper, alpha=0.2, color='b', label="95% DKW band")
axes[0, 0].set_xlabel("x")
axes[0, 0].set_ylabel("F(x)")
axes[0, 0].set_title(f"Empirical CDF with DKW Confidence Bands\nKS stat={ks_stat:.4f}, p={ks_p:.4f}")
axes[0, 0].legend(fontsize=8)
axes[0, 0].grid(True, alpha=0.3)

glivenko_cantelli = np.max(np.abs(ecdf - true_cdf))
print(f"Glivenko-Cantelli: max|F_n - F| = {glivenko_cantelli:.4f}")
print(f"DKW bound ε_n = {eps_n:.4f}")
print(f"DKW bound satisfied: {glivenko_cantelli <= eps_n}")

ns_ks = [10, 20, 50, 100, 200, 500]
ks_stats_sim = []
for ni in ns_ks:
    max_devs = []
    for _ in range(5000):
        di = np.random.normal(0, 1, ni)
        max_devs.append(np.max(np.abs(
            np.linspace(0, 1, ni, endpoint=False) -
            norm.cdf(np.sort(di)))))
    ks_stats_sim.append(np.mean(max_devs))

axes[0, 1].loglog(ns_ks, ks_stats_sim, 'o-', lw=2, label="Empirical")
theoretical = np.sqrt(np.log(2/0.05) / (2 * np.array(ns_ks)))
axes[0, 1].loglog(ns_ks, theoretical, 's--', lw=2, label="DKW bound")
axes[0, 1].set_xlabel("n")
axes[0, 1].set_ylabel("Mean max deviation")
axes[0, 1].set_title("DKW Bound: Max Deviation vs n")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

p_values_h0 = []
for _ in range(2000):
    di = np.random.normal(0, 1, n)
    _, p = kstest(di, 'norm')
    p_values_h0.append(p)

axes[0, 2].hist(p_values_h0, bins=40, density=True, alpha=0.6, color='steelblue')
axes[0, 2].axhline(1.0, color='r', ls='--', label="Uniform(0,1)")
axes[0, 2].set_xlabel("p-value")
axes[0, 2].set_ylabel("Density")
axes[0, 2].set_title("Distribution of KS p-values\nunder H₀ (should be uniform)")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)
print(f"Type I error rate: {np.mean(np.array(p_values_h0) < 0.05):.4f} (expected: 0.05)")

n_alternatives = [50, 100, 200]
power_vs_effect = []
effect_sizes = np.linspace(0, 1.5, 15)
for es in effect_sizes:
    reject = 0
    for _ in range(500):
        di = np.random.normal(es, 1, n)
        _, p = kstest(di, 'norm')
        if p < 0.05:
            reject += 1
    power_vs_effect.append(reject / 500)

axes[1, 0].plot(effect_sizes, power_vs_effect, 'o-', lw=2)
axes[1, 0].axhline(0.8, color='r', ls='--', label="80% power")
axes[1, 0].axhline(0.05, color='k', ls=':', label="α=0.05")
axes[1, 0].set_xlabel("Effect size (mean shift)")
axes[1, 0].set_ylabel("Power")
axes[1, 0].set_title("KS Test Power vs Effect Size")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].step(np.sort(data), np.linspace(0, 1, n, endpoint=False), where='post', lw=2, label="ECDF")
axes[1, 1].plot(x_grid, lower, 'b:', lw=1, label="DKW lower")
axes[1, 1].plot(x_grid, upper, 'b:', lw=1, label="DKW upper")
axes[1, 1].fill_between(x_grid, lower, upper, alpha=0.1, color='b')
axes[1, 1].axvline(0, color='gray', ls='--')
axes[1, 1].set_xlabel("x")
axes[1, 1].set_ylabel("F(x)")
axes[1, 1].set_title("ECDF with DKW Bands\n(zoomed, 95% confidence)")
axes[1, 1].legend(fontsize=8)
axes[1, 1].grid(True, alpha=0.3)

distances = np.maximum(upper - ecdf, ecdf - lower)
axes[1, 2].plot(x_grid, distances, 'g-', lw=2)
axes[1, 2].axhline(eps_n, color='r', ls='--', label=f"DKW ε_n={eps_n:.4f}")
axes[1, 2].set_xlabel("x")
axes[1, 2].set_ylabel("Distance to band edge")
axes[1, 2].set_title("Distance from ECDF to DKW Band Edge")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/30-empirical-processes.png")
plt.close()

print("\n" + "=" * 60)
print("EMPIRICAL PROCESSES ANALYSIS")
print("=" * 60)
print(f"\nn = {n}")
print(f"KS statistic: {ks_stat:.4f} (p-value: {ks_p:.4f})")
print(f"95% DKW bandwidth ε_n = {eps_n:.4f}")
print(f"Maximum deviation: {np.max(np.abs(ecdf - true_cdf)):.4f}")
print(f"DKW bound satisfied: {np.max(np.abs(ecdf - true_cdf)) <= eps_n}")
print(f"\nAs n→∞, the ECDF converges uniformly to the true CDF (Glivenko-Cantelli)")
print(f"The DKW inequality provides finite-sample confidence bands.")
