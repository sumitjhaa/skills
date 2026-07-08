"""04.26 Measure theory: Lebesgue integral, Radon-Nikodym."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, beta, gaussian_kde

np.random.seed(42)

def lebesgue_approximation(f, a, b, n_levels=20):
    xs = np.linspace(a, b, 1000)
    y_vals = f(xs)
    y_min, y_max = np.min(y_vals), np.max(y_vals)
    levels = np.linspace(y_min, y_max, n_levels)
    approx = 0
    for i in range(n_levels - 1):
        y_lower = levels[i]
        y_upper = levels[i+1]
        indicator = np.sum((y_vals >= y_lower) & (y_vals < y_upper)) / len(xs) * (b - a)
        approx += y_lower * indicator
    integral = np.sum(y_vals) * (xs[1] - xs[0])
    return approx, integral, levels, y_vals

def radon_nikodym_estimate(p_samples, q_samples, n_bins=30):
    bins = np.linspace(min(p_samples.min(), q_samples.min()),
                       max(p_samples.max(), q_samples.max()), n_bins)
    p_hist, _ = np.histogram(p_samples, bins=bins, density=True)
    q_hist, _ = np.histogram(q_samples, bins=bins, density=True)
    dP_dQ = p_hist / (q_hist + 1e-10)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    return bin_centers, dP_dQ

approx, integral, levels, y_vals = lebesgue_approximation(
    lambda x: np.sin(2*np.pi*x) + 0.5, -1, 1, n_levels=15)

p_samples = np.random.beta(2, 5, 2000)
q_samples = np.random.beta(5, 2, 2000)
bin_centers, dP_dQ = radon_nikodym_estimate(p_samples, q_samples)

mu_range = np.linspace(-3, 3, 1000)
p_gauss = norm.pdf(mu_range, 0, 1)
q_gauss = norm.pdf(mu_range, 1, 1.5)
rn_derivative = p_gauss / (q_gauss + 1e-300)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

xs = np.linspace(-1, 1, 1000)
f_vals = np.sin(2*np.pi*xs) + 0.5
axes[0, 0].plot(xs, f_vals, "b-", lw=2, label="f(x) = sin(2πx) + 0.5")
for i in range(len(levels) - 1):
    axes[0, 0].axhline(levels[i], color="gray", lw=0.5, alpha=0.5)
    mask = (f_vals >= levels[i]) & (f_vals < levels[i+1])
    axes[0, 0].fill_between(xs, levels[i], levels[i+1], where=mask,
                            alpha=0.1, color="red")
axes[0, 0].fill_between(xs, f_vals, alpha=0.2, color="blue")
axes[0, 0].set_xlabel("x")
axes[0, 0].set_ylabel("f(x)")
axes[0, 0].set_title(f"Lebesgue Integral Approximation\n"
                     f"Riemann={integral:.4f}, Lebesgue≈{approx:.4f}")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].hist(p_samples, bins=30, density=True, alpha=0.6, label="P (Beta(2,5))")
axes[0, 1].hist(q_samples, bins=30, density=True, alpha=0.6, label="Q (Beta(5,2))")
axes[0, 1].set_xlabel("x")
axes[0, 1].set_ylabel("Density")
axes[0, 1].set_title("Radon-Nikodym: dP/dQ\nTwo Beta Distributions")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

axes[0, 2].plot(bin_centers, dP_dQ, "b-", lw=2)
axes[0, 2].axhline(1, color="k", ls="--", alpha=0.5)
axes[0, 2].set_xlabel("x")
axes[0, 2].set_ylabel("dP/dQ")
axes[0, 2].set_title("Estimated dP/dQ (density ratio)")
axes[0, 2].grid(True, alpha=0.3)

axes[1, 0].plot(mu_range, p_gauss, "b-", lw=2, label="P = N(0,1)")
axes[1, 0].plot(mu_range, q_gauss, "r-", lw=2, label="Q = N(1,1.5²)")
axes[1, 0].set_xlabel("x")
axes[1, 0].set_ylabel("Density")
axes[1, 0].set_title("Gaussian P and Q\n(absolutely continuous)")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].plot(mu_range, rn_derivative, "purple", lw=2)
axes[1, 1].set_xlabel("x")
axes[1, 1].set_ylabel("dP/dQ(x)")
axes[1, 1].set_title("Radon-Nikodym Derivative\n"
                     "dP/dQ = p(x)/q(x)")
axes[1, 1].grid(True, alpha=0.3)

n_levels_range = np.arange(5, 50, 3)
approx_errors = []
for nl in n_levels_range:
    a_val, i_val, _, _ = lebesgue_approximation(
        lambda x: np.sin(2*np.pi*x) + 0.5, -1, 1, n_levels=nl)
    approx_errors.append(abs(a_val - i_val))
axes[1, 2].plot(n_levels_range, approx_errors, "o-", lw=2)
axes[1, 2].set_xlabel("Number of levels (n)")
axes[1, 2].set_ylabel("|Lebesgue - Riemann|")
axes[1, 2].set_title("Lebesgue Approximation Error\nvs Discretization")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/26-measure-theory.png")
plt.close()

print("=" * 60)
print("MEASURE THEORY")
print("=" * 60)
print(f"\nLebesgue vs Riemann integral:")
print(f"  Riemann: ∫ f(x) dx = {integral:.6f}")
print(f"  Lebesgue approx (15 levels): {approx:.6f}")
print(f"  Error: {abs(approx - integral):.6f}")

print(f"\nRadon-Nikodym (Beta distributions):")
bc_width = bin_centers[1] - bin_centers[0]
p_bin, _ = np.histogram(p_samples, bins=len(bin_centers)+1, density=True)
check = np.sum(p_bin[:len(bin_centers)]) * bc_width
print(f"  ∫ dP = {check:.4f} (should ≈ 1.0)")

print(f"\nGaussian Radon-Nikodym:")
print(f"  dP/dQ(0) = {rn_derivative[mu_range == 0][0] if np.any(mu_range == 0) else rn_derivative[np.argmin(np.abs(mu_range))]:.4f}")
dx = mu_range[1] - mu_range[0]
print(f"  ∫ dP/dQ · dQ = {np.sum(rn_derivative * q_gauss) * dx:.4f}")

print(f"\nKey concepts:")
print(f"  • σ-algebra: collection of measurable sets")
print(f"  • Lebesgue integral: sum over level sets of f")
print(f"  • Radon-Nikodym: P << Q → ∃ dP/dQ")
print(f"  • P << Q (abs. cont.) → P(A)=0 whenever Q(A)=0")
