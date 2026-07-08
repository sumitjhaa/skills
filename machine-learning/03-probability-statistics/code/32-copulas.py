"""03.32 Copulas: Gaussian and Clayton copula simulation."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, kendalltau, t as t_dist, chi2

np.random.seed(42)
n = 1000
rho = 0.7

Z = np.random.multivariate_normal([0, 0], [[1, rho], [rho, 1]], n)
U_gauss = norm.cdf(Z)

theta = 2.0
V = np.random.gamma(1/theta, 1, n)
U1_clay = np.random.uniform(0, 1, n)
U2_clay = (1 - np.log(U1_clay) / V) ** (-1/theta)

df_t = 4
Z_t = np.random.multivariate_normal([0, 0], [[1, rho], [rho, 1]], n)
chi2_samples = np.random.chisquare(df_t, n)
U_t = t_dist.cdf(Z_t / np.sqrt(chi2_samples[:, None] / df_t), df_t)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].scatter(U_gauss[:, 0], U_gauss[:, 1], s=2, alpha=0.4)
axes[0, 0].set_title(f"Gaussian Copula (ρ={rho})")
axes[0, 0].set_xlabel("U₁")
axes[0, 0].set_ylabel("U₂")
axes[0, 0].set_xlim(0, 1)
axes[0, 0].set_ylim(0, 1)
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].scatter(U1_clay, U2_clay, s=2, alpha=0.4)
axes[0, 1].set_title(f"Clayton Copula (θ={theta})")
axes[0, 1].set_xlabel("U₁")
axes[0, 1].set_ylabel("U₂")
axes[0, 1].set_xlim(0, 1)
axes[0, 1].set_ylim(0, 1)
axes[0, 1].grid(True, alpha=0.3)

axes[0, 2].scatter(U_t[:, 0], U_t[:, 1], s=2, alpha=0.4)
axes[0, 2].set_title(f"t-Copula (ρ={rho}, ν={df_t})")
axes[0, 2].set_xlabel("U₁")
axes[0, 2].set_ylabel("U₂")
axes[0, 2].set_xlim(0, 1)
axes[0, 2].set_ylim(0, 1)
axes[0, 2].grid(True, alpha=0.3)

Z_gauss = norm.ppf(U_gauss)
Z_clay = np.column_stack([norm.ppf(U1_clay), norm.ppf(U2_clay)])
Z_t_marg = np.column_stack([norm.ppf(U_t[:, 0]), norm.ppf(U_t[:, 1])])

axes[1, 0].scatter(Z_gauss[:, 0], Z_gauss[:, 1], s=2, alpha=0.4)
axes[1, 0].set_title("Gaussian: N(0,1) margins")
axes[1, 0].set_xlabel("Z₁")
axes[1, 0].set_ylabel("Z₂")
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].scatter(Z_clay[:, 0], Z_clay[:, 1], s=2, alpha=0.4)
axes[1, 1].set_title("Clayton: N(0,1) margins\n(upper tail dependence)")
axes[1, 1].set_xlabel("Z₁")
axes[1, 1].set_ylabel("Z₂")
axes[1, 1].grid(True, alpha=0.3)

axes[1, 2].scatter(Z_t_marg[:, 0], Z_t_marg[:, 1], s=2, alpha=0.4)
axes[1, 2].set_title("t-Copula: N(0,1) margins\n(upper+lower tail)"
                      , fontsize=10)
axes[1, 2].set_xlabel("Z₁")
axes[1, 2].set_ylabel("Z₂")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/32-copulas.png")
plt.close()

print("=" * 60)
print("COPULA ANALYSIS")
print("=" * 60)

tau_gauss, _ = kendalltau(U_gauss[:, 0], U_gauss[:, 1])
tau_clay, _ = kendalltau(U1_clay, U2_clay)
tau_t, _ = kendalltau(U_t[:, 0], U_t[:, 1])

tau_gauss_theory = 2/np.pi * np.arcsin(rho)
tau_clay_theory = theta / (theta + 2)
tau_t_theory = 2/np.pi * np.arcsin(rho)

print(f"\n{'Copula':<20s} {'Kendall τ':>12s} {'Theoretical':>12s}")
print("-" * 44)
print(f"{'Gaussian':<20s} {tau_gauss:>12.4f} {tau_gauss_theory:>12.4f}")
print(f"{'Clayton':<20s} {tau_clay:>12.4f} {tau_clay_theory:>12.4f}")
print(f"{'t-copula':<20s} {tau_t:>12.4f} {tau_t_theory:>12.4f}")

print(f"\nTail dependence:")
print(f"  Gaussian:   λ_u = λ_l = 0 (no tail dependence)")
print(f"  Clayton:    λ_u = {2**(-1/theta):.4f}, λ_l = 0 (upper tail only)")
print(f"  t-copula:   λ_u = λ_l = {2 * t_dist.cdf(-np.sqrt((df_t+1)*(1-rho)/(1+rho)), df_t+1):.4f}")

print(f"\nSklar's theorem: Any multivariate distribution can be")
print(f"decomposed into marginal distributions + a copula.")
