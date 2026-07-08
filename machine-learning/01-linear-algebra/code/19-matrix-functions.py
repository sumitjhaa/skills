import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm as scipy_expm, logm as scipy_logm, sqrtm as scipy_sqrtm
from scipy.linalg import schur


def expm_series(A, max_terms=100, tol=1e-15):
    """Matrix exponential via Taylor series."""
    n = A.shape[0]
    result = np.eye(n)
    term = np.eye(n)
    for k in range(1, max_terms):
        term = term @ A / k
        result += term
        if np.linalg.norm(term, np.inf) < tol:
            break
    return result


def expm_scaling_squaring(A, s=6):
    """Matrix exponential via scaling and squaring."""
    A_scaled = A / (2 ** s)
    E = expm_series(A_scaled)
    for _ in range(s):
        E = E @ E
    return E


def expm_eig(A):
    """Matrix exponential via eigendecomposition (for diagonalizable A)."""
    eigvals, eigvecs = np.linalg.eig(A)
    return eigvecs @ np.diag(np.exp(eigvals)) @ np.linalg.inv(eigvecs)


def logm_series(A, max_iter=100, tol=1e-12):
    """Matrix logarithm via inverse scaling and squaring (simplified)."""
    n = A.shape[0]
    I = np.eye(n)

    s = 0
    while np.linalg.norm(A - I, np.inf) > 0.5:
        A = scipy_sqrtm(A)
        s += 1

    A = A - I
    result = np.zeros((n, n))
    term = A.copy()
    k = 1
    while np.linalg.norm(term, np.inf) > tol and k < max_iter:
        if k % 2 == 1:
            result += term / k
        else:
            result -= term / k
        k += 1
        term = term @ A

    return (2 ** s) * result


def sqrtm_eig(A):
    """Matrix square root via eigendecomposition (for symmetric A)."""
    eigvals, eigvecs = np.linalg.eigh(A)
    return eigvecs @ np.diag(np.sqrt(np.maximum(eigvals, 0))) @ eigvecs.T


def sqrtm_denman_beavers(A, max_iter=50, tol=1e-12):
    """Matrix square root via Denman-Beavers iteration."""
    n = A.shape[0]
    Y = A.copy()
    Z = np.eye(n)
    for _ in range(max_iter):
        Y_inv = np.linalg.inv(Y)
        Z_inv = np.linalg.inv(Z)
        Y_new = 0.5 * (Y + Z_inv)
        Z_new = 0.5 * (Z + Y_inv)
        if np.linalg.norm(Y_new - Y, np.inf) < tol and \
           np.linalg.norm(Z_new - Z, np.inf) < tol:
            break
        Y, Z = Y_new, Z_new
    return Y


def frechet_exp(A, E):
    """Finite difference Fréchet derivative of expm."""
    n = A.shape[0]
    M = np.block([[A, E],
                  [np.zeros((n, n)), A]])
    return scipy_expm(M)[:n, n:]


def main():
    print("=" * 60)
    print("MATRIX FUNCTIONS - expm, logm, sqrtm")
    print("=" * 60)

    np.random.seed(42)

    print("\n--- Matrix Exponential ---")
    A = np.random.randn(5, 5)
    A = A - A.T  # Skew-symmetric (exp is orthogonal)

    E_series = expm_series(A, max_terms=50)
    E_ss = expm_scaling_squaring(A, s=6)
    E_scipy = scipy_expm(A)

    print(f"Series error: {np.linalg.norm(E_series - E_scipy):.2e}")
    print(f"Scale-square error: {np.linalg.norm(E_ss - E_scipy):.2e}")
    print(f"exp(A)^T exp(A) (should be I for skew-sym):\n"
          f"{np.round(E_scipy.T @ E_scipy, 4)}")

    print("\n--- Matrix Exponential ODE Solution ---")
    t_values = np.linspace(0, 5, 50)
    x0 = np.array([1.0, 0.0])

    A_ode = np.array([[0, -1], [1, 0]])
    x_t = np.array([scipy_expm(t * A_ode) @ x0 for t in t_values])

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.plot(x_t[:, 0], x_t[:, 1], 'b-', linewidth=2)
    ax.plot(x0[0], x0[1], 'ro', markersize=10)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Solution of dx/dt = A x via Matrix Exponential')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    plt.show()

    print("\n--- Matrix Logarithm ---")
    A_rot = scipy_expm(np.array([[0, -1], [1, 0]]))
    L_scipy = scipy_logm(A_rot)
    print(f"log(exp(A)):\n{np.round(L_scipy, 4)}")
    print(f"log error: {np.linalg.norm(scipy_expm(L_scipy) - A_rot):.2e}")

    print("\n--- Matrix Square Root ---")
    A_spd = np.array([[4.0, 2.0], [2.0, 3.0]])
    S_eig = sqrtm_eig(A_spd)
    S_db = sqrtm_denman_beavers(A_spd)
    S_scipy = scipy_sqrtm(A_spd)

    print(f"A =\n{A_spd}")
    print(f"sqrt (eig):\n{np.round(S_eig, 4)}")
    print(f"sqrt (DB):\n{np.round(S_db, 4)}")
    print(f"sqrt (scipy):\n{np.round(S_scipy, 4)}")
    print(f"sqrt^2 == A (eig): {np.allclose(S_eig @ S_eig, A_spd)}")
    print(f"sqrt^2 == A (DB): {np.allclose(S_db @ S_db, A_spd)}")

    print("\n--- Matrix Function Properties ---")
    for n_test in [3, 5, 10]:
        A_test = np.random.randn(n_test, n_test) / n_test
        B_test = np.random.randn(n_test, n_test) / n_test

        exp_AB = scipy_expm(A_test + B_test)
        exp_A_exp_B = scipy_expm(A_test) @ scipy_expm(B_test)
        print(f"n={n_test}: exp(A+B) ≈ exp(A)exp(B): "
              f"{np.linalg.norm(exp_AB - exp_A_exp_B):.2e} (not equal unless commuting)")

    print("\n--- Schur-Parlett for General Functions ---")
    A_schur = np.random.randn(4, 4)
    T, Z = schur(A_schur)
    print(f"Schur form T:\n{np.round(T, 3)}")
    print(f"Z^T A Z == T: {np.allclose(Z.T @ A_schur @ Z, T)}")

    f_T = np.diag(np.exp(np.diag(T)))
    f_A = Z @ f_T @ Z.T
    f_A_ref = scipy_expm(A_schur)
    print(f"Diagonal Schur-Parlett exp error: {np.linalg.norm(f_A - f_A_ref):.2e}")

    print("\n--- Matrix Exponential Convergence ---")
    norms = []
    A_norm = np.random.randn(5, 5)
    for k in range(1, 30):
        term = np.linalg.matrix_power(A_norm, k) / np.math.factorial(k)
        norms.append(np.linalg.norm(term, np.inf))
    print(f"Series terms decay: first={norms[0]:.4f}, last={norms[-1]:.2e}")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.semilogy(range(1, 30), norms, 'b-o')
    ax.set_xlabel('Term index k')
    ax.set_ylabel('||A^k/k!||')
    ax.set_title('Taylor Series Term Decay for exp(A)')
    ax.grid(True, alpha=0.3)
    plt.show()


if __name__ == "__main__":
    main()
