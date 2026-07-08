"""03.34 Missing Data: MCAR/MAR mechanisms and multiple imputation demo."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

np.random.seed(42)
n = 500

X1 = np.random.normal(0, 1, n)
X2 = 0.5 * X1 + np.random.normal(0, 0.5, n)
y = 0.8 * X1 + 1.2 * X2 + np.random.normal(0, 0.3, n)

mask_mcar = np.random.binomial(1, 0.3, n).astype(bool)
X1_mcar = X1.copy()
X1_mcar[mask_mcar] = np.nan

logit_p = -1 + 0.8 * X2
p_mar = 1 / (1 + np.exp(-logit_p))
mask_mar = np.random.binomial(1, p_mar, n).astype(bool)
X1_mar = X1.copy()
X1_mar[mask_mar] = np.nan

X1_mcar_mean = X1_mcar.copy()
X1_mcar_mean[np.isnan(X1_mcar_mean)] = np.nanmean(X1_mcar_mean)
X1_mar_mean = X1_mar.copy()
X1_mar_mean[np.isnan(X1_mar_mean)] = np.nanmean(X1_mar_mean)

def fit_coefs(X, y):
    Xc = X.copy()
    if np.any(np.isnan(Xc)):
        Xc[np.isnan(Xc)] = np.nanmean(Xc)
    Xm = np.column_stack([np.ones(len(y)), Xc])
    return np.linalg.lstsq(Xm, y, rcond=None)[0]

coef_true = fit_coefs(np.column_stack([X1, X2]), y)
coef_mcar_complete = fit_coefs(np.column_stack([X1_mcar, X2])[~mask_mcar], y[~mask_mcar])
coef_mcar_impute = fit_coefs(np.column_stack([X1_mcar_mean, X2]), y)

n_imputations = 50
imputed_coefs = np.zeros((n_imputations, 3))
for m in range(n_imputations):
    X1_imp = X1_mar.copy()
    missing_idx = np.where(np.isnan(X1_mar))[0]
    observed_idx = np.where(~np.isnan(X1_mar))[0]
    mu_obs = np.mean(X1_mar[observed_idx])
    std_obs = np.std(X1_mar[observed_idx], ddof=1)
    X1_imp[missing_idx] = np.random.normal(mu_obs, std_obs, len(missing_idx))
    coef_imp = fit_coefs(np.column_stack([X1_imp, X2]), y)
    imputed_coefs[m] = coef_imp

pooled_mean = np.mean(imputed_coefs, axis=0)
within_var = np.mean(np.var(imputed_coefs, axis=0, ddof=1))
between_var = np.var(imputed_coefs, axis=0, ddof=1)
total_var = within_var + (1 + 1/n_imputations) * between_var
rubin_se = np.sqrt(total_var)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

for ax, mask, label, color in zip(
    [axes[0, 0], axes[0, 1]],
    [mask_mcar, mask_mar],
    ["MCAR", "MAR"],
    ['blue', 'red']
):
    ax.scatter(X1[~mask], y[~mask], alpha=0.4, s=15, label="Observed", color='steelblue')
    ax.scatter(X1[mask], y[mask], alpha=0.4, marker='x', s=20, label="Missing", color='coral')
    ax.set_xlabel("X₁")
    ax.set_ylabel("y")
    ax.set_title(f"{label}: {mask.mean():.0%} missing")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

axes[0, 2].hist(imputed_coefs[:, 1], bins=25, density=True, alpha=0.6, color='steelblue', edgecolor='white')
axes[0, 2].axvline(coef_true[1], color='g', lw=2, ls='--', label=f"True β₁={coef_true[1]:.3f}")
axes[0, 2].axvline(pooled_mean[1], color='r', lw=2, label=f"Pooled β₁={pooled_mean[1]:.3f}")
axes[0, 2].set_xlabel("β₁")
axes[0, 2].set_ylabel("Density")
axes[0, 2].set_title(f"Multiple Imputation (M={n_imputations})\nDistribution of β₁ estimates")
axes[0, 2].legend(fontsize=8)
axes[0, 2].grid(True, alpha=0.3)

methods = ["Full data", "MCAR (complete\ncase)", "MCAR (mean\nimpute)", "MI (MAR)"]
coefs_plot = [coef_true[1], coef_mcar_complete[1], coef_mcar_impute[1], pooled_mean[1]]
se_plot = [0, 0, 0, rubin_se[1]]
colors_bar = ['green', 'coral', 'orange', 'steelblue']
axes[1, 0].bar(range(4), coefs_plot, color=colors_bar, alpha=0.7)
for i, se in enumerate(se_plot):
    if se > 0:
        axes[1, 0].errorbar(i, coefs_plot[i], yerr=1.96*se, color='k', capsize=5)
axes[1, 0].axhline(coef_true[1], color='g', ls='--', lw=2, label=f"True β₁={coef_true[1]:.3f}")
axes[1, 0].set_xticks(range(4))
axes[1, 0].set_xticklabels(methods, fontsize=8)
axes[1, 0].set_ylabel("β₁ (coefficient of X₁)")
axes[1, 0].set_title("Comparison of Missing Data Methods")
axes[1, 0].legend(fontsize=8)
axes[1, 0].grid(True, axis='y', alpha=0.3)

mar_probs = np.sort(p_mar)
axes[1, 1].hist(mar_probs, bins=30, density=True, alpha=0.6, color='coral', edgecolor='white')
axes[1, 1].axvline(0.3, color='k', ls='--', label="MCAR rate (30%)")
axes[1, 1].set_xlabel("P(missing | X₂)")
axes[1, 1].set_ylabel("Density")
axes[1, 1].set_title("MAR: Missing Probability Distribution")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

rmse_methods = [
    np.sqrt(np.mean((np.column_stack([np.ones(n), X1, X2]) @ coef_true - y)**2)),
    np.sqrt(np.mean((np.column_stack([np.ones(n), X1_mcar, X2]) @ coef_mcar_complete - y)**2)),
    np.sqrt(np.mean((np.column_stack([np.ones(n), X1_mcar_mean, X2]) @ coef_mcar_impute - y)**2)),
]
axes[1, 2].bar(range(3), rmse_methods, color=['green', 'coral', 'orange'], alpha=0.7)
axes[1, 2].set_xticks(range(3))
axes[1, 2].set_xticklabels(["Full data", "MCAR complete", "MCAR impute"], fontsize=8)
axes[1, 2].set_ylabel("RMSE")
axes[1, 2].set_title("Prediction RMSE Comparison")
axes[1, 2].grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/34-missing-data.png")
plt.close()

print("=" * 60)
print("MISSING DATA ANALYSIS")
print("=" * 60)
print(f"\nMissing mechanism types:")
print(f"  MCAR: P(missing|X₁,X₂,y) = P(missing)")
print(f"  MAR:  P(missing|X₁,X₂,y) = P(missing|X₂)")
print(f"  MNAR: P(missing|X₁,X₂,y) = P(missing|X₁,X₂,y)")

print(f"\nRegression coefficient for X₁:")
print(f"  Full data:              {coef_true[1]:.3f}")
print(f"  MCAR complete case:     {coef_mcar_complete[1]:.3f}")
print(f"  MCAR mean impute:       {coef_mcar_impute[1]:.3f}")
print(f"  MI (MAR) pooled:        {pooled_mean[1]:.3f}")
print(f"  MI (MAR) Rubin SE:      {rubin_se[1]:.4f}")
print(f"  MI (MAR) 95% CI:        [{pooled_mean[1] - 1.96*rubin_se[1]:.3f}, {pooled_mean[1] + 1.96*rubin_se[1]:.3f}]")

print(f"\nMCAR: Complete case analysis gives unbiased estimates")
print(f"MAR:  Multiple imputation needed for valid inference")
print(f"MNAR: Requires sensitivity analysis")
