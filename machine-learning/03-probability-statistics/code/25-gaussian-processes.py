"""03.25 Gaussian Processes: GP regression with RBF kernel."""
import numpy as np
import matplotlib.pyplot as plt

def rbf_kernel(x1, x2, sigma_f=1.0, l=1.0):
    sqdist = (x1[:, None] - x2[None, :])**2
    return sigma_f**2 * np.exp(-0.5 * sqdist / l**2)

np.random.seed(42)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

n_prior = 100
X_prior = np.linspace(-6, 6, n_prior)
K_prior = rbf_kernel(X_prior, X_prior, sigma_f=1.0, l=1.0)
L_prior = np.linalg.cholesky(K_prior + 1e-6 * np.eye(n_prior))
f_prior = L_prior @ np.random.randn(n_prior, 5)

for i in range(5):
    axes[0, 0].plot(X_prior, f_prior[:, i], lw=1, alpha=0.7)
axes[0, 0].set_xlabel("x")
axes[0, 0].set_ylabel("f(x)")
axes[0, 0].set_title("GP Prior: Sample Functions\n(σ_f=1, l=1)")
axes[0, 0].grid(True, alpha=0.3)

n_train = 20
X_train = np.random.uniform(-5, 5, n_train)
y_train = np.sin(X_train) + np.random.normal(0, 0.1, n_train)
X_test = np.linspace(-6, 6, 200)
sigma_n = 0.1

K = rbf_kernel(X_train, X_train)
K_s = rbf_kernel(X_train, X_test)
K_ss = rbf_kernel(X_test, X_test)
L = np.linalg.cholesky(K + sigma_n**2 * np.eye(n_train))
alpha = np.linalg.solve(L.T, np.linalg.solve(L, y_train))
mu = K_s.T @ alpha
v = np.linalg.solve(L, K_s)
var = np.diag(K_ss) - np.sum(v**2, axis=0)
std = np.sqrt(np.maximum(var, 0))

axes[0, 1].fill_between(X_test, mu - 2*std, mu + 2*std, alpha=0.3, color='b', label="95% CI")
axes[0, 1].plot(X_test, mu, 'b-', lw=2, label="GP posterior mean")
axes[0, 1].plot(X_test, np.sin(X_test), 'r--', lw=2, label="True sin(x)")
axes[0, 1].scatter(X_train, y_train, c='k', s=30, label="Training data")
axes[0, 1].set_xlabel("x")
axes[0, 1].set_ylabel("f(x)")
axes[0, 1].set_title("GP Regression with RBF Kernel")
axes[0, 1].legend(fontsize=8)
axes[0, 1].grid(True, alpha=0.3)

l_values = [0.3, 1.0, 3.0]
for li, lval in enumerate(l_values):
    Ki = rbf_kernel(X_train, X_train, l=lval)
    K_si = rbf_kernel(X_train, X_test, l=lval)
    K_ssi = rbf_kernel(X_test, X_test, l=lval)
    Li = np.linalg.cholesky(Ki + sigma_n**2 * np.eye(n_train))
    alphai = np.linalg.solve(Li.T, np.linalg.solve(Li, y_train))
    mui = K_si.T @ alphai
    axes[0, 2].plot(X_test, mui, lw=2, label=f"l={lval}")

axes[0, 2].plot(X_test, np.sin(X_test), 'k--', lw=2, label="True")
axes[0, 2].scatter(X_train, y_train, c='k', s=15, alpha=0.5)
axes[0, 2].set_xlabel("x")
axes[0, 2].set_ylabel("f(x)")
axes[0, 2].set_title("Effect of Lengthscale l")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

sigma_f_vals = [0.5, 1.0, 2.0]
for sfi, sfval in enumerate(sigma_f_vals):
    Ki = rbf_kernel(X_train, X_train, sigma_f=sfval)
    K_si = rbf_kernel(X_train, X_test, sigma_f=sfval)
    K_ssi = rbf_kernel(X_test, X_test, sigma_f=sfval)
    Li = np.linalg.cholesky(Ki + sigma_n**2 * np.eye(n_train))
    alphai = np.linalg.solve(Li.T, np.linalg.solve(Li, y_train))
    mui = K_si.T @ alphai
    axes[1, 0].plot(X_test, mui, lw=2, label=f"σ_f={sfval}")

