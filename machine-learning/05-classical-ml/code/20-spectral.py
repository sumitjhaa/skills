"""Spectral clustering from scratch with in-house KMeans."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_circles, make_moons, make_blobs

class KMeans:
    def __init__(self, k=2, max_iter=100):
        self.k = k
        self.max_iter = max_iter

    def fit(self, X):
        n = X.shape[0]
        idx = np.random.choice(n, self.k, replace=False)
        self.centroids = X[idx].copy()

        for _ in range(self.max_iter):
            dists = np.zeros((n, self.k))
            for j in range(self.k):
                dists[:, j] = np.sum((X - self.centroids[j])**2, axis=1)
            self.labels_ = np.argmin(dists, axis=1)
            new_centroids = np.array([X[self.labels_ == j].mean(axis=0) for j in range(self.k)])
            if np.allclose(new_centroids, self.centroids):
                break
            self.centroids = new_centroids
        return self

class SpectralClustering:
    def __init__(self, n_clusters=2, gamma=1.0):
        self.n_clusters = n_clusters
        self.gamma = gamma

    def _rbf_affinity(self, X):
        sq_dists = np.sum(X**2, axis=1)[:, None] + np.sum(X**2, axis=1)[None, :] - 2 * X @ X.T
        return np.exp(-self.gamma * sq_dists)

    def fit(self, X):
        n = X.shape[0]
        W = self._rbf_affinity(X)

        D = np.diag(W.sum(axis=1))
        D_inv_sqrt = np.diag(1.0 / np.sqrt(np.diag(D) + 1e-10))
        L_sym = np.eye(n) - D_inv_sqrt @ W @ D_inv_sqrt

        eigvals, eigvecs = np.linalg.eigh(L_sym)
        U = eigvecs[:, :self.n_clusters]
        norms = np.sqrt(np.sum(U**2, axis=1, keepdims=True)) + 1e-10
        U = U / norms

        km = KMeans(k=self.n_clusters)
        km.fit(U)
        self.labels_ = km.labels_
        return self

    def fit_predict(self, X):
        self.fit(X)
        return self.labels_

def evaluate_spectral(X, n_clusters, gamma, name):
    sc = SpectralClustering(n_clusters=n_clusters, gamma=gamma)
    return sc.fit_predict(X)

if __name__ == "__main__":
    np.random.seed(42)

    datasets = {
        "Concentric Circles": make_circles(n_samples=200, noise=0.05, factor=0.5, random_state=42),
        "Moons": make_moons(n_samples=200, noise=0.05, random_state=42),
        "Blobs (3)": make_blobs(n_samples=200, n_features=2, centers=3, random_state=42),
    }

    fig, axes = plt.subplots(3, 4, figsize=(16, 12))

    for row, (name, (X, y)) in enumerate(datasets.items()):
        n_clusters = len(np.unique(y))
        gamma = 1.0 if "Circles" in name else (0.5 if "Moons" in name else 0.1)

        pred = evaluate_spectral(X, n_clusters, gamma, name)
        axes[row, 0].scatter(X[:, 0], X[:, 1], c=pred, cmap='tab10', s=20, alpha=0.7)
        axes[row, 0].set_title(f"Spectral (ours) - {name}")
        axes[row, 0].set_xticks([]); axes[row, 0].set_yticks([])

        from sklearn.cluster import SpectralClustering as SKSpectral
        sk = SKSpectral(n_clusters=n_clusters, gamma=gamma, random_state=42)
        sk_pred = sk.fit_predict(X)
        axes[row, 1].scatter(X[:, 0], X[:, 1], c=sk_pred, cmap='tab10', s=20, alpha=0.7)
        axes[row, 1].set_title(f"Spectral (sklearn) - {name}")
        axes[row, 1].set_xticks([]); axes[row, 1].set_yticks([])

        km = KMeans(k=n_clusters)
        km_pred = km.fit(X).labels_
        axes[row, 2].scatter(X[:, 0], X[:, 1], c=km_pred, cmap='tab10', s=20, alpha=0.7)
        axes[row, 2].set_title(f"KMeans (ours) - {name}")
        axes[row, 2].set_xticks([]); axes[row, 2].set_yticks([])

        axes[row, 3].scatter(X[:, 0], X[:, 1], c=y, cmap='tab10', s=20, alpha=0.7)
        axes[row, 3].set_title(f"Ground Truth - {name}")
        axes[row, 3].set_xticks([]); axes[row, 3].set_yticks([])

    plt.tight_layout()
    plt.savefig("../../assets/phase05/20-spectral.png")
    plt.close()
    print("Figure saved to 20-spectral.png")

    print("=== Edge Cases ===")
    sc = SpectralClustering(n_clusters=2, gamma=1.0)

    X_two = np.array([[0.0, 0.0], [2.0, 2.0]])
    sc.fit(X_two)
    print(f"  Two points: labels={sc.labels_}")

    X, y = make_circles(n_samples=200, noise=0.05, factor=0.5, random_state=42)
    print("  Gamma sensitivity on circles:")
    for g in [0.1, 0.5, 1.0, 5.0]:
        pred = evaluate_spectral(X, 2, g, "circles")
        from sklearn.metrics import adjusted_rand_score
        ari = adjusted_rand_score(y, pred)
        n1, n2 = np.bincount(pred) if len(np.unique(pred)) == 2 else (0, 0)
        print(f"    gamma={g:.1f}: ARI={ari:.4f}, cluster sizes=[{n1},{n2}]")

    print("\n=== Comparison of ARI scores ===")
    from sklearn.metrics import adjusted_rand_score
    for name, (X, y) in datasets.items():
        n_clusters = len(np.unique(y))
        gamma = 1.0 if "Circles" in name else (0.5 if "Moons" in name else 0.1)
        pred = evaluate_spectral(X, n_clusters, gamma, name)
        ari = adjusted_rand_score(y, pred)
        from sklearn.cluster import SpectralClustering as SKSpectral
        sk = SKSpectral(n_clusters=n_clusters, gamma=gamma, random_state=42)
        sk_pred = sk.fit_predict(X)
        sk_ari = adjusted_rand_score(y, sk_pred)
        print(f"  {name}: ours ARI={ari:.4f}, sklearn ARI={sk_ari:.4f}")
