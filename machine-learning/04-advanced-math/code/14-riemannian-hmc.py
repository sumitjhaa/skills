"""04.14 Riemannian manifold HMC."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.linalg import cholesky, solve_triangular

def riemannian_hmc(U, grad_U, G, grad_G_inv, n_iter=500, eps=0.1, L=10, x0=np.array([0.0])):
    d = len(x0)
    samples = np.zeros((n_iter, d))
    current = x0.copy()
    n_accept = 0
    for i in range(n_iter):
        G_curr = G(current)
        L_mat = cholesky(G_curr, lower=True)
        v = np.random.randn(d)
        p = L_mat.T @ v
        q, p_old = current.copy(), p.copy()
        p_half = p - 0.5 * eps * grad_U(q) - 0.5 * eps * grad_G_inv(q, p)
        for _ in range(L):
            G_inv = np.linalg.inv(G(q))
            q += eps * G_inv @ p_half
            p_half_new = p_half - eps * grad_U(q) - eps * grad_G_inv(q, p_half)
            p_half = p_half_new
        p_new = p_half - 0.5 * eps * grad_U(q) - 0.5 * eps * grad_G_inv(q, p_half)
        H_old = 0.5 * p_old @ np.linalg.solve(G_curr, p_old) + U(current)
        G_new = G(q)
        H_new = 0.5 * p_new @ np.linalg.solve(G_new, p_new) + U(q)
        if np.log(np.random.rand()) < min(0, H_old - H_new):
            current = q.copy()
            n_accept += 1
        samples[i] = current
    return samples, n_accept / n_iter

d = 1
G_1d = lambda x: np.array([[1.0 + 0.5 * np.sin(x[0])**2]])
grad_G_inv_1d = lambda x, p: np.array([
    -0.5 * np.sin(2*x[0]) * p[0]**2 / (1 + 0.5*np.sin(x[0])**2)**2
])
U_1d = lambda x: 0.5 * x[0]**2
grad_U_1d = lambda x: np.array([x[0]])

samples_rh, ar_rh = riemannian_hmc(U_1d, grad_U_1d, G_1d, grad_G_inv_1d,
                                     n_iter=1000, eps=0.2, L=10, x0=np.array([2.0]))

np.random.seed(42)
X, Y = np.meshgrid(np.linspace(-3, 3, 50), np.linspace(-3, 3, 50))
G_vals = np.zeros((50, 50))
for i in range(50):
    for j in range(50):
        G_vals[i, j] = 1.0 + 0.5 * np.sin(X[i, j])**2

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

contour = axes[0, 0].contourf(X, Y, G_vals, levels=20, cmap="viridis")
plt.colorbar(contour, ax=axes[0, 0])
axes[0, 0].set_xlabel("x")
axes[0, 0].set_ylabel("y")
axes[0, 0].set_title("Fisher Information Metric G(x)\nG(x)=1+0.5sin²(x)")
axes[0, 0].grid(True, alpha=0.3)

xs = np.linspace(-3, 3, 200)
p_true = norm.pdf(xs, 0, 1)
axes[0, 1].hist(samples_rh.ravel(), bins=40, density=True, alpha=0.6, label="RHMC")
axes[0, 1].plot(xs, p_true, "r-", lw=2, label="N(0,1)")
axes[0, 1].set_xlabel("x")
axes[0, 1].set_ylabel("Density")
axes[0, 1].set_title(f"Riemannian HMC\nAR={ar_rh:.3f}")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

axes[0, 2].plot(samples_rh[:300], "b-", lw=1)
axes[0, 2].set_xlabel("Iteration")
axes[0, 2].set_ylabel("x")
axes[0, 2].set_title("RHMC Trace (first 300)")
axes[0, 2].grid(True, alpha=0.3)

x_line = np.linspace(-3, 3, 100)
G_line = 1.0 + 0.5 * np.sin(x_line)**2
axes[1, 0].plot(x_line, G_line, "b-", lw=2)
axes[1, 0].set_xlabel("x")
axes[1, 0].set_ylabel("G(x)")
axes[1, 0].set_title("Metric G(x) along x")
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].imshow(np.array([[1.5, 0.2], [0.2, 1.3]]), cmap="Blues", interpolation="nearest")
for i in range(2):
    for j in range(2):
        axes[1, 1].text(j, i, f"{[[1.5, 0.2], [0.2, 1.3]][i][j]:.1f}", ha="center", va="center")
axes[1, 1].set_xticks([0, 1])
axes[1, 1].set_yticks([0, 1])
axes[1, 1].set_xticklabels(["q₁", "q₂"])
axes[1, 1].set_yticklabels(["q₁", "q₂"])
axes[1, 1].set_title("2D Metric Tensor Example\nG(q) at a point")
plt.colorbar(axes[1, 1].images[0], ax=axes[1, 1])

eps_vals = np.linspace(0.05, 0.5, 20)
ar_vals = []
for ep in eps_vals:
    _, ar = riemannian_hmc(U_1d, grad_U_1d, G_1d, grad_G_inv_1d,
                            n_iter=300, eps=ep, L=10, x0=np.array([2.0]))
    ar_vals.append(ar)
axes[1, 2].plot(eps_vals, ar_vals, "o-", lw=2)
axes[1, 2].set_xlabel("Step size ε")
axes[1, 2].set_ylabel("Acceptance Rate")
axes[1, 2].set_title("RHMC: AR vs Step Size")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/14-riemannian-hmc.png")
plt.close()

print("=" * 60)
print("RIEMANNIAN MANIFOLD HMC")
print("=" * 60)
print(f"\nRiemannian HMC (1D, N(0,1) target, adaptive metric):")
print(f"  Acceptance rate: {ar_rh:.3f}")
print(f"  Sample mean: {np.mean(samples_rh):.4f}")
print(f"  Sample std:  {np.std(samples_rh):.4f}")

print(f"\nMetric G(x) = 1 + 0.5·sin²(x)")
print(f"  Detects regions of high curvature")
print(f"  Larger step sizes in low-curvature regions")

print(f"\nKey concepts:")
print(f"  • Riemannian HMC uses position-dependent metric")
print(f"  • Fisher info matrix as natural metric")
print(f"  • Requires G(q) and ∇_q G(q) gradients")
print(f"  • More efficient in curved spaces than standard HMC")
print(f"  • Adaptive step sizes via the metric")
