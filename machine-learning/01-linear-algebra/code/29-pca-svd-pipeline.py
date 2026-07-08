import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_olivetti_faces


def compute_eigenfaces(face_images, k=50):
    """Compute eigenfaces via PCA/SVD."""
    n_samples, n_pixels = face_images.shape
    mean_face = face_images.mean(axis=0)
    centered = face_images - mean_face

    U, s, Vt = np.linalg.svd(centered, full_matrices=False)

    eigenfaces = Vt[:k]
    singular_vals = s[:k]
    explained_var = s[:k]**2 / (s**2).sum()

    return mean_face, eigenfaces, singular_vals, explained_var


def project_face(face, mean_face, eigenfaces):
    """Project face onto eigenface basis."""
    return eigenfaces @ (face - mean_face)


def reconstruct_face(coeffs, mean_face, eigenfaces):
    """Reconstruct face from eigenface coefficients."""
    return mean_face + eigenfaces.T @ coeffs


def compress_image(img, k):
    """Compress image using truncated SVD."""
    U, s, Vt = np.linalg.svd(img, full_matrices=False)
    return U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :], s


def denoise_image(img_noisy, threshold):
    """Denoise image via singular value thresholding."""
    U, s, Vt = np.linalg.svd(img_noisy, full_matrices=False)
    s_denoised = np.maximum(s - threshold, 0)
    return U @ np.diag(s_denoised) @ Vt


