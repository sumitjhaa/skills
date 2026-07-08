"""03.14 MAP: MAP with different priors — ridge vs lasso regularization."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
n, p = 100, 5
X = np.random.normal(0, 1, (n, p))
beta_true = np.array([3.0, -1.5, 0.0, 0.0, 2.0])
y = X @ beta_true + np.random.normal(0, 0.5, n)

beta_ols = np.linalg.lstsq(X, y, rcond=None)[0]

def soft_threshold(x, lam):
    return np.sign(x) * np.maximum(np.abs(x) - lam, 0)

def lasso_cd(X, y, lam, max_iter=2000, tol=1e-6):
    beta = np.zeros(p)
    for _ in range(max_iter):
        beta_old = beta.copy()
        for j in range(p):
            r = y - X @ beta + X[:, j] * beta[j]
            beta[j] = soft_threshold(X[:, j] @ r, lam) / (X[:, j] @ X[:, j])
        if np.max(np.abs(beta - beta_old)) < tol:
            break
    return beta

lambdas = np.logspace(-2, 2, 30)
ridge_path = np.zeros((len(lambdas), p))
lasso_path = np.zeros((len(lambdas), p))

for i, lam in enumerate(lambdas):
    ridge_path[i] = np.linalg.solve(X.T @ X + lam * np.eye(p), X.T @ y)
    lasso_path[i] = lasso_cd(X, y, lam)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

lambda_ridge = 2.0
beta_ridge = np.linalg.solve(X.T @ X + lambda_ridge * np.eye(p), X.T @ y)
beta_lasso = lasso_cd(X, y, lambda_ridge)

methods = ["True", "OLS (MLE)", "Ridge (MAP)", "Lasso (MAP)"]
betas = np.column_stack([beta_true, beta_ols, beta_ridge, beta_lasso])
x_pos = np.arange(p)
width = 0.2
for i, (name, b) in enumerate(zip(methods, betas.T)):
    axes[0, 0].bar(x_pos + i*width, b, width, label=name, alpha=0.8)
axes[0, 0].set_xticks(x_pos + width*1.5)
axes[0, 0].set_xticklabels([f"β{j}" for j in range(p)])
axes[0, 0].axhline(0, color='gray', lw=0.5)
axes[0, 0].set_ylabel("Coefficient")
axes[0, 0].set_title("MLE vs MAP: Coefficient Comparison")
axes[0, 0].legend(fontsize=8)
axes[0, 0].grid(True, alpha=0.3)

for j in range(p):
    axes[0, 1].semilogx(lambdas, ridge_path[:, j], label=f"β{j}", lw=2)
axes[0, 1].axvline(lambda_ridge, color='k', ls='--', alpha=0.5)
axes[0, 1].set_xlabel("λ (log scale)")
axes[0, 1].set_ylabel("Coefficient")
axes[0, 1].set_title("Ridge Regularization Path")
axes[0, 1].legend(fontsize=8)
axes[0, 1].grid(True, alpha=0.3)

for j in range(p):
    axes[0, 2].semilogx(lambdas, lasso_path[:, j], label=f"β{j}", lw=2)
axes[0, 2].axvline(lambda_ridge, color='k', ls='--', alpha=0.5)
axes[0, 2].set_xlabel("λ (log scale)")
axes[0, 2].set_ylabel("Coefficient")
axes[0, 2].set_title("Lasso Regularization Path")
axes[0, 2].legend(fontsize=8)
axes[0, 2].grid(True, alpha=0.3)

lam_test = np.logspace(-2, 2, 50)
mse_ridge = []
mse_lasso = []
for lam in lam_test:
    br = np.linalg.solve(X.T @ X + lam * np.eye(p), X.T @ y)
    bl = lasso_cd(X, y, lam)
    mse_ridge.append(np.mean((X @ br - y)**2))
    mse_lasso.append(np.mean((X @ bl - y)**2))

axes[1, 0].loglog(lam_test, mse_ridge, label="Ridge", lw=2)
axes[1, 0].loglog(lam_test, mse_lasso, label="Lasso", lw=2)
axes[1, 0].set_xlabel("λ")
axes[1, 0].set_ylabel("MSE")
axes[1, 0].set_title("Training MSE vs λ")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

beta_diff_ridge = np.sqrt(np.sum((ridge_path - beta_true)**2, axis=1))
beta_diff_lasso = np.sqrt(np.sum((lasso_path - beta_true)**2, axis=1))
axes[1, 1].semilogx(lambdas, beta_diff_ridge, 'o-', label="Ridge", lw=2)
axes[1, 1].semilogx(lambdas, beta_diff_lasso, 's-', label="Lasso", lw=2)
axes[1, 1].set_xlabel("λ")
axes[1, 1].set_ylabel("||β̂ - β_true||₂")
axes[1, 1].set_title("Estimation Error vs λ")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

sparsity = [np.sum(np.abs(lasso_path[i]) < 1e-6) for i in range(len(lambdas))]
axes[1, 2].semilogx(lambdas, sparsity, 'o-', color='green', lw=2)
axes[1, 2].set_xlabel("λ")
axes[1, 2].set_ylabel("Number of zero coefficients")
axes[1, 2].set_title("Lasso Sparsity vs λ")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/14-map.png")
plt.close()

print("=" * 60)
print("MAP ESTIMATION: RIDGE VS LASSO")
print("=" * 60)
print(f"\nTrue coefficients:  {beta_true}")
print(f"OLS (MLE):          {np.round(beta_ols, 3)}")
print(f"Ridge (λ=2):        {np.round(beta_ridge, 3)}")
print(f"Lasso (λ=2):        {np.round(beta_lasso, 3)}")

print(f"\nRidge shrinks all coefficients toward 0")
print(f"Lasso shrinks AND selects (β₂, β₃ → 0)")
print(f"\nOptimal λ (min estimation error):")
best_r = lambdas[np.argmin(beta_diff_ridge)]
best_l = lambdas[np.argmin(beta_diff_lasso)]
print(f"  Ridge: λ = {best_r:.4f}")
print(f"  Lasso: λ = {best_l:.4f}")

print(f"\nPrediction error (MSE):")
X_test = np.random.normal(0, 1, (50, p))
y_test = X_test @ beta_true + np.random.normal(0, 0.5, 50)
print(f"  OLS:   {np.mean((X_test @ beta_ols - y_test)**2):.4f}")
print(f"  Ridge: {np.mean((X_test @ beta_ridge - y_test)**2):.4f}")
print(f"  Lasso: {np.mean((X_test @ beta_lasso - y_test)**2):.4f}")
