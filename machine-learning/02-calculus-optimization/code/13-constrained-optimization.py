import numpy as np
from scipy.optimize import minimize, LinearConstraint, Bounds
import matplotlib.pyplot as plt

def main():
    print("=" * 60)
    print("CONSTRAINED OPTIMIZATION")
    print("=" * 60)

    print("\n--- Equality-constrained: Lagrange Multipliers ---")
    f = lambda x: x[0]**2 + x[1]**2
    cons_eq = {'type': 'eq', 'fun': lambda x: x[0] + x[1] - 1}
    result = minimize(f, x0=[0, 0], constraints=cons_eq)
    print(f"min x²+y² s.t. x+y=1")
    print(f"  Solution: x={result.x}")
    print(f"  f(x) = {result.fun:.6f} (expected: 0.25)")

    print(f"\n--- Inequality-constrained: KKT ---")
    f2 = lambda x: (x[0] - 1)**2 + (x[1] - 2)**2
    constraints = [
        {'type': 'ineq', 'fun': lambda x: 1 - x[0] - x[1]},
        {'type': 'ineq', 'fun': lambda x: x[0]},
        {'type': 'ineq', 'fun': lambda x: x[1]},
    ]
    result2 = minimize(f2, x0=[0, 0], constraints=constraints, method='SLSQP')
    print(f"min (x-1)²+(y-2)² s.t. x+y≤1, x≥0, y≥0")
    print(f"  Solution: x={result2.x}")
    print(f"  f(x) = {result2.fun:.6f}")

    print(f"\n--- KKT Residual Check ---")
    x_star = result2.x
    lam = result2.get('constr_violation', [0])
    print(f"  Stationarity: ∇f = {np.array([2*(x_star[0]-1), 2*(x_star[1]-2)])}")
    print(f"  Primal feasible: x+y-1 = {x_star[0] + x_star[1] - 1:.6f}")
    print(f"  Complementarity: μⱼhⱼ(x) = {result2.fun:.6f}")

    print(f"\n--- Interior Point Method ---")
    result_ip = minimize(f2, x0=[0, 0], constraints=constraints, method='trust-constr')
    print(f"  Trust-constr: x={result_ip.x}, f={result_ip.fun:.6f}")

    print(f"\n--- Convex vs Non-convex Constraints ---")
    f3 = lambda x: x[0]**2 + x[1]**2
    cons_nonconvex = {'type': 'ineq', 'fun': lambda x: 0.5 - np.sin(x[0] * x[1])}
    result3 = minimize(f3, x0=[1, 1], constraints=cons_nonconvex, method='SLSQP')
    print(f"min x²+y² s.t. sin(xy) ≤ 0.5")
    print(f"  Solution: x={result3.x}, f={result3.fun:.6f}")

    print(f"\n--- Multiple Constraints ---")
    f4 = lambda x: -x[0] - x[1]
    constraints4 = [
        {'type': 'ineq', 'fun': lambda x: 5 - x[0]**2 - x[1]**2},
        {'type': 'ineq', 'fun': lambda x: x[0]},
        {'type': 'ineq', 'fun': lambda x: x[1]},
    ]
    result4 = minimize(f4, x0=[1, 1], constraints=constraints4, method='SLSQP')
    print(f"max x+y s.t. x²+y² ≤ 5, x,y ≥ 0")
    print(f"  Solution: x={result4.x}, f={-result4.fun:.6f} (expected ≈ 3.16)")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    xs = np.linspace(-0.5, 2, 100)
    ys = np.linspace(-0.5, 2, 100)
    X, Y = np.meshgrid(xs, ys)
    Z_f2 = (X - 1)**2 + (Y - 2)**2
    axes[0].contour(X, Y, Z_f2, levels=20, cmap='viridis')
    axes[0].plot([0, 0, 1, 0], [1, 0, 0, 1], 'r-', linewidth=2, label='Feasible region')
    axes[0].fill([0, 0, 1, 0], [1, 0, 0, 1], 'r', alpha=0.1)
    axes[0].plot(result2.x[0], result2.x[1], 'k*', markersize=15, label='Optimum')
    axes[0].set_xlabel('x'); axes[0].set_ylabel('y')
    axes[0].set_title('Inequality-constrained Problem')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)
    axes[0].set_xlim(-0.5, 2); axes[0].set_ylim(-0.5, 2)

    xs2 = np.linspace(-3, 3, 100)
    X2, Y2 = np.meshgrid(xs2, xs2)
    Z_f4 = -X2 - Y2
    axes[1].contour(X2, Y2, Z_f4, levels=20, cmap='viridis')
    circle = plt.Circle((0, 0), np.sqrt(5), fill=False, color='r', linewidth=2, label='x²+y² ≤ 5')
    axes[1].add_patch(circle)
    axes[1].plot(result4.x[0], result4.x[1], 'k*', markersize=15, label='Optimum')
    axes[1].fill_between([0, np.sqrt(5)], 0, np.sqrt(5 - np.linspace(0, 5, 100)**2), alpha=0.1, color='r')
    axes[1].set_xlabel('x'); axes[1].set_ylabel('y')
    axes[1].set_title('Constrained Maximization')
    axes[1].legend(); axes[1].grid(True, alpha=0.3)
    axes[1].set_aspect('equal')
    plt.tight_layout()
    plt.savefig('../../assets/phase02/13_constrained_optimization.png', dpi=100)
    print(f"\nPlot saved to /tmp/13_constrained_optimization.png")

if __name__ == "__main__":
    main()
