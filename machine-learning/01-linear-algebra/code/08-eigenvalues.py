import numpy as np
import matplotlib.pyplot as plt


def power_iteration(A, max_iter=10000, tol=1e-10):
    """Power iteration for dominant eigenvalue."""
    n = A.shape[0]
    v = np.random.randn(n)
    v = v / np.linalg.norm(v)
    errors = []

    for i in range(max_iter):
        Av = A @ v
        v_new = Av / np.linalg.norm(Av)
        lam = v_new @ (A @ v_new)

        err = np.linalg.norm(v_new - v)
        errors.append(err)

        if err < tol:
            break
        v = v_new

    return lam, v, errors


def inverse_iteration(A, mu, max_iter=100, tol=1e-10):
    """Inverse iteration to find eigenvalue near mu."""
    n = A.shape[0]
    v = np.random.randn(n)
    v = v / np.linalg.norm(v)
    B = A - mu * np.eye(n)
    errors = []

    for _ in range(max_iter):
        w = np.linalg.solve(B, v)
        v_new = w / np.linalg.norm(w)
        lam = v_new @ (A @ v_new)

        err = np.linalg.norm(v_new - v)
        errors.append(err)

        if err < tol:
            break
        v = v_new

    return lam, v, errors


def rayleigh_quotient_iteration(A, max_iter=100, tol=1e-14):
    """Rayleigh quotient iteration (cubic convergence)."""
    n = A.shape[0]
    v = np.random.randn(n)
    v = v / np.linalg.norm(v)
    mu = v @ (A @ v)
    errors = []

    for _ in range(max_iter):
        B = A - mu * np.eye(n)
        try:
            w = np.linalg.solve(B, v)
        except np.linalg.LinAlgError:
            break
        v_new = w / np.linalg.norm(w)
        mu_new = v_new @ (A @ v_new)

        err = abs(mu_new - mu)
        errors.append(err)

        if err < tol:
            break
        v = v_new
        mu = mu_new

    return mu, v, errors


def qr_algorithm(A, max_iter=10000, tol=1e-12):
    """Basic QR algorithm for all eigenvalues."""
    T = A.copy().astype(float)
    n = A.shape[0]
    off_diagonal_norms = []

    for i in range(max_iter):
        Q, R = np.linalg.qr(T)
        T = R @ Q

        off_diag = np.linalg.norm(np.tril(T, -1))
        off_diagonal_norms.append(off_diag)

        if off_diag < tol:
            break

    return np.sort(np.diag(T)), off_diagonal_norms


def qr_algorithm_with_shifts(A, max_iter=10000, tol=1e-12):
    """QR algorithm with Wilkinson shifts (faster convergence)."""
    n = A.shape[0]
    T = A.copy().astype(float)
    eigenvalues = []
    off_diagonal_norms = []

    def wilkinson_shift(T, n):
        if n == 1:
            return T[0, 0]
        d = (T[n-2, n-2] - T[n-1, n-1]) / 2
        return T[n-1, n-1] - np.sign(d) * (T[n-1, n-1] - T[n-2, n-2]) / \
            (abs(d) + np.sqrt(d**2 + T[n-1, n-2]**2)) if d != 0 else T[n-1, n-1]

    remaining = n
    while remaining > 0:
        off_diag = np.linalg.norm(np.diag(T[:remaining, :remaining], -1))
        off_diagonal_norms.append(off_diag)

        if off_diag < tol:
            eigenvalues.append(T[remaining-1, remaining-1])
            remaining -= 1
            continue

        shift = wilkinson_shift(T, remaining)
        Q, R = np.linalg.qr(T[:remaining, :remaining] - shift * np.eye(remaining))
        T[:remaining, :remaining] = R @ Q + shift * np.eye(remaining)

    return np.sort(eigenvalues), off_diagonal_norms


def lanczos(A, k):
    """Lanczos iteration for tridiagonalizing a symmetric matrix."""
    n = A.shape[0]
    v = np.random.randn(n)
    v = v / np.linalg.norm(v)

    alpha = np.zeros(k)
    beta = np.zeros(k)
    V = np.zeros((n, k + 1))
    V[:, 0] = v

    for j in range(k):
        w = A @ V[:, j]
        alpha[j] = V[:, j] @ w
        w -= alpha[j] * V[:, j]
        if j > 0:
            w -= beta[j - 1] * V[:, j - 1]
        beta[j] = np.linalg.norm(w)
        if beta[j] > 1e-14:
            V[:, j + 1] = w / beta[j]
        else:
            break

    T = np.diag(alpha)
    if k > 1:
        T += np.diag(beta[:k - 1], 1) + np.diag(beta[:k - 1], -1)
    return T, V, alpha, beta


