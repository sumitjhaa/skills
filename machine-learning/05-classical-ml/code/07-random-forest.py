"""Random Forest from scratch (bagging + random subspace)."""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from collections import Counter

class DecisionTree:
    def __init__(self, max_depth=None, min_samples_split=2, max_features=None):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.max_features = max_features
        self.tree = None

    def fit(self, X, y):
        self.n_features = X.shape[1]
        if self.max_features is None:
            self.max_features = int(np.sqrt(self.n_features))
        self.tree = self._grow(X, y, depth=0)

    class Node:
        def __init__(self):
            self.feature = None; self.thresh = None
            self.left = None; self.right = None; self.value = None

    def _gini(self, y):
        if len(y) == 0: return 0
        p = np.bincount(y.astype(int)) / len(y)
        return 1 - np.sum(p**2)

    def _best_split(self, X, y, features):
        best = None
        best_gain = -1
        for f in features:
            thresholds = np.unique(X[:, f])
            for t in thresholds:
                left = y[X[:, f] <= t]
                right = y[X[:, f] > t]
                if len(left) < 1 or len(right) < 1: continue
                g = self._gini(y) - (len(left)*self._gini(left)+len(right)*self._gini(right))/len(y)
                if g > best_gain:
                    best_gain = g
                    best = (f, t)
        return best

    def _grow(self, X, y, depth):
        node = self.Node()
        if len(set(y)) == 1 or len(y) < self.min_samples_split or (self.max_depth and depth >= self.max_depth):
            node.value = Counter(y).most_common(1)[0][0]
            return node
        n_feats = min(self.max_features, X.shape[1])
        feat_idx = np.random.choice(X.shape[1], n_feats, replace=False)
        split = self._best_split(X, y, feat_idx)
        if split is None:
            node.value = Counter(y).most_common(1)[0][0]
            return node
        node.feature, node.thresh = split
        idx = X[:, node.feature] <= node.thresh
        node.left = self._grow(X[idx], y[idx], depth+1)
        node.right = self._grow(X[~idx], y[~idx], depth+1)
        return node

    def predict(self, X):
        return np.array([self._predict(x, self.tree) for x in X])

    def _predict(self, x, node):
        if node.value is not None: return node.value
        if x[node.feature] <= node.thresh:
            return self._predict(x, node.left)
        return self._predict(x, node.right)

class RandomForest:
    def __init__(self, n_estimators=100, max_depth=None, max_features=None):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.max_features = max_features
        self.trees = []

    def fit(self, X, y):
        n = X.shape[0]
        for _ in range(self.n_estimators):
            idx = np.random.choice(n, n, replace=True)
            tree = DecisionTree(max_depth=self.max_depth, max_features=self.max_features)
            tree.fit(X[idx], y[idx])
            self.trees.append(tree)

    def predict(self, X):
        preds = np.array([t.predict(X) for t in self.trees])
        out = []
        for i in range(X.shape[0]):
            out.append(Counter(preds[:, i]).most_common(1)[0][0])
        return np.array(out)

if __name__ == "__main__":
    X, y = make_classification(n_samples=300, n_features=10, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf = RandomForest(n_estimators=20, max_depth=5)
    rf.fit(X_train, y_train)
    print(f"RF Accuracy: {accuracy_score(y_test, rf.predict(X_test)):.4f}")

    from sklearn.ensemble import RandomForestClassifier
    sk = RandomForestClassifier(n_estimators=20, max_depth=5, random_state=42).fit(X_train, y_train)
    print(f"sklearn RF: {accuracy_score(y_test, sk.predict(X_test)):.4f}")
