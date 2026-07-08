import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import lu as scipy_lu


def forward_substitution(L, b):
    """Solve L y = b where L is lower triangular."""
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = (b[i] - L[i, :i] @ y[:i]) / L[i, i]
    return y


def back_substitution(U, y):
    """Solve U x = y where U is upper triangular."""
    n = len(y)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - U[i, i+1:] @ x[i+1:]) / U[i, i]
    return x


def gauss_elimination_partial(A, b):
    """Gaussian elimination with partial pivoting."""
    n = len(b)
    M = A.astype(float).copy()
    rhs = b.astype(float).copy()

    for col in range(n):
        max_row = np.argmax(np.abs(M[col:, col])) + col
        if max_row != col:
            M[[col, max_row]] = M[[max_row, col]]
            rhs[[col, max_row]] = rhs[[max_row, col]]

        pivot = M[col, col]
        if abs(pivot) < 1e-14:
            raise ValueError(f"Zero pivot at column {col}")

        for row in range(col + 1, n):
            factor = M[row, col] / pivot
            M[row, col:] -= factor * M[col, col:]
            rhs[row] -= factor * rhs[col]

    return back_substitution(M, rhs)


def gauss_elimination_complete(A, b):
    """Gaussian elimination with complete pivoting."""
    n = len(b)
    M = A.astype(float).copy()
    rhs = b.astype(float).copy()
    col_perm = np.arange(n)

    for k in range(n):
        sub = M[k:, k:]
        i, j = np.unravel_index(np.argmax(np.abs(sub)), sub.shape)
        i += k
        j += k

        if i != k:
            M[[k, i]] = M[[i, k]]
            rhs[[k, i]] = rhs[[i, k]]
        if j != k:
            M[:, [k, j]] = M[:, [j, k]]
            col_perm[[k, j]] = col_perm[[j, k]]

        pivot = M[k, k]
        if abs(pivot) < 1e-14:
            raise ValueError(f"Zero pivot at column {k}")

        for row in range(k + 1, n):
            factor = M[row, k] / pivot
            M[row, k:] -= factor * M[k, k:]
            rhs[row] -= factor * rhs[k]

    x = back_substitution(M, rhs)
    x_inv_perm = np.zeros(n)
    x_inv_perm[col_perm] = x
    return x_inv_perm


def lu_decomposition(A):
    """LU decomposition with partial pivoting. Returns P, L, U."""
    n = A.shape[0]
    M = A.astype(float).copy()
    L = np.eye(n)
    P = np.eye(n)

    for k in range(n - 1):
        max_row = np.argmax(np.abs(M[k:, k])) + k
        if max_row != k:
            M[[k, max_row]] = M[[max_row, k]]
            P[[k, max_row]] = P[[max_row, k]]
            if k > 0:
                L[[k, max_row], :k] = L[[max_row, k], :k]

        pivot = M[k, k]
        if abs(pivot) < 1e-14:
            continue

        for i in range(k + 1, n):
            L[i, k] = M[i, k] / pivot
            M[i, k:] -= L[i, k] * M[k, k:]

    U = np.triu(M)
    return P, L, U


def solve_with_lu(A, b):
    """Solve Ax = b using LU decomposition."""
    P, L, U = lu_decomposition(A)
    y = forward_substitution(L, P @ b)
    x = back_substitution(U, y)
    return x


def condition_number(A):
    """Estimate condition number via SVD."""
    s = np.linalg.svd(A, compute_uv=False)
    return s[0] / s[-1]


def stability_experiment():
    """Compare stability of different pivoting strategies."""
    n_values = [5, 10, 20, 50]
    results = []

    for n in n_values:
        for _ in range(10):
            A = np.random.randn(n, n) * 10
            x_true = np.random.randn(n)
            b = A @ x_true

            x_partial = gauss_elimination_partial(A, b)
            x_complete = gauss_elimination_complete(A, b)
            x_numpy = np.linalg.solve(A, b)

            error_partial = np.linalg.norm(x_partial - x_true) / np.linalg.norm(x_true)
            error_complete = np.linalg.norm(x_complete - x_true) / np.linalg.norm(x_true)
            error_numpy = np.linalg.norm(x_numpy - x_true) / np.linalg.norm(x_true)

            results.append((n, error_partial, error_complete, error_numpy))

    return results


