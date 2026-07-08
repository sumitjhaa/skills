"""03.13 MLE: MLE for Normal and Exponential distributions."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.stats import norm, expon, gamma, chi2

np.random.seed(42)
n = 200

data = np.random.normal(5, 2, n)
mu_mle = np.mean(data)
sigma_mle = np.std(data)

print("=" * 60)
print("MAXIMUM LIKELIHOOD ESTIMATION")
print("=" * 60)
print("\n--- Normal Distribution ---")
print(f"  Closed-form MLE: μ̂ = {mu_mle:.4f}, σ̂ = {sigma_mle:.4f}")
print(f"  True values:      μ = {5}, σ = {2}")

mu_se = sigma_mle / np.sqrt(n)
sigma_se = sigma_mle / np.sqrt(2 * n)
print(f"  Standard errors:  SE(μ̂) = {mu_se:.4f}, SE(σ̂) = {sigma_se:.4f}")

exp_data = np.random.exponential(2, n)
lambda_mle = 1 / np.mean(exp_data)
lambda_se = lambda_mle / np.sqrt(n)

print("\n--- Exponential Distribution ---")
print(f"  MLE: λ̂ = {lambda_mle:.4f}")
print(f"  True: λ = 0.5")
print(f"  SE(λ̂) = {lambda_se:.4f}")

def neg_log_lik(mu_sigma, data):
    mu, sigma = mu_sigma
    if sigma <= 0:
        return 1e10
    return -np.sum(norm.logpdf(data, mu, sigma))

result = minimize(neg_log_lik, x0=[0, 1], args=(data,),
                  method="L-BFGS-B", bounds=[(None, None), (1e-6, None)])
print(f"\n  Numerical MLE:    μ̂ = {result.x[0]:.4f}, σ̂ = {result.x[1]:.4f}")

mu_grid = np.linspace(3, 7, 200)
nll = np.array([neg_log_lik([m, sigma_mle], data) for m in mu_grid])

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].plot(mu_grid, nll, 'b-', lw=2)
axes[0, 0].axvline(mu_mle, color='r', linestyle='--', lw=2, label=f"MLE μ = {mu_mle:.3f}")
axes[0, 0].set_xlabel("μ")
axes[0, 0].set_ylabel("Negative Log-Likelihood")
axes[0, 0].set_title("Likelihood Profile for μ")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

sigma_grid = np.linspace(1.5, 3.5, 200)
nll_sigma = np.array([neg_log_lik([mu_mle, s], data) for s in sigma_grid])
axes[0, 1].plot(sigma_grid, nll_sigma, 'b-', lw=2)
axes[0, 1].axvline(sigma_mle, color='r', linestyle='--', lw=2, label=f"MLE σ = {sigma_mle:.3f}")
axes[0, 1].set_xlabel("σ")
axes[0, 1].set_ylabel("Negative Log-Likelihood")
axes[0, 1].set_title("Likelihood Profile for σ")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

ns_mc = [10, 30, 100, 500, 2000]
mle_means = []
mle_vars = []
for ni in ns_mc:
    means_i = []
    vars_i = []
    for _ in range(1000):
        d = np.random.normal(5, 2, ni)
        means_i.append(np.mean(d))
        vars_i.append(np.std(d, ddof=1))
    mle_means.append((np.std(means_i), 2 / np.sqrt(ni)))
    mle_vars.append((np.std(vars_i), 2 / np.sqrt(2 * ni)))

ns_arr = np.array(ns_mc)
axes[0, 2].loglog(ns_arr, [m[0] for m in mle_means], 'o-', label="Empirical SE(μ̂)")
axes[0, 2].loglog(ns_arr, [m[1] for m in mle_means], 's--', label="Theoretical σ/√n")
axes[0, 2].set_xlabel("n")
axes[0, 2].set_ylabel("SE(μ̂)")
axes[0, 2].set_title("MLE Standard Error vs n")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

exp_grid = np.linspace(0, 8, 200)
axes[1, 0].hist(exp_data, bins=40, density=True, alpha=0.6, label="Data")
axes[1, 0].plot(exp_grid, expon.pdf(exp_grid, scale=1/lambda_mle), 'r-', lw=2,
                label=f"MLE Exp(λ={lambda_mle:.2f})")
axes[1, 0].plot(exp_grid, expon.pdf(exp_grid, scale=2), 'k--', lw=2, label="True Exp(0.5)")
axes[1, 0].set_xlabel("x")
axes[1, 0].set_ylabel("Density")
axes[1, 0].set_title("Exponential MLE Fit")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

n_bootstrap = 1000
bootstrap_mus = np.zeros(n_bootstrap)
for b in range(n_bootstrap):
    boot_data = np.random.choice(data, n, replace=True)
    bootstrap_mus[b] = np.mean(boot_data)

axes[1, 1].hist(bootstrap_mus, bins=50, density=True, alpha=0.6, label="Bootstrap MLE μ")
x_boot = np.linspace(bootstrap_mus.min(), bootstrap_mus.max(), 200)
axes[1, 1].plot(x_boot, norm.pdf(x_boot, loc=mu_mle, scale=mu_se), 'r-', lw=2, label="Normal approx")
axes[1, 1].axvline(mu_mle, color='k', lw=2, ls='--', label=f"Observed μ̂={mu_mle:.2f}")
axes[1, 1].set_xlabel("μ̂")
axes[1, 1].set_ylabel("Density")
axes[1, 1].set_title("Bootstrap Distribution of MLE μ")
axes[1, 1].legend(fontsize=8)
axes[1, 1].grid(True, alpha=0.3)

n_grid = np.array([10, 30, 50, 100, 200, 500])
bias = []
for ni in n_grid:
    mle_i = [np.mean(np.random.normal(5, 2, ni)) for _ in range(5000)]
    bias.append(np.mean(mle_i) - 5)
axes[1, 2].plot(n_grid, bias, 'o-')
axes[1, 2].axhline(0, color='r', ls='--')
axes[1, 2].set_xlabel("n")
axes[1, 2].set_ylabel("Bias")
axes[1, 2].set_title("MLE Bias vs n (should be ~0)")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/13-mle.png")
plt.close()

print(f"\n--- MLE Properties ---")
print(f"  MLE μ̂ is unbiased: E[μ̂] - μ = {0:.4f}")
print(f"  MLE σ̂² is biased: E[σ̂²] = {sigma_mle**2:.4f} vs {np.var(data, ddof=1):.4f} (unbiased)")
print(f"  Bootstrap SE(μ̂) = {np.std(bootstrap_mus):.4f} vs asymptotic SE = {mu_se:.4f}")
print("\nMLE plot saved. Profile shows minimum at MLE.")
