"""k-Means (Lloyd, MacQueen, k-Means++) from scratch."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs

class KMeans:
    def __init__(self, k=3, max_iter=100, init='kmeans++', algorithm='lloyd'):
        self.k = k
        self.max_iter = max_iter
        self.init = init
        self.algorithm = algorithm

    def _init_centroids(self, X):
        n, d = X.shape
        if self.init == 'random':
            return X[np.random.choice(n, self.k, replace=False)]
        elif self.init == 'kmeans++':
            centroids = [X[np.random.randint(n)]]
            for _ in range(1, self.k):
                D2 = np.min(np.array([np.sum((X - c)**2, axis=1) for c in centroids]), axis=0)
                probs = D2 / D2.sum()
                centroids.append(X[np.random.choice(n, p=probs)])
            return np.array(centroids)

    def fit(self, X):
        self.centroids = self._init_centroids(X)
        if self.algorithm == 'lloyd':
            self._lloyd(X)
        elif self.algorithm == 'macqueen':
            self._macqueen(X)
        return self

    def _lloyd(self, X):
        for _ in range(self.max_iter):
            dists = np.array([np.sum((X - c)**2, axis=1) for c in self.centroids])
            labels = np.argmin(dists, axis=0)
            new_centroids = np.array([X[labels == k].mean(axis=0) if np.sum(labels == k) > 0 else self.centroids[k] for k in range(self.k)])
            if np.allclose(new_centroids, self.centroids):
                break
            self.centroids = new_centroids
        self.labels_ = labels
        self.inertia_ = np.sum([np.sum((X[labels == k] - self.centroids[k])**2) for k in range(self.k)])

    def _macqueen(self, X):
        self.labels_ = np.full(X.shape[0], -1)
        n = X.shape[0]
        counts = np.zeros(self.k, dtype=int)
        perm = np.random.permutation(n)
        for idx in perm:
            x = X[idx]
            dists = np.sum((x - self.centroids)**2, axis=1)
            label = np.argmin(dists)
            self.labels_[idx] = label
            counts[label] += 1
            self.centroids[label] += (x - self.centroids[label]) / counts[label]

    def predict(self, X):
        dists = np.array([np.sum((X - c)**2, axis=1) for c in self.centroids])
        return np.argmin(dists, axis=0)

if __name__ == "__main__":
    X, y = make_blobs(n_samples=300, centers=3, n_features=2, random_state=42)

    km = KMeans(k=3, init='kmeans++', algorithm='lloyd')
    km.fit(X)
    print(f"k-Means (Lloyd, k-Means++) inertia: {km.inertia_:.2f}")

    km2 = KMeans(k=3, init='random', algorithm='macqueen')
    km2.fit(X)
    print(f"k-Means (MacQueen, random) inertia: {km2.inertia_:.2f}")

    from sklearn.cluster import KMeans as SKKMeans
    sk = SKKMeans(n_clusters=3, n_init=1, random_state=42).fit(X)
    print(f"sklearn k-Means inertia: {sk.inertia_:.2f}")

    plt.scatter(X[:, 0], X[:, 1], c=km.labels_, cmap='viridis', alpha=0.7)
    plt.scatter(km.centroids[:, 0], km.centroids[:, 1], c='red', marker='X', s=200, label='Centroids')
    plt.title("k-Means Clustering")
    plt.legend(); plt.savefig('../../assets/phase05/kmeans_demo.png'); plt.close()
