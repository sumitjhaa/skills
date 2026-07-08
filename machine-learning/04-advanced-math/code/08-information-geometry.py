"""04.08 Information geometry and natural gradient."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, beta, entropy
from scipy.spatial.distance import jensenshannon

def fisher_normal(mu, sigma):
    return np.linalg.inv(np.array([[1/sigma**2, 0], [0, 2/sigma**2]]))

def natural_gradient_step(theta, grad, fisher_inv, lr=0.1):
    return theta - lr * fisher_inv @ grad

def kl_gaussian(mu1, s1, mu2, s2):
    return np.log(s2/s1) + (s1**2 + (mu1-mu2)**2) / (2*s2**2) - 0.5

thetas = np.linspace(-2, 2, 50)
mus = np.zeros(50)
for i, th in enumerate(thetas):
    idx = np.digitize(th, np.linspace(-2, 2, 50))
    mus[i] = 0.5 * th

np.random.seed(42)
points = np.random.randn(20, 2) * 0.5

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

mu_range = np.linspace(-3, 3, 20)
sigma_range = np.linspace(0.5, 2.5, 20)
MU, SIGMA = np.meshgrid(mu_range, sigma_range)
KL = np.zeros_like(MU)
for i in range(len(mu_range)):
    for j in range(len(sigma_range)):
        KL[i, j] = kl_gaussian(MU[i, j], SIGMA[i, j], 0, 1)

contour = axes[0, 0].contourf(MU, SIGMA, KL, levels=20, cmap="viridis")
plt.colorbar(contour, ax=axes[0, 0])
axes[0, 0].set_xlabel("μ")
axes[0, 0].set_ylabel("σ")
axes[0, 0].set_title("KL(p(μ,σ) || p(0,1))\non Gaussian manifold")
axes[0, 0].grid(True, alpha=0.3)

mu_test = np.linspace(-3, 3, 100)
fisher_mu = 1.0 / (1.0**2)
axes[0, 1].plot(mu_test, fisher_mu * np.ones_like(mu_test), "b-", lw=2)
axes[0, 1].set_xlabel("μ")
axes[0, 1].set_ylabel("Fisher information")
axes[0, 1].set_title("Fisher Information I(μ)\nfor N(μ, 1)")
axes[0, 1].grid(True, alpha=0.3)

x = np.linspace(-4, 4, 200)
for mu, sigma, ls in [(0, 1, "-"), (1, 1.5, "--"), (-1, 0.5, ":")]:
    axes[0, 2].plot(x, norm.pdf(x, mu, sigma), ls=ls, lw=2,
                    label=f"N({mu},{sigma}²)")
axes[0, 2].set_xlabel("x")
axes[0, 2].set_ylabel("Density")
axes[0, 2].set_title("Points on Gaussian Manifold")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

theta = np.array([0.0, 0.0])
grad = np.array([0.5, 0.3])
F_inv = fisher_normal(0, 1)
theta_sgd = theta - 0.1 * grad
theta_ng = natural_gradient_step(theta, grad, F_inv, lr=0.1)

axes[1, 0].arrow(0, 0, -0.1*grad[0], -0.1*grad[1], head_width=0.02, fc="red", ec="red",
                label="SGD")
axes[1, 0].arrow(0, 0, theta_ng[0]-theta[0], theta_ng[1]-theta[1], head_width=0.02,
                fc="blue", ec="blue", label="Natural Grad")
axes[1, 0].set_xlim(-0.08, 0.02)
axes[1, 0].set_ylim(-0.05, 0.02)
axes[1, 0].axhline(0, color="gray", lw=0.5)
axes[1, 0].axvline(0, color="gray", lw=0.5)
axes[1, 0].set_xlabel("Δμ")
axes[1, 0].set_ylabel("Δσ")
axes[1, 0].set_title("SGD vs Natural Gradient\nStep Directions")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

js_dist = jensenshannon
alphas = np.linspace(0, 1, 50)
js_divs = []
for a in alphas:
    p = np.array([a, 1-a])
    q = np.array([0.5, 0.5])
    js_divs.append(jensenshannon(p, q, base=2)**2)
axes[1, 1].plot(alphas, js_divs, lw=2)
axes[1, 1].set_xlabel("α (Bernoulli parameter)")
axes[1, 1].set_ylabel("JS² divergence from fair coin")
axes[1, 1].set_title("Geodesic on Bernoulli Manifold")
axes[1, 1].grid(True, alpha=0.3)

x_b = np.linspace(0.01, 0.99, 100)
a_params = [(2, 5), (5, 2), (1, 1), (0.5, 0.5)]
for a, b in a_params:
    axes[1, 2].plot(x_b, beta.pdf(x_b, a, b), lw=2, label=f"Beta({a},{b})")
axes[1, 2].set_xlabel("x")
axes[1, 2].set_ylabel("Density")
axes[1, 2].set_title("Beta Distribution Family\non Statistical Manifold")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/08-information-geometry.png")
plt.close()

print("=" * 60)
print("INFORMATION GEOMETRY")
print("=" * 60)
print(f"\nGaussian manifold: parameter space (μ, σ)")
F_at_origin = fisher_normal(0, 1)
print(f"  Fisher info at (μ=0, σ=1):")
print(f"  F = diag({F_at_origin[0,0]:.2f}, {F_at_origin[1,1]:.2f})")

print(f"\nSGD vs Natural Gradient:")
print(f"  SGD step:          Δθ = ({-0.1*grad[0]:.4f}, {-0.1*grad[1]:.4f})")
print(f"  Natural grad step: Δθ = ({theta_ng[0]:.6f}, {theta_ng[1]:.6f})")

print(f"\nKey concepts:")
print(f"  • Statistical manifold: space of probability distributions")
print(f"  • Fisher metric: local curvature of KL divergence")
print(f"  • Natural gradient: steepest descent in Fisher metric")
print(f"  • α-divergence: family connecting KL, Hellinger, χ²")
print(f"  • Geodesics: shortest paths in Riemannian geometry")
