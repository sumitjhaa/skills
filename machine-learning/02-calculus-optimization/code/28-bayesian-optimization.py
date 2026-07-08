import numpy as np
from scipy.linalg import cholesky, solve_triangular
from scipy.stats import norm
import matplotlib.pyplot as plt

def gp_posterior(X_train, y_train, X_test, sigma_noise=1e-3, length_scale=1.0):
    def rbf(x1, x2):
        dist2 = np.sum((x1[:, None] - x2[None, :])**2, axis=-1)
        return np.exp(-dist2 / (2 * length_scale**2))

    K = rbf(X_train, X_train) + sigma_noise * np.eye(len(X_train))
    K_s = rbf(X_train, X_test)
    K_ss = rbf(X_test, X_test) + sigma_noise * np.eye(len(X_test))
    L = cholesky(K, lower=True)
    alpha = solve_triangular(L.T, solve_triangular(L, y_train, lower=True))
    mu = K_s.T @ alpha
    v = solve_triangular(L, K_s, lower=True)
    var = np.diag(K_ss) - np.sum(v**2, axis=0)
    return mu, np.sqrt(np.maximum(var, 0))

def expected_improvement(mu, sigma, f_best):
    imp = mu - f_best
    Z = imp / (sigma + 1e-10)
    ei = imp * norm.cdf(Z) + sigma * norm.pdf(Z)
    ei[sigma < 1e-10] = 0
    return ei

def bayesian_optimization(f, bounds, n_init=5, n_iter=20, length_scale=0.5):
    dim = len(bounds)
    X = np.random.uniform(bounds[:, 0], bounds[:, 1], (n_init, dim))
    y = np.array([f(x) for x in X])

    for i in range(n_iter):
        X_candidates = np.random.uniform(bounds[:, 0], bounds[:, 1], (2000, dim))
        mu, sigma = gp_posterior(X, y, X_candidates, length_scale=length_scale)
        f_best = y.min()
        ei = expected_improvement(mu, sigma, f_best)
        x_next = X_candidates[ei.argmax()]
        y_next = f(x_next)
        X = np.vstack([X, x_next.reshape(1, -1)])
        y = np.hstack([y, y_next])
    return X, y

def main():
    print("=" * 60)
    print("BAYESIAN OPTIMIZATION")
    print("=" * 60)

    print("\n--- 1D Bayesian Optimization ---")
    np.random.seed(42)

    f = lambda x: np.sin(3*x) + x**2 + 0.1 * np.random.randn()
    bounds = np.array([[-1.5, 1.5]])

    X_init = np.random.uniform(-1.5, 1.5, (3, 1))
    y_init = np.array([f(x) for x in X_init])

    X_test = np.linspace(-1.5, 1.5, 300).reshape(-1, 1)
    mu, sigma = gp_posterior(X_init, y_init, X_test, length_scale=0.4)
    ei = expected_improvement(mu, sigma, y_init.min())

    best_idx = np.argmin(y_init)
    print(f"  Best point so far: x={X_init[best_idx, 0]:.4f}, f(x)={y_init[best_idx]:.4f}")
    print(f"  Next candidate (max EI): x={X_test[ei.argmax(), 0]:.4f}")
    print(f"  EI value: {ei.max():.4f}")

    X_bo, y_bo = bayesian_optimization(f, bounds, n_init=3, n_iter=15, length_scale=0.4)
    print(f"\n  After 15 BO iterations:")
    best_idx = np.argmin(y_bo)
    print(f"  Best: x={X_bo[best_idx, 0]:.4f}, f(x)={y_bo[best_idx]:.4f}")

    print(f"\n--- Acquisition Functions ---")
    mu_test, sigma_test = mu, sigma
    ei = expected_improvement(mu_test, sigma_test, y_init.min())
    ucb = mu_test + 2.0 * sigma_test
    lcb = mu_test - 2.0 * sigma_test
    print(f"  Max EI:  {ei.max():.4f} at x={X_test[ei.argmax(), 0]:.4f}")
    print(f"  Max UCB: {ucb.max():.4f} at x={X_test[ucb.argmax(), 0]:.4f}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].plot(X_test, mu, 'b-', linewidth=2, label='GP mean')
    axes[0].fill_between(X_test.flatten(), mu - 2*sigma_test, mu + 2*sigma_test,
                         alpha=0.2, color='b', label='±2σ')
    axes[0].scatter(X_init, y_init, c='r', s=80, zorder=5, label='Observations')
    axes[0].plot(X_test, f(X_test), 'k--', alpha=0.5, label='True (noiseless)')
    axes[0].set_xlabel('x'); axes[0].set_ylabel('f(x)')
    axes[0].set_title('GP Surrogate After Initial Points')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    axes[1].plot(X_test, ei, 'g-', linewidth=2, label='EI')
    axes[1].plot(X_test, ucb, 'm-', label='UCB (κ=2)')
    axes[1].axvline(X_test[ei.argmax()], color='g', linestyle=':', alpha=0.7)
    axes[1].axvline(X_test[ucb.argmax()], color='m', linestyle=':', alpha=0.7)
    axes[1].set_xlabel('x'); axes[1].set_ylabel('Acquisition Value')
    axes[1].set_title('Acquisition Functions')
    axes[1].legend(); axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/28_bayesian_optimization.png', dpi=100)
    print(f"\nPlot saved to /tmp/28_bayesian_optimization.png")

if __name__ == "__main__":
    main()
