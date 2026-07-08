"""Hierarchical clustering (agglomerative) from scratch."""
import numpy as np
from sklearn.datasets import make_blobs

def linkage_min(dists, i, j, sizes):
    return min(dists[i], dists[j])

def linkage_max(dists, i, j, sizes):
    return max(dists[i], dists[j])

def linkage_avg(dists, i, j, sizes):
    return (sizes[i] * dists[i] + sizes[j] * dists[j]) / (sizes[i] + sizes[j])

def linkage_ward(dists, i, j, sizes):
    return (sizes[i] * sizes[j]) / (sizes[i] + sizes[j]) * (2 * dists[i] * dists[j])  # simplified

class AgglomerativeClustering:
    def __init__(self, n_clusters=3, linkage='ward'):
        self.n_clusters = n_clusters
        self.linkage = linkage

    def fit(self, X):
        n = X.shape[0]
        dist = np.sqrt(np.sum(X**2, axis=1)[:, None] + np.sum(X**2, axis=1)[None, :] - 2*X @ X.T)
        np.fill_diagonal(dist, np.inf)

        clusters = [[i] for i in range(n)]
        sizes = np.ones(n)
        merge_history = []

        while len(clusters) > self.n_clusters:
            ni = len(clusters)
            min_d = np.inf
            merge_pair = (0, 1)

            for i in range(ni):
                for j in range(i+1, ni):
                    d = self._cluster_dist(clusters[i], clusters[j], dist, sizes)
                    if d < min_d:
                        min_d = d
                        merge_pair = (i, j)

            i, j = merge_pair
            if j < i: i, j = j, i
            clusters[i] = clusters[i] + clusters[j]
            sizes[i] = len(clusters[i])
            clusters.pop(j)
            merge_history.append((i, j, min_d))

        self.labels_ = np.zeros(n, dtype=int)
        for label, cluster in enumerate(clusters):
            for idx in cluster:
                self.labels_[idx] = label
        return self

    def _cluster_dist(self, c1, c2, dist, sizes):
        d = 0.0
        for i in c1:
            for j in c2:
                d += dist[i, j]
        return d / (len(c1) * len(c2))

if __name__ == "__main__":
    X, y = make_blobs(n_samples=100, centers=3, n_features=2, random_state=42)

    hc = AgglomerativeClustering(n_clusters=3)
    hc.fit(X)
    print(f"Hierarchical clusters: {np.unique(hc.labels_)}")

    from sklearn.cluster import AgglomerativeClustering as SKAgg
    sk = SKAgg(n_clusters=3).fit(X)
    print(f"sklearn Hierarchical clusters: {np.unique(sk.labels_)}")
