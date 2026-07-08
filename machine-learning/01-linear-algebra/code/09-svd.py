import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import svd as scipy_svd
from scipy.linalg import sqrtm
import time


def truncated_svd(A, k):
    """Truncated SVD keeping top k components."""
    U, s, Vt = scipy_svd(A, full_matrices=False)
    return U[:, :k], s[:k], Vt[:k, :]


def randomized_svd(A, k, n_oversamples=10, n_iter=2):
    """Randomized SVD (Halko–Martinsson–Tropp)."""
    m, n = A.shape
    p = min(k + n_oversamples, n)

    Omega = np.random.randn(n, p)
    Y = A @ Omega

    for _ in range(n_iter):
        Y = A @ (A.T @ Y)

    Q, _ = np.linalg.qr(Y)

    B = Q.T @ A
    Ub, s, Vt = scipy_svd(B, full_matrices=False)

    U = Q @ Ub[:, :k]
    return U, s[:k], Vt[:k, :]


def pca_svd(X, k):
    """PCA via SVD."""
    mean = X.mean(axis=0)
    X_centered = X - mean

    U, s, Vt = scipy_svd(X_centered, full_matrices=False)

    components = Vt[:k]
    scores = X_centered @ components.T

    var_explained = (s[:k] ** 2) / (s ** 2).sum()

    return scores, components, var_explained, mean, s


def compress_image(A, k):
    """Compress matrix using truncated SVD."""
    U, s, Vt = truncated_svd(A, k)
    return U @ np.diag(s) @ Vt, s


def denoise_svt(A, threshold):
    """Denoise via singular value thresholding."""
    U, s, Vt = scipy_svd(A, full_matrices=False)
    s_denoised = np.maximum(s - threshold, 0)
    return U @ np.diag(s_denoised) @ Vt, s, s_denoised


def compare_svd_algorithms():
    """Compare performance of full vs randomized SVD."""
    sizes = [100, 200, 500, 1000]
    k = 20
    results = {'full': [], 'randomized': []}

    for n in sizes:
        A = np.random.randn(n, n)

        t0 = time.perf_counter()
        U1, s1, Vt1 = scipy_svd(A, full_matrices=False)
        t_full = time.perf_counter() - t0
        results['full'].append(t_full)

        t0 = time.perf_counter()
        U2, s2, Vt2 = randomized_svd(A, k)
        t_rand = time.perf_counter() - t0
        results['randomized'].append(t_rand)

        print(f"n={n}: full={t_full:.4f}s, randomized(k={k})={t_rand:.4f}s")

    return sizes, results