def main():
    print("=" * 60)
    print("PCA/SVD PIPELINE - Eigenfaces, Compression, Denoising")
    print("=" * 60)

    np.random.seed(42)

    print("\n--- Loading Olivetti Faces Dataset ---")
    try:
        dataset = fetch_olivetti_faces(shuffle=True, random_state=42)
        faces = dataset.data
        faces_images = dataset.images
        target = dataset.target
        n_samples, h, w = faces_images.shape
        print(f"Loaded {n_samples} faces of size {h}x{w}")
    except:
        print("Could not load Olivetti faces. Using synthetic data.")
        n_samples, h, w = 100, 32, 32
        faces = np.random.randn(n_samples, h * w)
        faces_images = faces.reshape(n_samples, h, w)
        target = np.random.randint(0, 10, n_samples)

    print("\n--- Eigenface Computation ---")
    k = 25
    mean_face, eigenfaces, s, var_explained = compute_eigenfaces(faces, k=k)
    print(f"Computed {k} eigenfaces")
    print(f"First 5 eigenvalues: {np.round(s[:5], 2)}")
    print(f"Variance explained by top {k}: {var_explained.sum() * 100:.2f}%")

    print("\n--- Eigenface Visualization ---")
    fig, axes = plt.subplots(3, 6, figsize=(15, 8))
    axes[0, 0].imshow(mean_face.reshape(h, w), cmap='gray')
    axes[0, 0].set_title('Mean Face')
    axes[0, 0].axis('off')

    for i in range(1, 6):
        axes[0, i].imshow(eigenfaces[i-1].reshape(h, w), cmap='gray')
        axes[0, i].set_title(f'Eigenface {i}')
        axes[0, i].axis('off')

    for i in range(6):
        axes[1, i].imshow(eigenfaces[i+5].reshape(h, w), cmap='gray')
        axes[1, i].set_title(f'Eigenface {i+6}')
        axes[1, i].axis('off')

    for i in range(6):
        axes[2, i].imshow(eigenfaces[i+11].reshape(h, w), cmap='gray')
        axes[2, i].set_title(f'Eigenface {i+12}')
        axes[2, i].axis('off')

    plt.suptitle('Top Eigenfaces')
    plt.tight_layout()
    plt.show()

    print("\n--- Face Reconstruction at Different Compression Levels ---")
    test_face = faces_images[0]
    test_face_flat = faces[0]

    fig, axes = plt.subplots(2, 5, figsize=(15, 6))

    axes[0, 0].imshow(test_face, cmap='gray')
    axes[0, 0].set_title('Original')
    axes[0, 0].axis('off')

    for idx, k_rec in enumerate([1, 5, 10, 25]):
        coeffs = project_face(test_face_flat, mean_face, eigenfaces[:k_rec])
        recon = reconstruct_face(coeffs[:k_rec], mean_face, eigenfaces[:k_rec])
        axes[0, idx + 1].imshow(recon.reshape(h, w), cmap='gray')
        err = np.linalg.norm(test_face_flat - recon) / np.linalg.norm(test_face_flat)
        axes[0, idx + 1].set_title(f'k={k_rec}, err={err:.3f}')
        axes[0, idx + 1].axis('off')

    axes[1, 0].imshow(test_face, cmap='gray')
    axes[1, 0].set_title('Original')
    axes[1, 0].axis('off')

    for idx, k_rec in enumerate([50, 75, 100, 200]):
        if k_rec <= len(eigenfaces):
            coeffs = project_face(test_face_flat, mean_face, eigenfaces[:k_rec])
            recon = reconstruct_face(coeffs[:k_rec], mean_face, eigenfaces[:k_rec])
            axes[1, idx + 1].imshow(recon.reshape(h, w), cmap='gray')
            err = np.linalg.norm(test_face_flat - recon) / np.linalg.norm(test_face_flat)
            axes[1, idx + 1].set_title(f'k={k_rec}, err={err:.3f}')
            axes[1, idx + 1].axis('off')

    plt.suptitle('Face Reconstruction with Varying Number of Eigenfaces')
    plt.tight_layout()
    plt.show()

    print("\n--- SVD Image Compression (Synthetic Image) ---")
    synthetic_img = np.random.randn(64, 64)
    U_s, s_s, Vt_s = np.linalg.svd(synthetic_img, full_matrices=False)

    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes[0, 0].imshow(synthetic_img, cmap='gray')
    axes[0, 0].set_title('Original')
    axes[0, 0].axis('off')

    for idx, k_comp in enumerate([2, 5, 10, 20]):
        img_comp, _ = compress_image(synthetic_img, k_comp)
        axes[0, idx + 1].imshow(img_comp, cmap='gray')
        err = np.linalg.norm(synthetic_img - img_comp, 'fro') / np.linalg.norm(synthetic_img, 'fro')
        axes[0, idx + 1].set_title(f'k={k_comp}, err={err:.3f}')
        axes[0, idx + 1].axis('off')

    for idx, k_comp in enumerate([30, 40, 50, 60]):
        if k_comp <= 64:
            img_comp, _ = compress_image(synthetic_img, k_comp)
            axes[1, idx].imshow(img_comp, cmap='gray')
            err = np.linalg.norm(synthetic_img - img_comp, 'fro') / np.linalg.norm(synthetic_img, 'fro')
            axes[1, idx].set_title(f'k={k_comp}, err={err:.3f}')
            axes[1, idx].axis('off')

    plt.suptitle('SVD Image Compression')
    plt.tight_layout()
    plt.show()

    print("\n--- Denoising via SVT ---")
    true_low_rank = np.random.randn(40, 10) @ np.random.randn(10, 40)
    noise = np.random.randn(40, 40) * 0.3
    noisy = true_low_rank + noise

    for threshold in [0.1, 0.3, 0.5, 1.0]:
        denoised = denoise_image(noisy, threshold)
        orig_err = np.linalg.norm(true_low_rank - noisy, 'fro')
        denoised_err = np.linalg.norm(true_low_rank - denoised, 'fro')
        improvement = (orig_err - denoised_err) / orig_err * 100
        print(f"  Threshold {threshold}: error={denoised_err:.4f}, "
              f"improvement={improvement:.1f}%")

    print("\n--- Variance Explained ---")
    cumulative_var = np.cumsum(var_explained) * 100
    n_components_90 = np.searchsorted(cumulative_var, 90) + 1
    n_components_95 = np.searchsorted(cumulative_var, 95) + 1
    print(f"Components for 90% variance: {n_components_90}")
    print(f"Components for 95% variance: {n_components_95}")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(range(1, len(cumulative_var) + 1), cumulative_var, 'b-')
    ax.axhline(y=90, color='r', linestyle='--', alpha=0.5)
    ax.axhline(y=95, color='g', linestyle='--', alpha=0.5)
    ax.set_xlabel('Number of components')
    ax.set_ylabel('Cumulative variance explained (%)')
    ax.set_title('Variance Explained by Eigenfaces')
    ax.grid(True, alpha=0.3)
    plt.show()

    print("\n--- Recognition with Eigenfaces ---")
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.model_selection import train_test_split

    X_proj = faces @ eigenfaces[:k].T
    X_train, X_test, y_train, y_test = train_test_split(
        X_proj, target, test_size=0.3, random_state=42)

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)
    accuracy = knn.score(X_test, y_test)
    print(f"Recognition accuracy (k={k} eigenfaces): {accuracy * 100:.1f}%")


if __name__ == "__main__":
    main()
