import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import svd


def truncated_svd(A, k):
    """Truncated SVD keeping top k components."""
    U, s, Vt = svd(A, full_matrices=False)
    return U[:, :k], s[:k], Vt[:k, :]


def low_rank_approximation(A, k):
    """Best rank-k approximation via truncated SVD."""
    Uk, sk, Vtk = truncated_svd(A, k)
    return Uk @ np.diag(sk) @ Vtk


def approximation_errors(A):
    """Compute errors for all ranks."""
    U, s, Vt = svd(A, full_matrices=False)
    r = np.linalg.matrix_rank(A)
    frob_errors = []
    spec_errors = []

    for k in range(1, r + 1):
        Ak = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]
        frob_errors.append(np.linalg.norm(A - Ak, 'fro'))
        spec_errors.append(np.linalg.norm(A - Ak, 2))

    return frob_errors, spec_errors, s


def nuclear_norm_minimization(A_obs, mask, lam=1.0, max_iter=500, tol=1e-7):
    """Nuclear norm minimization via iterative soft-thresholding (SVT)."""
    X = np.zeros_like(A_obs)
    errors = []

    for i in range(max_iter):
        U, s, Vt = svd(X, full_matrices=False)
        s_shrunk = np.maximum(s - lam, 0)
        X_new = U @ np.diag(s_shrunk) @ Vt
        X_new[mask] = A_obs[mask]

        change = np.linalg.norm(X_new - X)
        errors.append(change)

        if change < tol:
            break
        X = X_new

    return X, errors


def image_compression_demo():
    """Demonstrate image compression with synthetic data."""
    true_rank = 10
    m, n = 100, 100
    U_true, _, Vt_true = np.linalg.svd(np.random.randn(m, m))
    s_true = np.exp(-np.arange(m) / 5)
    A = U_true @ np.diag(s_true) @ Vt_true[:m, :n]

    ranks = [1, 2, 5, 10, 20, 50]
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    for idx, k in enumerate(ranks):
        Ak = low_rank_approximation(A, k)
        ax = axes[idx // 3, idx % 3]
        ax.imshow(Ak, cmap='viridis')
        frob_err = np.linalg.norm(A - Ak, 'fro') / np.linalg.norm(A, 'fro')
        spec_err = np.linalg.norm(A - Ak, 2) / np.linalg.norm(A, 2)
        ax.set_title(f'rank={k}, fr={frob_err:.3f}, sp={spec_err:.3f}')

    plt.suptitle('Low-Rank Approximation (Eckart-Young)')
    plt.tight_layout()
    plt.show()

    return A


def matrix_completion_demo(m=50, n=40, rank=5, obs_ratio=0.3):
    """Matrix completion via nuclear norm minimization."""
    U = np.random.randn(m, rank)
    V = np.random.randn(rank, n)
    A_true = U @ V

    mask = np.random.rand(m, n) < obs_ratio
    A_obs = np.zeros((m, n))
    A_obs[mask] = A_true[mask]

    A_completed, errors = nuclear_norm_minimization(
        A_obs, mask, lam=1.0)

    error = np.linalg.norm(A_completed - A_true) / np.linalg.norm(A_true)
    print(f"Matrix completion: {obs_ratio*100:.0f}% observed, "
          f"relative error = {error:.4f}")

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(A_true, cmap='viridis')
    axes[0].set_title('True Matrix')
    axes[1].imshow(A_obs, cmap='viridis')
    axes[1].set_title(f'Observed ({obs_ratio*100:.0f}%)')
    axes[2].imshow(A_completed, cmap='viridis')
    axes[2].set_title('Completed')
    plt.tight_layout()
    plt.show()

    return A_true, A_completed, errors


def main():
    print("=" * 60)
    print("LOW-RANK APPROXIMATIONS - Eckart-Young")
    print("=" * 60)

    np.random.seed(42)

    print("\n--- Eckart-Young Verification ---")
    A = np.random.randn(8, 6)
    U, s, Vt = svd(A, full_matrices=False)
    r = np.linalg.matrix_rank(A)

    for k in [1, 2, 3, 4]:
        Ak = low_rank_approximation(A, k)
        frob_err = np.linalg.norm(A - Ak, 'fro')
        spec_err = np.linalg.norm(A - Ak, 2)
        expected_frob = np.sqrt(np.sum(s[k:] ** 2))
        expected_spec = s[k] if k < len(s) else 0
        print(f"k={k}: frob_err={frob_err:.6f} (expected={expected_frob:.6f}), "
              f"spec_err={spec_err:.6f} (expected={expected_spec:.6f})")
        print(f"  Match: frob={abs(frob_err - expected_frob) < 1e-10}, "
              f"spec={abs(spec_err - expected_spec) < 1e-10}")

    print("\n--- Error vs Rank ---")
    frob_errs, spec_errs, singular_vals = approximation_errors(A)
    ranks = range(1, len(frob_errs) + 1)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(ranks, frob_errs, 'bo-', label='Frobenius')
    axes[0].plot(ranks, spec_errs, 'rs-', label='Spectral')
    axes[0].set_xlabel('Rank k')
    axes[0].set_ylabel('||A - A_k||')
    axes[0].set_title('Approximation Error vs Rank')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].semilogy(range(1, len(singular_vals) + 1), singular_vals, 'g^-')
    axes[1].axvline(x=3, color='r', linestyle='--', alpha=0.5, label='k=3')
    axes[1].set_xlabel('Index')
    axes[1].set_ylabel('Singular Value')
    axes[1].set_title('Singular Value Spectrum')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    print("\n--- Image Compression Demo ---")
    image_compression_demo()

    print("\n--- Matrix Completion Demo ---")
    matrix_completion_demo(m=40, n=30, rank=5, obs_ratio=0.4)

    print("\n--- Low-Rank vs Approximation Quality ---")
    for true_rank in [2, 5, 10]:
        U = np.random.randn(50, true_rank)
        V = np.random.randn(true_rank, 30)
        A_rank = U @ V

        for approx_rank in [1, 2, 5, 10, 15]:
            Ak = low_rank_approximation(A_rank, approx_rank)
            err = np.linalg.norm(A_rank - Ak, 'fro') / np.linalg.norm(A_rank, 'fro')
            print(f"True rank {true_rank}, approx rank {approx_rank}: relative error = {err:.4f}")

    print("\n--- Storage Comparison ---")
    m, n = 100, 100
    for k in [1, 5, 10, 20, 50]:
        full_storage = m * n
        low_rank_storage = k * (m + n)
        ratio = low_rank_storage / full_storage
        print(f"k={k}: full={full_storage}, low-rank={low_rank_storage}, "
              f"compression ratio={ratio:.3f}")


if __name__ == "__main__":
    main()
