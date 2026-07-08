"""03.16 Bayesian Inference: Conjugate Beta-Binomial model."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta, binom, norm

np.random.seed(42)
n, y = 20, 7
alpha_prior, beta_prior = 2, 2

prior = beta(alpha_prior, beta_prior)
alpha_post = alpha_prior + y
beta_post = beta_prior + n - y
posterior = beta(alpha_post, beta_post)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

theta = np.linspace(0, 1, 300)
axes[0, 0].plot(theta, prior.pdf(theta), 'b-', lw=2, label=f"Beta({alpha_prior},{beta_prior}) Prior")
axes[0, 0].plot(theta, posterior.pdf(theta), 'r-', lw=2, label=f"Beta({alpha_post},{beta_post}) Posterior")
lik = binom.pmf(y, n, theta)
lik /= np.trapezoid(lik, theta)
axes[0, 0].plot(theta, lik, 'g--', lw=2, label="Scaled Likelihood")
axes[0, 0].set_xlabel("θ")
axes[0, 0].set_ylabel("Density")
axes[0, 0].set_title(f"Bayesian Inference: Binomial(n={n}, y={y})")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

prior_mean = alpha_prior / (alpha_prior + beta_prior)
post_mean = alpha_post / (alpha_post + beta_post)
mle = y / n

axes[0, 1].bar(["Prior Mean", "Posterior Mean", "MLE"],
               [prior_mean, post_mean, mle],
               color=['blue', 'red', 'green'], alpha=0.7)
axes[0, 1].axhline(post_mean, color='k', ls='--', alpha=0.3)
for i, v in enumerate([prior_mean, post_mean, mle]):
    axes[0, 1].text(i, v + 0.01, f"{v:.3f}", ha='center', fontsize=10)
axes[0, 1].set_ylabel("θ estimate")
axes[0, 1].set_title("Point Estimates Comparison")
axes[0, 1].grid(True, axis='y', alpha=0.3)

ns_sim = np.arange(5, 101, 5)
post_means = []
post_vars = []
mles = []
for ni in ns_sim:
    yi = np.random.binomial(ni, 0.4)
    api = 2 + yi
    bpi = 2 + ni - yi
    post_means.append(api / (api + bpi))
    post_vars.append(api * bpi / ((api + bpi)**2 * (api + bpi + 1)))
    mles.append(yi / ni)

axes[1, 0].plot(ns_sim, post_means, 'o-', label="Posterior mean", lw=2)
axes[1, 0].plot(ns_sim, mles, 's-', label="MLE", lw=2)
axes[1, 0].axhline(0.4, color='r', ls='--', label="True θ=0.4")
axes[1, 0].set_xlabel("n")
axes[1, 0].set_ylabel("θ estimate")
axes[1, 0].set_title("Posterior Mean vs MLE as n grows")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

post_var = posterior.var()
hpd_lower = posterior.ppf(0.025)
hpd_upper = posterior.ppf(0.975)
cred_width = hpd_upper - hpd_lower

theta_fine = np.linspace(0, 1, 500)
post_fine = posterior.pdf(theta_fine)
axes[1, 1].plot(theta_fine, post_fine, 'r-', lw=2, label="Posterior PDF")
axes[1, 1].fill_between(theta_fine, 0, post_fine,
                         where=(theta_fine >= hpd_lower) & (theta_fine <= hpd_upper),
                         alpha=0.3, color='red', label="95% Credible Interval")
axes[1, 1].axvline(hpd_lower, color='k', ls='--')
axes[1, 1].axvline(hpd_upper, color='k', ls='--')
axes[1, 1].set_xlabel("θ")
axes[1, 1].set_ylabel("Density")
axes[1, 1].set_title("95% Credible Interval")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/16-bayesian-inference.png")
plt.close()

print("=" * 60)
print("BAYESIAN INFERENCE: BETA-BINOMIAL CONJUGATE")
print("=" * 60)
print(f"Data: {y} successes in {n} trials")
print(f"\nPrior: Beta({alpha_prior}, {beta_prior})")
print(f"  Prior mean: {prior_mean:.4f}")
print(f"  Prior variance: {prior.var():.4f}")

print(f"\nPosterior: Beta({alpha_post}, {beta_post})")
print(f"  Posterior mean:   {post_mean:.4f}")
print(f"  Posterior variance: {post_var:.4f}")
print(f"  Posterior SD: {np.sqrt(post_var):.4f}")
print(f"  95% credible interval: [{hpd_lower:.4f}, {hpd_upper:.4f}]")
print(f"  Credible interval width: {cred_width:.4f}")

print(f"\nMLE (frequentist): {mle:.4f}")
print(f"  MLE 95% CI (approx): [{mle - 1.96*np.sqrt(mle*(1-mle)/n):.4f}, {mle + 1.96*np.sqrt(mle*(1-mle)/n):.4f}]")

print(f"\nKey insight: Posterior mean is a weighted average of prior mean and MLE")
print(f"  w_prior = {alpha_prior + beta_prior}/{alpha_prior + beta_prior + n} = {(alpha_prior+beta_prior)/(alpha_prior+beta_prior+n):.3f}")
print(f"  w_data = {n}/{alpha_prior + beta_prior + n} = {n/(alpha_prior+beta_prior+n):.3f}")
weighted = (alpha_prior+beta_prior)/(alpha_prior+beta_prior+n) * prior_mean + n/(alpha_prior+beta_prior+n) * mle
print(f"  Weighted avg: {weighted:.4f} = posterior mean? {np.isclose(weighted, post_mean)}")