def main():
    print("=" * 60)
    print("EIGENVALUES - Power Iteration, QR, Rayleigh, Lanczos")
    print("=" * 60)

    np.random.seed(42)
    n = 10
    A = np.random.randn(n, n)
    A = A.T @ A  # Make symmetric

    eigvals_ref = np.sort(np.linalg.eigvalsh(A))
    print(f"Reference eigenvalues (first 5): {np.round(eigvals_ref[:5], 4)}")

    print("\n--- Power Iteration ---")
    lam, v, pi_errors = power_iteration(A, max_iter=1000)
    print(f"Dominant eigenvalue: {lam:.6f} (ref: {eigvals_ref[-1]:.6f})")
    print(f"Error: {abs(lam - eigvals_ref[-1]):.2e}")
    print(f"Iterations: {len(pi_errors)}")

    print("\n--- Inverse Iteration ---")
    target = eigvals_ref[n // 2]
    lam_inv, v_inv, inv_errors = inverse_iteration(A, target + 1.0)
    print(f"Eigenvalue near {target:.4f}: {lam_inv:.6f}")
    print(f"Error: {abs(lam_inv - target):.2e}")

    print("\n--- Rayleigh Quotient Iteration ---")
    lam_rq, v_rq, rq_errors = rayleigh_quotient_iteration(A, max_iter=50)
    nearest_ref = eigvals_ref[np.argmin(np.abs(eigvals_ref - lam_rq))]
    print(f"Rayleigh quotient eigenvalue: {lam_rq:.6f}")
    print(f"Nearest reference: {nearest_ref:.6f}")
    print(f"Error: {abs(lam_rq - nearest_ref):.2e}")
    print(f"Iterations: {len(rq_errors)}")

    print("\n--- QR Algorithm ---")
    eigvals_qr, off_norms = qr_algorithm(A, max_iter=5000)
    print(f"QR eigenvalues (first 5): {np.round(eigvals_qr[:5], 4)}")
    print(f"Max error: {np.max(np.abs(eigvals_qr - eigvals_ref)):.2e}")

    print("\n--- QR Algorithm with Wilkinson Shifts ---")
    eigvals_qr_shift, off_norms_shift = qr_algorithm_with_shifts(A, max_iter=5000)
    print(f"QR shifted eigenvalues (first 5): {np.round(eigvals_qr_shift[:5], 4)}")
    print(f"Max error: {np.max(np.abs(eigvals_qr_shift - eigvals_ref)):.2e}")

    print("\n--- Lanczos Iteration ---")
    T, V, alpha, beta = lanczos(A, k=5)
    lanczos_eigvals = np.sort(np.linalg.eigvalsh(T))
    print(f"Lanczos (k=5) eigenvalues: {np.round(lanczos_eigvals, 4)}")
    print(f"Reference extreme eigenvalues: {np.round(eigvals_ref[0], 4)}, {np.round(eigvals_ref[-1], 4)}")
    print(f"Extreme eigenvalue errors: {abs(lanczos_eigvals[0] - eigvals_ref[0]):.2e}, "
          f"{abs(lanczos_eigvals[-1] - eigvals_ref[-1]):.2e}")

    print("\n--- Convergence Visualization ---")
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    axes[0, 0].semilogy(pi_errors)
    axes[0, 0].set_title('Power Iteration Convergence')
    axes[0, 0].set_xlabel('Iteration')
    axes[0, 0].set_ylabel('||v_{k+1} - v_k||')
    axes[0, 0].grid(True, alpha=0.3)

    axes[0, 1].semilogy(inv_errors)
    axes[0, 1].set_title('Inverse Iteration Convergence')
    axes[0, 1].set_xlabel('Iteration')
    axes[0, 1].set_ylabel('Error')
    axes[0, 1].grid(True, alpha=0.3)

    axes[1, 0].semilogy(rq_errors)
    axes[1, 0].set_title('Rayleigh Quotient Iteration (Cubic)')
    axes[1, 0].set_xlabel('Iteration')
    axes[1, 0].set_ylabel('|mu_{k+1} - mu_k|')
    axes[1, 0].grid(True, alpha=0.3)

    axes[1, 1].semilogy(off_norms, label='Basic QR')
    axes[1, 1].semilogy(off_norms_shift[:len(off_norms)], label='QR + Shift')
    axes[1, 1].set_title('QR Algorithm Convergence')
    axes[1, 1].set_xlabel('Iteration')
    axes[1, 1].set_ylabel('Off-diagonal norm')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    print("\n--- Large Sparse (Lanczos Demonstration) ---")
    large_n = 500
    A_large = np.random.randn(large_n, large_n)
    A_large = A_large.T @ A_large / large_n

    for k in [3, 5, 10, 20]:
        T_k, _, _, _ = lanczos(A_large, k)
        eig_k = np.linalg.eigvalsh(T_k)
        eig_full = np.linalg.eigvalsh(A_large)
        print(f"k={k}: smallest={eig_k[0]:.4f} (ref={eig_full[0]:.4f}), "
              f"largest={eig_k[-1]:.4f} (ref={eig_full[-1]:.4f})")


if __name__ == "__main__":
    main()
