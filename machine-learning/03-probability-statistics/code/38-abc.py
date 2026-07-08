#!/usr/bin/env python3
"""03.38 ABC: Approximate Bayesian Computation for a simple model."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# True parameter
theta_true = 2.0

def simulate(theta):
    """Simulate from model: X ~ N(θ, 1), n=50"""
    return np.random.normal(theta, 1, 50)

# Observed data
x_obs = simulate(theta_true)
obs_stat = np.mean(x_obs)

# Rejection ABC
n_sims = 50000
accepted = []
eps = 0.2

for i in range(n_sims):
    theta_star = np.random.uniform(-5, 8)
    x_star = simulate(theta_star)
    sim_stat = np.mean(x_star)
    if np.abs(sim_stat - obs_stat) <= eps:
        accepted.append(theta_star)

accepted = np.array(accepted)

# ABC posterior
theta_grid = np.linspace(-2, 5, 200)
prior = np.ones_like(theta_grid) / 7  # Uniform(-5, 8)

plt.figure(figsize=(10, 5))
plt.subplot(121)
plt.hist(accepted, bins=40, density=True, alpha=0.6, label="ABC posterior")
plt.axvline(theta_true, color='r', lw=2, label=f"True θ={theta_true}")
plt.axvline(obs_stat, color='g', ls='--', lw=2, label=f"Observed mean={obs_stat:.2f}")
plt.axvline(np.mean(accepted), color='k', ls=':', lw=2, label=f"Posterior mean={np.mean(accepted):.2f}")
plt.xlabel("θ")
plt.ylabel("Density")
plt.title(f"ABC: ε={eps}, accepted={len(accepted)}/{n_sims} ({100*len(accepted)/n_sims:.1f}%)")
plt.legend()
plt.grid(True)

# ε sensitivity
eps_grid = np.linspace(0.05, 0.5, 10)
accept_rates = []
posterior_means = []
for e in eps_grid:
    acc = []
    for i in range(10000):
        theta = np.random.uniform(-5, 8)
        sim = simulate(theta)
        if np.abs(np.mean(sim) - obs_stat) <= e:
            acc.append(theta)
    accept_rates.append(len(acc)/10000)
    posterior_means.append(np.mean(acc) if acc else 0)

plt.subplot(122)
plt.plot(eps_grid, accept_rates, 'o-', label="Acceptance rate")
plt.plot(eps_grid, posterior_means, 's-', label="Posterior mean")
plt.axhline(theta_true, color='r', ls='--', label=f"True θ={theta_true}")
plt.xlabel("ε")
plt.ylabel("Value")
plt.title("ABC: ε Sensitivity")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("../../assets/phase03/38-abc.png")
plt.close()

print(f"ABC posterior mean: {np.mean(accepted):.3f}")
print(f"True parameter: {theta_true}")
print(f"Data sample mean: {obs_stat:.3f}")
