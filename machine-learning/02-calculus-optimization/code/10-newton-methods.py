import numpy as np
import matplotlib.pyplot as plt

def newton_root(f, fp, x0, n_iter=20):
    x = x0
    for i in range(n_iter):
        fx = f(x)
        if abs(fx) < 1e-15:
            break
        x = x - fx / fp(x)
    return x

def newton_optimize(grad_f, hess_f, x0, n_iter=20):
    x = x0.copy()
    traj = [x.copy()]
    for i in range(n_iter):
        g = grad_f(x)
        H = hess_f(x)
        x = x - np.linalg.solve(H, g)
        traj.append(x.copy())
    return np.array(traj)

def main():
    print("=" * 60)
    print("NEWTON'S METHODS")
    print("=" * 60)

    print("\n--- Newton-Raphson for Root Finding ---")
    f = lambda x: x**2 - 2
    fp = lambda x: 2*x
    for x0 in [1.0, 1.5, 10.0]:
        root = newton_root(f, fp, x0)
        print(f"sqrt(2) from x0={x0}: {root:.10f} (error: {abs(root - np.sqrt(2)):.2e})")

    f2 = lambda x: x**3 - 2*x - 5
    fp2 = lambda x: 3*x**2 - 2
    root2 = newton_root(f2, fp2, 2.0)
    print(f"\nRoot of x³ - 2x - 5 = 0: {root2:.10f}")

    print(f"\n--- Quadratic Convergence ---")
    x0, exact_root = 10.0, np.sqrt(2)
    x = x0
    print(f"\nNewton on f(x) = x² - 2:")
    for i in range(6):
        err = abs(x - exact_root)
        print(f"  Iter {i}: x={x:.10f}, error={err:.2e}")
        x = x - (x**2 - 2) / (2*x)

    print(f"\n--- Newton for Optimization ---")
    f_quad = lambda x: x[0]**2 + 10*x[1]**2
    grad_f = lambda x: np.array([2*x[0], 20*x[1]])
    hess_f = lambda x: np.array([[2, 0], [0, 20]])

    x0 = np.array([5.0, 1.0])
    traj = newton_optimize(grad_f, hess_f, x0)
    print(f"Minimizing x² + 10y²:")
    print(f"  Starting: ({x0[0]}, {x0[1]})")
    print(f"  Final: ({traj[-1, 0]:.6f}, {traj[-1, 1]:.6f})")
    print(f"  Exact: (0, 0)")

    def rosenbrock(x):
        return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

    def grad_rosenbrock(x):
        dx = -2*(1 - x[0]) - 400*x[0]*(x[1] - x[0]**2)
        dy = 200*(x[1] - x[0]**2)
        return np.array([dx, dy])

    def hess_rosenbrock(x):
        dxx = 2 - 400*(x[1] - 3*x[0]**2)
        dxy = -400*x[0]
        dyy = 200
        return np.array([[dxx, dxy], [dxy, dyy]])

    x0_rosen = np.array([-1.5, 1.5])
    traj_newton = newton_optimize(grad_rosenbrock, hess_rosenbrock, x0_rosen, 10)
    print(f"\nNewton on Rosenbrock:")
    print(f"  Final: ({traj_newton[-1, 0]:.6f}, {traj_newton[-1, 1]:.6f})")
    print(f"  f(x*) = {rosenbrock(traj_newton[-1]):.6e}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    x_vals = np.linspace(0.01, 3, 100)
    axes[0].plot(x_vals, np.sqrt(x_vals), 'k-', linewidth=2, label='sqrt(x)')

    def sqrt_newton_step(x):
        return x - (x**2 - 2) / (2*x)
    x = 3.0
    xs, ys = [x], [np.sqrt(x)]
    for _ in range(5):
        for _ in range(3):
            pass
        x = sqrt_newton_step(x)
        xs.append(x); ys.append(np.sqrt(x))
    axes[0].plot(xs[:], ys[:], 'ro-', markersize=6)
    axes[0].axhline(np.sqrt(2), color='gray', linestyle=':', alpha=0.5)
    axes[0].set_xlabel('x'); axes[0].set_ylabel('sqrt(x)')
    axes[0].set_title('Newton for sqrt(2)')
    axes[0].grid(True, alpha=0.3)

    Xc, Yc = np.meshgrid(np.linspace(-2, 2, 80), np.linspace(-1, 3, 80))
    Zc = np.array([[rosenbrock([x, y]) for x in Xc[0]] for y in Yc[:, 0]])
    axes[1].contour(Xc, Yc, Zc, levels=np.logspace(-1, 3, 20), cmap='viridis')
    axes[1].plot(traj_newton[:, 0], traj_newton[:, 1], 'r-', linewidth=2, markersize=4)
    axes[1].plot(1, 1, 'k*', markersize=12)
    axes[1].set_xlabel('x'); axes[1].set_ylabel('y')
    axes[1].set_title('Newton on Rosenbrock (2 iterations)')
    plt.tight_layout()
    plt.savefig('../../assets/phase02/10_newton_methods.png', dpi=100)
    print(f"\nPlot saved to /tmp/10_newton_methods.png")

if __name__ == "__main__":
    main()