def main():
    print("=" * 60)
    print("GAUSSIAN ELIMINATION AND LU DECOMPOSITION")
    print("=" * 60)

    A = np.array([[2.0, 1.0, -1.0],
                  [-3.0, -1.0, 2.0],
                  [-2.0, 1.0, 2.0]])
    b = np.array([8.0, -11.0, -3.0])

    print(f"\nSystem A =\n{A}")
    print(f"\nb = {b}")

    x_partial = gauss_elimination_partial(A, b)
    x_numpy = np.linalg.solve(A, b)
    print(f"\nSolution (partial pivoting): {x_partial}")
    print(f"Solution (numpy):             {x_numpy}")
    print(f"Match: {np.allclose(x_partial, x_numpy)}")
    print(f"Residual: {np.linalg.norm(A @ x_partial - b):.2e}")

    x_complete = gauss_elimination_complete(A, b)
    print(f"\nSolution (complete pivoting): {x_complete}")
    print(f"Match: {np.allclose(x_complete, x_numpy)}")

    print("\n--- LU Decomposition ---")
    P, L, U = lu_decomposition(A)
    print(f"P:\n{P}")
    print(f"L:\n{np.round(L, 4)}")
    print(f"U:\n{np.round(U, 4)}")
    print(f"P * L * U == A: {np.allclose(P @ L @ U, A)}")

    x_lu = solve_with_lu(A, b)
    print(f"\nLU solve: {x_lu}")
    print(f"Match: {np.allclose(x_lu, x_numpy)}")

    print("\n--- Condition Number ---")
    cond = condition_number(A)
    print(f"Condition number of A: {cond:.6e}")
    print(f"log10(cond) ≈ {np.log10(cond):.2f} (digits lost)")

    ill_conditioned = np.array([[1, 1],
                                [1, 1.0001]])
    cond_ill = condition_number(ill_conditioned)
    print(f"\nIll-conditioned matrix:\n{ill_conditioned}")
    print(f"Condition number: {cond_ill:.6e}")

    print("\n--- Stability Experiment ---")
    np.random.seed(42)
    results = stability_experiment()

    n_list = sorted(set(r[0] for r in results))
    print(f"\nMatrix sizes tested: {n_list}")

    fig, ax = plt.subplots(figsize=(10, 6))
    for n in n_list:
        n_results = [r for r in results if r[0] == n]
        partial_errors = [r[1] for r in n_results]
        complete_errors = [r[2] for r in n_results]
        numpy_errors = [r[3] for r in n_results]

        ax.scatter([n] * len(partial_errors), partial_errors,
                   alpha=0.5, label=f'n={n} partial' if n == n_list[0] else '')
        ax.scatter([n] * len(complete_errors), complete_errors,
                   alpha=0.5, marker='s', label=f'n={n} complete' if n == n_list[0] else '')
        ax.scatter([n] * len(numpy_errors), numpy_errors,
                   alpha=0.5, marker='^', label=f'n={n} numpy' if n == n_list[0] else '')

    ax.set_xlabel('Matrix size n')
    ax.set_ylabel('Relative error')
    ax.set_yscale('log')
    ax.set_title('Stability Comparison of Pivoting Strategies')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()

    print("\n--- Symmetric Positive Definite ---")
    A_spd = np.array([[4, 1], [1, 3]])
    x_true = np.array([1.0, 2.0])
    b_spd = A_spd @ x_true
    x_solved = gauss_elimination_partial(A_spd, b_spd)
    print(f"SPD solution: {x_solved}, true: {x_true}")


if __name__ == "__main__":
    main()
