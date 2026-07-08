#!/usr/bin/env python3
"""03.40 Full Bayesian Workflow: Prior predictive → Posterior → PPC."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
n = 100

# Generate data from true model
mu_true, sigma_true = 3.0, 1.5
data = np.random.normal(mu_true, sigma_true, n)

# 1. Prior predictive simulation
n_sims = 5000
mu_prior = np.random.normal(0, 10, n_sims)
sigma_prior = np.abs(np.random.normal(0, 3, n_sims))

# Simulate from prior
prior_pred = np.random.normal(mu_prior[:, None], sigma_prior[:, None], (n_sims, n))

# Check: min, max, sd of prior predictive
prior_min = prior_pred.min(axis=1)
prior_max = prior_pred.max(axis=1)
prior_sd = prior_pred.std(axis=1)

print("Prior Predictive Checks:")
print(f"  Observed range: [{data.min():.1f}, {data.max():.1f}]")
print(f"  Prior predictive 95% min interval: [{np.percentile(prior_min, 2.5):.1f}, {np.percentile(prior_min, 97.5):.1f}]")
print(f"  Prior predictive 95% max interval: [{np.percentile(prior_max, 2.5):.1f}, {np.percentile(prior_max, 97.5):.1f}]")

# 2. Simple Metropolis-Hastings for posterior (normal model)
# Prior: μ ~ N(0, 10), σ ~ Half-Normal(3)
mu = 0.0
sigma = 2.0
n_iter = 10000
mu_chain = np.zeros(n_iter)
sigma_chain = np.zeros(n_iter)
accept = 0

for i in range(n_iter):
    # Propose
    mu_star = mu + np.random.normal(0, 0.5)
    sigma_star = sigma + np.random.normal(0, 0.3)
    if sigma_star <= 0:
        mu_chain[i] = mu
        sigma_chain[i] = sigma
        continue
    
    # Log-posterior (up to constant)
    log_lik = np.sum(-np.log(sigma_star) - 0.5*((data - mu_star)/sigma_star)**2)
    log_lik_curr = np.sum(-np.log(sigma) - 0.5*((data - mu)/sigma)**2)
    log_prior_mu = -0.5*(mu_star/10)**2 + 0.5*(mu/10)**2
    log_prior_sigma = -0.5*(sigma_star/3)**2 + 0.5*(sigma/3)**2  # approx
    
    log_r = log_lik - log_lik_curr + log_prior_mu + log_prior_sigma
    if np.log(np.random.uniform()) < log_r:
        mu = mu_star
        sigma = sigma_star
        accept += 1
    
    mu_chain[i] = mu
    sigma_chain[i] = sigma

# 3. Posterior predictive check
post_mu = mu_chain[int(n_iter/2):]
post_sigma = sigma_chain[int(n_iter/2):]
n_ppc = 2000
idx = np.random.choice(len(post_mu), n_ppc)
ppc_data = np.random.normal(post_mu[idx, None], post_sigma[idx, None], (n_ppc, n))

# Test statistic: mean and skewness
obs_mean = np.mean(data)
obs_sd = np.std(data)
ppc_mean = np.mean(ppc_data, axis=1)
ppc_sd = np.std(ppc_data, axis=1)

print(f"\nPosterior Summaries (MCMC):")
print(f"  μ: mean={np.mean(post_mu):.2f}, SD={np.std(post_mu):.2f}")
print(f"  σ: mean={np.mean(post_sigma):.2f}, SD={np.std(post_sigma):.2f}")
print(f"  Acceptance rate: {accept/n_iter:.2f}")

print(f"\nPosterior Predictive Check:")
print(f"  Observed mean: {obs_mean:.2f}")
print(f"  PPC mean (95% interval): [{np.percentile(ppc_mean, 2.5):.2f}, {np.percentile(ppc_mean, 97.5):.2f}]")
print(f"  Posterior predictive p-value (mean): {np.mean(ppc_mean >= obs_mean):.3f}")

# Visualization
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
axes[0, 0].plot(mu_chain, alpha=0.5)
axes[0, 0].axhline(mu_true, color='r')
axes[0, 0].set_title("μ Chain")
axes[0, 0].set_xlabel("Iteration")
axes[0, 1].plot(sigma_chain, alpha=0.5)
axes[0, 1].axhline(sigma_true, color='r')
axes[0, 1].set_title("σ Chain")
axes[0, 1].set_xlabel("Iteration")

axes[0, 2].hist(prior_min, bins=40, alpha=0.5, label="Prior")
axes[0, 2].axvline(data.min(), color='r', lw=2, label="Observed")
axes[0, 2].set_title("Prior Predictive: Min")
axes[0, 2].legend()

axes[1, 0].hist(post_mu, bins=50, density=True, alpha=0.6)
axes[1, 0].axvline(mu_true, color='r', lw=2)
axes[1, 0].set_title("Posterior μ")
axes[1, 0].set_xlabel("μ")

axes[1, 1].hist(post_sigma, bins=50, density=True, alpha=0.6)
axes[1, 1].axvline(sigma_true, color='r', lw=2)
axes[1, 1].set_title("Posterior σ")
axes[1, 1].set_xlabel("σ")

axes[1, 2].hist(ppc_mean, bins=50, alpha=0.6, label="PPC")
axes[1, 2].axvline(obs_mean, color='r', lw=2, label="Observed")
axes[1, 2].set_title(f"PPC: Mean (p={np.mean(ppc_mean >= obs_mean):.3f})")
axes[1, 2].legend()

plt.tight_layout()
plt.savefig("../../assets/phase03/40-bayesian-workflow.png")
plt.close()
print("\nFull Bayesian workflow complete: prior → posterior → PPC.")
