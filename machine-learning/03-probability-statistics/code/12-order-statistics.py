"""03.12 Order Statistics: Distribution of min, max, median."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta, gumbel_r, norm

np.random.seed(42)
n_sims = 50000
n = 10

samples = np.random.uniform(0, 1, size=(n_sims, n))
sorted_samples = np.sort(samples, axis=1)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

k_values = [1, 3, 5, 7, 9, 10]
for ax, k in zip(axes.ravel(), k_values):
    ax.hist(sorted_samples[:, k-1], bins=60, density=True, alpha=0.6, label=f"Empirical X_({k})")
    x = np.linspace(0, 1, 200)
    ax.plot(x, beta.pdf(x, k, n - k + 1), 'r-', lw=2, label=f"Beta({k},{n-k+1})")
    ax.set_title(f"Order Statistic X_({k})")
    ax.set_xlabel("Value")
    ax.set_ylabel("Density")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/12-order-statistics.png")
plt.close()

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

ns = [10, 50, 200, 1000]
maxima = [np.max(np.random.uniform(0, 1, (5000, n)), axis=1) for n in ns]

for i, ni in enumerate(ns):
    ax = axes.ravel()[i]
    ax.hist(maxima[i], bins=50, density=True, alpha=0.6, label=f"Max, n={ni}")
    x = np.linspace(0.5, 1, 200)
    ax.plot(x, beta.pdf(x, ni, 1), 'r-', lw=2, label=f"Beta({ni},1)")
    ax.set_title(f"Max of n={ni} Uniforms")
    ax.set_xlabel("x")
    ax.set_ylabel("Density")
    ax.legend(fontsize=8)

for i in range(4, 6):
    axes.ravel()[i].set_visible(False)

m_theoretical = 1 - 1 / (np.arange(1, 1001))
m_empirical = []
for ni in np.arange(1, 1001, 10):
    m_empirical.append(np.mean(np.max(np.random.uniform(0, 1, (500, ni)), axis=1)))

axes[1, 0].plot(np.arange(1, 1001), m_theoretical, 'r-', lw=2, label="Theoretical E[Max]")
axes[1, 0].plot(np.arange(1, 1001, 10), m_empirical, 'o', markersize=3, label="Empirical")
axes[1, 0].set_xlabel("n")
axes[1, 0].set_ylabel("E[Max]")
axes[1, 0].set_title("Expected Maximum vs n")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

minima = [np.min(np.random.uniform(0, 1, (5000, n)), axis=1) for n in ns]
for i, n_val in enumerate(ns):
    axes[1, 1].hist(minima[i], bins=50, density=True, alpha=0.5, label=f"Min, n={n_val}")
x = np.linspace(0, 0.5, 200)
for n_val in ns[:2]:
    axes[1, 1].plot(x, beta.pdf(x, 1, n_val), '--', lw=2)
axes[1, 1].set_xlabel("x")
axes[1, 1].set_ylabel("Density")
axes[1, 1].set_title("Distribution of Minimum")
axes[1, 1].legend(fontsize=8)
axes[1, 1].grid(True, alpha=0.3)

medians = [np.median(np.random.uniform(0, 1, (5000, n_val)), axis=1) for n_val in [9, 19, 49, 99]]
for i, n_val in enumerate([9, 19, 49, 99]):
    axes[1, 2].hist(medians[i], bins=50, density=True, alpha=0.5, label=f"n={n_val}")
x_m = np.linspace(0.3, 0.7, 200)
for n_val in [9, 49]:
    k = (n_val + 1) // 2
    axes[1, 2].plot(x_m, beta.pdf(x_m, k, n_val - k + 1), '--', lw=2)
axes[1, 2].set_xlabel("x")
axes[1, 2].set_ylabel("Density")
axes[1, 2].set_title("Distribution of Median")
axes[1, 2].legend(fontsize=8)
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/12-extreme-values.png")
plt.close()

print("=" * 60)
print("ORDER STATISTICS ANALYSIS")
print("=" * 60)
print(f"\nSample size: n={n}, Simulations: {n_sims}")
for k in [1, 5, 10]:
    emp_mean = np.mean(sorted_samples[:, k-1])
    theo_mean = k / (n + 1)
    emp_var = np.var(sorted_samples[:, k-1])
    theo_var = k * (n - k + 1) / ((n + 1)**2 * (n + 2))
    print(f"\nX_({k}):")
    print(f"  Mean: {emp_mean:.4f} vs theoretical {theo_mean:.4f}")
    print(f"  Var:  {emp_var:.4f} vs theoretical {theo_var:.4f}")

print(f"\nMaximum Convergence:")
for n, mx in zip(ns, maxima):
    print(f"  n={n:4d}: E[Max]={np.mean(mx):.4f}, expected={n/(n+1):.4f}")

print(f"\nMedian Distribution (n=9):")
print(f"  Mean: {np.mean(medians[0]):.4f}, Var: {np.var(medians[0]):.4f}")

print("\nOrder statistic plots saved.")
