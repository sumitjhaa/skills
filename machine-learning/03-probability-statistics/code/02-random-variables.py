"""03.02 Random Variables: Demonstrate CDF and transformations."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon, norm

np.random.seed(42)
n = 10000

X = np.random.exponential(scale=1.0, size=n)
x_grid = np.linspace(0, 6, 200)
ecdf = np.array([np.mean(X <= x) for x in x_grid])
true_cdf = 1 - np.exp(-x_grid)

fig, axes = plt.subplots(2, 3, figsize=(14, 8))

axes[0, 0].plot(x_grid, ecdf, label="Empirical CDF", lw=2)
axes[0, 0].plot(x_grid, true_cdf, '--', label="True Exp(1) CDF", lw=2)
axes[0, 0].set_xlabel("x")
axes[0, 0].set_ylabel("F(x)")
axes[0, 0].set_title("Exponential(1) CDF")
axes[0, 0].legend()
axes[0, 0].grid(True)
max_dev = np.max(np.abs(ecdf - true_cdf))
axes[0, 0].text(3, 0.3, f"Max dev: {max_dev:.4f}", fontsize=10,
                bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

Y = np.random.normal(0, 1, n)
y_grid = np.linspace(-4, 4, 200)
ecdf_y = np.array([np.mean(Y <= y) for y in y_grid])
true_cdf_y = norm.cdf(y_grid)

axes[0, 1].plot(y_grid, ecdf_y, label="Empirical CDF", lw=2)
axes[0, 1].plot(y_grid, true_cdf_y, '--', label="True N(0,1) CDF", lw=2)
axes[0, 1].set_xlabel("y")
axes[0, 1].set_ylabel("F(y)")
axes[0, 1].set_title("Standard Normal CDF")
axes[0, 1].legend()
axes[0, 1].grid(True)
max_dev_y = np.max(np.abs(ecdf_y - true_cdf_y))
axes[0, 1].text(1.5, 0.3, f"Max dev: {max_dev_y:.4f}", fontsize=10,
                bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

Z = X + np.random.normal(0, 0.3, n)
z_grid = np.linspace(-2, 8, 200)
ecdf_z = np.array([np.mean(Z <= z) for z in z_grid])
axes[0, 2].plot(z_grid, ecdf_z, lw=2, label="ECDF of X+N(0,0.3)")
axes[0, 2].set_xlabel("z")
axes[0, 2].set_ylabel("F(z)")
axes[0, 2].set_title("Sum of RVs: Exp(1) + N(0,0.3)")
axes[0, 2].legend()
axes[0, 2].grid(True)

axes[1, 0].hist(X, bins=60, density=True, alpha=0.6, label="Sample")
x_dens = np.linspace(0, 6, 200)
axes[1, 0].plot(x_dens, expon.pdf(x_dens), 'r-', lw=2, label="Exp(1) PDF")
axes[1, 0].set_xlabel("x")
axes[1, 0].set_ylabel("Density")
axes[1, 0].set_title("Exponential PDF")
axes[1, 0].legend()
axes[1, 0].grid(True)

axes[1, 1].hist(Y, bins=60, density=True, alpha=0.6, label="Sample")
y_dens = np.linspace(-4, 4, 200)
axes[1, 1].plot(y_dens, norm.pdf(y_dens), 'r-', lw=2, label="N(0,1) PDF")
axes[1, 1].set_xlabel("y")
axes[1, 1].set_ylabel("Density")
axes[1, 1].set_title("Normal PDF")
axes[1, 1].legend()
axes[1, 1].grid(True)

U = np.random.uniform(0, 1, n)
transformed = -np.log(1 - U)
axes[1, 2].hist(transformed, bins=60, density=True, alpha=0.6, label="Inverse CDF")
axes[1, 2].plot(x_dens, expon.pdf(x_dens), 'r-', lw=2, label="Exp(1) PDF")
axes[1, 2].set_xlabel("x")
axes[1, 2].set_ylabel("Density")
axes[1, 2].set_title("Inverse Transform: U(0,1) → Exp(1)")
axes[1, 2].legend()
axes[1, 2].grid(True)

plt.tight_layout()
plt.savefig("../../assets/phase03/02-random-variables.png")
plt.close()

print("=" * 60)
print("RANDOM VARIABLE ANALYSIS")
print("=" * 60)
print(f"\nSample size: {n}")
print(f"\nExponential(1):")
print(f"  Sample mean: {np.mean(X):.4f} (true: 1.0)")
print(f"  Sample var:  {np.var(X):.4f} (true: 1.0)")
print(f"  Max CDF deviation: {max_dev:.4f}")
print(f"\nNormal(0,1):")
print(f"  Sample mean: {np.mean(Y):.4f} (true: 0.0)")
print(f"  Sample var:  {np.var(Y):.4f} (true: 1.0)")
print(f"  Max CDF deviation: {max_dev_y:.4f}")
print(f"\nInverse Transform: U(0,1) → Exp(1)")
print(f"  Mean: {np.mean(transformed):.4f} (true: 1.0)")
