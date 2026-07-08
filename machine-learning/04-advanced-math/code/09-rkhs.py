"""04.09 Reproducing kernel Hilbert spaces."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist, pdist, squareform

def rbf_kernel(x1, x2, sigma=1.0, lengthscale=1.0):
    return sigma**2 * np.exp(-cdist(x1, x2)**2 / (2 * lengthscale**2))

def poly_kernel(x1, x2, degree=3, c=1):
    return (x1 @ x2.T + c)**degree

def laplace_kernel(x1, x2, sigma=1.0, lengthscale=1.0):
    return sigma**2 * np.exp(-cdist(x1, x2) / lengthscale)

X = np.linspace(-5, 5, 100).reshape(-1, 1)
X_train = np.linspace(-4, 4, 9).reshape(-1, 1)
y_train = np.sin(X_train).ravel() + 0.05 * np.random.RandomState(42).randn(9)

K_rbf = rbf_kernel(X_train, X_train, sigma=1.0, lengthscale=1.0)
K_test = rbf_kernel(X, X_train, sigma=1.0, lengthscale=1.0)
K_self = rbf_kernel(X, X, sigma=1.0, lengthscale=1.0)
alpha_rbf = np.linalg.solve(K_rbf + 1e-6 * np.eye(9), y_train)
y_pred_rbf = K_test @ alpha_rbf

K_poly = poly_kernel(X_train, X_train, degree=3)
K_test_poly = poly_kernel(X, X_train, degree=3)
alpha_poly = np.linalg.solve(K_poly + 1e-6 * np.eye(9), y_train)
y_pred_poly = K_test_poly @ alpha_poly

K_lap = laplace_kernel(X_train, X_train, sigma=1.0, lengthscale=1.0)
K_test_lap = laplace_kernel(X, X_train, sigma=1.0, lengthscale=1.0)
alpha_lap = np.linalg.solve(K_lap + 1e-6 * np.eye(9), y_train)
y_pred_lap = K_test_lap @ alpha_lap

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].plot(X.ravel(), y_pred_rbf, "b-", lw=2, label="RBF kernel")
axes[0, 0].plot(X.ravel(), y_pred_poly, "r--", lw=2, label="Poly kernel (d=3)")
axes[0, 0].plot(X.ravel(), y_pred_lap, "g:", lw=2, label="Laplace kernel")
axes[0, 0].scatter(X_train.ravel(), y_train, c="k", s=40, zorder=5)
axes[0, 0].set_xlabel("x")
axes[0, 0].set_ylabel("y")
axes[0, 0].set_title("Kernel Ridge Regression\n(9 training points)")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

X2 = np.linspace(-5, 5, 50).reshape(-1, 1)
K_rbf_grid = rbf_kernel(X2, np.array([[0]]), sigma=1.0, lengthscale=1.0)
K_poly_grid = poly_kernel(X2, np.array([[0]]), degree=3)
K_laplace_grid = laplace_kernel(X2, np.array([[0]]), sigma=1.0, lengthscale=1.0)
axes[0, 1].plot(X2.ravel(), K_rbf_grid.ravel(), "b-", lw=2, label="RBF")
axes[0, 1].plot(X2.ravel(), K_poly_grid.ravel(), "r--", lw=2, label="Poly(d=3)")
axes[0, 1].plot(X2.ravel(), K_laplace_grid.ravel(), "g:", lw=2, label="Laplace")
axes[0, 1].set_xlabel("x - x'")
axes[0, 1].set_ylabel("k(x, 0)")
axes[0, 1].set_title("Kernel Functions\n(centered at 0)")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

eigvals_rbf = np.linalg.eigvalsh(K_rbf)
eigvals_poly = np.linalg.eigvalsh(K_poly)
eigvals_lap = np.linalg.eigvalsh(K_lap)
axes[0, 2].plot(eigvals_rbf[::-1], "o-", lw=2, label="RBF")
axes[0, 2].plot(eigvals_poly[::-1], "s-", lw=2, label="Poly")
axes[0, 2].plot(eigvals_lap[::-1], "^-", lw=2, label="Laplace")
axes[0, 2].set_xlabel("Index")
axes[0, 2].set_ylabel("Eigenvalue")
axes[0, 2].set_title("Kernel Matrix Eigenvalues")
axes[0, 2].set_yscale("log")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

sigma_range = np.linspace(0.3, 3, 30)
mmd_vals = []
np.random.seed(0)
X_p = np.random.randn(50, 1)
X_q = np.random.randn(50, 1) + 0.5
for s in sigma_range:
    K_pp = rbf_kernel(X_p, X_p, sigma=1.0, lengthscale=s)
    K_qq = rbf_kernel(X_q, X_q, sigma=1.0, lengthscale=s)
    K_pq = rbf_kernel(X_p, X_q, sigma=1.0, lengthscale=s)
    mmd = np.sqrt(np.mean(K_pp) + np.mean(K_qq) - 2 * np.mean(K_pq))
    mmd_vals.append(mmd)
axes[1, 0].plot(sigma_range, mmd_vals, lw=2)
axes[1, 0].set_xlabel("Kernel lengthscale")
axes[1, 0].set_ylabel("MMD")
axes[1, 0].set_title("Maximum Mean Discrepancy\nvs Kernel Parameter")
axes[1, 0].grid(True, alpha=0.3)

n_pts = np.arange(5, 101, 5)
k_rkhs = []
for n in n_pts:
    X_n = np.random.randn(n, 1)
    K_n = rbf_kernel(X_n, X_n, sigma=1.0, lengthscale=1.0)
    k_rkhs.append(np.trace(K_n) / n)
axes[1, 1].plot(n_pts, k_rkhs, "o-", lw=2)
axes[1, 1].set_xlabel("n")
axes[1, 1].set_ylabel("Tr(K)/n")
axes[1, 1].set_title("Average RKHS Norm\n‖Φ(x)‖²_H in Feature Space")
axes[1, 1].grid(True, alpha=0.3)

x_pca = np.linspace(-5, 5, 200).reshape(-1, 1)
K_pca = rbf_kernel(x_pca, x_pca, sigma=1.0, lengthscale=1.0)
eigvals, eigvecs = np.linalg.eigh(K_pca)
idx = np.argsort(eigvals)[::-1]
eigvals = eigvals[idx]
eigvecs = eigvecs[:, idx]
for i in range(3):
    axes[1, 2].plot(x_pca.ravel(), eigvecs[:, i], lw=2, label=f"PC {i+1}")
axes[1, 2].set_xlabel("x")
axes[1, 2].set_ylabel("Eigenfunction")
axes[1, 2].set_title("RKHS Eigenfunctions\nof RBF Kernel")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/09-rkhs.png")
plt.close()

print("=" * 60)
print("REPRODUCING KERNEL HILBERT SPACES")
print("=" * 60)
print(f"\nKernel Ridge Regression (RMSE):")
rmse_rbf = np.sqrt(np.mean((y_pred_rbf - np.sin(X.ravel()))**2))
rmse_poly = np.sqrt(np.mean((y_pred_poly - np.sin(X.ravel()))**2))
rmse_lap = np.sqrt(np.mean((y_pred_lap - np.sin(X.ravel()))**2))
print(f"  RBF kernel:     RMSE = {rmse_rbf:.4f}")
print(f"  Poly kernel:    RMSE = {rmse_poly:.4f}")
print(f"  Laplace kernel: RMSE = {rmse_lap:.4f}")

print(f"\nKernel matrix eigenvalues:")
print(f"  RBF:     λ_max = {eigvals_rbf[-1]:.4f}, λ_min = {eigvals_rbf[0]:.4f}")
print(f"  Poly:    λ_max = {eigvals_poly[-1]:.4f}, λ_min = {eigvals_poly[0]:.4f}")
print(f"  Laplace: λ_max = {eigvals_lap[-1]:.4f}, λ_min = {eigvals_lap[0]:.4f}")

print(f"\nMMD between N(0,1) and N(0.5,1):")
print(f"  Best lengthscale = {sigma_range[np.argmax(mmd_vals)]:.2f}")
print(f"  Max MMD = {max(mmd_vals):.4f}")
print(f"\nThe kernel trick: k(x,x') = ⟨φ(x), φ(x')⟩_H")