axes[1, 0].plot(X_test, np.sin(X_test), 'k--', lw=2, label="True")
axes[1, 0].scatter(X_train, y_train, c='k', s=15, alpha=0.5)
axes[1, 0].set_xlabel("x")
axes[1, 0].set_ylabel("f(x)")
axes[1, 0].set_title("Effect of Signal Variance σ_f")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

log_marg_lik = (-0.5 * y_train @ alpha -
                0.5 * np.linalg.slogdet(K + sigma_n**2 * np.eye(n_train))[1] -
                n_train/2 * np.log(2*np.pi))
print(f"Log marginal likelihood: {log_marg_lik:.2f}")

l_grid = np.logspace(-1, 1, 20)
lml_vals = []
for lval in l_grid:
    Ki = rbf_kernel(X_train, X_train, l=lval)
    Ki_fix = Ki + sigma_n**2 * np.eye(n_train)
    Li = np.linalg.cholesky(Ki_fix)
    alphai = np.linalg.solve(Li.T, np.linalg.solve(Li, y_train))
    lml = (-0.5 * y_train @ alphai - 0.5 * np.linalg.slogdet(Ki_fix)[1] - n_train/2 * np.log(2*np.pi))
    lml_vals.append(lml)

axes[1, 1].semilogx(l_grid, lml_vals, 'o-', lw=2)
best_l = l_grid[np.argmax(lml_vals)]
axes[1, 1].axvline(best_l, color='r', ls='--', label=f"Best l={best_l:.2f}")
axes[1, 1].set_xlabel("Lengthscale l")
axes[1, 1].set_ylabel("Log Marginal Likelihood")
axes[1, 1].set_title("Hyperparameter Selection via LML")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

n_samples_gp = 5
f_samples = np.zeros((len(X_test), n_samples_gp))
post_cov = K_ss - K_s.T @ v
post_cov = (post_cov + post_cov.T) / 2
eigvals, eigvecs = np.linalg.eigh(post_cov + 1e-6 * np.eye(len(X_test)))
L_post = eigvecs @ np.diag(np.sqrt(np.maximum(eigvals, 0)))
for i in range(n_samples_gp):
    f_samples[:, i] = mu + L_post @ np.random.randn(len(X_test))

for i in range(n_samples_gp):
    axes[1, 2].plot(X_test, f_samples[:, i], lw=1, alpha=0.6)
axes[1, 2].plot(X_test, mu, 'b-', lw=2, label="Mean")
axes[1, 2].scatter(X_train, y_train, c='k', s=20)
axes[1, 2].set_xlabel("x")
axes[1, 2].set_ylabel("f(x)")
axes[1, 2].set_title("Samples from GP Posterior")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/25-gaussian-processes.png")
plt.close()

print("=" * 60)
print("GAUSSIAN PROCESS REGRESSION")
print("=" * 60)
print(f"\nTraining data: {n_train} points")
print(f"Test data: {len(X_test)} points")
print(f"Signal variance: σ_f=1.0, Lengthscale: l=1.0")

print(f"\nPredictions:")
idx_0 = np.argmin(np.abs(X_test - 0))
idx_1 = np.argmin(np.abs(X_test - 1))
print(f"  f(0) = {mu[idx_0]:.4f} ± {2*std[idx_0]:.4f} (95% CI)")
print(f"  f(1) = {mu[idx_1]:.4f} ± {2*std[idx_1]:.4f} (95% CI)")
print(f"  True: sin(0)=0, sin(1)={np.sin(1):.4f}")

print(f"\nLog marginal likelihood: {log_marg_lik:.2f}")
print(f"Optimal lengthscale: {best_l:.2f}")
print(f"\nGP provides both predictions and uncertainty quantification.")
