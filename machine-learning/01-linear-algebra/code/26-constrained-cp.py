import numpy as np
import matplotlib.pyplot as plt


def soft_threshold(x, lam):
    """Soft-thresholding operator."""
    return np.sign(x) * np.maximum(np.abs(x) - lam, 0)


def orthogonalize(A):
    """Project onto Stiefel manifold (orthogonal columns)."""
    Q, R = np.linalg.qr(A)
    return Q


def cp_als(X, rank, max_iter=200, tol=1e-8):
    """Standard CP-ALS for comparison."""
    I, J, K = X.shape
    A = np.random.randn(I, rank)
    B = np.random.randn(J, rank)
    C = np.random.randn(K, rank)
    errors = []

    for it in range(max_iter):
        A = np.linalg.lstsq((B.T @ B) * (C.T @ C),
            np.tensordot(X, B, axes=([1], [0])).reshape(I, J*K) @ np.kron(C, B),
            rcond=None)[0].reshape(I, rank)
        B = np.linalg.lstsq((A.T @ A) * (C.T @ C),
            np.tensordot(X.transpose(1, 0, 2), A, axes=([1], [0])).reshape(J, I*K) @ np.kron(C, A),
            rcond=None)[0].reshape(J, rank)
        C = np.linalg.lstsq((A.T @ A) * (B.T @ B),
            np.tensordot(X.transpose(2, 0, 1), A, axes=([1], [0])).reshape(K, I*J) @ np.kron(B, A),
            rcond=None)[0].reshape(K, rank)

        X_recon = np.zeros((I, J, K))
        for r in range(rank):
            X_recon += np.tensordot(A[:, r], np.tensordot(B[:, r], C[:, r], axes=0), axes=0)
        err = np.linalg.norm(X - X_recon) / np.linalg.norm(X)
        errors.append(err)

        if it > 0 and abs(errors[-2] - err) < tol:
            break

    return A, B, C, errors


def orthogonal_cp(X, rank, max_iter=200, tol=1e-8):
    """CP with orthogonality constraints on all factors."""
    I, J, K = X.shape
    A, _ = np.linalg.qr(np.random.randn(I, rank))
    B, _ = np.linalg.qr(np.random.randn(J, rank))
    C, _ = np.linalg.qr(np.random.randn(K, rank))
    errors = []

    for it in range(max_iter):
        BtB = B.T @ B
        CtC = C.T @ C
        A = np.tensordot(X, B, axes=([1], [0])).reshape(I, J*K) @ np.kron(C, B)
        A = np.linalg.solve(BtB * CtC, A.T).T
        A, _ = np.linalg.qr(A)

        AtA = A.T @ A
        B = np.tensordot(X.transpose(1, 0, 2), A, axes=([1], [0])).reshape(J, I*K) @ np.kron(C, A)
        B = np.linalg.solve(AtA * CtC, B.T).T
        B, _ = np.linalg.qr(B)

        AtA = A.T @ A
        BtB = B.T @ B
        C = np.tensordot(X.transpose(2, 0, 1), A, axes=([1], [0])).reshape(K, I*J) @ np.kron(B, A)
        C = np.linalg.solve(AtA * BtB, C.T).T
        C, _ = np.linalg.qr(C)

        X_recon = np.zeros((I, J, K))
        for r in range(rank):
            X_recon += np.tensordot(A[:, r], np.tensordot(B[:, r], C[:, r], axes=0), axes=0)
        err = np.linalg.norm(X - X_recon) / np.linalg.norm(X)
        errors.append(err)

        if it > 0 and abs(errors[-2] - err) < tol:
            break

    return A, B, C, errors


def sparse_cp(X, rank, lam=0.1, max_iter=200, tol=1e-8):
    """CP with L1 sparsity regularization."""
    I, J, K = X.shape
    A = np.random.randn(I, rank)
    B = np.random.randn(J, rank)
    C = np.random.randn(K, rank)
    errors = []

    for it in range(max_iter):
        A_unreg = np.linalg.lstsq((B.T @ B) * (C.T @ C),
            np.tensordot(X, B, axes=([1], [0])).reshape(I, J*K) @ np.kron(C, B),
            rcond=None)[0].reshape(I, rank)
        A = soft_threshold(A_unreg, lam)

        B_unreg = np.linalg.lstsq((A.T @ A) * (C.T @ C),
            np.tensordot(X.transpose(1, 0, 2), A, axes=([1], [0])).reshape(J, I*K) @ np.kron(C, A),
            rcond=None)[0].reshape(J, rank)
        B = soft_threshold(B_unreg, lam)

        C_unreg = np.linalg.lstsq((A.T @ A) * (B.T @ B),
            np.tensordot(X.transpose(2, 0, 1), A, axes=([1], [0])).reshape(K, I*J) @ np.kron(B, A),
            rcond=None)[0].reshape(K, rank)
        C = soft_threshold(C_unreg, lam)

        X_recon = np.zeros((I, J, K))
        for r in range(rank):
            X_recon += np.tensordot(A[:, r], np.tensordot(B[:, r], C[:, r], axes=0), axes=0)
        err = np.linalg.norm(X - X_recon) / np.linalg.norm(X)
        errors.append(err)

        if it > 0 and abs(errors[-2] - err) < tol:
            break

    return A, B, C, errors


