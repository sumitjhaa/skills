"""DBSCAN from scratch with comprehensive comparison."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_blobs, make_circles

class DBSCAN:
    def __init__(self, eps=0.5, min_pts=5):
        self.eps = eps
        self.min_pts = min_pts

    def fit(self, X):
        n = X.shape[0]
        self.labels_ = np.full(n, -1)
        visited = np.zeros(n, dtype=bool)
        cluster_id = 0

        dists = np.sqrt(np.sum(X**2, axis=1)[:, None] + np.sum(X**2, axis=1)[None, :] - 2 * X @ X.T)

        def region_query(i):
            return np.where(dists[i] <= self.eps)[0]

        def expand(i, neighbors):
            self.labels_[i] = cluster_id
            seed = list(neighbors)
            while seed:
                j = seed.pop()
                if not visited[j]:
                    visited[j] = True
                    nb = region_query(j)
                    if len(nb) >= self.min_pts:
                        seed.extend(nb)
                if self.labels_[j] == -1:
                    self.labels_[j] = cluster_id

        for i in range(n):
            if not visited[i]:
                visited[i] = True
                neighbors = region_query(i)
                if len(neighbors) < self.min_pts:
                    self.labels_[i] = -1
                else:
                    expand(i, neighbors)
                    cluster_id += 1

        self.n_clusters_ = cluster_id
        return self

    def fit_predict(self, X):
        self.fit(X)
        return self.labels_

def evaluate_dbscan(X, y_true, eps, min_pts, name):
    from sklearn.metrics import adjusted_rand_score
    db = DBSCAN(eps=eps, min_pts=min_pts)
    pred = db.fit_predict(X)
    n_clusters = len(set(pred)) - (1 if -1 in pred else 0)
    n_noise = list(pred).count(-1)
    ari = adjusted_rand_score(y_true, pred) if n_clusters > 1 else 0
    return pred, n_clusters, n_noise, ari

def test_edge_cases():
    print("=== Edge Cases ===")
    db = DBSCAN(eps=0.5, min_pts=5)

    # Single point
    X_single = np.array([[0.0, 0.0]])
    db.fit(X_single)
    print(f"  Single point: labels={db.labels_}, n_clusters={db.n_clusters_}")

    # Two far points
    X_far = np.array([[0.0, 0.0], [10.0, 10.0]])
    db.fit(X_far)
    print(f"  Two far points: labels={db.labels_}, n_clusters={db.n_clusters_}")

    # All same point
    X_same = np.ones((10, 2)) * 0.5
    db.fit(X_same)
    print(f"  All same point: labels={db.labels_}, n_clusters={db.n_clusters_}")

    # Test eps sensitivity
    X, y = make_moons(n_samples=200, noise=0.05, random_state=42)
    for eps in [0.1, 0.2, 0.3, 0.5, 1.0]:
        pred, nc, nn, ari = evaluate_dbscan(X, y, eps, 5, "moons")
        print(f"  eps={eps:.1f}: {nc} clusters, {nn} noise, ARI={ari:.4f}")

if __name__ == "__main__":
    test_edge_cases()

    datasets = {
        "Moons": make_moons(n_samples=300, noise=0.05, random_state=42),
        "Circles": make_circles(n_samples=300, noise=0.05, factor=0.5, random_state=42),
        "Blobs": make_blobs(n_samples=300, n_features=2, centers=2, random_state=42),
    }

    fig, axes = plt.subplots(3, 3, figsize=(14, 12))

    for row, (name, (X, y)) in enumerate(datasets.items()):
        # Our DBSCAN
        eps = 0.3 if name != "Blobs" else 0.5
        pred, nc, nn, ari = evaluate_dbscan(X, y, eps, 5, name)

        axes[row, 0].scatter(X[:, 0], X[:, 1], c=pred, cmap='tab10', s=20, alpha=0.7)
        axes[row, 0].set_title(f"DBSCAN (ours): {nc} clusters, {nn} noise")
        axes[row, 0].set_xticks([]); axes[row, 0].set_yticks([])

        # sklearn DBSCAN
        from sklearn.cluster import DBSCAN as SKDBSCAN
        sk = SKDBSCAN(eps=eps, min_samples=5).fit(X)
        sk_nc = len(set(sk.labels_)) - (1 if -1 in sk.labels_ else 0)
        sk_nn = list(sk.labels_).count(-1)
        axes[row, 1].scatter(X[:, 0], X[:, 1], c=sk.labels_, cmap='tab10', s=20, alpha=0.7)
        axes[row, 1].set_title(f"sklearn DBSCAN: {sk_nc} clusters, {sk_nn} noise")
        axes[row, 1].set_xticks([]); axes[row, 1].set_yticks([])

        # Ground truth
        axes[row, 2].scatter(X[:, 0], X[:, 1], c=y, cmap='tab10', s=20, alpha=0.7)
        axes[row, 2].set_title(f"Ground Truth ({name})")
        axes[row, 2].set_xticks([]); axes[row, 2].set_yticks([])

        print(f"\n{name}: ARI={ari:.4f}")

    plt.tight_layout()
    plt.savefig("../../assets/phase05/17-dbscan.png")
    plt.close()
    print("\nFigure saved to 17-dbscan.png")
