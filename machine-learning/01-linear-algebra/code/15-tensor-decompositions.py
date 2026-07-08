import numpy as np
import matplotlib.pyplot as plt


def khatri_rao(A, B):
    """Khatri-Rao product (column-wise Kronecker)."""
    I, K = A.shape
    J, K2 = B.shape
    assert K == K2, "Inner dimensions must match"
    C = np.zeros((I * J, K))
    for k in range(K):
        C[:, k] = np.kron(A[:, k], B[:, k])
    return C


def cp_als(X, rank, max_iter=200, tol=1e-8):
    """CP decomposition via ALS."""
    I, J, K = X.shape

    A = np.random.randn(I, rank)
    B = np.random.randn(J, rank)
    C = np.random.randn(K, rank)
    errors = []

    for it in range(max_iter):
        A = np.linalg.lstsq(
            (B.T @ B) * (C.T @ C),
            np.tensordot(X, B, axes=([1], [0])).reshape(I, J*K) @ np.kron(C, B),
            rcond=None)[0].reshape(I, rank)

        B = np.linalg.lstsq(
            (A.T @ A) * (C.T @ C),
            np.tensordot(X.transpose(1, 0, 2), A, axes=([1], [0])).reshape(J, I*K) @ np.kron(C, A),
            rcond=None)[0].reshape(J, rank)

        C = np.linalg.lstsq(
            (A.T @ A) * (B.T @ B),
            np.tensordot(X.transpose(2, 0, 1), A, axes=([1], [0])).reshape(K, I*J) @ np.kron(B, A),
            rcond=None)[0].reshape(K, rank)

        recon = np.tensordot(A, np.tensordot(B, C, axes=([1], [1])), axes=([1], [0]))
        recon = recon.transpose(1, 0, 2)
        err = np.linalg.norm(X - recon) / np.linalg.norm(X)
        errors.append(err)

        if it > 0 and abs(errors[-2] - err) < tol:
            break

    return A, B, C, errors


def cp_reconstruct(A, B, C):
    """Reconstruct tensor from CP factors."""
    I, R = A.shape
    J, _ = B.shape
    K, _ = C.shape
    X = np.zeros((I, J, K))
    for r in range(R):
        X += np.tensordot(A[:, r], np.tensordot(B[:, r], C[:, r], axes=0), axes=0)
    return X


def tucker_hooi(X, rank, max_iter=50, tol=1e-8):
    """Tucker decomposition via HOOI (Higher-Order Orthogonal Iteration)."""
    I, J, K = X.shape
    R1, R2, R3 = rank

    A = np.linalg.svd(X.reshape(I, J*K), compute_uv=True)[0][:, :R1]
    B = np.linalg.svd(X.transpose(1, 0, 2).reshape(J, I*K), compute_uv=True)[0][:, :R2]
    C = np.linalg.svd(X.transpose(2, 0, 1).reshape(K, I*J), compute_uv=True)[0][:, :R3]
    errors = []

    for it in range(max_iter):
        X1 = np.tensordot(X, B, axes=([1], [0]))
        X1 = np.tensordot(X1, C, axes=([2], [0]))
        A = np.linalg.svd(X1.reshape(I, R2*R3), compute_uv=True)[0][:, :R1]

        X2 = np.tensordot(X, A, axes=([0], [0]))
        X2 = np.tensordot(X2, C, axes=([2], [0]))
        B = np.linalg.svd(X2.reshape(J, R1*R3), compute_uv=True)[0][:, :R2]

        X3 = np.tensordot(X, A, axes=([0], [0]))
        X3 = np.tensordot(X3, B, axes=([1], [0]))
        C = np.linalg.svd(X3.reshape(K, R1*R2), compute_uv=True)[0][:, :R3]

        core = np.tensordot(X, A, axes=([0], [0]))
        core = np.tensordot(core, B, axes=([0], [0]))
        core = np.tensordot(core, C, axes=([0], [0]))

        recon = np.tensordot(core, A, axes=([0], [1]))
        recon = np.tensordot(recon, B, axes=([0], [1]))
        recon = np.tensordot(recon, C, axes=([0], [1])).transpose(1, 2, 0)

        err = np.linalg.norm(X - recon) / np.linalg.norm(X)
        errors.append(err)

        if it > 0 and abs(errors[-2] - err) < tol:
            break

    return core, (A, B, C), errors


