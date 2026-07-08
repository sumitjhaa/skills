"""03.23 Mixed Effects: Random intercept model simulation and fit."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import block_diag

np.random.seed(42)
n_groups = 20
n_per_group = 10
sigma_b = 1.5
sigma_e = 0.5
beta_0 = 2.0
beta_1 = 0.8

groups = np.repeat(range(n_groups), n_per_group)
x = np.random.normal(0, 1, n_groups * n_per_group)
b = np.random.normal(0, sigma_b, n_groups)
y = beta_0 + beta_1 * x + np.repeat(b, n_per_group) + np.random.normal(0, sigma_e, n_groups * n_per_group)

group_means = np.array([np.mean(y[groups == g]) for g in range(n_groups)])
grand_mean = np.mean(y)

MSB = n_per_group * np.var(group_means, ddof=1)
MSW = np.mean([np.var(y[groups == g], ddof=1) for g in range(n_groups)])
ICC = (MSB - MSW) / (MSB + (n_per_group - 1) * MSW)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

for g in range(n_groups):
    idx = groups == g
    axes[0, 0].plot(x[idx], y[idx], 'o', alpha=0.5, markersize=4)
    axes[0, 0].plot(x[idx], beta_0 + beta_1 * x[idx] + b[g], '-', alpha=0.3)
axes[0, 0].plot(x, beta_0 + beta_1 * x, 'k-', lw=2, label="Fixed effect (population)")
axes[0, 0].set_xlabel("x")
axes[0, 0].set_ylabel("y")
axes[0, 0].set_title(f"Group-Specific Lines (n_groups={n_groups})")
axes[0, 0].legend(fontsize=8)
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].hist(b, bins=15, density=True, alpha=0.6, color='steelblue', edgecolor='white')
x_b = np.linspace(-5, 5, 200)
axes[0, 1].plot(x_b, 1/np.sqrt(2*np.pi*sigma_b**2)*np.exp(-x_b**2/(2*sigma_b**2)),
                'r-', lw=2, label=f"N(0, σ²={sigma_b**2})")
axes[0, 1].set_xlabel("Random intercept b_g")
axes[0, 1].set_ylabel("Density")
axes[0, 1].set_title(f"Random Effects Distribution\nσ_b={sigma_b}")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

group_slopes = np.zeros(n_groups)
for g in range(n_groups):
    idx = groups == g
    A = np.column_stack([np.ones(n_per_group), x[idx]])
    coef = np.linalg.lstsq(A, y[idx], rcond=None)[0]
    group_slopes[g] = coef[1]

axes[0, 2].hist(group_slopes, bins=15, density=True, alpha=0.6, color='orange', edgecolor='white')
axes[0, 2].axvline(beta_1, color='r', lw=2, ls='--', label=f"True β₁={beta_1}")
axes[0, 2].set_xlabel("Group-specific slope")
axes[0, 2].set_ylabel("Density")
axes[0, 2].set_title("Distribution of Group Slopes")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

grand_coef = np.polyfit(x, y, 1)
grand_line = np.poly1d(grand_coef)
axes[1, 0].scatter(x, y, alpha=0.3, s=10, label="Data")
axes[1, 0].plot(np.sort(x), grand_line(np.sort(x)), 'r-', lw=2, label="OLS ignoring groups")
axes[1, 0].plot(np.sort(x), beta_0 + beta_1 * np.sort(x), 'g--', lw=2, label="True fixed effect")
axes[1, 0].set_xlabel("x")
axes[1, 0].set_ylabel("y")
axes[1, 0].set_title("Population-Level Fit (OLS vs True)")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

n_sims = 1000
icc_sim = []
for _ in range(n_sims):
    b_sim = np.random.normal(0, sigma_b, n_groups)
    e_sim = np.random.normal(0, sigma_e, n_groups * n_per_group)
    y_sim = beta_0 + beta_1 * x + np.repeat(b_sim, n_per_group) + e_sim
    gm_sim = np.array([np.mean(y_sim[groups == g]) for g in range(n_groups)])
    msb_sim = n_per_group * np.var(gm_sim, ddof=1)
    msw_sim = np.mean([np.var(y_sim[groups == g], ddof=1) for g in range(n_groups)])
    icc_sim.append((msb_sim - msw_sim) / (msb_sim + (n_per_group - 1) * msw_sim))

axes[1, 1].hist(icc_sim, bins=30, density=True, alpha=0.6, color='green', edgecolor='white')
axes[1, 1].axvline(ICC, color='k', lw=2, ls='--', label=f"Estimated ICC={ICC:.3f}")
true_icc = sigma_b**2 / (sigma_b**2 + sigma_e**2)
axes[1, 1].axvline(true_icc, color='r', lw=2, label=f"True ICC={true_icc:.3f}")
axes[1, 1].set_xlabel("ICC")
axes[1, 1].set_ylabel("Density")
axes[1, 1].set_title(f"Distribution of ICC Estimates\n(n_sim={n_sims})")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

design_effect = 1 + (n_per_group - 1) * true_icc
eff_sample = (n_groups * n_per_group) / design_effect
axes[1, 2].bar(["Actual n", "Effective n", "Design effect"], [n_groups * n_per_group, eff_sample, design_effect],
               color=['steelblue', 'coral', 'green'], alpha=0.7)
axes[1, 2].set_ylabel("Sample size")
axes[1, 2].set_title("Design Effect of Clustering")
axes[1, 2].grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/23-mixed-effects.png")
plt.close()

print("=" * 60)
print("MIXED EFFECTS (RANDOM INTERCEPT) MODEL")
print("=" * 60)
print(f"\nTrue Parameters:")
print(f"  Fixed effects: β₀={beta_0}, β₁={beta_1}")
print(f"  Random intercept SD: σ_b={sigma_b}")
print(f"  Residual SD: σ_e={sigma_e}")

print(f"\nIntraclass Correlation (ICC):")
print(f"  True ICC: {true_icc:.4f}")
print(f"  Estimated ICC: {ICC:.4f}")
print(f"  Mean simulated ICC: {np.mean(icc_sim):.4f}")
print(f"  Interpretation: {true_icc*100:.1f}% of variance is between-group")

print(f"\nDesign Effect:")
print(f"  Actual n: {n_groups * n_per_group}")
print(f"  Effective n (accounting for clustering): {eff_sample:.1f}")
print(f"  Design effect: {design_effect:.2f}")

print(f"\nGroup-level estimates:")
print(f"  Mean of group means: {np.mean(group_means):.3f}")
print(f"  SD of group means: {np.std(group_means):.3f}")
print(f"  Mean of group slopes: {np.mean(group_slopes):.3f}")

print(f"\nOLS (ignoring groups):")
print(f"  Slope: {grand_coef[0]:.4f}, Intercept: {grand_coef[1]:.4f}")
print(f"  (Should be similar to β₁={beta_1} due to balanced design)")
