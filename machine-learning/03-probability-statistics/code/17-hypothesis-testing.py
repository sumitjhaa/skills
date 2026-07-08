"""03.17 Hypothesis Testing: t-test, Wald test, LRT."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t, norm, chi2, f as f_dist

np.random.seed(42)

n1, n2 = 30, 30
mu1, mu2 = 0, 0.8
sigma = 1.0
x1 = np.random.normal(mu1, sigma, n1)
x2 = np.random.normal(mu2, sigma, n2)

sp = np.sqrt(((n1-1)*np.var(x1, ddof=1) + (n2-1)*np.var(x2, ddof=1)) / (n1+n2-2))
t_stat = (np.mean(x2) - np.mean(x1)) / (sp * np.sqrt(1/n1 + 1/n2))
df = n1 + n2 - 2
p_val = 2 * (1 - t.cdf(np.abs(t_stat), df))

print("=" * 60)
print("HYPOTHESIS TESTING")
print("=" * 60)
print("\nTwo-sample t-test:")
print(f"  Group 1: mean={np.mean(x1):.3f}, var={np.var(x1, ddof=1):.3f}")
print(f"  Group 2: mean={np.mean(x2):.3f}, var={np.var(x2, ddof=1):.3f}")
print(f"  Pooled SE: {sp:.4f}")
print(f"  t = {t_stat:.4f}, df = {df}, p = {p_val:.6f}")
print(f"  Significant at α=0.05: {p_val < 0.05}")

effect_sizes = np.linspace(0, 2, 50)
alpha = 0.05
power = []
for es in effect_sizes:
    reject = 0
    for _ in range(2000):
        x1b = np.random.normal(0, sigma, n1)
        x2b = np.random.normal(es, sigma, n2)
        spb = np.sqrt(((n1-1)*np.var(x1b,ddof=1)+(n2-1)*np.var(x2b,ddof=1))/(n1+n2-2))
        tb = (np.mean(x2b)-np.mean(x1b)) / (spb*np.sqrt(1/n1+1/n2))
        if np.abs(tb) > t.ppf(1-alpha/2, df):
            reject += 1
    power.append(reject / 2000)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].plot(effect_sizes, power, lw=2)
axes[0, 0].axhline(0.8, color='r', linestyle='--', label="80% power")
axes[0, 0].axvline(0.8, color='gray', linestyle=':', label=f"True δ={mu2-mu1}")
axes[0, 0].set_xlabel("Effect size (Cohen's d)")
axes[0, 0].set_ylabel("Power")
axes[0, 0].set_title("Power Curve: Two-Sample t-Test")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)
power_at_true = power[int(0.8/2*49)]
print(f"  Power at δ=0.8: {power_at_true:.3f}")
print(f"  Sample size needed for 80% power at δ=0.8: ~{2*((t.ppf(1-alpha/2, df)+t.ppf(0.8, df))/0.8)**2:.0f}")

ns_sim = [10, 20, 50, 100, 200]
power_by_n = []
for ni in ns_sim:
    reject = 0
    for _ in range(2000):
        x1b = np.random.normal(0, sigma, ni)
        x2b = np.random.normal(0.5, sigma, ni)
        spb = np.sqrt(((ni-1)*np.var(x1b,ddof=1)+(ni-1)*np.var(x2b,ddof=1))/(2*ni-2))
        tb = (np.mean(x2b)-np.mean(x1b)) / (spb*np.sqrt(2/ni))
        if np.abs(tb) > t.ppf(1-alpha/2, 2*ni-2):
            reject += 1
    power_by_n.append(reject / 2000)

axes[0, 1].plot(ns_sim, power_by_n, 'o-', lw=2)
axes[0, 1].axhline(0.8, color='r', ls='--')
axes[0, 1].set_xlabel("n per group")
axes[0, 1].set_ylabel("Power")
axes[0, 1].set_title("Power vs Sample Size (δ=0.5)")
axes[0, 1].grid(True, alpha=0.3)

n_wald = 200
x_wald = np.random.normal(0.2, 1, n_wald)
mu_wald = np.mean(x_wald)
se_wald = np.std(x_wald, ddof=1) / np.sqrt(n_wald)
wald_stat = mu_wald / se_wald
wald_p = 2 * (1 - norm.cdf(np.abs(wald_stat)))

print(f"\nWald test (H₀: μ=0):")
print(f"  μ̂ = {mu_wald:.4f}, SE = {se_wald:.4f}")
print(f"  Wald Z = {wald_stat:.4f}, p = {wald_p:.4f}")

n_binom = 100
y_binom = 35
p_hat = y_binom / n_binom
p0 = 0.5
se_w = np.sqrt(p_hat * (1 - p_hat) / n_binom)
wald_binom = (p_hat - p0) / se_w
wald_p_binom = 2 * (1 - norm.cdf(np.abs(wald_binom)))

print(f"\nWald test for binomial proportion (H₀: p=0.5):")
print(f"  p̂ = {p_hat:.4f}, observed {y_binom}/{n_binom}")
print(f"  Wald Z = {wald_binom:.4f}, p = {wald_p_binom:.4f}")

null_ll = y_binom * np.log(p0) + (n_binom - y_binom) * np.log(1 - p0)
alt_ll = y_binom * np.log(p_hat) + (n_binom - y_binom) * np.log(1 - p_hat)
lrt_stat = -2 * (null_ll - alt_ll)
lrt_p = 1 - chi2.cdf(lrt_stat, 1)

print(f"  LRT statistic = {lrt_stat:.4f}, p = {lrt_p:.4f}")

p_grid = np.linspace(0.01, 0.99, 100)
log_lik = y_binom * np.log(p_grid) + (n_binom - y_binom) * np.log(1 - p_grid)
lrt_stat_grid = -2 * (log_lik.max() - log_lik)

axes[0, 2].plot(p_grid, log_lik, lw=2)
axes[0, 2].axvline(p_hat, color='r', ls='--', label=f"MLE p̂={p_hat:.3f}")
axes[0, 2].axvline(p0, color='g', ls='--', label=f"H₀ p₀={p0}")
axes[0, 2].set_xlabel("p")
axes[0, 2].set_ylabel("Log-likelihood")
axes[0, 2].set_title("Binomial Log-Likelihood\nfor Wald Test")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

p_types = ["t-test\n(p)", "Wald\n(p)", "LRT\n(p)"]
p_vals_plot = [p_val, wald_p_binom, lrt_p]
colors_plot = ['red' if p < 0.05 else 'green' for p in p_vals_plot]
axes[1, 0].bar(p_types, p_vals_plot, color=colors_plot, alpha=0.7)
axes[1, 0].axhline(0.05, color='k', ls='--', label="α=0.05")
axes[1, 0].set_ylabel("p-value")
axes[1, 0].set_title("p-value Comparison")
axes[1, 0].legend()
axes[1, 0].grid(True, axis='y', alpha=0.3)

p_values = []
for _ in range(5000):
    x1_null = np.random.normal(0, sigma, n1)
    x2_null = np.random.normal(0, sigma, n2)
    sp_null = np.sqrt(((n1-1)*np.var(x1_null,ddof=1)+(n2-1)*np.var(x2_null,ddof=1))/(n1+n2-2))
    t_null = (np.mean(x2_null)-np.mean(x1_null)) / (sp_null*np.sqrt(1/n1+1/n2))
    p_values.append(2 * (1 - t.cdf(np.abs(t_null), df)))

axes[1, 1].hist(p_values, bins=50, density=True, alpha=0.6)
axes[1, 1].axhline(1.0, color='r', ls='--', label="Uniform(0,1)")
axes[1, 1].set_xlabel("p-value")
axes[1, 1].set_ylabel("Density")
axes[1, 1].set_title("Distribution of p-values\nunder H₀ (should be uniform)")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

f_grid = np.linspace(0, 5, 200)
f_pdf = f_dist.pdf(f_grid, 1, 98)
axes[1, 2].plot(f_grid, f_pdf, 'b-', lw=2)
crit_val = f_dist.ppf(0.95, 1, 98)
axes[1, 2].fill_between(f_grid, 0, f_pdf, where=(f_grid >= crit_val), alpha=0.3, color='red')
axes[1, 2].axvline(crit_val, color='r', ls='--', label=f"F₀.₀₅({1},{98})={crit_val:.2f}")
axes[1, 2].set_xlabel("F-statistic")
axes[1, 2].set_ylabel("Density")
axes[1, 2].set_title("F-Distribution (df₁=1, df₂=98)")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/17-hypothesis-testing.png")
plt.close()

print(f"\nType I error rate (estimated): {np.mean(np.array(p_values) < 0.05):.4f} (should be 0.05)")
print("\nHypothesis testing plots saved.")
