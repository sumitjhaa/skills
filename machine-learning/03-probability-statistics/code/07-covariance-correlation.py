"""03.07 Covariance & Correlation: Pearson vs Spearman vs Kendall."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr, kendalltau

np.random.seed(42)
n = 500

X = np.random.normal(0, 1, n)
Y_linear = 2 * X + np.random.normal(0, 0.5, n)
Y_nonlinear = np.exp(X) + np.random.normal(0, 0.3, n)
Y_independent = np.random.normal(0, 1, n)
Y_outlier = 2 * X + np.random.normal(0, 0.5, n)
Y_outlier[0] = 20

Y_quad = X**2 + np.random.normal(0, 0.3, n)
Y_heterosked = X * np.random.normal(0, 1, n)

datasets = [
    ("Linear", X, Y_linear, 'blue'),
    ("Nonlinear (exp)", X, Y_nonlinear, 'green'),
    ("Independent", X, Y_independent, 'gray'),
    ("With Outlier", X, Y_outlier, 'red'),
    ("Quadratic", X, Y_quad, 'purple'),
    ("Heteroskedastic", X, Y_heterosked, 'orange'),
]

fig, axes = plt.subplots(2, 3, figsize=(14, 9))
axes = axes.ravel()

results = []
for ax, (name, x, y, color) in zip(axes, datasets):
    ax.scatter(x, y, alpha=0.4, s=10, color=color, edgecolor='k', linewidth=0.3)
    p_coef, p_pval = pearsonr(x, y)
    s_coef, s_pval = spearmanr(x, y)
    k_coef, k_pval = kendalltau(x, y)
    ax.set_title(f"{name}\nP={p_coef:.3f} S={s_coef:.3f} K={k_coef:.3f}", fontsize=10)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True, alpha=0.3)
    results.append((name, p_coef, p_pval, s_coef, s_pval, k_coef, k_pval))

plt.tight_layout()
plt.savefig("../../assets/phase03/07-covariance-correlation.png")
plt.close()

print("=" * 70)
print("CORRELATION MEASURES COMPARISON")
print("=" * 70)
print(f"{'Dataset':<25s} {'Pearson':>8s} {'p-val':>8s} {'Spearman':>8s} {'p-val':>8s} {'Kendall':>8s} {'p-val':>8s}")
print("-" * 70)
for name, p_coef, p_pval, s_coef, s_pval, k_coef, k_pval in results:
    print(f"{name:<25s} {p_coef:>8.3f} {p_pval:>8.2e} {s_coef:>8.3f} {s_pval:>8.2e} {k_coef:>8.3f} {k_pval:>8.2e}")

cov_mat = np.cov(np.column_stack([Y_linear, Y_nonlinear, Y_independent, Y_outlier]).T)
print("\n" + "=" * 70)
print("COVARIANCE MATRIX (4 variables): Linear, Nonlinear, Independent, Outlier")
print("=" * 70)
print(np.round(cov_mat, 3))

corr_mat = np.corrcoef(np.column_stack([Y_linear, Y_nonlinear, Y_independent, Y_outlier]).T)
print("\nCORRELATION MATRIX:")
print("=" * 70)
print(np.round(corr_mat, 3))

print("\n" + "=" * 70)
print("SPURIOUS CORRELATION EXAMPLE")
print("=" * 70)
n_spur = 1000
X_spur = np.random.randn(n_spur)
Y_spur = np.random.randn(n_spur)
p_spur, _ = pearsonr(X_spur, Y_spur)
print(f"  Independent N(0,1) variables: r = {p_spur:.4f}")
print(f"  |r| > 0.1 occurs with probability ~{2*(1-0.1):.0%} by chance")

fig2, axes2 = plt.subplots(2, 2, figsize=(12, 8))
measures = ['Pearson', 'Spearman', 'Kendall']
names = [r[0] for r in results]
p_vals = np.array([[r[1], r[3], r[5]] for r in results])
x_idx = np.arange(len(names))
width = 0.25

for i, (measure, color) in enumerate(zip(measures, ['blue', 'green', 'red'])):
    axes2[0, 0].bar(x_idx + i * width, p_vals[:, i], width, label=measure, color=color, alpha=0.7)
axes2[0, 0].set_xticks(x_idx + width)
axes2[0, 0].set_xticklabels(names, rotation=30, fontsize=8)
axes2[0, 0].set_ylabel("Correlation")
axes2[0, 0].set_title("Correlation Measures by Dataset")
axes2[0, 0].legend(fontsize=8)
axes2[0, 0].grid(True, alpha=0.3)

p_pvals = np.array([[-np.log10(r[2]), -np.log10(r[4]), -np.log10(r[6])] for r in results])
for i, (measure, color) in enumerate(zip(measures, ['blue', 'green', 'red'])):
    axes2[0, 1].bar(x_idx + i * width, p_pvals[:, i], width, label=measure, color=color, alpha=0.7)
axes2[0, 1].set_xticks(x_idx + width)
axes2[0, 1].set_xticklabels(names, rotation=30, fontsize=8)
axes2[0, 1].set_ylabel("-log10(p-value)")
axes2[0, 1].set_title("Significance (-log10 p-value)")
axes2[0, 1].legend(fontsize=8)
axes2[0, 1].axhline(-np.log10(0.05), color='k', ls='--', alpha=0.5, label="p=0.05")
axes2[0, 1].grid(True, alpha=0.3)

axes2[1, 0].scatter(Y_linear, Y_nonlinear, alpha=0.3, s=5)
axes2[1, 0].set_xlabel("Linear")
axes2[1, 0].set_ylabel("Nonlinear")
axes2[1, 0].set_title(f"Cross-correlation: {pearsonr(Y_linear, Y_nonlinear)[0]:.3f}")
axes2[1, 0].grid(True, alpha=0.3)

axes2[1, 1].scatter(Y_independent, Y_outlier, alpha=0.3, s=5)
axes2[1, 1].set_xlabel("Independent")
axes2[1, 1].set_ylabel("With Outlier")
axes2[1, 1].set_title(f"Cross-correlation: {pearsonr(Y_independent, Y_outlier)[0]:.3f}")
axes2[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/07-covariance-correlation-analysis.png")
plt.close()
print("\nCorrelation analysis plots saved.")
