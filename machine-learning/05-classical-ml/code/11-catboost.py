"""CatBoost-style ordered boosting with categorical encoding."""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class OrderedTargetEncoder:
    def fit(self, X_cat, y):
        self.maps_ = {}
        for col in range(X_cat.shape[1]):
            prior = y.mean()
            self.maps_[col] = {}
            perm = np.random.permutation(len(y))
            X_perm = X_cat[perm, col]
            y_perm = y[perm]
            sums = {}
            counts = {}
            for i, val in enumerate(X_perm):
                if val not in sums:
                    self.maps_[col][val] = prior
                    sums[val] = 0.0
                    counts[val] = 0
                self.maps_[col][val] = (sums[val] + prior * 10) / (counts[val] + 10)
                sums[val] += y_perm[i]
                counts[val] += 1

    def transform(self, X_cat):
        out = np.zeros_like(X_cat, dtype=float)
        for col in range(X_cat.shape[1]):
            for i, val in enumerate(X_cat[i, col]):
                out[i, col] = self.maps_.get(col, {}).get(val, 0.5)
        return out

class CatBoostTree:
    def __init__(self, max_depth=3, lr=0.1):
        self.max_depth = max_depth
        self.lr = lr
    class Node:
        def __init__(self):
            self.feature = None; self.thresh = None; self.left = None; self.right = None; self.pred = None
    def fit(self, X, residuals):
        self.tree = self._grow(X, residuals, 0)
    def _grow(self, X, r, depth):
        node = self.Node()
        if depth >= self.max_depth or len(r) < 5:
            node.pred = r.mean() * self.lr
            return node
        best = None; best_loss = float('inf')
        for f in range(X.shape[1]):
            threshs = np.unique(X[:, f])
            for t in threshs:
                idx = X[:, f] <= t
                if sum(idx) < 2 or sum(~idx) < 2: continue
                loss = np.var(r[idx])*sum(idx) + np.var(r[~idx])*sum(~idx)
                if loss < best_loss:
                    best_loss = loss; best = (f, t)
        if best is None:
            node.pred = r.mean() * self.lr; return node
        idx = X[:, best[0]] <= best[1]
        node.feature, node.thresh = best
        node.left = self._grow(X[idx], r[idx], depth+1)
        node.right = self._grow(X[~idx], r[~idx], depth+1)
        return node
    def predict(self, X):
        return np.array([self._pred(x, self.tree) for x in X])
    def _pred(self, x, node):
        if node.pred is not None: return node.pred
        if x[node.feature] <= node.thresh: return self._pred(x, node.left)
        return self._pred(x, node.right)

class CatBoost:
    def __init__(self, n_estimators=50, lr=0.1, max_depth=3):
        self.n_estimators = n_estimators
        self.lr = lr
        self.max_depth = max_depth
        self.trees = []
    def fit(self, X, y):
        self.base = y.mean()
        pred = np.full(len(y), self.base)
        for _ in range(self.n_estimators):
            r = y - pred
            t = CatBoostTree(max_depth=self.max_depth, lr=self.lr)
            t.fit(X, r)
            pred += t.predict(X)
            self.trees.append(t)
    def predict(self, X):
        pred = np.full(X.shape[0], self.base)
        for t in self.trees:
            pred += t.predict(X)
        return (pred >= 0.5).astype(int)

if __name__ == "__main__":
    X, y = make_classification(n_samples=300, n_features=5, random_state=42)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    cb = CatBoost(n_estimators=30, lr=0.1, max_depth=3)
    cb.fit(X_tr, y_tr)
    print(f"CatBoost Accuracy: {accuracy_score(y_te, cb.predict(X_te)):.4f}")
