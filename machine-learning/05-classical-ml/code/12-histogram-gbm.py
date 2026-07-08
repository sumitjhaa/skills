"""Histogram-based Gradient Boosting with bin splitting."""
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

class HistGBM:
    def __init__(self, n_estimators=50, lr=0.1, max_bins=64, max_depth=3):
        self.n_estimators = n_estimators
        self.lr = lr
        self.max_bins = max_bins
        self.max_depth = max_depth
        self.trees = []

    def _bin(self, X):
        n, d = X.shape
        Xb = np.zeros_like(X, dtype=np.int32)
        edges = []
        for f in range(d):
            uniq = np.unique(X[:, f])
            if len(uniq) <= self.max_bins:
                e = uniq
            else:
                e = np.percentile(X[:, f], np.linspace(0, 100, self.max_bins+2)[1:-1])
            edges.append(e)
            Xb[:, f] = np.digitize(X[:, f], e, right=True)
        return Xb, edges

    def fit(self, X, y):
        Xb, self.edges_ = self._bin(X)
        self.base = y.mean()
        pred = np.full(len(y), self.base)
        for _ in range(self.n_estimators):
            r = y - pred
            tree = HistTree(max_depth=self.max_depth, lr=self.lr)
            tree.fit(Xb, r)
            pred += tree.predict(Xb)
            self.trees.append(tree)
        self.Xb_ = Xb

    def predict(self, X):
        Xb, _ = self._bin(X)
        pred = np.full(X.shape[0], self.base)
        for t in self.trees:
            pred += t.predict(Xb)
        return pred

class HistTree:
    def __init__(self, max_depth=3, lr=0.1):
        self.max_depth = max_depth; self.lr = lr; self.tree = None

    class Node:
        def __init__(self):
            self.feat = None; self.bin = None; self.left = None; self.right = None; self.val = None

    def fit(self, X, residuals):
        self.tree = self._grow(X, residuals, 0)

    def _grow(self, X, r, depth):
        node = self.Node()
        if depth >= self.max_depth or len(r) < 5:
            node.val = r.mean() * self.lr; return node
        best_f, best_b, best_l = None, None, float('inf')
        for f in range(X.shape[1]):
            for b in range(X[:, f].max() + 1):
                idx = X[:, f] <= b
                if sum(idx) < 2 or sum(~idx) < 2: continue
                loss = np.var(r[idx])*sum(idx) + np.var(r[~idx])*sum(~idx)
                if loss < best_l:
                    best_l = loss; best_f = f; best_b = b
        if best_f is None:
            node.val = r.mean() * self.lr; return node
        idx = X[:, best_f] <= best_b
        node.feat, node.bin = best_f, best_b
        node.left = self._grow(X[idx], r[idx], depth+1)
        node.right = self._grow(X[~idx], r[~idx], depth+1)
        return node

    def predict(self, X):
        return np.array([self._pred(x, self.tree) for x in X])

    def _pred(self, x, node):
        if node.val is not None: return node.val
        if x[node.feat] <= node.bin: return self._pred(x, node.left)
        return self._pred(x, node.right)

if __name__ == "__main__":
    X, y = make_regression(n_samples=300, n_features=5, noise=0.1, random_state=42)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    hgb = HistGBM(n_estimators=50, lr=0.1, max_bins=32, max_depth=3)
    hgb.fit(X_tr, y_tr)
    print(f"HistGBM MSE: {mean_squared_error(y_te, hgb.predict(X_te)):.4f}")