def main():
    print("=" * 60)
    print("CONSTRAINED CP - Orthogonal, Sparse, Nonnegative")
    print("=" * 60)

    np.random.seed(42)

    I, J, K, rank = 10, 8, 6, 3
    A_true = np.random.randn(I, rank)
    B_true = np.random.randn(J, rank)
    C_true = np.random.randn(K, rank)
    X = np.zeros((I, J, K))
    for r in range(rank):
        X += np.tensordot(A_true[:, r], np.tensordot(B_true[:, r], C_true[:, r], axes=0), axes=0)
    X += 0.05 * np.random.randn(I, J, K)

    print("--- Standard CP ---")
    A_s, B_s, C_s, err_s = cp_als(X, rank)
    print(f"  Error: {err_s[-1]:.4f}")

    print("\n--- Orthogonal CP ---")
    A_o, B_o, C_o, err_o = orthogonal_cp(X, rank)
    print(f"  Error: {err_o[-1]:.4f}")
    print(f"  A^T A (should be I):\n{np.round(A_o.T @ A_o, 2)}")
    print(f"  B^T B (should be I):\n{np.round(B_o.T @ B_o, 2)}")
    print(f"  C^T C (should be I):\n{np.round(C_o.T @ C_o, 2)}")

    print("\n--- Sparse CP (L1 regularization) ---")
    for lam in [0.01, 0.05, 0.1, 0.2]:
        A_sp, B_sp, C_sp, err_sp = sparse_cp(X, rank, lam=lam)
        sparsity_A = np.mean(np.abs(A_sp) < 1e-4)
        sparsity_B = np.mean(np.abs(B_sp) < 1e-4)
        sparsity_C = np.mean(np.abs(C_sp) < 1e-4)
        print(f"  lambda={lam}: error={err_sp[-1]:.4f}, sparsity: "
              f"A={sparsity_A:.2f}, B={sparsity_B:.2f}, C={sparsity_C:.2f}")

    print("\n--- Constraint Comparison ---")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    axes[0, 0].semilogy(err_s, label='Standard')
    axes[0, 0].semilogy(err_o, label='Orthogonal')
    axes[0, 0].set_title('Convergence: Standard vs Orthogonal')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    lam_test = 0.05
    A_sp2, B_sp2, C_sp2, err_sp2 = sparse_cp(X, rank, lam=lam_test)
    axes[0, 1].semilogy(err_s, label='Standard')
    axes[0, 1].semilogy(err_sp2, label=f'Sparse (lam={lam_test})')
    axes[0, 1].set_title('Convergence: Standard vs Sparse')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Sparsity pattern visualization
    axes[1, 0].spy(A_sp2, markersize=3)
    axes[1, 0].set_title(f'Sparse A (sparsity={np.mean(np.abs(A_sp2) < 1e-4):.2f})')

    axes[1, 1].spy(C_sp2, markersize=3)
    axes[1, 1].set_title(f'Sparse C (sparsity={np.mean(np.abs(C_sp2) < 1e-4):.2f})')

    plt.tight_layout()
    plt.show()

    print("\n--- Orthogonality vs Sparsity vs Fit ---")
    results = []
    for lam_test2 in [0, 0.01, 0.05, 0.1, 0.2, 0.5]:
        A_t, B_t, C_t, e_t = sparse_cp(X, rank, lam=lam_test2, max_iter=150)
        sparsity = np.mean(np.abs(A_t) < 1e-4)
        results.append((lam_test2, e_t[-1], sparsity))
        print(f"  lam={lam_test2:.2f}: error={e_t[-1]:.4f}, sparsity={sparsity:.2f}")

    print("\n--- Factor Correlation (Orthogonal) ---")
    corr_A = np.corrcoef(A_o.T)
    corr_B = np.corrcoef(B_o.T)
    print(f"  A factor correlations:\n{np.round(corr_A, 2)}")
    print(f"  B factor correlations:\n{np.round(corr_B, 2)}")

    print("\n--- Factor Correlation (Standard) ---")
    corr_A_s = np.corrcoef(A_s.T)
    print(f"  A factor correlations:\n{np.round(corr_A_s, 2)}")


if __name__ == "__main__":
    main()
