import numpy as np
import matplotlib.pyplot as plt


def cholesky(A):
    """Cholesky decomposition A = L L^T for SPD matrices."""
    n = A.shape[0]
    L = np.zeros((n, n)).astype(float)

    for j in range(n):
        s = A[j, j]
        for k in range(j):
            s -= L[j, k] ** 2
        if s <= 1e-14:
            raise np.linalg.LinAlgError(
                "Matrix is not positive definite")
        L[j, j] = np.sqrt(s)

        for i in range(j + 1, n):
            s = A[i, j]
            for k in range(j):
                s -= L[i, k] * L[j, k]
            L[i, j] = s / L[j, j]

    return L


def cholesky_solve(A, b):
    """Solve A x = b using Cholesky decomposition."""
    L = cholesky(A)
    n = len(b)

    y = np.zeros(n)
    for i in range(n):
        y[i] = (b[i] - L[i, :i] @ y[:i]) / L[i, i]

    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - L[i+1:, i] @ x[i+1:]) / L[i, i]

    return x


def ldl_decomposition(A):
    """LDL^T decomposition for symmetric matrices (may not be PD)."""
    n = A.shape[0]
    L = np.eye(n)
    D = np.zeros(n)

    for j in range(n):
        v = np.zeros(j)
        for i in range(j):
            v[i] = L[j, i] * D[i]

        s = A[j, j] - L[j, :j] @ v[:j]
        D[j] = s

        if abs(D[j]) < 1e-14:
            raise ValueError("Nearly singular leading submatrix")

        for i in range(j + 1, n):
            s = A[i, j] - L[j, :j] @ (L[i, :j] * D[:j])
            L[i, j] = s / D[j]

    return L, np.diag(D)


def is_positive_definite(A):
    """Check if A is positive definite via Cholesky."""
    try:
        cholesky(A)
        return True
    except (np.linalg.LinAlgError, ValueError):
        return False


def check_spd_eigenvalues(A):
    """Check positive definiteness via eigenvalues."""
    eigvals = np.linalg.eigvalsh(A)
    return np.all(eigvals > 0), eigvals


def cholesky_det(A):
    """Compute determinant via Cholesky."""
    L = cholesky(A)
    return np.prod(np.diag(L)) ** 2


def main():
    print("=" * 60)
    print("CHOLESKY AND LDL^T DECOMPOSITION")
    print("=" * 60)

    print("\n--- Positive Definiteness Checking ---")
    A_spd = np.array([[4.0, 2.0, -2.0],
                      [2.0, 10.0, 2.0],
                      [-2.0, 2.0, 5.0]])

    A_not_spd = np.array([[1.0, 2.0],
                          [2.0, 1.0]])

    print(f"SPD matrix:\n{A_spd}")
    print(f"Is SPD (Cholesky): {is_positive_definite(A_spd)}")
    spd_eig, eigvals = check_spd_eigenvalues(A_spd)
    print(f"Is SPD (eigenvalues): {spd_eig}, eigenvalues: {np.round(eigvals, 4)}")

    print(f"\nNon-SPD matrix:\n{A_not_spd}")
    print(f"Is SPD (Cholesky): {is_positive_definite(A_not_spd)}")
    spd_eig2, eigvals2 = check_spd_eigenvalues(A_not_spd)
    print(f"Is SPD (eigenvalues): {spd_eig2}, eigenvalues: {np.round(eigvals2, 4)}")

    print("\n--- Cholesky Decomposition ---")
    L = cholesky(A_spd)
    print(f"L:\n{np.round(L, 4)}")
    print(f"L L^T:\n{np.round(L @ L.T, 4)}")
    print(f"L L^T == A: {np.allclose(L @ L.T, A_spd)}")

    print(f"\nDeterminant via Cholesky: {cholesky_det(A_spd):.4f}")
    print(f"Determinant via numpy: {np.linalg.det(A_spd):.4f}")

    print("\n--- Solve via Cholesky ---")
    b = np.array([1.0, 2.0, 3.0])
    x_chol = cholesky_solve(A_spd, b)
    x_np = np.linalg.solve(A_spd, b)
    print(f"Cholesky solve: {x_chol}")
    print(f"NumPy solve:    {x_np}")
    print(f"Match: {np.allclose(x_chol, x_np)}")
    print(f"Residual: {np.linalg.norm(A_spd @ x_chol - b):.2e}")

    print("\n--- LDL^T Decomposition ---")
    A_sym = np.array([[4.0, 2.0, 1.0],
                      [2.0, 1.0, 3.0],
                      [1.0, 3.0, -2.0]])
    L_ldl, D_ldl = ldl_decomposition(A_sym)
    print(f"A:\n{A_sym}")
    print(f"L:\n{np.round(L_ldl, 4)}")
    print(f"D:\n{np.round(D_ldl, 4)}")
    reconstruction = L_ldl @ D_ldl @ L_ldl.T
    print(f"L D L^T:\n{np.round(reconstruction, 4)}")
    print(f"Match: {np.allclose(reconstruction, A_sym)}")

    print("\n--- Performance Comparison ---")
    import time
    for n in [50, 100, 200]:
        A = np.random.randn(n, n)
        A = A.T @ A + n * np.eye(n)

        t0 = time.perf_counter()
        L1 = cholesky(A)
        t_chol = time.perf_counter() - t0

        t0 = time.perf_counter()
        L2 = np.linalg.cholesky(A)
        t_np = time.perf_counter() - t0

        print(f"n={n}: scratch={t_chol:.4f}s, numpy={t_np:.4f}s")

    print("\n--- Random SPD Verification ---")
    for n in [5, 10, 20]:
        B = np.random.randn(n, n)
        A = B.T @ B + 0.1 * np.eye(n)
        print(f"n={n}: is_spd={is_positive_definite(A)}")
        L = cholesky(A)
        print(f"  Max error ||LL^T - A||: {np.linalg.norm(L @ L.T - A):.2e}")


if __name__ == "__main__":
    main()
