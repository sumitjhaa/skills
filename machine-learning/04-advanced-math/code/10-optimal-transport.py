"""04.10 Optimal transport and Wasserstein distance."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import wasserstein_distance, norm
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist

def earth_mover_1d(x, y, p=1):
    x_sorted = np.sort(x)
    y_sorted = np.sort(y)
    m = min(len(x), len(y))
    return np.mean(np.abs(x_sorted[:m] - y_sorted[:m])**p)**(1/p)

def sinkhorn(Px, Py, C, reg=0.1, max_iter=100, tol=1e-6):
    n, m = C.shape
    K = np.exp(-C / reg)
    u = np.ones(n) / n
    v = np.ones(m) / m
    for _ in range(max_iter):
        u_old = u.copy()
        v = Py / (K.T @ u)
        u = Px / (K @ v)
        if np.max(np.abs(u - u_old)) < tol:
            break
    T = np.diag(u) @ K @ np.diag(v)
    return T, np.sum(T * C)

np.random.seed(42)
n1, n2 = 100, 80
X1 = np.random.randn(n1) * 0.5
X2 = np.random.randn(n2) * 1.0 + 1.5

w1 = wasserstein_distance(X1, X2)
w2 = earth_mover_1d(X1, X2, p=2)**(1/2)
w1_emp = earth_mover_1d(X1, X2, p=1)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].hist(X1, bins=30, density=True, alpha=0.6, label="P (σ=0.5)")
axes[0, 0].hist(X2, bins=30, density=True, alpha=0.6, label="Q (σ=1.0, μ=1.5)")
x_g = np.linspace(-3, 5, 200)
axes[0, 0].plot(x_g, norm.pdf(x_g, 0, 0.5), "b-", lw=2)
axes[0, 0].plot(x_g, norm.pdf(x_g, 1.5, 1.0), "r-", lw=2)
axes[0, 0].set_xlabel("x")
axes[0, 0].set_ylabel("Density")
axes[0, 0].set_title(f"1D Distributions\nW₁ = {w1:.4f}, W₂ = {w2:.4f}")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

X1_s = np.sort(X1)
X2_s = np.sort(X2)
axes[0, 1].plot(X1_s, np.linspace(0, 1, n1), "b-", lw=2, label="CDF P")
axes[0, 1].plot(X2_s, np.linspace(0, 1, n2), "r-", lw=2, label="CDF Q")
for i in range(0, min(n1, n2), 10):
    axes[0, 1].plot([X1_s[i], X2_s[i]], [i/(n1-1), i/(n2-1)], "k-", lw=0.5, alpha=0.3)
axes[0, 1].set_xlabel("x")
axes[0, 1].set_ylabel("CDF")
axes[0, 1].set_title("Optimal Transport Map (1D)\nQuantile matching")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

shifts = np.linspace(0, 5, 40)
w1_shifts = []
for shift in shifts:
    X2_shift = np.random.randn(n2) + shift
    w1_shifts.append(wasserstein_distance(X1, X2_shift))
axes[0, 2].plot(shifts, w1_shifts, "o-", lw=2)
axes[0, 2].set_xlabel("Mean shift δ")
axes[0, 2].set_ylabel("W₁ distance")
axes[0, 2].set_title("Wasserstein-1 vs Distribution Shift")
axes[0, 2].grid(True, alpha=0.3)

n_grid = 50
XA, YA = np.meshgrid(np.linspace(-3, 5, n_grid), np.linspace(-2, 4, n_grid))
XA_flat = XA.ravel()
YA_flat = YA.ravel()
points = np.column_stack([XA_flat, YA_flat])
n_source = 200
source = np.random.randn(n_source, 2) * 0.5
target = np.random.randn(n_source, 2) * 1.0 + np.array([1.5, 1.0])
C_mat = cdist(source, target, metric="sqeuclidean")
Px_unif = np.ones(n_source) / n_source
Py_unif = np.ones(n_source) / n_source
T_mat, cost = sinkhorn(Px_unif, Py_unif, C_mat, reg=0.05, max_iter=50)
row_idx, col_idx = linear_sum_assignment(C_mat)

axes[1, 0].scatter(source[:, 0], source[:, 1], c="blue", s=20, alpha=0.6, label="Source")
axes[1, 0].scatter(target[:, 0], target[:, 1], c="red", s=20, alpha=0.6, label="Target")
for i, j in zip(row_idx[:30], col_idx[:30]):
    axes[1, 0].plot([source[i, 0], target[j, 0]], [source[i, 1], target[j, 1]],
                   "k-", lw=0.3, alpha=0.5)
axes[1, 0].set_xlabel("x")
axes[1, 0].set_ylabel("y")
axes[1, 0].set_title("OT Assignment (2D, 200 points)")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

regs = np.logspace(-3, 0, 20)
costs_reg = []
for r in regs:
    T, c = sinkhorn(Px_unif, Py_unif, C_mat, reg=r, max_iter=200)
    costs_reg.append(c)
axes[1, 1].semilogx(regs, costs_reg, "o-", lw=2)
axes[1, 1].set_xlabel("Regularization ε")
axes[1, 1].set_ylabel("Transport cost")
axes[1, 1].set_title("Sinkhorn Cost vs Regularization")
axes[1, 1].grid(True, alpha=0.3)

dims = [1, 2, 5, 10, 20, 50, 100]
w_rates = []
for d in dims:
    X_d = np.random.randn(200, d)
    Y_d = np.random.randn(200, d) * 1.5 + 0.5
    w_rates.append(wasserstein_distance(X_d.ravel(), Y_d.ravel()) / np.sqrt(d))
axes[1, 2].plot(dims, w_rates, "o-", lw=2)
axes[1, 2].set_xlabel("Dimension d")
axes[1, 2].set_ylabel("W₁ / √d")
axes[1, 2].set_title("Curse of Dimensionality\nin Optimal Transport")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/10-optimal-transport.png")
plt.close()

print("=" * 60)
print("OPTIMAL TRANSPORT")
print("=" * 60)
print(f"\n1D Wasserstein distances:")
print(f"  W₁(P, Q) = {w1:.4f}")
print(f"  W₂(P, Q) = {w2:.4f}")
print(f"  Theoretical W₁(N(0,0.5²), N(1.5,1.0²)) = 1.5 (mean difference)")

print(f"\n2D Optimal Transport (n={n_source}):")
print(f"  Sinkhorn (ε=0.05) cost: {cost:.4f}")
print(f"  Exact OT (Hungarian) cost: {C_mat[row_idx, col_idx].sum()/n_source:.4f}")

w1_10 = w1 / np.sqrt(1)
print(f"\nDimensional scaling of W₁:")
for d, w in zip(dims, w_rates):
    print(f"  d={d:3d}: W₁/√d = {w:.4f}")

print(f"\nKey concepts:")
print(f"  • Wasserstein-1: W₁ = inf E[|X-Y|] (earth mover)")
print(f"  • Wasserstein-2: W₂ = E[|X-Y|²]^{{1/2}}")
print(f"  • Sinkhorn: entropic OT with O(n²) complexity")
print(f"  • Curse of dimensionality: W₁ ~ √d")
