"""03.22 GLMs: Logistic regression via IRLS."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, poisson, chi2

np.random.seed(42)
n = 500
X = np.random.normal(0, 1, (n, 2))
beta_true = np.array([-1.0, 2.0])
log_odds = X @ beta_true
p = 1 / (1 + np.exp(-log_odds))
y = np.random.binomial(1, p)

X_int = np.column_stack([np.ones(n), X])
beta = np.zeros(3)

for i in range(100):
    eta = X_int @ beta
    p_hat = 1 / (1 + np.exp(-eta))
    W = np.diag(p_hat * (1 - p_hat))
    z = eta + (y - p_hat) / (p_hat * (1 - p_hat) + 1e-10)
    beta_new = np.linalg.solve(X_int.T @ W @ X_int, X_int.T @ W @ z)
    if np.max(np.abs(beta_new - beta)) < 1e-6:
        print(f"IRLS converged in {i+1} iterations")
        break
    beta = beta_new

y_pred = (1 / (1 + np.exp(-X_int @ beta))) >= 0.5
accuracy = np.mean(y_pred == y)
log_lik = np.sum(y * np.log(p_hat + 1e-10) + (1 - y) * np.log(1 - p_hat + 1e-10))
null_model = np.mean(y)
null_log_lik = np.sum(y * np.log(null_model) + (1 - y) * np.log(1 - null_model))
deviance = -2 * (log_lik - null_log_lik)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

xx, yy = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-3, 3, 200))
Z = 1 / (1 + np.exp(-(beta[0] + beta[1]*xx + beta[2]*yy)))
contour = axes[0, 0].contourf(xx, yy, Z, levels=30, cmap="RdBu", alpha=0.6)
axes[0, 0].contour(xx, yy, Z, levels=[0.5], colors='k', linewidths=2)
axes[0, 0].scatter(X[:, 0], X[:, 1], c=y, cmap="RdBu", edgecolors='k', alpha=0.7, s=15)
axes[0, 0].set_xlabel("X₁")
axes[0, 0].set_ylabel("X₂")
axes[0, 0].set_title(f"Logistic Regression: Accuracy={accuracy:.3f}")
plt.colorbar(contour, ax=axes[0, 0], label="P(Y=1)")

axes[0, 1].hist(p_hat[y == 0], bins=40, alpha=0.5, color='blue', label="Y=0", density=True)
axes[0, 1].hist(p_hat[y == 1], bins=40, alpha=0.5, color='red', label="Y=1", density=True)
axes[0, 1].set_xlabel("Predicted P(Y=1)")
axes[0, 1].set_ylabel("Density")
axes[0, 1].set_title("Predicted Probabilities by Class")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

p_sorted = np.sort(p_hat)
fpr = np.cumsum(y[np.argsort(p_hat)[::-1]] == 0) / np.sum(y == 0)
tpr = np.cumsum(y[np.argsort(p_hat)[::-1]] == 1) / np.sum(y == 1)
auc = np.trapezoid(tpr, fpr)
axes[0, 2].plot(fpr, tpr, lw=2, label=f"ROC (AUC={auc:.3f})")
axes[0, 2].plot([0, 1], [0, 1], 'k--', label="Random")
axes[0, 2].set_xlabel("False Positive Rate")
axes[0, 2].set_ylabel("True Positive Rate")
axes[0, 2].set_title("ROC Curve")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

n_poisson = 200
X_pois = np.random.normal(0, 1, (n_poisson, 1))
rate = np.exp(0.5 + 0.8 * X_pois[:, 0])
y_pois = np.random.poisson(rate)
X_pois_int = np.column_stack([np.ones(n_poisson), X_pois[:, 0]])
beta_pois = np.zeros(2)

for i in range(100):
    eta_pois = X_pois_int @ beta_pois
    mu_pois = np.exp(eta_pois)
    W_pois = np.diag(mu_pois)
    z_pois = eta_pois + (y_pois - mu_pois) / (mu_pois + 1e-10)
    beta_pois_new = np.linalg.solve(X_pois_int.T @ W_pois @ X_pois_int, X_pois_int.T @ W_pois @ z_pois)
    if np.max(np.abs(beta_pois_new - beta_pois)) < 1e-6:
        print(f"Poisson IRLS converged in {i+1} iterations")
        break
    beta_pois = beta_pois_new

print(f"Poisson GLM: β₀={beta_pois[0]:.4f}, β₁={beta_pois[1]:.4f} (true: 0.5, 0.8)")

x_pois_grid = np.linspace(-2, 2, 100)
y_pois_pred = np.exp(beta_pois[0] + beta_pois[1] * x_pois_grid)
axes[1, 0].scatter(X_pois, y_pois, alpha=0.5, s=15)
axes[1, 0].plot(x_pois_grid, y_pois_pred, 'r-', lw=2, label="Poisson GLM fit")
axes[1, 0].plot(x_pois_grid, np.exp(0.5 + 0.8 * x_pois_grid), 'g--', lw=2, label="True")
axes[1, 0].set_xlabel("X")
axes[1, 0].set_ylabel("Count")
axes[1, 0].set_title("Poisson Regression")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

eps = 1e-10
log_lik_null = np.sum(y * np.log(np.mean(y)+eps) + (1-y) * np.log(1-np.mean(y)+eps))
log_lik_sat = np.sum(y * np.log(y+eps) + (1-y) * np.log(2-y+eps))
pseudo_r2 = 1 - log_lik / log_lik_null
mcfadden_r2 = 1 - log_lik / log_lik_null

metrics = ["Accuracy", "AUC", "Deviance R²", "McFadden R²"]
values = [accuracy, auc, 1 - deviance / (-2 * null_log_lik), mcfadden_r2]
axes[1, 1].bar(metrics, values, color=['steelblue', 'green', 'coral', 'purple'], alpha=0.7)
axes[1, 1].set_ylabel("Value")
axes[1, 1].set_title("Model Performance Metrics")
axes[1, 1].grid(True, axis='y', alpha=0.3)

confusion = np.zeros((2, 2))
for i in range(2):
    for j in range(2):
        confusion[i, j] = np.sum((y_pred == j) & (y == i))
axes[1, 2].imshow(confusion, cmap='Blues', interpolation='nearest')
for i in range(2):
    for j in range(2):
        axes[1, 2].text(j, i, f"{int(confusion[i, j])}", ha='center', va='center', fontsize=14)
axes[1, 2].set_xticks([0, 1])
axes[1, 2].set_yticks([0, 1])
axes[1, 2].set_xticklabels(["Pred 0", "Pred 1"])
axes[1, 2].set_yticklabels(["True 0", "True 1"])
axes[1, 2].set_title("Confusion Matrix")

plt.tight_layout()
plt.savefig("../../assets/phase03/22-glms.png")
plt.close()

print("\n" + "=" * 60)
print("GENERALIZED LINEAR MODELS")
print("=" * 60)
print("\nLogistic Regression:")
print(f"  True β: [{beta_true[0]:.1f}, {beta_true[1]:.1f}]")
print(f"  Estimated β: [{beta[1]:.3f}, {beta[2]:.3f}]")
print(f"  Intercept: {beta[0]:.3f}")
print(f"  Accuracy: {accuracy:.3f}")
print(f"  AUC: {auc:.3f}")
print(f"  McFadden R²: {mcfadden_r2:.4f}")

print(f"\nPoisson Regression:")
print(f"  True β: (0.5, 0.8)")
print(f"  Estimated β: ({beta_pois[0]:.4f}, {beta_pois[1]:.4f})")
print(f"\nGLMs extend linear models to non-normal distributions")
print("via link functions and exponential family distributions.")
