"""XGBoost-style gradient boosting (Newton boosting, regularization)."""
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

class XGBoostTree:
    def __init__(self, max_depth=3, reg_lambda=1.0, gamma=0.0):
        self.max_depth = max_depth
        self.reg_lambda = reg_lambda
        self.gamma = gamma
        self.tree = None

    class Node:
        def __init__(self):
            self.feature = None; self.threshold = None
            self.left = None; self.right = None; self.weight = None

    def fit(self, X, g, h):
        self.tree = self._grow(X, g, h, 0)

    def _grow(self, X, g, h, depth):
        node = self.Node()
        if depth >= self.max_depth:
            node.weight = -g.sum() / (h.sum() + self.reg_lambda)
            return node
        best_gain = 0; best_feat = None; best_thresh = None
        G = g.sum(); H = h.sum()
        for f in range(X.shape[1]):
            idx = np.argsort(X[:, f])
            G_l, H_l = 0.0, 0.0
            for i in range(len(idx)):
                x_i = idx[i]
                G_l += g[x_i]; H_l += h[x_i]
                if i < len(idx) - 1 and X[idx[i], f] == X[idx[i+1], f]:
                    continue
                G_r = G - G_l; H_r = H - H_l
                gain = 0.5 * (G_l**2/(H_l+self.reg_lambda) + G_r**2/(H_r+self.reg_lambda) - G**2/(H+self.reg_lambda)) - self.gamma
                if gain > best_gain:
                    best_gain = gain; best_feat = f; best_thresh = X[x_i, f]
        if best_gain <= 0:
            node.weight = -G / (H + self.reg_lambda)
            return node
        idx = X[:, best_feat] <= best_thresh
        node.feature = best_feat; node.threshold = best_thresh
        node.left = self._grow(X[idx], g[idx], h[idx], depth+1)
        node.right = self._grow(X[~idx], g[~idx], h[~idx], depth+1)
        return node

    def predict(self, X):
        return np.array([self._predict(x, self.tree) for x in X])

    def _predict(self, x, node):
        if node.weight is not None: return node.weight
        if x[node.feature] <= node.threshold: return self._predict(x, node.left)
        return self._predict(x, node.right)

class XGBoostRegressor:
    def __init__(self, n_estimators=50, lr=0.3, max_depth=3, reg_lambda=1.0, gamma=0.0):
        self.n_estimators = n_estimators
        self.lr = lr
        self.max_depth = max_depth
        self.reg_lambda = reg_lambda
        self.gamma = gamma
        self.trees = []
        self.base_pred = None

    def fit(self, X, y):
        self.base_pred = y.mean()
        pred = np.full(len(y), self.base_pred)
        for _ in range(self.n_estimators):
            g = pred - y
            h = np.ones_like(y)
            tree = XGBoostTree(max_depth=self.max_depth, reg_lambda=self.reg_lambda, gamma=self.gamma)
            tree.fit(X, g, h)
            pred += self.lr * tree.predict(X)
            self.trees.append(tree)

    def predict(self, X):
        pred = np.full(X.shape[0], self.base_pred)
        for tree in self.trees:
            pred += self.lr * tree.predict(X)
        return pred

if __name__ == "__main__":
    X, y = make_regression(n_samples=300, n_features=5, noise=0.1, random_state=42)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

    xgb = XGBoostRegressor(n_estimators=50, lr=0.3, max_depth=3)
    xgb.fit(X_tr, y_tr)
    print(f"XGBoost MSE: {mean_squared_error(y_te, xgb.predict(X_te)):.4f}")
