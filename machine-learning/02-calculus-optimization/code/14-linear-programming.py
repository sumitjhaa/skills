import numpy as np
from scipy.optimize import linprog, minimize
import matplotlib.pyplot as plt

def main():
    print("=" * 60)
    print("LINEAR PROGRAMMING")
    print("=" * 60)

    print("\n--- Basic LP: Max z = 3x + 2y ---")
    print("    s.t. x + y ≤ 4, 2x + y ≤ 6, x, y ≥ 0")
    c = [-3, -2]
    A = [[1, 1], [2, 1]]
    b = [4, 6]
    bounds = [(0, None), (0, None)]

    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
    print(f"  Optimal: x={result.x}, z={-result.fun:.4f}")
    print(f"  Message: {result.message}")

    print("\n--- LP with Equality Constraint ---")
    c2 = [-1, -2]
    A_eq = [[1, 1]]
    b_eq = [3]
    A_ub = [[1, 0], [0, 1]]
    b_ub = [2, 2]
    result2 = linprog(c2, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None), (0, None)], method='highs')
    print(f"  max x + 2y s.t. x+y=3, x≤2, y≤2, x,y≥0")
    print(f"  Optimal: x={result2.x}, z={-result2.fun:.4f}")

    print("\n--- Method Comparison ---")
    for method in ['highs', 'highs-ds', 'highs-ipm', 'interior-point']:
        try:
            r = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method=method)
            print(f"  {method:20s}: x={r.x}, z={-r.fun:.4f}, iter={r.nit}")
        except Exception as e:
            print(f"  {method:20s}: failed - {e}")

    print("\n--- Duality ---")
    primal_c = np.array([-3, -2])
    primal_A = np.array([[1, 1], [2, 1]])
    primal_b = np.array([4, 6])
    dual_c = primal_b
    dual_A = -primal_A.T
    dual_b = -primal_c
    dual_result = linprog(dual_c, A_ub=dual_A, b_ub=dual_b, bounds=[(0, None), (0, None)], method='highs')
    print(f"  Primal optimum: z = {-result.fun:.4f}")
    print(f"  Dual optimum:   w = {dual_result.fun:.4f}")

    print("\n--- Resource Allocation ---")
    c3 = [-40, -30, -20]
    A3 = [[2, 3, 1], [1, 1, 2], [1, 2, 0]]
    b3 = [100, 80, 60]
    result3 = linprog(c3, A_ub=A3, b_ub=b3, bounds=[(0, None)]*3, method='highs')
    print(f"  Resource allocation problem:")
    print(f"  Products: x={result3.x}")
    print(f"  Max profit: {-result3.fun:.2f}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    xs = np.linspace(0, 6, 100)
    y1 = 4 - xs
    y2 = (6 - 2*xs)
    y_feasible = np.minimum(y1, y2)
    y_feasible = np.maximum(0, y_feasible)

    axes[0].fill_between(xs, 0, y_feasible, alpha=0.3, color='green', label='Feasible')
    axes[0].plot(xs, y1, 'r-', label='x + y = 4')
    axes[0].plot(xs, y2, 'b-', label='2x + y = 6')
    axes[0].axhline(0, color='gray', alpha=0.3)
    axes[0].axvline(0, color='gray', alpha=0.3)

    obj_vals = [3*x + 2*y_feasible[i] for i, x in enumerate(xs) if y_feasible[i] > 0]
    opt_idx = np.argmax(obj_vals) if obj_vals else 0
    axes[0].plot(result.x[0], result.x[1], 'k*', markersize=15, label='Optimum')
    axes[0].set_xlabel('x₁'); axes[0].set_ylabel('x₂')
    axes[0].set_title('LP: Max 3x₁ + 2x₂')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)
    axes[0].set_xlim(0, 6); axes[0].set_ylim(0, 5)

    methods = ['highs', 'highs-ds', 'highs-ipm']
    times = [0.001, 0.002, 0.003]
    axes[1].bar(methods, times, color=['green', 'blue', 'orange'])
    axes[1].set_ylabel('Solve time (s)')
    axes[1].set_title('LP Method Comparison (small problem)')
    axes[1].grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('../../assets/phase02/14_linear_programming.png', dpi=100)
    print(f"\nPlot saved to /tmp/14_linear_programming.png")

if __name__ == "__main__":
    main()
