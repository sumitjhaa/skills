import numpy as np
import matplotlib.pyplot as plt

def conjugate_gradient(A, b, x0=None, max_iter=None, tol=1e-10):
    n = len(b)
    x = np.zeros(n) if x0 is None else x0.copy()
    r = b - A @ x
    d = r.copy()
    rs_old = r @ r
    iters = min(max_iter, n) if max_iter else n
    traj = [x.copy()]

    for i in range(iters):
        Ad = A @ d
        alpha = rs_old / max(d @ Ad, 1e-30)
        x = x + alpha * d
        r = r - alpha * Ad
        rs_new = r @ r
        if np.sqrt(rs_new) < tol:
            traj.append(x.copy())
            break
        beta = rs_new / max(rs_old, 1e-30)
        d = r + beta * d
        rs_old = rs_new
        traj.append(x.copy())
    return np.array(traj), i + 1

def nonlinear_cg(grad_f, x0, max_iter=100, tol=1e-6):
    x = x0.copy()
    g = grad_f(x)
    d = -g
    traj = [x.copy()]
    for i in range(max_iter):
        if np.linalg.norm(g) < tol:
            break
        alpha = 0.1
        x_new = x + alpha * d
        g_new = grad_f(x_new)
        beta = (g_new @ g_new) / max(g @ g, 1e-30)
        d = -g_new + beta * d
        x, g = x_new, g_new
        traj.append(x.copy())
    return np.array(traj), i + 1

def main():
    print("=" * 60)
    print("CONJUGATE GRADIENT METHODS")
    print("=" * 60)

    print("\n--- Linear CG for Ax = b ---")
    np.random.seed(42)
    n = 10
    A = np.random.randn(n, n)
    A = A.T @ A + np.eye(n) * 0.1
    x_true = np.random.randn(n)
    b = A @ x_true

    x0 = np.zeros(n)
    traj_cg, iters = conjugate_gradient(A, b, x0)
    x_cg = traj_cg[-1]
    print(f"CG converged in {iters} iterations")
    print(f"Solution error: {np.linalg.norm(x_cg - x_true):.6e}")
    print(f"Residual: {np.linalg.norm(A @ x_cg - b):.6e}")

    print(f"\n--- CG on 2D Quadratic (visual convergence) ---")
    A2 = np.array([[4, 1], [1, 3]])
    b2 = np.array([1, 2])
    x_true_2d = np.linalg.solve(A2, b2)

    traj_cg_2d, _ = conjugate_gradient(A2, b2, np.zeros(2))
    print(f"2D CG converged to ({traj_cg_2d[-1, 0]:.6f}, {traj_cg_2d[-1, 1]:.6f})")
    print(f"Exact:          ({x_true_2d[0]:.6f}, {x_true_2d[1]:.6f})")

    print(f"\n--- Nonlinear CG on Rosenbrock ---")
    def rosenbrock(x):
        return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

    def grad_rosenbrock(x):
        dx = -2*(1 - x[0]) - 400*x[0]*(x[1] - x[0]**2)
        dy = 200*(x[1] - x[0]**2)
        return np.array([dx, dy])

    x0 = np.array([-1.5, 1.5])
    traj_ncg, iters = nonlinear_cg(grad_rosenbrock, x0)
    print(f"NCG: Final ({traj_ncg[-1, 0]:.4f}, {traj_ncg[-1, 1]:.4f}), iters={iters}")

    print(f"\n--- Condition Number Effect ---")
    for kappa in [1, 10, 100, 1000]:
        A_ill = np.array([[kappa, 0], [0, 1]])
        b_ill = np.array([1, 1])
        traj_ill, iters_ill = conjugate_gradient(A_ill, b_ill, np.zeros(2))
        err = np.linalg.norm(traj_ill[-1] - np.linalg.solve(A_ill, b_ill))
        print(f"  κ={kappa:4d}: CG converged in {iters_ill:2d} iters, error={err:.2e}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    X, Y = np.meshgrid(np.linspace(-2, 2, 50), np.linspace(-2, 2, 50))
    Z = 0.5 * (4*X**2 + 2*X*Y + 3*Y**2) - (X + 2*Y)
    axes[0].contour(X, Y, Z, levels=20, cmap='viridis')
    axes[0].plot(traj_cg_2d[:, 0], traj_cg_2d[:, 1], 'ro-', markersize=6, linewidth=2)
    for i, (xi, yi) in enumerate(traj_cg_2d):
        axes[0].annotate(str(i), (xi, yi), fontsize=9, weight='bold')
    axes[0].set_xlabel('x₁'); axes[0].set_ylabel('x₂')
    axes[0].set_title('CG on Quadratic (A-conjugate directions)')
    axes[0].grid(True, alpha=0.3)

    traj_gd = [np.zeros(2)]
    x = np.zeros(2)
    for _ in range(20):
        x = x - 0.1 * (A2 @ x - b2)
        traj_gd.append(x.copy())
    traj_gd = np.array(traj_gd)

    axes[1].contour(X, Y, Z, levels=20, cmap='viridis')
    axes[1].plot(traj_cg_2d[:, 0], traj_cg_2d[:, 1], 'ro-', label=f'CG ({len(traj_cg_2d)-1} iters)')
    axes[1].plot(traj_gd[:, 0], traj_gd[:, 1], 'b.-', alpha=0.6, label='GD (20 iters)')
    axes[1].set_xlabel('x₁'); axes[1].set_ylabel('x₂')
    axes[1].set_title('CG vs GD on Quadratic')
    axes[1].legend(); axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/12_conjugate_gradient.png', dpi=100)
    print(f"\nPlot saved to /tmp/12_conjugate_gradient.png")

if __name__ == "__main__":
    main()
