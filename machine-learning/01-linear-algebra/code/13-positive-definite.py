import numpy as np
import matplotlib.pyplot as plt


def is_positive_definite(A):
    """Check via Cholesky."""
    try:
        np.linalg.cholesky(A)
        return True
    except np.linalg.LinAlgError:
        return False


def rayleigh_quotient(A, x):
    """Compute Rayleigh quotient rho(x) = x^T A x / x^T x."""
    return (x @ (A @ x)) / (x @ x)


def rayleigh_quotient_gradient(A, x):
    """Gradient of Rayleigh quotient."""
    rq = rayleigh_quotient(A, x)
    n = x @ x
    return 2 * (A @ x - rq * x) / n


def rayleigh_quotient_maximization(A, max_iter=100, lr=0.1):
    """Optimize Rayleigh quotient via gradient ascent."""
    n = A.shape[0]
    x = np.random.randn(n)
    x = x / np.linalg.norm(x)
    trajectory = []

    for _ in range(max_iter):
        rq = rayleigh_quotient(A, x)
        trajectory.append(rq)
        grad = rayleigh_quotient_gradient(A, x)
        x_new = x + lr * grad
        x_new = x_new / np.linalg.norm(x_new)
        x = x_new

    return rayleigh_quotient(A, x), x, trajectory


def courant_fischer_check(A):
    """Verify Courant-Fischer min-max theorem."""
    eigvals = np.sort(np.linalg.eigvalsh(A))
    n = A.shape[0]
    print("Courant-Fischer verification:")
    print(f"  Computed eigenvalues: {np.round(eigvals, 4)}")

    for k in [1, 2, n - 1, n]:
        if k <= n:
            print(f"  lambda_{k} = {eigvals[k-1]:.4f}")


def generalized_eigenvalues(A, B):
    """Solve generalized eigenvalue problem A v = lambda B v."""
    B_chol = np.linalg.cholesky(B)
    B_inv = np.linalg.solve(B_chol.T, np.linalg.solve(B_chol, np.eye(B.shape[0])))
    A_tilde = B_inv @ A @ B_inv.T
    eigvals = np.linalg.eigvalsh(A_tilde)
    return eigvals


def quadratic_form_contour(A, ax=None):
    """Plot quadratic form contours."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))

    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)

    for i in range(len(x)):
        for j in range(len(y)):
            v = np.array([X[i, j], Y[i, j]])
            Z[i, j] = v @ (A @ v)

    contour = ax.contour(X, Y, Z, levels=20, cmap='viridis')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'Quadratic Form x^T A x')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    return ax


def main():
    print("=" * 60)
    print("POSITIVE DEFINITE MATRICES AND RAYLEIGH QUOTIENT")
    print("=" * 60)

    np.random.seed(42)

    print("\n--- Positive Definiteness ---")
    A_spd = np.array([[4.0, 1.0], [1.0, 3.0]])
    A_not = np.array([[1.0, 2.0], [2.0, 1.0]])

    print(f"SPD matrix:\n{A_spd}")
    print(f"Is PD: {is_positive_definite(A_spd)}")
    print(f"Eigenvalues: {np.linalg.eigvalsh(A_spd)}")

    print(f"\nNon-PD matrix:\n{A_not}")
    print(f"Is PD: {is_positive_definite(A_not)}")
    print(f"Eigenvalues: {np.linalg.eigvalsh(A_not)}")

    print("\n--- Quadratic Form ---")
    x = np.array([2.0, 1.0])
    qf = x @ (A_spd @ x)
    print(f"Q({x}) = x^T A x = {qf:.4f}")
    print(f"Q is positive: {qf > 0}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    quadratic_form_contour(A_spd, axes[0])
    axes[0].plot(x[0], x[1], 'r*', markersize=15, label=f'x={x}')
    axes[0].legend()

    quadratic_form_contour(A_not, axes[1])
    axes[1].set_title('Non-PD: x^T A x')
    plt.tight_layout()
    plt.show()

    print("\n--- Rayleigh Quotient ---")
    eigvals_ref = np.sort(np.linalg.eigvalsh(A_spd))
    print(f"Eigenvalue range: [{eigvals_ref[0]:.4f}, {eigvals_ref[-1]:.4f}]")

    for i in range(5):
        x_rand = np.random.randn(2)
        rq = rayleigh_quotient(A_spd, x_rand)
        print(f"  Random x: rho={rq:.4f} "
              f"(in [{eigvals_ref[0]:.4f}, {eigvals_ref[-1]:.4f}]): "
              f"{eigvals_ref[0] <= rq <= eigvals_ref[-1]}")

    print("\n--- Rayleigh Quotient Maximization (Gradient Ascent) ---")
    max_rq, max_x, trajectory = rayleigh_quotient_maximization(
        A_spd, max_iter=50, lr=0.5)
    print(f"Maximized RQ: {max_rq:.6f} (true max eigenval: {eigvals_ref[-1]:.6f})")
    print(f"Error: {abs(max_rq - eigvals_ref[-1]):.2e}")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(trajectory, 'b-')
    ax.axhline(y=eigvals_ref[-1], color='r', linestyle='--',
               label=f'True max eigenvalue = {eigvals_ref[-1]:.4f}')
    ax.axhline(y=eigvals_ref[0], color='g', linestyle='--',
               label=f'True min eigenvalue = {eigvals_ref[0]:.4f}')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Rayleigh Quotient')
    ax.set_title('Rayleigh Quotient Maximization')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()

    print("\n--- Courant-Fischer Verification ---")
    n = 5
    B = np.random.randn(n, n)
    A_test = B.T @ B + np.eye(n)
    courant_fischer_check(A_test)

    print("\n--- Generalized Eigenvalues ---")
    A_gen = np.array([[4.0, 1.0], [1.0, 3.0]])
    B_gen = np.array([[2.0, 0.0], [0.0, 1.0]])
    print(f"A_gen =\n{A_gen}")
    print(f"B_gen =\n{B_gen}")

    gen_eigvals = generalized_eigenvalues(A_gen, B_gen)
    print(f"Generalized eigenvalues: {np.round(gen_eigvals, 4)}")

    w, _ = np.linalg.eig(np.linalg.solve(B_gen, A_gen))
    print(f"Via scipy: {np.round(np.sort(np.real(w)), 4)}")

    print("\n--- Rayleigh Quotient for Large Matrix ---")
    n_large = 100
    C = np.random.randn(n_large, n_large)
    A_large = C.T @ C + np.eye(n_large)
    true_eigvals = np.linalg.eigvalsh(A_large)

    max_rq_large, _, _ = rayleigh_quotient_maximization(A_large, max_iter=200, lr=0.1)
    print(f"Max RQ: {max_rq_large:.4f} (true: {true_eigvals[-1]:.4f})")
    print(f"Error: {abs(max_rq_large - true_eigvals[-1]):.2e}")


if __name__ == "__main__":
    main()
