import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

def main():
    print("=" * 60)
    print("QUADRATIC PROGRAMMING")
    print("=" * 60)

    print("\n--- Simple Convex QP ---")
    Q = np.array([[2, 0], [0, 2]])
    c = np.array([-2, -4])

    def objective(x):
        return 0.5 * x @ Q @ x + c @ x

    constraints = [
        {'type': 'ineq', 'fun': lambda x: 1 - x[0] - x[1]},
        {'type': 'ineq', 'fun': lambda x: x[0]},
        {'type': 'ineq', 'fun': lambda x: x[1]},
    ]
    result = minimize(objective, x0=[0, 0], constraints=constraints, method='SLSQP')
    print(f"min (x₁-1)²+(x₂-2)² s.t. x₁+x₂≤1, x₁,x₂≥0")
    print(f"  Solution: x={result.x}")
    print(f"  f(x) = {result.fun:.6f}")

    print(f"\n--- SVM Dual QP ---")
    np.random.seed(42)
    X_pos = np.random.randn(10, 2) + np.array([2, 2])
    X_neg = np.random.randn(10, 2) + np.array([-2, -2])
    X = np.vstack([X_pos, X_neg])
    y = np.hstack([np.ones(10), -np.ones(10)])
    n = len(y)

    def svm_dual(alpha):
        K = X @ X.T
        return 0.5 * np.sum((alpha[:, None] * y[:, None]) * (alpha[None, :] * y[None, :]) * K) - np.sum(alpha)

    alpha0 = np.zeros(n)
    bounds = [(0, 1) for _ in range(n)]
    cons_eq = {'type': 'eq', 'fun': lambda a: np.dot(a, y)}

    svm_result = minimize(svm_dual, alpha0, bounds=bounds, constraints=cons_eq, method='SLSQP')
    alpha = svm_result.x
    sv_idx = alpha > 1e-4
    w = np.sum((alpha[sv_idx] * y[sv_idx])[:, None] * X[sv_idx], axis=0)
    b = np.mean(y[sv_idx] - X[sv_idx] @ w)
    print(f"SVM dual QP:")
    print(f"  Support vectors: {np.sum(sv_idx)}")
    print(f"  w = {w}, b = {b:.4f}")
    print(f"  Accuracy: {np.mean(np.sign(X @ w + b) == y):.2%}")

    print(f"\n--- Equality-constrained QP ---")
    Q_eq = np.array([[4, 1], [1, 2]])
    c_eq = np.array([1, 1])
    A_eq = np.array([[1, 1]])
    b_eq = np.array([1])

    from scipy.optimize import LinearConstraint
    cons = LinearConstraint(A_eq, b_eq, b_eq)

    def qp_obj(x):
        return 0.5 * x @ Q_eq @ x + c_eq @ x

    result_eq = minimize(qp_obj, x0=[0, 0], constraints=cons, method='SLSQP')
    print(f"min ½xᵀQx + cᵀx s.t. x₁+x₂=1")
    print(f"  Q={Q_eq}, c={c_eq}")
    print(f"  Solution: x={result_eq.x}, f={result_eq.fun:.6f}")

    print(f"\n--- QP Form via KKT System ---")
    def solve_qp_kkt(Q, c, A, b):
        n = Q.shape[0]
        m = A.shape[0]
        KKT = np.block([
            [Q, A.T],
            [A, np.zeros((m, m))]
        ])
        rhs = np.hstack([-c, b])
        sol = np.linalg.solve(KKT, rhs)
        return sol[:n], sol[n:]

    x_kkt, lam_kkt = solve_qp_kkt(Q_eq, c_eq, A_eq, b_eq)
    print(f"  KKT solution: x={x_kkt}, λ={lam_kkt}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    xs = np.linspace(-0.5, 2, 100)
    ys = np.linspace(-0.5, 2, 100)
    Xg, Yg = np.meshgrid(xs, ys)
    Z = (Xg - 1)**2 + (Yg - 2)**2
    axes[0].contour(Xg, Yg, Z, levels=20, cmap='viridis')
    axes[0].plot([0, 0, 1, 0], [1, 0, 0, 1], 'r-', linewidth=2)
    axes[0].fill([0, 0, 1, 0], [1, 0, 0, 1], 'r', alpha=0.1)
    axes[0].plot(result.x[0], result.x[1], 'k*', markersize=15)
    axes[0].set_xlabel('x₁'); axes[0].set_ylabel('x₂')
    axes[0].set_title('Convex QP with Linear Constraints')
    axes[0].grid(True, alpha=0.3)

    for idx in np.where(sv_idx)[0]:
        axes[1].plot(X[idx, 0], X[idx, 1], 'ko', markersize=10, fillstyle='none')
    axes[1].scatter(X[y > 0, 0], X[y > 0, 1], c='blue', label='+1', s=50)
    axes[1].scatter(X[y < 0, 0], X[y < 0, 1], c='red', label='-1', s=50)

    x_line = np.linspace(-4, 4, 100)
    axes[1].plot(x_line, (-w[0]*x_line - b)/w[1], 'k-', label='Decision boundary')
    axes[1].set_xlabel('x₁'); axes[1].set_ylabel('x₂')
    axes[1].set_title('SVM via QP')
    axes[1].legend(); axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/15_quadratic_programming.png', dpi=100)
    print(f"\nPlot saved to /tmp/15_quadratic_programming.png")

if __name__ == "__main__":
    main()
