import numpy as np
from scipy.optimize import minimize, LinearConstraint
import matplotlib.pyplot as plt

def randomized_rounding(X, n_trials=100):
    n = X.shape[0]
    try:
        L = np.linalg.cholesky(X + 1e-8 * np.eye(n))
    except:
        L = np.linalg.eigh(X + 1e-8 * np.eye(n))
        L = L[1] @ np.diag(np.sqrt(np.maximum(L[0], 0.0)))
    best = -np.inf
    for _ in range(n_trials):
        r = np.random.randn(n)
        y = np.sign(L @ r)
        cut = 0.25 * np.sum(W * (1 - np.outer(y, y)))
        if cut > best:
            best = cut
            best_y = y
    return best_y, best

def main():
    print("=" * 60)
    print("RELAXATION TECHNIQUES")
    print("=" * 60)

    print("\n--- L0 → L1 Relaxation for Sparse Recovery ---")
    np.random.seed(42)
    n, d = 20, 50
    A = np.random.randn(n, d)
    x_true = np.zeros(d)
    x_true[:5] = np.random.randn(5)
    b = A @ x_true + 0.05 * np.random.randn(n)

    lasso_obj = lambda x: 0.5 * np.linalg.norm(A @ x - b)**2 + 0.1 * np.linalg.norm(x, 1)
    x_lasso = minimize(lasso_obj, np.zeros(d), method='L-BFGS-B').x
    print(f"  True non-zeros: {np.sum(np.abs(x_true) > 1e-4)}")
    print(f"  L1 recovery non-zeros: {np.sum(np.abs(x_lasso) > 1e-3)}")
    print(f"  Recovery error: {np.linalg.norm(x_lasso - x_true):.4f}")

    print(f"\n--- LP Relaxation of Integer Program ---")
    c = np.array([-3, -2, -4])
    A_ub = np.array([[1, 1, 1], [2, 1, 3]])
    b_ub = np.array([30, 60])

    # LP relaxation (integer → continuous)
    from scipy.optimize import linprog
    res_lp = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None)]*3, method='highs')
    print(f"  LP relaxation: x={res_lp.x}, z={-res_lp.fun:.2f}")

    res_int = linprog(c, A_ub=A_ub, b_ub=b_ub,
                      bounds=[(0, None), (0, None), (0, None)],
                      integrality=[1, 1, 1], method='highs')
    if res_int.success:
        print(f"  Integer solution: x={res_int.x}, z={-res_int.fun:.2f}")
        print(f"  Gap: {(-res_lp.fun + res_int.fun) / -res_int.fun * 100:.2f}%")

    print(f"\n--- Max-Cut: SDP Relaxation + Randomized Rounding ---")
    global W
    W = np.array([
        [0, 1, 2, 0, 1],
        [1, 0, 1, 1, 2],
        [2, 1, 0, 2, 1],
        [0, 1, 2, 0, 1],
        [1, 2, 1, 1, 0]
    ])
    D = np.diag(np.sum(W, axis=1))
    L = D - W
    eigvals, eigvecs = np.linalg.eigh(L)
    X_sdp = np.outer(eigvecs[:, -1], eigvecs[:, -1])

    best_y, best_cut = randomized_rounding(X_sdp)
    print(f"  Best cut value: {best_cut:.2f}")
    print(f"  Cut assignment: {best_y}")

    print(f"\n--- Lagrangian Relaxation ---")
    f_obj = lambda x: x[0]**2 + x[1]**2
    cons = {'type': 'eq', 'fun': lambda x: x[0] + x[1] - 2}

    res_orig = minimize(f_obj, x0=[0, 0], constraints=cons)
    print(f"  Original: x={res_orig.x}, f={res_orig.fun:.4f}")

    def lagrangian(x, lam):
        return f_obj(x) + lam * (x[0] + x[1] - 2)

    xs = np.linspace(-1, 3, 200)
    Xg, Yg = np.meshgrid(xs, xs)
    Z = f_obj([Xg, Yg])
    constraint_line = 2 - Xg - Yg

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    cp = axes[0].contourf(Xg, Yg, Z, levels=20, cmap='viridis', alpha=0.7)
    axes[0].contour(Xg, Yg, constraint_line, levels=[0], colors='r', linewidths=2)
    axes[0].plot(res_orig.x[0], res_orig.x[1], 'k*', markersize=15)
    axes[0].set_xlabel('x₁'); axes[0].set_ylabel('x₂')
    axes[0].set_title('Equality-constrained Problem')
    plt.colorbar(cp, ax=axes[0])

    recovery = np.abs(x_lasso)
    axes[1].stem(recovery[:15], linefmt='b-', markerfmt='bo', label='Recovered')
    axes[1].stem(range(5), np.abs(x_true[:5]), linefmt='r--', markerfmt='r*',
                 label='True non-zero', bottom=0)
    axes[1].set_xlabel('Index'); axes[1].set_ylabel('Magnitude')
    axes[1].set_title('L1 Relaxation for Sparse Recovery')
    axes[1].legend(); axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/32_relaxation.png', dpi=100)
    print(f"\nPlot saved to /tmp/32_relaxation.png")

if __name__ == "__main__":
    main()
