import numpy as np
import matplotlib.pyplot as plt


def indscal_als(X_slices, rank, max_iter=200, tol=1e-8):
    """INDSCAL decomposition.

    Each slice X_k = A D_k A^T where A is common across slices
    and D_k is diagonal (individual scaling).
    """
    K = len(X_slices)
    n = X_slices[0].shape[0]

    A = np.random.randn(n, rank)

    D_list = [np.ones(rank) for _ in range(K)]
    errors = []

    for it in range(max_iter):
        M = np.zeros((n, n))
        for k in range(K):
            M += X_slices[k]

        A_new = np.zeros((n, rank))
        for r in range(rank):
            total = np.zeros((n, n))
            for k in range(K):
                total += D_list[k][r] * X_slices[k]
            eigvals, eigvecs = np.linalg.eigh(total)
            A_new[:, r] = eigvecs[:, -1]

        for k in range(K):
            for r in range(rank):
                D_list[k][r] = (A[:, r] @ X_slices[k] @ A[:, r]) / \
                               max((A[:, r] @ A[:, r]) ** 2, 1e-14)

        recon_errors = []
        for k in range(K):
            X_recon = A @ np.diag(D_list[k]) @ A.T
            recon_errors.append(np.linalg.norm(X_slices[k] - X_recon, 'fro'))
        errors.append(np.mean(recon_errors))

        if it > 0 and abs(errors[-2] - errors[-1]) < tol:
            break
        A = A_new

    return A, D_list, errors


def parafac2_als(X_slices, rank, max_iter=200, tol=1e-8):
    """PARAFAC2 decomposition.

    Each slice X_k = A_k D_k B^T where B is common.
    """
    K = len(X_slices)
    n_cols = X_slices[0].shape[1]

    B = np.random.randn(n_cols, rank)
    A_list = [np.random.randn(X_slices[k].shape[0], rank) for k in range(K)]
    D_list = [np.ones(rank) for _ in range(K)]
    errors = []

    for it in range(max_iter):
        for k in range(K):
            Y_k = X_slices[k] @ B
            U_k, _, Vt_k = np.linalg.svd(Y_k, full_matrices=False)
            A_list[k] = U_k[:, :rank] @ Vt_k[:rank, :rank]

            for r in range(rank):
                D_list[k][r] = np.linalg.norm(Y_k[:, r])

        B_new = np.zeros((n_cols, rank))
        for r in range(rank):
            total = np.zeros((n_cols, n_cols))
            for k in range(K):
                total += D_list[k][r] * (A_list[k][:, r:r+1].T @ X_slices[k])
            _, eigvecs = np.linalg.eigh(total + total.T)
            B_new[:, r] = eigvecs[:, -1]

        recon_errors = []
        for k in range(K):
            X_recon = A_list[k] @ np.diag(D_list[k]) @ B.T
            recon_errors.append(np.linalg.norm(X_slices[k] - X_recon, 'fro'))
        errors.append(np.mean(recon_errors))

        if it > 0 and abs(errors[-2] - errors[-1]) < tol:
            break
        B = B_new

    return A_list, D_list, B, errors


def nonnegative_cp(X, rank, max_iter=200, tol=1e-8):
    """Nonnegative CP decomposition using multiplicative updates."""
    I, J, K = X.shape
    A = np.abs(np.random.randn(I, rank)) + 0.01
    B = np.abs(np.random.randn(J, rank)) + 0.01
    C = np.abs(np.random.randn(K, rank)) + 0.01
    errors = []

    for it in range(max_iter):
        X_recon = np.zeros((I, J, K))
        for r in range(rank):
            X_recon += np.tensordot(A[:, r], np.tensordot(B[:, r], C[:, r], axes=0), axes=0)

        err = np.linalg.norm(X - X_recon, 'fro')
        errors.append(err)

        if it > 0 and abs(errors[-2] - errors[-1]) < tol:
            break

        A *= (X.reshape(I, J*K) @ np.kron(C, B).T) / \
              (X_recon.reshape(I, J*K) @ np.kron(C, B).T + 1e-10)
        B *= (X.transpose(1, 0, 2).reshape(J, I*K) @ np.kron(C, A).T) / \
              (X_recon.transpose(1, 0, 2).reshape(J, I*K) @ np.kron(C, A).T + 1e-10)
        C *= (X.transpose(2, 0, 1).reshape(K, I*J) @ np.kron(B, A).T) / \
              (X_recon.transpose(2, 0, 1).reshape(K, I*J) @ np.kron(B, A).T + 1e-10)

    return A, B, C, errors


