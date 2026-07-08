import numpy as np
import matplotlib.pyplot as plt

def two_timescale_compositional(sample_g, sample_grad_f, sample_jac_g, x0, n_iter=1000, alpha=0.01, beta=0.1):
    x = x0.copy()
    y = sample_g(x)
    traj = [x.copy()]
    for t in range(n_iter):
        g_val = sample_g(x)
        y = y - beta * (y - g_val)
        jac = sample_jac_g(x)
        grad = sample_grad_f(y)
        x = x - alpha * jac.T @ grad
        traj.append(x.copy())
    return np.array(traj)

def main():
    print("=" * 60)
    print("COMPOSITIONAL OPTIMIZATION")
    print("=" * 60)

    print("\n--- Simple Compositional Problem: F(x) = f(g(x)) ---")
    f = lambda y: y**2
    g = lambda x: 2*x + 1
    grad_f = lambda y: 2*y
    jac_g = lambda x: np.array([2.0])
    F = lambda x: f(g(x))

    x = np.array([3.0])
    analytical = grad_f(g(x)) * jac_g(x)
    print(f"  F(x) = (2x+1)² at x=3")
    print(f"  F(3) = {F(3):.4f}")
    print(f"  dF/dx = {analytical[0]:.4f}")

    x_opt = -0.5
    print(f"  Theoretical optimum: x = {x_opt}, F(x*) = 0")

    x0 = np.array([3.0])
    traj = two_timescale_compositional(
        lambda x: g(x[0]),
        lambda y: np.array([2*y]),
        lambda x: np.array([[2.0]]),
        x0, n_iter=500, alpha=0.1, beta=0.5
    )
    print(f"  Two-timescale result: x = {traj[-1, 0]:.6f}, F = {F(traj[-1, 0]):.6f}")

    print(f"\n--- Conditional Value-at-Risk (CVaR) as Compositional Problem ---")
    np.random.seed(42)
    n_samples = 1000
    losses = np.abs(np.random.randn(n_samples)) * 2

    alpha_cvar = 0.95
    t_start = np.percentile(losses, 50)

    def cvar_objective(t):
        return t + (1 / (1 - alpha_cvar)) * np.mean(np.maximum(losses - t, 0))

    from scipy.optimize import minimize_scalar
    res = minimize_scalar(cvar_objective)
    cvar_val = res.fun
    print(f"  CVaR_{alpha_cvar:.0%} = {cvar_val:.4f}")
    print(f"  VaR_{alpha_cvar:.0%} (threshold) = {res.x:.4f}")
    print(f"  Mean loss: {losses.mean():.4f}, Max loss: {losses.max():.4f}")

    print(f"\n--- Nested Composition: Expected Value of Function of Expectation ---")
    np.random.seed(42)
    n_outer = 2000
    n_inner = 100
    X = np.random.randn(n_outer, n_inner)

    empirical_means = X.mean(axis=1)
    F_empirical = np.mean(np.exp(empirical_means**2) * 0.5)
    print(f"  E[exp(E[Z]²) / 2] ≈ {F_empirical:.4f}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    xs = np.linspace(-3, 3, 200)
    axes[0].plot(xs, xs**2, 'b-', linewidth=2, label='g(x) = x')
    axes[0].plot(xs, f(xs), 'r-', linewidth=2, label='f(g) = g²')
    axes[0].plot(xs, F(xs), 'g-', linewidth=2, label='F(x) = (2x+1)²')
    axes[0].axvline(-0.5, color='k', linestyle=':', alpha=0.5)
    axes[0].set_xlabel('x'); axes[0].set_ylabel('Function value')
    axes[0].set_title('Compositional Function: f(g(x))')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    F_hist = [F(p[0]) for p in traj]
    axes[1].semilogy(F_hist, 'b-', linewidth=2)
    axes[1].axhline(0, color='r', linestyle='--', alpha=0.5)
    axes[1].set_xlabel('Iteration'); axes[1].set_ylabel('F(x)')
    axes[1].set_title('Two-Timescale Compositional GD')
    axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/34_compositional_optimization.png', dpi=100)
    print(f"\nPlot saved to /tmp/34_compositional_optimization.png")

if __name__ == "__main__":
    main()
