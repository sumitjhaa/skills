"""04.15 Stochastic processes: Gaussian processes and random walks."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

def rbf_kernel(x1, x2, sigma=1.0, lengthscale=1.0):
    return sigma**2 * np.exp(-cdist(x1, x2, "sqeuclidean") / (2 * lengthscale**2))

def gp_sample(K, n_samples=5, seed=42):
    rng = np.random.RandomState(seed)
    L = np.linalg.cholesky(K + 1e-6 * np.eye(K.shape[0]))
    return L @ rng.randn(K.shape[0], n_samples)

def brownian_motion(n_steps=1000, n_paths=5, T=1.0):
    dt = T / n_steps
    t = np.linspace(0, T, n_steps + 1)
    dw = np.sqrt(dt) * np.random.randn(n_steps, n_paths)
    w = np.vstack([np.zeros((1, n_paths)), np.cumsum(dw, axis=0)])
    return t, w

def ornstein_uhlenbeck(n_steps=1000, n_paths=5, theta=1.0, sigma=1.0, T=2.0):
    dt = T / n_steps
    t = np.linspace(0, T, n_steps + 1)
    x = np.zeros((n_steps + 1, n_paths))
    for i in range(1, n_steps + 1):
        x[i] = x[i-1] - theta * x[i-1] * dt + sigma * np.sqrt(dt) * np.random.randn(n_paths)
    return t, x

np.random.seed(42)
n_pts = 50
X = np.linspace(-3, 3, n_pts).reshape(-1, 1)
K = rbf_kernel(X, X, sigma=1.0, lengthscale=0.5)
gp_samps = gp_sample(K, n_samples=5, seed=42)

t_bm, w_bm = brownian_motion(n_steps=1000, n_paths=5)
t_ou, x_ou = ornstein_uhlenbeck(n_steps=1000, n_paths=5, theta=1.0, sigma=1.0)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

for i in range(gp_samps.shape[1]):
    axes[0, 0].plot(X.ravel(), gp_samps[:, i], lw=1.5)
axes[0, 0].set_xlabel("x")
axes[0, 0].set_ylabel("f(x)")
axes[0, 0].set_title("Gaussian Process Samples\nRBF kernel (σ=1, ℓ=0.5)")
axes[0, 0].grid(True, alpha=0.3)

mean_gp = np.zeros(n_pts)
std_gp = np.sqrt(np.diag(K))
axes[0, 1].fill_between(X.ravel(), mean_gp - 2*std_gp, mean_gp + 2*std_gp,
                        alpha=0.2, label="±2σ")
axes[0, 1].plot(X.ravel(), mean_gp, "k--", lw=2, label="Mean")
axes[0, 1].set_xlabel("x")
axes[0, 1].set_ylabel("f(x)")
axes[0, 1].set_title("GP Prior: Mean and 2σ CI")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

for i in range(w_bm.shape[1]):
    axes[0, 2].plot(t_bm, w_bm[:, i], lw=1)
axes[0, 2].set_xlabel("t")
axes[0, 2].set_ylabel("W(t)")
axes[0, 2].set_title("Brownian Motion (Wiener Process)")
axes[0, 2].grid(True, alpha=0.3)

for i in range(x_ou.shape[1]):
    axes[1, 0].plot(t_ou, x_ou[:, i], lw=1)
axes[1, 0].set_xlabel("t")
axes[1, 0].set_ylabel("X(t)")
axes[1, 0].set_title(f"Ornstein-Uhlenbeck Process\nθ=1, σ=1")
axes[1, 0].grid(True, alpha=0.3)

lens = np.linspace(0.2, 2, 30)
mse_vals = []
rng_check = np.random.RandomState(0)
X_train = np.linspace(-3, 3, 10).reshape(-1, 1)
y_train = np.sin(X_train.ravel()) + 0.1 * rng_check.randn(10)
for l in lens:
    K_tr = rbf_kernel(X_train, X_train, sigma=1.0, lengthscale=l)
    K_ts = rbf_kernel(X, X_train, sigma=1.0, lengthscale=l)
    alpha = np.linalg.solve(K_tr + 1e-6 * np.eye(10), y_train)
    pred = K_ts @ alpha
    mse_vals.append(np.mean((pred - np.sin(X.ravel()))**2))
axes[1, 1].plot(lens, mse_vals, "o-", lw=2)
axes[1, 1].set_xlabel("Lengthscale ℓ")
axes[1, 1].set_ylabel("MSE")
axes[1, 1].set_title("GP Regression: MSE vs Lengthscale")
axes[1, 1].grid(True, alpha=0.3)

X1 = np.random.randn(40).reshape(-1, 1)
X2 = np.random.randn(40).reshape(-1, 1)
K12 = rbf_kernel(X1, X2, sigma=1.0, lengthscale=0.5)
sc = axes[1, 2].scatter(X1.ravel(), X2.ravel(), c=K12.diagonal(),
                        s=50, cmap="viridis")
plt.colorbar(sc, ax=axes[1, 2])
axes[1, 2].set_xlabel("x₁")
axes[1, 2].set_ylabel("x₂")
axes[1, 2].set_title("GP Covariance Structure\nk(x₁, x₂) between two sets")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/15-stochastic-processes.png")
plt.close()

print("=" * 60)
print("STOCHASTIC PROCESSES")
print("=" * 60)
print(f"\nGP Samples (RBF kernel, ℓ=0.5):")
print(f"  Mean across samples at x=0: {np.mean(gp_samps[n_pts//2]):.4f}")
print(f"  Variance at x=0: {np.var(gp_samps[n_pts//2]):.4f} (target: σ²=1)")

print(f"\nBrownian Motion:")
print(f"  Var(W(1)) = {np.var(w_bm[t_bm == 1.0]):.4f} (target: 1.0)")
print(f"  E[W(1)] = {np.mean(w_bm[t_bm == 1.0]):.4f}")

print(f"\nOrnstein-Uhlenbeck:")
print(f"  Stationary variance ≈ σ²/(2θ) = {1/(2*1):.4f}")
print(f"  Empirical variance at t=2: {np.var(x_ou[-1]):.4f}")

print(f"\nGP Regression:")
best_l = lens[np.argmin(mse_vals)]
print(f"  Optimal lengthscale: ℓ = {best_l:.2f}")
print(f"  Best MSE: {min(mse_vals):.6f}")

print(f"\nKey processes:")
print(f"  • GP: distribution over functions (kernels as covariance)")
print(f"  • BM: independent increments, W(t) ~ N(0,t)")
print(f"  • OU: mean-reverting, stationary Gaussian process")
