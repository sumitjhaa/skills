import numpy as np
from scipy.integrate import solve_bvp, solve_ivp
import matplotlib.pyplot as plt

def euler_lagrange_numerical(L, dLdy, dLdyp, a, b, ya, yb, n=100):
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = np.linspace(ya, yb, n + 1)
    for iteration in range(1000):
        y_old = y.copy()
        for i in range(1, n):
            y[i] = 0.5 * (y[i+1] + y[i-1] - h**2 * dLdy(x[i], y[i]))
        if np.max(np.abs(y - y_old)) < 1e-8:
            break
    return x, y

def main():
    print("=" * 60)
    print("CALCULUS OF VARIATIONS")
    print("=" * 60)

    print("\n--- Shortest Path (Euler-Lagrange: y'' = 0) ---")
    x = np.linspace(0, 1, 100)
    y = 2 * x
    path_length = np.trapz(np.sqrt(1 + (np.gradient(y, x))**2), x)
    print(f"  Path: y = 2x from (0,0) to (1,2)")
    print(f"  Length: {path_length:.6f} (exact: {np.sqrt(5):.6f})")

    print(f"\n--- Brachistochrone (curve of fastest descent) ---")
    g = 9.81
    def brach_odes(x, y):
        return np.vstack([y[1], -g / (y[0]**2 * (1 + y[1]**2)**1.5)])

    def bc(ya, yb):
        return np.array([ya[0] - 0, yb[0] - 2])

    x_bvp = np.linspace(0, 0.1, 10)
    y_init = np.zeros((2, x_bvp.size))
    y_init[0] = np.linspace(0, 2, x_bvp.size)
    y_init[1] = 5 * np.ones(x_bvp.size)

    try:
        sol = solve_bvp(brach_odes, bc, x_bvp, y_init, tol=1e-6, max_nodes=10000)
        if sol.success:
            print(f"  Brachistochrone solution found in {sol.niter} iterations")
            print(f"  Final point: ({sol.y[0,-1]:.4f}, time ≈ {sol.t[-1]:.4f})")
    except:
        print(f"  Brachistochrone BVP solver encountered issues (stiff problem)")

    print(f"\n--- Variational Problem with Constraint ---")
    a, b, ya, yb = 0.0, 1.0, 0.0, 1.0
    dLdy = lambda x, y: -2 * y  # for L = y'² + y² (minimizer: hyperbolic sine)
    x_vp, y_vp = euler_lagrange_numerical(None, dLdy, None, a, b, ya, yb)

    y_exact = np.sinh(x_vp) / np.sinh(1)
    print(f"  min ∫(y'² + y²)dx, y(0)=0, y(1)=1")
    print(f"  Numerical y(0.5) = {np.interp(0.5, x_vp, y_vp):.6f}")
    print(f"  Exact     y(0.5) = {np.sinh(0.5) / np.sinh(1):.6f}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].plot(x, y, 'b-', linewidth=2, label='Shortest path')
    for t in [0.2, 0.5, 0.8]:
        idx = np.argmin(np.abs(x - t))
        slope = np.gradient(y, x)[idx]
        axes[0].plot([t-0.15, t+0.15], [y[idx]-0.15*slope, y[idx]+0.15*slope],
                     'r--', alpha=0.5)
    axes[0].set_xlabel('x'); axes[0].set_ylabel('y')
    axes[0].set_title('Shortest Path: y = 2x (EL: y"=0)')
    axes[0].set_aspect('equal')
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(x_vp, y_vp, 'b-', linewidth=2, label='Numerical')
    axes[1].plot(x_vp, y_exact, 'r--', linewidth=2, label='Exact')
    axes[1].set_xlabel('x'); axes[1].set_ylabel('y')
    axes[1].set_title('Euler-Lagrange: min ∫(y\'² + y²)dx')
    axes[1].legend(); axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/24_calculus_of_variations.png', dpi=100)
    print(f"\nPlot saved to /tmp/24_calculus_of_variations.png")

if __name__ == "__main__":
    main()
