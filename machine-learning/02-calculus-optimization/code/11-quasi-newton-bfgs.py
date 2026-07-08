import numpy as np
import matplotlib.pyplot as plt

def bfgs(grad_f, x0, max_iter=100, tol=1e-6):
    n = len(x0)
    x = x0.copy()
    H_inv = np.eye(n)
    traj = [x.copy()]
    for i in range(max_iter):
        g = grad_f(x)
        if np.linalg.norm(g) < tol:
            break
        d = -H_inv @ g
        alpha = 1.0
        x_new = x + alpha * d
        g_new = grad_f(x_new)
        s = x_new - x
        y = g_new - g
        rho = 1.0 / (y @ s) if abs(y @ s) > 1e-12 else 0
        if rho > 0:
            I = np.eye(n)
            H_inv = (I - rho * np.outer(s, y)) @ H_inv @ (I - rho * np.outer(y, s)) + rho * np.outer(s, s)
        x = x_new
        traj.append(x.copy())
    return np.array(traj), i + 1

def main():
    print("=" * 60)
    print("QUASI-NEWTON BFGS")
    print("=" * 60)

    def rosenbrock(x):
        return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

    def grad_rosenbrock(x):
        dx = -2*(1 - x[0]) - 400*x[0]*(x[1] - x[0]**2)
        dy = 200*(x[1] - x[0]**2)
        return np.array([dx, dy])

    x0 = np.array([-1.5, 1.5])
    traj_bfgs, n_iter = bfgs(grad_rosenbrock, x0)
    print(f"BFGS on Rosenbrock:")
    print(f"  Iterations: {n_iter}")
    print(f"  Final: ({traj_bfgs[-1, 0]:.6f}, {traj_bfgs[-1, 1]:.6f})")
    print(f"  f(x*) = {rosenbrock(traj_bfgs[-1]):.6e}")

    print(f"\n--- BFGS on Quadratic ---")
    def grad_quad(x):
        Q = np.array([[10, 2], [2, 5]])
        return Q @ x

    x0 = np.array([5.0, 3.0])
    traj_quad, _ = bfgs(grad_quad, x0)
    print(f"  Final: ({traj_quad[-1, 0]:.6f}, {traj_quad[-1, 1]:.6f})")
    print(f"  Expected: (0, 0)")

    print(f"\n--- BFGS on Beale Function ---")
    def beale(x):
        return (1.5 - x[0] + x[0]*x[1])**2 + (2.25 - x[0] + x[0]*x[1]**2)**2 + (2.625 - x[0] + x[0]*x[1]**3)**2

    def grad_beale(x):
        h = 1e-7
        g = np.zeros(2)
        for i in range(2):
            xp = x.copy(); xp[i] += h
            xm = x.copy(); xm[i] -= h
            g[i] = (beale(xp) - beale(xm)) / (2 * h)
        return g

    x0_beale = np.array([0.5, 0.5])
    traj_beale, _ = bfgs(grad_beale, x0_beale)
    print(f"  Final: ({traj_beale[-1, 0]:.6f}, {traj_beale[-1, 1]:.6f})")
    print(f"  Expected: (3, 0.5)")

    print(f"\n--- Comparison: Newton vs BFGS vs GD on Quadratic ---")
    def grad_simple(x):
        return np.array([2*x[0], 10*x[1]])

    x0 = np.array([4.0, 4.0])
    traj_bfgs_s, _ = bfgs(grad_simple, x0)

    x = x0.copy()
    traj_gd = [x.copy()]
    for _ in range(50):
        x = x - 0.05 * grad_simple(x)
        traj_gd.append(x.copy())

    newton_s = lambda x: x - np.linalg.solve(np.array([[2, 0], [0, 10]]), grad_simple(x))
    x = x0.copy()
    traj_newton_s = [x.copy()]
    for _ in range(5):
        x = newton_s(x)
        traj_newton_s.append(x.copy())

    print(f"  GD (50 iter):   ({traj_gd[-1, 0]:.4f}, {traj_gd[-1, 1]:.4f})")
    print(f"  BFGS ({len(traj_bfgs_s)-1} iter): ({traj_bfgs_s[-1, 0]:.4f}, {traj_bfgs_s[-1, 1]:.4f})")
    print(f"  Newton (5 iter): ({traj_newton_s[-1, 0]:.4f}, {traj_newton_s[-1, 1]:.4f})")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    Xc, Yc = np.meshgrid(np.linspace(-2, 2, 80), np.linspace(-1, 3, 80))
    Zc = np.array([[rosenbrock([x, y]) for x in Xc[0]] for y in Yc[:, 0]])
    axes[0].contour(Xc, Yc, Zc, levels=np.logspace(-1, 3, 20), cmap='viridis')
    axes[0].plot(traj_bfgs[:, 0], traj_bfgs[:, 1], 'r-', linewidth=2)
    axes[0].plot(1, 1, 'k*', markersize=12)
    axes[0].set_xlabel('x'); axes[0].set_ylabel('y')
    axes[0].set_title(f'BFGS on Rosenbrock ({n_iter} iter)')

    Xq, Yq = np.meshgrid(np.linspace(-5, 5, 50), np.linspace(-5, 5, 50))
    Zq = 0.5 * (10*Xq**2 + 4*Xq*Yq + 5*Yq**2)
    axes[1].contour(Xq, Yq, Zq, levels=20, cmap='viridis')
    axes[1].plot(np.array(traj_gd)[:, 0], np.array(traj_gd)[:, 1], 'b-', label='GD')
    axes[1].plot(traj_bfgs_s[:, 0], traj_bfgs_s[:, 1], 'r-', label=f'BFGS')
    axes[1].plot(np.array(traj_newton_s)[:, 0], np.array(traj_newton_s)[:, 1], 'g-', label='Newton')
    axes[1].plot(0, 0, 'k*', markersize=12)
    axes[1].set_xlabel('x'); axes[1].set_ylabel('y')
    axes[1].set_title('Comparison on Quadratic')
    axes[1].legend()
    plt.tight_layout()
    plt.savefig('../../assets/phase02/11_quasi_newton_bfgs.png', dpi=100)
    print(f"\nPlot saved to /tmp/11_quasi_newton_bfgs.png")

if __name__ == "__main__":
    main()