def tensor_train_decompose(X, rank):
    """Simple Tensor Train decomposition."""
    d = X.ndim
    cores = []
    shape = list(X.shape)
    ranks = [1] + list(rank) + [1]

    current = X
    for i in range(d - 1):
        current = current.reshape(ranks[i] * shape[i], -1)
        U, s, Vt = np.linalg.svd(current, full_matrices=False)
        r = min(ranks[i + 1], len(s))
        U = U[:, :r]
        s = s[:r]
        Vt = Vt[:r, :]

        core = U.reshape(ranks[i], shape[i], r)
        cores.append(core)
        current = np.diag(s) @ Vt

    core_last = current.reshape(ranks[d - 1], shape[d - 1], ranks[d])
    cores.append(core_last)

    return cores


def main():
    print("=" * 60)
    print("TENSOR DECOMPOSITIONS - CP, Tucker, TT")
    print("=" * 60)

    np.random.seed(42)

    print("\n--- CP Decomposition ---")
    I, J, K, R = 10, 8, 6, 3
    A_true = np.random.randn(I, R)
    B_true = np.random.randn(J, R)
    C_true = np.random.randn(K, R)

    X = cp_reconstruct(A_true, B_true, C_true)
    X_noisy = X + 0.1 * np.random.randn(I, J, K)
    print(f"Tensor shape: {X.shape}, true rank: {R}")

    A, B, C, errors = cp_als(X_noisy, R)
    X_recon = cp_reconstruct(A, B, C)
    rel_err = np.linalg.norm(X_noisy - X_recon) / np.linalg.norm(X_noisy)
    print(f"CP reconstruction error: {rel_err:.4f}")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.semilogy(errors)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Relative Error')
    ax.set_title('CP-ALS Convergence')
    ax.grid(True, alpha=0.3)
    plt.show()

    print("\n--- Tucker Decomposition ---")
    rank_tucker = (3, 3, 3)
    core, factors, tucker_errs = tucker_hooi(X_noisy, rank_tucker)
    print(f"Core shape: {core.shape}")
    print(f"Factor shapes: {[f.shape for f in factors]}")
    print(f"Tucker final error: {tucker_errs[-1]:.4f}")

    print("\n--- Tensor Train Decomposition ---")
    shape_tt = (4, 4, 4, 4)
    X_tt = np.random.randn(*shape_tt)
    tt_rank = (3, 3, 3)
    cores_tt = tensor_train_decompose(X_tt, tt_rank)
    print(f"Number of TT cores: {len(cores_tt)}")
    for i, core in enumerate(cores_tt):
        print(f"  Core {i+1}: {core.shape}")

    print("\n--- Rank Selection ---")
    for test_rank in [1, 2, 3, 4, 5]:
        A_t, B_t, C_t, e_t = cp_als(X_noisy, test_rank, max_iter=100)
        err_t = e_t[-1] if e_t else 1.0
        print(f"  Rank {test_rank}: relative error = {err_t:.4f}")

    print("\n--- Noise Sensitivity ---")
    for noise_level in [0.01, 0.05, 0.1, 0.2, 0.5]:
        X_noisy_lvl = X + noise_level * np.random.randn(I, J, K)
        A_n, B_n, C_n, e_n = cp_als(X_noisy_lvl, R, max_iter=100)
        err_n = e_n[-1] if e_n else 1.0
        print(f"  Noise {noise_level}: relative error = {err_n:.4f}")


if __name__ == "__main__":
    main()
