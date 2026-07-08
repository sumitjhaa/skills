import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.sparse.linalg import gmres as scipy_gmres, cg as scipy_cg


def arnoldi(A, b, k):
    """Arnoldi iteration for general matrices."""
    n = A.shape[0]
    v = b / np.linalg.norm(b)
    V = np.zeros((n, k + 1))
    V[:, 0] = v
    H = np.zeros((k + 1, k))

    for j in range(k):
        w = A @ V[:, j]
        for i in range(j + 1):
            H[i, j] = V[:, i] @ w
            w -= H[i, j] * V[:, i]
        H[j + 1, j] = np.linalg.norm(w)
        if H[j + 1, j] > 1e-14:
            V[:, j + 1] = w / H[j + 1, j]
        else:
            break

    return V, H


def gmres(A, b, max_iter=100, tol=1e-10, restart=20):
    """GMRES solver with restart."""
    n = len(b)
    x = np.zeros(n)
    r = b - A @ x
    beta = np.linalg.norm(r)
    residuals = [beta]

    for outer in range(max_iter // restart):
        V, H = arnoldi(A, r / beta, restart)
        k = H.shape[1]

        e1 = np.zeros(k + 1)
        e1[0] = beta

        y, _, _, _ = np.linalg.lstsq(H[:k + 1, :k], e1, rcond=None)
        x += V[:, :k] @ y

        r = b - A @ x
        beta = np.linalg.norm(r)
        residuals.append(beta)

        if beta < tol:
            break

    return x, residuals


def lanczos(A, v, k):
    """Lanczos iteration for symmetric matrices."""
    n = A.shape[0]
    V = np.zeros((n, k + 1))
    alpha = np.zeros(k)
    beta = np.zeros(k)

    V[:, 0] = v / np.linalg.norm(v)

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

    return V, alpha, beta


def conjugate_gradient(A, b, max_iter=1000, tol=1e-10):
    """Conjugate Gradient method for SPD matrices."""
    x = np.zeros(len(b))
    r = b - A @ x
    p = r.copy()
    rsq = r @ r
    residuals = [np.sqrt(rsq)]

    for i in range(max_iter):
        Ap = A @ p
        alpha = rsq / (p @ Ap)
        x += alpha * p
        r -= alpha * Ap
        rsq_new = r @ r
        residuals.append(np.sqrt(rsq_new))

        if np.sqrt(rsq_new) < tol:
            break
        p = r + (rsq_new / rsq) * p
        rsq = rsq_new

    return x, residuals


def jacobi_preconditioner(A):
    """Jacobi preconditioner M = diag(A)."""
    d = np.diag(A).copy()
    d[np.abs(d) < 1e-14] = 1.0
    return 1.0 / d


def preconditioned_cg(A, b, M_diag, max_iter=1000, tol=1e-10):
    """CG with diagonal preconditioner."""
    x = np.zeros(len(b))
    r = b - A @ x
    z = M_diag * r
    p = z.copy()
    rz = r @ z
    residuals = [np.linalg.norm(r)]

    for i in range(max_iter):
        Ap = A @ p
        alpha = rz / (p @ Ap)
        x += alpha * p
        r -= alpha * Ap
        z = M_diag * r
        rz_new = r @ z
        residuals.append(np.linalg.norm(r))

        if residuals[-1] < tol:
            break
        p = z + (rz_new / rz) * p
        rz = rz_new

    return x, residuals


def laplacian_1d(n):
    """1D Laplacian matrix."""
    return diags([-1, 2, -1], [-1, 0, 1], shape=(n, n)).toarray()


def main():
    print("=" * 60)
    print("KRYLOV METHODS - Arnoldi, Lanczos, GMRES, CG")
    print("=" * 60)

    np.random.seed(42)

    print("\n--- Arnoldi Iteration ---")
    n_arnoldi = 20
    A_arnoldi = np.random.randn(n_arnoldi, n_arnoldi)
    b_arnoldi = np.random.randn(n_arnoldi)
    V, H = arnoldi(A_arnoldi, b_arnoldi, 10)
    print(f"V shape: {V.shape}")
    print(f"H shape: {H.shape}")
    print(f"V^T V (should be I): {np.linalg.norm(V.T @ V - np.eye(V.shape[1])):.2e}")

    print("\n--- Lanczos Iteration ---")
    A_sym = A_arnoldi.T @ A_arnoldi
    V_lan, alpha, beta = lanczos(A_sym, b_arnoldi, 10)
    T = np.diag(alpha) + np.diag(beta[:-1], 1) + np.diag(beta[:-1], -1)
    print(f"Tridiagonal T:\n{np.round(T, 2)}")
    print(f"T symmetric: {np.allclose(T, T.T)}")

    print("\n--- GMRES ---")
    n_gmres = 50
    A_unsym = np.random.randn(n_gmres, n_gmres)
    b_gmres = np.random.randn(n_gmres)
    x_gmres, res_gmres = gmres(A_unsym, b_gmres, max_iter=200, restart=20)
    x_ref = np.linalg.solve(A_unsym, b_gmres)
    print(f"GMRES relative error: {np.linalg.norm(x_gmres - x_ref) / np.linalg.norm(x_ref):.2e}")
    print(f"GMRES iterations: {len(res_gmres)}")

    print("\n--- Conjugate Gradient ---")
    n_cg = 100
    A_cg = np.random.randn(n_cg, n_cg)
    A_cg = A_cg.T @ A_cg + np.eye(n_cg)
    b_cg = np.random.randn(n_cg)

    x_cg, res_cg = conjugate_gradient(A_cg, b_cg, max_iter=200)
    x_cg_ref = np.linalg.solve(A_cg, b_cg)
    print(f"CG relative error: {np.linalg.norm(x_cg - x_cg_ref) / np.linalg.norm(x_cg_ref):.2e}")
    print(f"CG iterations: {len(res_cg)}")

    print("\n--- Preconditioned CG ---")
    M_diag = jacobi_preconditioner(A_cg)
    x_pcg, res_pcg = preconditioned_cg(A_cg, b_cg, M_diag, max_iter=200)
    print(f"PCG relative error: {np.linalg.norm(x_pcg - x_cg_ref) / np.linalg.norm(x_cg_ref):.2e}")
    print(f"PCG iterations: {len(res_pcg)}")

    print("\n--- 1D Laplacian Solve ---")
    n_lapl = 50
    A_lapl = laplacian_1d(n_lapl)
    b_lapl = np.ones(n_lapl)

    x_cg_lapl, res_cg_lapl = conjugate_gradient(A_lapl, b_lapl, max_iter=500)
    x_direct = np.linalg.solve(A_lapl, b_lapl)
    print(f"Laplacian CG error: {np.linalg.norm(x_cg_lapl - x_direct):.2e}")
    print(f"Laplacian CG iterations: {len(res_cg_lapl)}")

    print("\n--- Convergence Comparison ---")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].semilogy(res_gmres, 'b-', label='GMRES')
    axes[0].set_xlabel('Iteration')
    axes[0].set_ylabel('Residual norm')
    axes[0].set_title('GMRES Convergence')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].semilogy(res_cg, 'g-', label='CG')
    axes[1].semilogy(res_pcg, 'r-', label='PCG (Jacobi)')
    axes[1].set_xlabel('Iteration')
    axes[1].set_ylabel('Residual norm')
    axes[1].set_title('CG vs PCG Convergence')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    print("\n--- Conditioning Effect on CG ---")
    for cond_target in [1e2, 1e4, 1e6]:
        U, _, Vt = np.linalg.svd(np.random.randn(50, 50))
        s = np.logspace(0, -np.log10(cond_target), 50)
        A_cond = U @ np.diag(s) @ Vt
        A_cond = A_cond.T @ A_cond
        b_cond = np.random.randn(50)

        x_c, res_c = conjugate_gradient(A_cond, b_cond, max_iter=1000, tol=1e-8)
        print(f"Cond={cond_target:.0e}: CG converged in {len(res_c)} iterations")

    print("\n--- Compare with SciPy ---")
    x_sp_cg, info_cg = scipy_cg(A_cg, b_cg, tol=1e-10)
    x_sp_gmres, info_gmres = scipy_gmres(A_unsym, b_gmres, tol=1e-10)
    print(f"SciPy CG error: {np.linalg.norm(x_sp_cg - x_cg_ref) / np.linalg.norm(x_cg_ref):.2e}")
    print(f"SciPy GMRES error: {np.linalg.norm(x_sp_gmres - x_ref) / np.linalg.norm(x_ref):.2e}")


if __name__ == "__main__":
    main()
