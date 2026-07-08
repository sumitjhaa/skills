"""03.11 Concentration Inequalities: Empirical verification."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

np.random.seed(42)
n, n_trials = 100, 5000

X = np.random.exponential(1, size=(n_trials, n))
means = np.mean(X, axis=1)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

eps_grid = np.linspace(0.05, 0.8, 50)
empirical = np.array([np.mean(np.abs(means - 1) >= eps) for eps in eps_grid])
chebyshev = 1 / (n * eps_grid**2)
markov = 1 / (n * eps_grid)
hoeffding = 2 * np.exp(-2 * n * eps_grid**2)

axes[0, 0].semilogy(eps_grid, empirical, 'o-', label="Empirical", markersize=4, lw=2)
axes[0, 0].semilogy(eps_grid, chebyshev, '--', label="Chebyshev", lw=2)
axes[0, 0].semilogy(eps_grid, markov, ':', label="Markov", lw=2)
axes[0, 0].semilogy(eps_grid, hoeffding, '-.', label="Hoeffding (unbounded)", lw=2)
axes[0, 0].set_xlabel("ε")
axes[0, 0].set_ylabel("P(|X̄ - μ| ≥ ε)")
axes[0, 0].set_title("Concentration Inequalities for Exp(1) n=100")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

M = 10
X_trunc = np.clip(X, 0, M)
means_trunc = np.mean(X_trunc, axis=1)
empirical_trunc = np.array([np.mean(np.abs(means_trunc - 1) >= eps) for eps in eps_grid])
bernoulli_bound = np.exp(-n * eps_grid**2 / (2 * M**2))
hoeffding_trunc = 2 * np.exp(-2 * n * eps_grid**2 / M**2)

axes[0, 1].semilogy(eps_grid, empirical_trunc, 'o-', label="Empirical (trunc)", markersize=4, lw=2)
axes[0, 1].semilogy(eps_grid, bernoulli_bound, '--', label="Bernstein-type", lw=2)
axes[0, 1].semilogy(eps_grid, hoeffding_trunc, '-.', label="Hoeffding (trunc)", lw=2)
axes[0, 1].set_xlabel("ε")
axes[0, 1].set_ylabel("P(|X̄ - μ| ≥ ε)")
axes[0, 1].set_title("Concentration for Truncated Exp(1) [0, 10]")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

n_small = [10, 50, 200, 1000]
for ni in n_small:
    Xi = np.random.exponential(1, size=(n_trials, ni))
    means_i = np.mean(Xi, axis=1)
    emp_i = np.array([np.mean(np.abs(means_i - 1) >= eps) for eps in eps_grid])
    axes[1, 0].semilogy(eps_grid, emp_i, label=f"n={ni}", lw=1.5)
axes[1, 0].set_xlabel("ε")
axes[1, 0].set_ylabel("P(|X̄ - μ| ≥ ε)")
axes[1, 0].set_title("Empirical Tail Probabilities by n")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

X_norm = np.random.normal(0, 1, size=(n_trials, n))
means_norm = np.mean(X_norm, axis=1)
empirical_norm = np.array([np.mean(np.abs(means_norm) >= eps) for eps in eps_grid])
gaussian_tail = 2 * (1 - norm.cdf(eps_grid * np.sqrt(n)))
chebyshev_norm = 1 / (n * eps_grid**2)

axes[1, 1].semilogy(eps_grid, empirical_norm, 'o-', label="Empirical (Normal)", markersize=4, lw=2)
axes[1, 1].semilogy(eps_grid, gaussian_tail, '-', label="Gaussian tail (exact)", lw=2)
axes[1, 1].semilogy(eps_grid, chebyshev_norm, '--', label="Chebyshev", lw=2)
axes[1, 1].set_xlabel("ε")
axes[1, 1].set_ylabel("P(|X̄| ≥ ε)")
axes[1, 1].set_title("Concentration: N(0,1) vs Bounds (n=100)")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/11-concentration-inequalities.png")
plt.close()

print("=" * 60)
print("CONCENTRATION INEQUALITIES")
print("=" * 60)
print(f"\nSetup: Exp(1), n={n}, {n_trials} trials")
print(f"\nAt ε=0.2:")
idx_eps = np.argmin(np.abs(eps_grid - 0.2))
print(f"  Empirical tail:      {empirical[idx_eps]:.4f}")
print(f"  Chebyshev bound:     {chebyshev[idx_eps]:.4f}")
print(f"  Markov bound:        {markov[idx_eps]:.4f}")
print(f"  Hoeffding bound:     {hoeffding[idx_eps]:.4f}")

print(f"\nAt ε=0.5:")
idx_eps = np.argmin(np.abs(eps_grid - 0.5))
print(f"  Empirical tail:      {empirical[idx_eps]:.4f}")
print(f"  Chebyshev bound:     {chebyshev[idx_eps]:.4f}")

print(f"\nConcentration speed (n={n_small}):")
for ni in n_small:
    Xi = np.random.exponential(1, size=(n_trials, ni))
    means_i = np.mean(Xi, axis=1)
    tail_i = np.mean(np.abs(means_i - 1) >= 0.2)
    print(f"  n={ni:4d}: P(|X̄-1|≥0.2) = {tail_i:.4f}")

print("\nConcentration plot saved.")
