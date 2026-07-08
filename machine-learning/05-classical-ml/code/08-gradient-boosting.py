"""Gradient Boosting from scratch (regression + classification)."""
import numpy as np
from sklearn.datasets import make_regression, make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score

class RegressionTree:
    def __init__(self, max_depth=3, min_samples_split=2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.tree = None

    class Node:
        def __init__(self):
            self.feature = None; self.thresh = None
            self.left = None; self.right = None; self.value = None

    def fit(self, X, y):
        self.tree = self._grow(X, y, 0)

    def _grow(self, X, y, depth):
        node = self.Node()
        if len(y) < self.min_samples_split or (self.max_depth and depth >= self.max_depth):
            node.value = y.mean()
            return node
        best_feat, best_thresh, best_loss = None, None, float('inf')
        for f in range(X.shape[1]):
            thresholds = np.unique(X[:, f])
            for t in thresholds:
                idx = X[:, f] <= t
                if sum(idx) < 1 or sum(~idx) < 1: continue
                loss = np.var(y[idx])*sum(idx) + np.var(y[~idx])*sum(~idx)
                if loss < best_loss:
                    best_loss = loss; best_feat = f; best_thresh = t
        if best_feat is None:
            node.value = y.mean(); return node
        idx = X[:, best_feat] <= best_thresh
        node.feature = best_feat; node.thresh = best_thresh
        node.left = self._grow(X[idx], y[idx], depth+1)
        node.right = self._grow(X[~idx], y[~idx], depth+1)
        return node

    def predict(self, X):
        return np.array([self._predict(x, self.tree) for x in X])

    def _predict(self, x, node):
        if node.value is not None: return node.value
        if x[node.feature] <= node.thresh: return self._predict(x, node.left)
        return self._predict(x, node.right)

class GradientBoosting:
    def __init__(self, n_estimators=100, lr=0.1, max_depth=3, task='regression'):
        self.n_estimators = n_estimators
        self.lr = lr
        self.max_depth = max_depth
        self.task = task
        self.trees = []

    def fit(self, X, y):
        if self.task == 'classification':
            y = y.astype(float) * 2 - 1
        self.F0 = y.mean()
        F = np.full(len(y), self.F0)
        for _ in range(self.n_estimators):
            if self.task == 'classification':
                p = 1.0 / (1.0 + np.exp(-F))
                residuals = y - p
            else:
                residuals = y - F
            tree = RegressionTree(max_depth=self.max_depth)
            tree.fit(X, residuals)
            F += self.lr * tree.predict(X)
            self.trees.append(tree)

    def predict(self, X):
        F = np.full(X.shape[0], self.F0)
        for tree in self.trees:
            F += self.lr * tree.predict(X)
        if self.task == 'classification':
            return (F >= 0).astype(int)
        return F

if __name__ == "__main__":
    X, y = make_regression(n_samples=200, n_features=5, noise=0.1, random_state=42)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    gb = GradientBoosting(n_estimators=50, lr=0.1, task='regression')
    gb.fit(X_tr, y_tr)
    print(f"GBM Regression MSE: {mean_squared_error(y_te, gb.predict(X_te)):.4f}")

    Xc, yc = make_classification(n_samples=300, n_features=5, random_state=42)
    Xc_tr, Xc_te, yc_tr, yc_te = train_test_split(Xc, yc, test_size=0.2, random_state=42)
    gbc = GradientBoosting(n_estimators=50, lr=0.1, task='classification')
    gbc.fit(Xc_tr, yc_tr)
    print(f"GBM Classif Accuracy: {accuracy_score(yc_te, gbc.predict(Xc_te)):.4f}")
