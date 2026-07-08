"""03.24 Bayesian Linear Regression: Conjugate analysis."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t as t_dist, norm, invgamma, multivariate_normal

np.random.seed(42)
n = 100
X = np.random.normal(0, 1, n)
beta_true = 2.0
sigma_true = 0.5
y = beta_true * X + np.random.normal(0, sigma_true, n)

tau2 = 10.0
nu0 = 1.0
sigma2_0 = 1.0

X_mat = X.reshape(-1, 1)
beta_ols = np.linalg.lstsq(X_mat, y, rcond=None)[0][0]
sse = np.sum((y - X_mat @ [beta_ols])**2)
sigma2_ols = sse / (n - 1)

beta_grid = np.linspace(1.5, 2.5, 500)
prior_beta = norm.pdf(beta_grid, 0, np.sqrt(tau2))
likelihood_beta = np.array([np.exp(-0.5/sigma_true**2 * np.sum((y - b*X)**2)) for b in beta_grid])
posterior_beta = prior_beta * likelihood_beta
posterior_beta /= np.trapezoid(posterior_beta, beta_grid)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].plot(beta_grid, prior_beta, 'b-', lw=2, label=f"Prior N(0,{tau2})")
axes[0, 0].plot(beta_grid, likelihood_beta / np.trapezoid(likelihood_beta, beta_grid),
                'g--', lw=2, label="Scaled Likelihood")
axes[0, 0].plot(beta_grid, posterior_beta, 'r-', lw=2, label="Posterior")
axes[0, 0].axvline(beta_ols, color='gray', ls=':', lw=2, label=f"OLS={beta_ols:.3f}")
post_mean_bayes = np.trapezoid(beta_grid * posterior_beta, beta_grid)
axes[0, 0].axvline(post_mean_bayes, color='k', ls='--', lw=2, label=f"Post mean={post_mean_bayes:.3f}")
axes[0, 0].set_xlabel("β")
axes[0, 0].set_ylabel("Density")
axes[0, 0].set_title("Bayesian Linear Regression\nKnown σ²")
axes[0, 0].legend(fontsize=8)
axes[0, 0].grid(True, alpha=0.3)

post_var_bayes = np.trapezoid((beta_grid - post_mean_bayes)**2 * posterior_beta, beta_grid)
post_sd_bayes = np.sqrt(post_var_bayes)

Lambda_n = 1/tau2 + X @ X / sigma_true**2
beta_n = (1/tau2 * 0 + X @ y / sigma_true**2) / Lambda_n
sigma_n = np.sqrt(1 / Lambda_n)

print(f"Conjugate update: β|y ~ N({beta_n:.4f}, {sigma_n**2:.4f})")

sigma2_grid = np.linspace(0.05, 0.8, 300)
prior_sigma2 = invgamma.pdf(sigma2_grid, a=nu0/2, scale=nu0*sigma2_0/2)
axes[0, 1].plot(sigma2_grid, prior_sigma2, 'b-', lw=2, label=f"Inv-χ²({nu0},{sigma2_0})")
nu_n = nu0 + n
sigma2_n = (nu0*sigma2_0 + sse) / nu_n
post_sigma2 = invgamma.pdf(sigma2_grid, a=nu_n/2, scale=nu_n*sigma2_n/2)
axes[0, 1].plot(sigma2_grid, post_sigma2, 'r-', lw=2, label=f"Posterior Inv-χ²({nu_n})")
axes[0, 1].axvline(sigma_true**2, color='k', ls='--', lw=2, label=f"True σ²={sigma_true**2}")
axes[0, 1].set_xlabel("σ²")
axes[0, 1].set_ylabel("Density")
axes[0, 1].set_title("Posterior for σ²\n(Inv-Chi-Squared)")
axes[0, 1].legend(fontsize=8)
axes[0, 1].grid(True, alpha=0.3)

joint_beta_sigma = posterior_beta[:, None] * post_sigma2[None, :]
axes[0, 2].contourf(beta_grid, sigma2_grid, joint_beta_sigma.T, levels=20, cmap='viridis')
axes[0, 2].set_xlabel("β")
axes[0, 2].set_ylabel("σ²")
axes[0, 2].set_title("Joint Posterior\nβ and σ²")
plt.colorbar(axes[0, 2].collections[0], ax=axes[0, 2], label="Density")

tau2_values = [0.1, 1, 10, 100]
for tau2i in tau2_values:
    prior_i = norm.pdf(beta_grid, 0, np.sqrt(tau2i))
    post_i = prior_i * likelihood_beta
    post_i /= np.trapezoid(post_i, beta_grid)
    axes[1, 0].plot(beta_grid, post_i, lw=2, label=f"τ²={tau2i}")
axes[1, 0].axvline(beta_ols, color='k', ls='--', label=f"OLS={beta_ols:.3f}")
axes[1, 0].set_xlabel("β")
axes[1, 0].set_ylabel("Posterior density")
axes[1, 0].set_title("Effect of Prior Variance")
axes[1, 0].legend(fontsize=7)
axes[1, 0].grid(True, alpha=0.3)
print(f"\nPrior sensitivity:")

prior_means = []
for tau2i in tau2_values:
    prior_i = norm.pdf(beta_grid, 0, np.sqrt(tau2i))
    post_i = prior_i * likelihood_beta
    post_i /= np.trapezoid(post_i, beta_grid)
    pm = np.trapezoid(beta_grid * post_i, beta_grid)
    prior_means.append(pm)
    print(f"  τ²={tau2i:5.0f}: posterior mean = {pm:.4f}")

n_prior = 5
post_predictive = np.zeros((len(beta_grid), n_prior))
for i in range(n_prior):
    b_draw = np.random.choice(beta_grid, p=posterior_beta/np.sum(posterior_beta))
    y_pred = b_draw * X[:n_prior] + np.random.normal(0, sigma_true, n_prior)
    axes[1, 1].plot(range(n_prior), y_pred, 'o-', alpha=0.5)

axes[1, 1].plot(range(n_prior), y[:n_prior], 'ks-', lw=2, markersize=8, label="Observed")
axes[1, 1].set_xlabel("Index")
axes[1, 1].set_ylabel("y")
axes[1, 1].set_title("Posterior Predictive\n(first 5 observations)")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

post_std_beta = np.sqrt(post_var_bayes)
cred_low = post_mean_bayes - 2*post_std_beta
cred_high = post_mean_bayes + 2*post_std_beta
beta_hist = np.random.normal(post_mean_bayes, post_std_beta, 10000)
axes[1, 2].hist(beta_hist, bins=50, density=True, alpha=0.6, color='steelblue')
axes[1, 2].axvline(beta_true, color='g', lw=2, label=f"True β={beta_true}")
axes[1, 2].axvline(post_mean_bayes, color='r', lw=2, ls='--', label=f"Post mean={post_mean_bayes:.3f}")
axes[1, 2].axvline(cred_low, color='k', ls=':', label=f"95% CI ({cred_low:.2f}, {cred_high:.2f})")
axes[1, 2].axvline(cred_high, color='k', ls=':')
axes[1, 2].set_xlabel("β")
axes[1, 2].set_ylabel("Density")
axes[1, 2].set_title("Posterior Distribution of β\nwith 95% Credible Interval")
axes[1, 2].legend(fontsize=7)
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/24-bayesian-linear-regression.png")
plt.close()

print("\n" + "=" * 60)
print("BAYESIAN LINEAR REGRESSION")
print("=" * 60)
print(f"\nOLS estimate: {beta_ols:.4f}")
print(f"Posterior mean: {post_mean_bayes:.4f}")
print(f"Posterior SD: {post_sd_bayes:.4f}")
print(f"95% Credible interval: [{cred_low:.4f}, {cred_high:.4f}]")
print(f"True β: {beta_true}")

print(f"\nShrinkage: OLS estimate shrunk toward prior mean (0)")
print(f"  Shrinkage factor: {1 - post_mean_bayes/beta_ols:.4f}")
print(f"  Effective prior strength: 1/τ² = {1/tau2:.2f}")