def main():
    print("=" * 60)
    print("SINGULAR VALUE DECOMPOSITION")
    print("=" * 60)

    np.random.seed(42)

    print("\n--- Basic SVD ---")
    A = np.random.randn(6, 4)
    U, s, Vt = scipy_svd(A)
    print(f"A shape: {A.shape}")
    print(f"U shape: {U.shape}")
    print(f"Singular values: {np.round(s, 4)}")
    print(f"Vt shape: {Vt.shape}")
    A_reconstructed = U @ np.diag(s) @ Vt
    print(f"U SV^T == A: {np.allclose(A_reconstructed, A)}")

    print("\n--- Truncated SVD ---")
    k = 2
    Uk, sk, Vtk = truncated_svd(A, k)
    A_truncated = Uk @ np.diag(sk) @ Vtk
    print(f"Truncated to k={k}")
    print(f"Frobenius error: {np.linalg.norm(A - A_truncated, 'fro'):.4f}")
    print(f"Relative error: {np.linalg.norm(A - A_truncated, 'fro') / np.linalg.norm(A, 'fro'):.4f}")

    print("\n--- Randomized SVD ---")
    np.random.seed(123)
    A_large = np.random.randn(200, 100)
    k = 10
    U_rand, s_rand, Vt_rand = randomized_svd(A_large, k)
    U_full, s_full, Vt_full = truncated_svd(A_large, k)
    print(f"Singular values (randomized): {np.round(s_rand[:5], 4)}")
    print(f"Singular values (full):       {np.round(s_full[:5], 4)}")
    print(f"Singular value error: {np.linalg.norm(s_rand - s_full):.2e}")

    print("\n--- PCA via SVD ---")
    n_samples, n_features = 100, 5
    X = np.random.randn(n_samples, n_features) @ np.diag([5, 3, 1, 0.5, 0.1])
    scores, components, var_explained, mean, s = pca_svd(X, k=2)
    print(f"Variance explained: {np.round(var_explained * 100, 2)}%")
    print(f"Total variance explained: {var_explained.sum() * 100:.2f}%")
    print(f"Components:\n{np.round(components, 4)}")

    X_reconstructed = scores @ components + mean
    print(f"Reconstruction error: {np.linalg.norm(X - X_reconstructed):.4f}")

    print("\n--- Image Compression (Synthetic) ---")
    img = np.random.randn(50, 50)
    compression_rates = [1, 2, 5, 10, 20, 30]
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title(f'Original (rank={np.linalg.matrix_rank(img)})')

    for idx, k in enumerate(compression_rates[:3]):
        img_comp, s_img = compress_image(img, k)
        axes[0, idx + 1].imshow(img_comp, cmap='gray')
        err = np.linalg.norm(img - img_comp, 'fro') / np.linalg.norm(img, 'fro')
        axes[0, idx + 1].set_title(f'k={k}, err={err:.3f}')

    # Second row: more compression rates
    for idx, k in enumerate(compression_rates[3:7]):
        if idx < 4:
            img_comp, s_img = compress_image(img, k)
            axes[1, idx].imshow(img_comp, cmap='gray')
            err = np.linalg.norm(img - img_comp, 'fro') / np.linalg.norm(img, 'fro')
            axes[1, idx].set_title(f'k={k}, err={err:.3f}')

    axes[1, 3].axis('off')
    plt.suptitle('SVD Image Compression')
    plt.tight_layout()
    plt.show()

    print("\n--- Denoising via SVT ---")
    true_rank = 5
    U_true, _, Vt_true = np.linalg.svd(np.random.randn(30, 30))
    X_true = U_true[:, :true_rank] @ np.diag([10, 8, 6, 4, 2]) @ Vt_true[:true_rank, :]
    noise = np.random.randn(30, 30) * 0.5
    X_noisy = X_true + noise

    threshold = np.std(noise) * np.sqrt(2 * 30)
    X_denoised, s_orig, s_den = denoise_svt(X_noisy, threshold)

    print(f"True rank: {true_rank}")
    print(f"Original singular values: {np.round(s_orig[:10], 2)}")
    print(f"Denoised singular values: {np.round(s_den[:10], 2)}")
    print(f"Denoising error: {np.linalg.norm(X_true - X_denoised, 'fro'):.4f}")
    print(f"Noisy error: {np.linalg.norm(X_true - X_noisy, 'fro'):.4f}")
    print(f"Improvement: {(np.linalg.norm(X_true - X_noisy) / np.linalg.norm(X_true - X_denoised) - 1) * 100:.1f}%")

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(X_true, cmap='gray')
    axes[0].set_title('True (low-rank)')
    axes[1].imshow(X_noisy, cmap='gray')
    axes[1].set_title('Noisy')
    axes[2].imshow(X_denoised, cmap='gray')
    axes[2].set_title('Denoised (SVT)')
    plt.tight_layout()
    plt.show()

    print("\n--- Algorithm Comparison ---")
    compare_svd_algorithms()

    print("\n--- Rank-Revealing Properties ---")
    rank_5 = np.random.randn(30, 5) @ np.random.randn(5, 30)
    U, s, Vt = scipy_svd(rank_5, full_matrices=False)
    print(f"Singular values of rank-5 matrix: {np.round(s, 4)}")
    print(f"Effective numerical rank: {np.sum(s > 1e-10)}")


if __name__ == "__main__":
    main()
