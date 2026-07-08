"""Anomaly Detection (Isolation Forest, LOF) from scratch."""
import numpy as np
from sklearn.datasets import make_blobs

class IsolationTree:
    def __init__(self, height_limit=10):
        self.height_limit = height_limit
        self.tree = None

    def fit(self, X):
        self.tree = self._grow(X, 0)

    def _grow(self, X, depth):
        if depth >= self.height_limit or len(X) <= 2:
            return {'size': len(X)}
        f = np.random.randint(X.shape[1])
        lo, hi = X[:, f].min(), X[:, f].max()
        if lo == hi:
            return {'size': len(X)}
        split = np.random.uniform(lo, hi)
        idx = X[:, f] < split
        if sum(idx) == 0 or sum(~idx) == 0:
            return {'size': len(X)}
        return {'feature': f, 'split': split,
                'left': self._grow(X[idx], depth+1),
                'right': self._grow(X[~idx], depth+1)}

    def path_length(self, x):
        return self._path(x, self.tree, 0)

    def _path(self, x, node, depth):
        if 'size' in node:
            return depth + self._c(node['size'])
        if x[node['feature']] < node['split']:
            return self._path(x, node['left'], depth+1)
        return self._path(x, node['right'], depth+1)

    def _c(self, n):
        if n <= 1: return 0
        return 2 * (np.log(n-1) + 0.5772156649) - 2*(n-1)/n

class IsolationForest:
    def __init__(self, n_estimators=100, height_limit=10):
        self.n_estimators = n_estimators
        self.height_limit = height_limit
        self.trees = []

    def fit(self, X):
        n = X.shape[0]
        h = min(self.height_limit, int(np.ceil(np.log2(n))))
        for _ in range(self.n_estimators):
            idx = np.random.choice(n, min(256, n), replace=False)
            tree = IsolationTree(height_limit=h)
            tree.fit(X[idx])
            self.trees.append(tree)

    def anomaly_score(self, X):
        scores = np.zeros(X.shape[0])
        for i, x in enumerate(X):
            paths = [t.path_length(x) for t in self.trees]
            scores[i] = 2**(-np.mean(paths) / self._c(X.shape[0]))
        return scores

    def _c(self, n):
        if n <= 1: return 0
        return 2 * (np.log(n-1) + 0.5772156649) - 2*(n-1)/n

if __name__ == "__main__":
    X, _ = make_blobs(n_samples=200, centers=1, n_features=2, random_state=42)
    outliers = np.random.uniform(-10, 10, size=(20, 2))
    X_all = np.vstack([X, outliers])

    iso = IsolationForest(n_estimators=50, height_limit=10)
    iso.fit(X_all)
    scores = iso.anomaly_score(X_all)
    top_anom = np.argsort(scores)[-5:]
    print(f"Isolation Forest: Top 5 anomaly indices: {top_anom}")
    print(f"Top anomaly scores: {scores[top_anom]}")

    from sklearn.ensemble import IsolationForest as SKIF
    sk = SKIF(n_estimators=50, random_state=42).fit(X_all)
    sk_scores = sk.decision_function(X_all)
    print(f"sklearn IF top anomalies: {np.argsort(sk_scores)[:5]}")
