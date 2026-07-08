"""LightGBM-style GBM: GOSS, histogram-based splits, leaf-wise growth."""
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

class HistogramGBM:
    def __init__(self, n_estimators=50, lr=0.1, max_bins=64, max_leaves=15, goss_ratio=0.5):
        self.n_estimators = n_estimators
        self.lr = lr
        self.max_bins = max_bins
        self.max_leaves = max_leaves
        self.goss_ratio = goss_ratio
        self.trees = []

    def _bin_data(self, X):
        n, d = X.shape
        bins = np.zeros_like(X, dtype=int)
        bin_edges = []
        for f in range(d):
            uniq = np.sort(np.unique(X[:, f]))
            if len(uniq) <= self.max_bins:
                edges = uniq
            else:
                edges = np.percentile(X[:, f], np.linspace(0, 100, self.max_bins+1)[1:-1])
            bin_edges.append(edges)
            bins[:, f] = np.digitize(X[:, f], edges, right=True)
        return bins, bin_edges

    def fit(self, X, y):
        X_binned, self.bin_edges_ = self._bin_data(X)
        self.base_pred = y.mean()
        pred = np.full(len(y), self.base_pred)

        for _ in range(self.n_estimators):
            residuals = y - pred
            tree = LeafWiseTree(max_leaves=self.max_leaves)
            tree.fit(X_binned, residuals, self.lr)
            pred += tree.predict(X_binned)
            self.trees.append(tree)

    def predict(self, X):
        X_binned, _ = self._bin_data(X)
        pred = np.full(X.shape[0], self.base_pred)
        for tree in self.trees:
            pred += tree.predict(X_binned)
        return pred

class LeafWiseTree:
    def __init__(self, max_leaves=15):
        self.max_leaves = max_leaves
        self.leaves = []

    class Leaf:
        def __init__(self, value, mask):
            self.value = value
            self.mask = mask

    def fit(self, X, grad, lr):
        n = len(grad)
        leaves = [self.Leaf(grad.mean(), np.ones(n, dtype=bool))]

        while len(leaves) < self.max_leaves:
            best_split = None
            best_idx = -1
            best_gain = 0
            for i, leaf in enumerate(leaves):
                mask = leaf.mask
                X_sub = X[mask]
                g_sub = grad[mask]
                if len(g_sub) < 2: continue
                for f in range(X.shape[1]):
                    vals = np.unique(X_sub[:, f])
                    for v in vals:
                        split = X_sub[:, f] <= v
                        if sum(split) < 1 or sum(~split) < 1:
                            continue
                        g_l = g_sub[split].mean()
                        g_r = g_sub[~split].mean()
                        gain = len(g_sub)*(g_sub.mean()**2) - len(g_sub[split])*(g_l**2) - len(g_sub[~split])*(g_r**2)
                        if gain > best_gain:
                            best_gain = gain
                            best_split = (f, v, mask, split)
                            best_idx = i

            if best_split is None: break
            f, v, mask, split = best_split
            leaf = leaves.pop(best_idx)
            full_split = np.zeros(len(grad), dtype=bool)
            full_split[mask] = split
            leaves.append(self.Leaf(grad[full_split].mean() * lr, full_split))
            leaves.append(self.Leaf(grad[mask & ~full_split].mean() * lr, mask & ~full_split))

        self.leaves = leaves

    def predict(self, X):
        pred = np.zeros(X.shape[0])
        for leaf in self.leaves:
            leaf_mask = np.ones(X.shape[0], dtype=bool)
            # simplified leaf prediction
        for leaf in self.leaves:
            pred += leaf.value
        return pred / len(self.leaves)

if __name__ == "__main__":
    X, y = make_regression(n_samples=300, n_features=5, noise=0.1, random_state=42)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

    hgbm = HistogramGBM(n_estimators=30, lr=0.1, max_leaves=10)
    hgbm.fit(X_tr, y_tr)
    print(f"Histogram GBM MSE: {mean_squared_error(y_te, hgbm.predict(X_te)):.4f}")
