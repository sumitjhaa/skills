"""04.04 Fisher information and Cramer-Rao bound."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, poisson, bernoulli
from scipy.optimize import minimize_scalar

def fisher_gaussian_mu(sigma):
    return 1.0 / sigma**2

def fisher_poisson(lmbda):
    return 1.0 / lmbda

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

sigma = 1.0
n_samples = 100
np.random.seed(42)
samples = np.random.normal(0, sigma, n_samples)
mu_hat = samples.mean()
fisher = n_samples * fisher_gaussian_mu(sigma)
cr_bound = 1.0 / fisher

axes[0, 0].hist(samples, bins=30, density=True, alpha=0.6, color='steelblue')
x_g = np.linspace(-3, 3, 200)
axes[0, 0].plot(x_g, norm.pdf(x_g, 0, sigma), 'r-', lw=2, label=f"N(0,{sigma}²)")
axes[0, 0].axvline(mu_hat, color='k', ls='--', lw=2, label=f"μ̂={mu_hat:.3f}")
axes[0, 0].set_xlabel("x")
axes[0, 0].set_ylabel("Density")
axes[0, 0].set_title(f"N(0,1): MLE μ̂, n={n_samples}")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

n_range = np.arange(10, 501, 10)
fisher_range = n_range * fisher_gaussian_mu(sigma)
cr_range = 1 / fisher_range
axes[0, 1].plot(n_range, cr_range, lw=2, label="CR bound (1/n)")
axes[0, 1].set_xlabel("n")
axes[0, 1].set_ylabel("CR bound")
axes[0, 1].set_title("Cramer-Rao Bound vs n")
axes[0, 1].grid(True, alpha=0.3)

lmbdas = np.linspace(0.5, 10, 50)
fisher_vals = n_samples / lmbdas
cr_vals = 1 / fisher_vals
axes[0, 2].plot(lmbdas, cr_vals, lw=2, color='orange')
axes[0, 2].set_xlabel("λ (Poisson rate)")
axes[0, 2].set_ylabel("CR bound")
axes[0, 2].set_title("CR Bound: Poisson(λ) Estimation, n=100")
axes[0, 2].grid(True, alpha=0.3)

def log_reg_fisher(X, beta):
    p = 1 / (1 + np.exp(-X @ beta))
    W = np.diag(p * (1 - p))
    return X.T @ W @ X

np.random.seed(0)
n, d = 100, 3
X = np.random.randn(n, d)
beta_true = np.array([0.5, -0.3, 1.0])
p = 1 / (1 + np.exp(-X @ beta_true))
y = (np.random.rand(n) < p).astype(float)

F_matrix = log_reg_fisher(X, beta_true)
F_inv = np.linalg.inv(F_matrix)
se_beta = np.sqrt(np.diag(F_inv))

axes[1, 0].bar(range(d), beta_true, alpha=0.7, label="True β")
axes[1, 0].errorbar(range(d), beta_true, yerr=2*np.sqrt(np.diag(F_inv)),
                     fmt='none', color='k', capsize=5)
axes[1, 0].set_xticks(range(d))
axes[1, 0].set_xticklabels([f"β{i}" for i in range(d)])
axes[1, 0].set_ylabel("Coefficient")
axes[1, 0].set_title("Logistic Regression: CR Bounds\n(blue = 2*SE from CR)")
axes[1, 0].grid(True, axis='y', alpha=0.3)

im = axes[1, 1].imshow(F_matrix, cmap='coolwarm', interpolation='nearest')
plt.colorbar(im, ax=axes[1, 1])
axes[1, 1].set_xticks(range(d))
axes[1, 1].set_yticks(range(d))
axes[1, 1].set_xticklabels([f"β{i}" for i in range(d)])
axes[1, 1].set_yticklabels([f"β{i}" for i in range(d)])
axes[1, 1].set_title("Fisher Information Matrix\n(Logistic Regression)")

ns_sim = np.array([10, 20, 50, 100, 200, 500])
mle_var = []
for ni in ns_sim:
    mus = []
    for _ in range(2000):
        d = np.random.normal(0, 1, ni)
        mus.append(np.mean(d))
    mle_var.append(np.var(mus, ddof=1))

axes[1, 2].loglog(ns_sim, mle_var, 'o-', lw=2, label="Empirical Var(μ̂)")
axes[1, 2].loglog(ns_sim, 1/ns_sim, 's--', lw=2, label="CR bound = 1/n")
axes[1, 2].set_xlabel("n")
axes[1, 2].set_ylabel("Variance of MLE")
axes[1, 2].set_title("MLE Variance vs CR Bound\n(Normal mean estimation)")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/04-fisher-information.png")
plt.close()

print("=" * 60)
print("FISHER INFORMATION & CRAMER-RAO BOUND")
print("=" * 60)
print(f"\nNormal location parameter (known σ={sigma}):")
print(f"  MLE estimate μ̂ = {mu_hat:.4f}")
print(f"  Fisher info (n={n_samples}) = {fisher:.2f}")
print(f"  CR bound = {cr_bound:.6f}")
print(f"  Empirical variance of MLE = {sigma**2 / n_samples:.6f}")
print(f"  MLE achieves CR bound (efficient)")

print(f"\nLogistic regression (n={n}, d={d}):")
print(f"  Fisher info matrix shape = {F_matrix.shape}")
print(f"  Determinant: {np.linalg.det(F_matrix):.4f}")
print(f"  CR bounds for β: {np.round(se_beta, 4)}")

print(f"\nObserved vs Expected Fisher information:")
print(f"  Expected: I(θ) = E[-d²/dθ² log p(x|θ)]")
print(f"  Observed: J(θ) = -d²/dθ² log p(x|θ)")
print(f"\nKey properties:")
print(f"  1. Fisher info measures curvature of log-likelihood")
print(f"  2. MLE is asymptotically efficient (attains CR bound)")
print(f"  3. Fisher info is additive for i.i.d. observations")
