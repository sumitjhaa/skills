#!/usr/bin/env python3
"""03.06 Joint/Marginal/Conditional: Bivariate Gaussian marginals and conditionals."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal, ks_2samp

np.random.seed(42)

def theoretical_marginal_x(x):
    return 1 / np.sqrt(2 * np.pi) * np.exp(-x**2 / 2)

def theoretical_marginal_y(y, mu_y=1, var_y=2):
    return 1 / np.sqrt(2 * np.pi * var_y) * np.exp(-(y - mu_y)**2 / (2 * var_y))

def theoretical_conditional(y, x_cond, mu, cov):
    mu_cond = mu[1] + cov[0][1] / cov[0][0] * (x_cond - mu[0])
    var_cond = cov[1][1] - cov[0][1]**2 / cov[0][0]
    return 1 / np.sqrt(2 * np.pi * var_cond) * np.exp(-(y - mu_cond)**2 / (2 * var_cond))

def test_joint_marginal_conditional(mu, cov, n=10000):
    data = np.random.multivariate_normal(mu, cov, n)
    x, y = data[:, 0], data[:, 1]

    # Test 1: empirical marginal X matches theoretical N(0,1)
    x_grid = np.linspace(-4, 4, 200)
    x_pdf = theoretical_marginal_x(x_grid)
    x_emp, _ = np.histogram(x, bins=60, range=(-4, 4), density=True)
    x_centers = np.linspace(-4, 4, 60)
    x_mse = np.mean((x_emp - theoretical_marginal_x(x_centers))**2)
    ks_stat, ks_p = ks_2samp(x, np.random.normal(0, 1, n))
    print(f"  Marginal X ~ N(0,1): MSE pdf={x_mse:.6f}, KS p={ks_p:.4f}")

    # Test 2: empirical conditional Y|X matches theory
    for x_cond in [-1.0, 0.0, 0.5, 1.5]:
        mu_c = mu[1] + cov[0][1] / cov[0][0] * (x_cond - mu[0])
        var_c = cov[1][1] - cov[0][1]**2 / cov[0][0]
        idx = np.abs(x - x_cond) < 0.1
        if len(idx) < 10:
            continue
        emp_mean = np.mean(y[idx])
        emp_var = np.var(y[idx])
        print(f"  Y|X={x_cond:.1f}: theory mean={mu_c:.3f} emp={emp_mean:.3f} | theory var={var_c:.3f} emp={emp_var:.3f}")

    # Test 3: correlation between X and Y
    corr = np.corrcoef(x, y)[0, 1]
    theoretical_corr = cov[0][1] / np.sqrt(cov[0][0] * cov[1][1])
    print(f"  Correlation: theory={theoretical_corr:.4f} empirical={corr:.4f}")

    return x, y

if __name__ == "__main__":
    configurations = [
        (0.0, "ρ=0 (independent)", [[1, 0.0], [0.0, 2]]),
        (0.6, "ρ=0.6 (moderate)", [[1, 0.6], [0.6, 2]]),
        (0.9, "ρ=0.9 (strong)", [[1, 0.9], [0.9, 2]]),
    ]

    fig, axes = plt.subplots(3, 4, figsize=(16, 12))

    for row, (rho, title, cov) in enumerate(configurations):
        print(f"\n--- {title} ---")
        mu = [0, 1]
        x, y = test_joint_marginal_conditional(mu, cov, n=10000)

        # Joint scatter
        axes[row, 0].scatter(x, y, s=1, alpha=0.3)
        axes[row, 0].axvline(0.5, color='r', ls='--', alpha=0.5)
        axes[row, 0].set_xlabel("X")
        axes[row, 0].set_ylabel("Y")
        axes[row, 0].set_title(f"Joint (ρ={rho})")

        # Marginal X
        axes[row, 1].hist(x, bins=60, density=True, alpha=0.7)
        x_grid = np.linspace(-4, 4, 200)
        axes[row, 1].plot(x_grid, theoretical_marginal_x(x_grid), 'r-', lw=2)
        axes[row, 1].set_title("Marginal X ~ N(0,1)")

        # Marginal Y
        axes[row, 2].hist(y, bins=60, density=True, alpha=0.7)
        y_grid = np.linspace(-4, 6, 200)
        axes[row, 2].plot(y_grid, theoretical_marginal_y(y_grid), 'r-', lw=2)
        axes[row, 2].set_title("Marginal Y ~ N(1,2)")

        # Conditional Y | X = 0.5
        x_cond = 0.5
        mu_cond = mu[1] + cov[0][1] / cov[0][0] * (x_cond - mu[0])
        var_cond = cov[1][1] - cov[0][1]**2 / cov[0][0]
        idx = np.abs(x - x_cond) < 0.1
        axes[row, 3].hist(y[idx], bins=30, density=True, alpha=0.7)
        yc = np.linspace(-3, 5, 200)
        axes[row, 3].plot(yc, theoretical_conditional(yc, x_cond, mu, cov), 'r-', lw=2)
        axes[row, 3].set_title(f"Y|X={x_cond:.1f}")

    plt.tight_layout()
    plt.savefig("../../assets/phase03/06-joint-marginal-conditional.png")
    plt.close()
    print("\nPlots saved to 06-joint-marginal-conditional.png")

    # Edge case: test with different sample sizes
    print("\n--- Sample Size Sensitivity ---")
    for n in [100, 1000, 10000, 100000]:
        mu = [0, 1]; cov = [[1, 0.6], [0.6, 2]]
        data = np.random.multivariate_normal(mu, cov, n)
        x, y = data[:, 0], data[:, 1]
        x_cond = 0.5
        idx = np.abs(x - x_cond) < 0.1
        mu_c = mu[1] + cov[0][1] / cov[0][0] * (x_cond - mu[0])
        emp_mean = np.mean(y[idx]) if len(idx) > 0 else float('nan')
        print(f"  n={n:6d}: |X-0.5|<0.1 count={len(idx):4d}, E[Y|X=0.5] theory={mu_c:.3f} emp={emp_mean:.3f}")
