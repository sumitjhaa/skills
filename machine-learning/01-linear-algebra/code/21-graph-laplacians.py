import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from scipy.spatial.distance import pdist, squareform


def unnormalized_laplacian(A):
    """Unnormalized graph Laplacian L = D - A."""
    D = np.diag(A.sum(axis=1))
    return D - A


def symmetric_normalized_laplacian(A):
    """Symmetric normalized Laplacian L_sym = D^{-1/2} L D^{-1/2}."""
    d = A.sum(axis=1)
    D_inv_sqrt = np.diag(1.0 / np.sqrt(np.maximum(d, 1e-14)))
    L = np.diag(d) - A
    return D_inv_sqrt @ L @ D_inv_sqrt


def random_walk_laplacian(A):
    """Random walk Laplacian L_rw = D^{-1} L."""
    d = A.sum(axis=1)
    D_inv = np.diag(1.0 / np.maximum(d, 1e-14))
    L = np.diag(d) - A
    return D_inv @ L


def knn_graph(X, k=5):
    """Build k-NN adjacency matrix."""
    n = X.shape[0]
    dists = squareform(pdist(X))
    A = np.zeros((n, n))
    for i in range(n):
        idx = np.argsort(dists[i])[1:k+1]
        A[i, idx] = 1
        A[idx, i] = 1
    return A


def spectral_clustering(A, k, laplacian_type='symmetric'):
    """Spectral clustering using graph Laplacian."""
    if laplacian_type == 'symmetric':
        L = symmetric_normalized_laplacian(A)
    elif laplacian_type == 'random_walk':
        L = random_walk_laplacian(A)
    else:
        L = unnormalized_laplacian(A)

    eigvals, eigvecs = np.linalg.eigh(L)
    X = eigvecs[:, :k]
    return KMeans(n_clusters=k, n_init=10, random_state=42).fit(X).labels_, eigvals


def cheeger_constant(A, labels):
    """Compute Cheeger constant for a given partition."""
    n = A.shape[0]
    vol_S = labels.sum()
    vol_total = n
    cut = 0
    for i in range(n):
        for j in range(n):
            if labels[i] == 0 and labels[j] == 1 and A[i, j] > 0:
                cut += A[i, j]
    h = cut / min(vol_S, vol_total - vol_S)
    return h


def main():
    print("=" * 60)
    print("GRAPH LAPLACIANS AND SPECTRAL CLUSTERING")
    print("=" * 60)

    np.random.seed(42)

    print("\n--- Graph Laplacian Construction ---")
    A = np.array([[0, 1, 1, 0],
                  [1, 0, 1, 0],
                  [1, 1, 0, 0],
                  [0, 0, 0, 0]])

    L_unnorm = unnormalized_laplacian(A)
    L_sym = symmetric_normalized_laplacian(A)
    L_rw = random_walk_laplacian(A)

    print(f"Adjacency:\n{A}")
    print(f"Unnormalized Laplacian:\n{L_unnorm}")
    print(f"Symmetric normalized Laplacian:\n{np.round(L_sym, 4)}")

    print("\n--- Eigenvalue Analysis ---")
    for L, name in [(L_unnorm, "Unnormalized"), (L_sym, "Symmetric"), (L_rw, "Random Walk")]:
        eigvals = np.linalg.eigvalsh(L)
        print(f"{name}: eigenvalues = {np.round(eigvals, 4)}")
        print(f"  Zero eigenvalue count = {np.sum(np.abs(eigvals) < 1e-10)} "
              f"(connected components)")

    print("\n--- Spectral Clustering on Synthetic Data ---")
    X, y_true = make_blobs(n_samples=300, n_features=2, centers=3,
                           cluster_std=0.8, random_state=42)
    A_knn = knn_graph(X, k=10)
    labels_spec, eigvals_spec = spectral_clustering(A_knn, k=3)

    kmeans = KMeans(n_clusters=3, n_init=10, random_state=42)
    labels_kmeans = kmeans.fit_predict(X)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    axes[0].scatter(X[:, 0], X[:, 1], c=y_true, cmap='viridis', s=20)
    axes[0].set_title('True Clusters')
    axes[1].scatter(X[:, 0], X[:, 1], c=labels_spec, cmap='viridis', s=20)
    axes[1].set_title('Spectral Clustering')
    axes[2].scatter(X[:, 0], X[:, 1], c=labels_kmeans, cmap='viridis', s=20)
    axes[2].set_title('K-Means')
    plt.tight_layout()
    plt.show()

    print("\n--- Eigenvalues of Laplacian (Connected Components) ---")
    A_2comp = np.zeros((6, 6))
    A_2comp[:3, :3] = np.ones((3, 3)) - np.eye(3)
    A_2comp[3:, 3:] = np.ones((3, 3)) - np.eye(3)
    L_2comp = unnormalized_laplacian(A_2comp)
    eigvals_2 = np.linalg.eigvalsh(L_2comp)
    print(f"Two components: eigenvalues = {np.round(eigvals_2, 4)}")
    print(f"  Zero eigenvalue count = {np.sum(np.abs(eigvals_2) < 1e-10)}")

    print("\n--- Cheeger Inequality ---")
    A_line = np.zeros((10, 10))
    for i in range(9):
        A_line[i, i+1] = A_line[i+1, i] = 1

    L_line = unnormalized_laplacian(A_line)
    eigvals_line = np.linalg.eigvalsh(L_line)
    lambda_2 = eigvals_line[1]

    labels_left = np.zeros(10)
    labels_left[:5] = 1
    h = cheeger_constant(A_line, labels_left)

    print(f"Path graph (10 nodes):")
    print(f"  lambda_2 = {lambda_2:.4f}")
    print(f"  Cheeger constant h = {h:.4f}")
    print(f"  lambda_2 / 2 = {lambda_2/2:.4f} <= h = {h:.4f} <= sqrt(2*lambda_2) = {np.sqrt(2*lambda_2):.4f}")
    print(f"  Cheeger holds: {lambda_2/2 <= h <= np.sqrt(2*lambda_2) + 1e-10}")

    print("\n--- Eigenvalue Visualization ---")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].plot(range(1, len(eigvals_spec) + 1), np.sort(eigvals_spec), 'b-o')
    axes[0].axvline(x=4, color='r', linestyle='--', label=f'k=3 cut')
    axes[0].set_xlabel('Index')
    axes[0].set_ylabel('Eigenvalue')
    axes[0].set_title('Laplacian Eigenvalues (Spectral Clustering)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    eigvals_unnorm = np.linalg.eigvalsh(L_unnorm)
    axes[1].bar(range(len(eigvals_unnorm)), np.sort(eigvals_unnorm))
    axes[1].set_xlabel('Index')
    axes[1].set_ylabel('Eigenvalue')
    axes[1].set_title('Unnormalized Laplacian Eigenvalues')
    axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