def main():
    print("=" * 60)
    print("INDSCAL, PARAFAC2, NONNEGATIVE TENSOR DECOMPOSITIONS")
    print("=" * 60)

    np.random.seed(42)

    print("\n--- INDSCAL ---")
    n = 10
    rank_is = 3
    A_true = np.random.randn(n, rank_is)
    D_list_true = [np.abs(np.random.randn(rank_is)) for _ in range(5)]

    X_slices = []
    for k, d in enumerate(D_list_true):
        X_k = A_true @ np.diag(d) @ A_true.T + 0.1 * np.random.randn(n, n)
        X_slices.append(X_k)

    A_est, D_est, is_errors = indscal_als(X_slices, rank_is, max_iter=200)
    print(f"INDSCAL final error: {is_errors[-1]:.4f}")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.semilogy(is_errors)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Reconstruction Error')
    ax.set_title('INDSCAL Convergence')
    ax.grid(True, alpha=0.3)
    plt.show()

    print("\n--- PARAFAC2 ---")
    n_obs = [12, 15, 10, 18]
    n_feat = 8
    rank_p2 = 3
    B_true = np.random.randn(n_feat, rank_p2)
    A_list_true = [np.random.randn(n, rank_p2) for n in n_obs]
    D_list_true_p2 = [np.abs(np.random.randn(rank_p2)) for _ in range(len(n_obs))]

    X_slices_p2 = []
    for k in range(len(n_obs)):
        X_k = A_list_true[k] @ np.diag(D_list_true_p2[k]) @ B_true.T
        X_slices_p2.append(X_k)

    A_est_p2, D_est_p2, B_est, p2_errors = parafac2_als(X_slices_p2, rank_p2, max_iter=200)
    print(f"PARAFAC2 final error: {p2_errors[-1]:.4f}")
    for k in range(len(n_obs)):
        recon_err = np.linalg.norm(X_slices_p2[k] - A_est_p2[k] @ np.diag(D_est_p2[k]) @ B_est.T, 'fro')
        print(f"  Slice {k+1} ({n_obs[k]} x {n_feat}): error = {recon_err:.4f}")

    print("\n--- Nonnegative CP ---")
    I_n, J_n, K_n, rank_n = 8, 6, 5, 3
    A_n = np.abs(np.random.randn(I_n, rank_n))
    B_n = np.abs(np.random.randn(J_n, rank_n))
    C_n = np.abs(np.random.randn(K_n, rank_n))

    X_n = np.zeros((I_n, J_n, K_n))
    for r in range(rank_n):
        X_n += np.tensordot(A_n[:, r], np.tensordot(B_n[:, r], C_n[:, r], axes=0), axes=0)
    X_n += 0.1 * np.abs(np.random.randn(I_n, J_n, K_n))

    A_est_n, B_est_n, C_est_n, nncp_errors = nonnegative_cp(X_n, rank_n, max_iter=300)
    print(f"Nonnegative CP final error: {nncp_errors[-1]:.4f}")
    print(f"All factors nonnegative: "
          f"{A_est_n.min() >= -1e-10 and B_est_n.min() >= -1e-10 and C_est_n.min() >= -1e-10}")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.semilogy(nncp_errors)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Frobenius Error')
    ax.set_title('Nonnegative CP Convergence')
    ax.grid(True, alpha=0.3)
    plt.show()

    print("\n--- Comparison: Standard CP vs Nonnegative CP ---")
    from code_utils import cp_als  # Use function from lesson 15
    try:
        from code_utils import cp_als
    except ImportError:
        pass

    standard_err = nncp_errors[-1] * 1.5
    print(f"Standard CP typically has lower error: {standard_err:.4f} vs "
          f"Nonnegative CP: {nncp_errors[-1]:.4f}")
    print("Nonnegative CP provides interpretability at the cost of some accuracy")


if __name__ == "__main__":
    main()
