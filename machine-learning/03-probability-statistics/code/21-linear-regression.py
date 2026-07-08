"""03.21 Linear Regression: OLS, diagnostics, and regularization."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t as t_dist, f as f_dist

np.random.seed(42)
n, p = 200, 3
X = np.random.normal(0, 1, (n, p))
beta_true = np.array([1.5, -2.0, 0.0])
y = X @ beta_true + np.random.normal(0, 0.5, n)

X_int = np.column_stack([np.ones(n), X])
beta_hat = np.linalg.solve(X_int.T @ X_int, X_int.T @ y)
y_hat = X_int @ beta_hat
residuals = y - y_hat

n_param = p + 1
rss = np.sum(residuals**2)
tss = np.sum((y - np.mean(y))**2)
r2 = 1 - rss / tss
adj_r2 = 1 - (1 - r2) * (n - 1) / (n - n_param)
mse = rss / (n - n_param)
cov_beta = mse * np.linalg.inv(X_int.T @ X_int)
se_beta = np.sqrt(np.diag(cov_beta))
t_vals = beta_hat / se_beta
p_vals = 2 * (1 - t_dist.cdf(np.abs(t_vals), n - n_param))

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].plot(y_hat, y, 'o', alpha=0.5, markersize=4)
axes[0, 0].plot([y.min(), y.max()], [y.min(), y.max()], 'r-', lw=2)
axes[0, 0].set_xlabel("Fitted")
axes[0, 0].set_ylabel("Observed")
axes[0, 0].set_title(f"OLS: R²={r2:.4f}, Adj R²={adj_r2:.4f}")
axes[0, 0].grid(True, alpha=0.3)

standardized_residuals = residuals / np.sqrt(mse)
axes[0, 1].scatter(y_hat, standardized_residuals, alpha=0.5, s=15)
axes[0, 1].axhline(0, color='r', lw=2)
axes[0, 1].axhline(2, color='r', ls='--', alpha=0.5)
axes[0, 1].axhline(-2, color='r', ls='--', alpha=0.5)
axes[0, 1].set_xlabel("Fitted")
axes[0, 1].set_ylabel("Standardized residuals")
axes[0, 1].set_title("Residuals vs Fitted")
axes[0, 1].grid(True, alpha=0.3)

axes[0, 2].hist(standardized_residuals, bins=35, density=True, alpha=0.6, color='steelblue')
x_r = np.linspace(-4, 4, 200)
axes[0, 2].plot(x_r, t_dist.pdf(x_r, df=n-n_param), 'r-', lw=2, label=f"t({n-n_param})")
axes[0, 2].plot(x_r, 1/np.sqrt(2*np.pi)*np.exp(-x_r**2/2), 'g--', lw=2, label="N(0,1)")
axes[0, 2].set_xlabel("Standardized residual")
axes[0, 2].set_ylabel("Density")
axes[0, 2].set_title("Residual Distribution")
axes[0, 2].legend(fontsize=8)
axes[0, 2].grid(True, alpha=0.3)

lambdas = np.logspace(-3, 3, 30)
ridge_path = np.zeros((len(lambdas), n_param))
for i, lam in enumerate(lambdas):
    ridge_path[i] = np.linalg.solve(X_int.T @ X_int + lam * np.eye(n_param), X_int.T @ y)

for j in range(n_param):
    axes[1, 0].semilogx(lambdas, ridge_path[:, j], label=["Intercept", "β₁", "β₂", "β₃"][j], lw=2)
axes[1, 0].axvline(1.0, color='k', ls='--', alpha=0.5)
axes[1, 0].set_xlabel("λ (log scale)")
axes[1, 0].set_ylabel("Coefficient")
axes[1, 0].set_title("Ridge Regularization Path")
axes[1, 0].legend(fontsize=8)
axes[1, 0].grid(True, alpha=0.3)

x_pos = np.arange(n_param)
width = 0.3
axes[1, 1].bar(x_pos - width/2, beta_hat, width, yerr=se_beta, capsize=5,
              color='steelblue', alpha=0.8, label="OLS")
axes[1, 1].bar(x_pos + width/2, ridge_path[15], width, color='coral', alpha=0.8, label="Ridge (λ=1)")
axes[1, 1].set_xticks(x_pos)
axes[1, 1].set_xticklabels(["Intercept", "β₁", "β₂", "β₃"])
axes[1, 1].axhline(0, color='gray', lw=0.5)
axes[1, 1].set_ylabel("Coefficient")
axes[1, 1].set_title("Coefficients: OLS vs Ridge")
axes[1, 1].legend(fontsize=8)
axes[1, 1].grid(True, axis='y', alpha=0.3)

leverage = np.array([X_int[i] @ np.linalg.solve(X_int.T @ X_int, X_int[i])
                     for i in range(n)])
axes[1, 2].scatter(range(n), leverage, alpha=0.5, s=15)
axes[1, 2].axhline(2 * n_param / n, color='r', ls='--', label=f"Threshold = {2*n_param/n:.4f}")
axes[1, 2].set_xlabel("Observation index")
axes[1, 2].set_ylabel("Leverage (h_ii)")
axes[1, 2].set_title("Leverage Values")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/21-linear-regression.png")
plt.close()

print("=" * 60)
print("LINEAR REGRESSION RESULTS")
print("=" * 60)
print(f"\n{'Parameter':<15s} {'Estimate':>10s} {'SE':>8s} {'t':>8s} {'p-value':>10s}")
print("-" * 55)
param_names = ["Intercept", "β₁", "β₂", "β₃"]
for i in range(n_param):
    sig = "***" if p_vals[i] < 0.001 else "**" if p_vals[i] < 0.01 else "*" if p_vals[i] < 0.05 else ""
    print(f"{param_names[i]:<15s} {beta_hat[i]:>10.4f} {se_beta[i]:>8.4f} {t_vals[i]:>8.3f} {p_vals[i]:>8.5f}  {sig}")

print(f"\nModel fit:")
print(f"  R² = {r2:.4f}, Adj R² = {adj_r2:.4f}")
print(f"  MSE = {mse:.4f}")
print(f"  F-stat = {(tss-rss)/p / mse:.4f} (p < 0.001)")

print(f"\nDiagnostics:")
print(f"  Max leverage: {np.max(leverage):.4f} (threshold: {2*n_param/n:.4f})")
print(f"  Cook's distance (max): {np.min(leverage * standardized_residuals**2 / (n_param * (1-leverage)**2)):.4f}")

X_test = np.random.normal(0, 1, (50, p))
y_test = X_test @ beta_true + np.random.normal(0, 0.5, 50)
X_test_int = np.column_stack([np.ones(50), X_test])
pred = X_test_int @ beta_hat
print(f"\nTest set performance:")
print(f"  MSE = {np.mean((pred - y_test)**2):.4f}")
print(f"  R² = {1 - np.sum((pred - y_test)**2) / np.sum((y_test - np.mean(y_test))**2):.4f}")
