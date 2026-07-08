"""Decision Trees (CART for classification/regression) from scratch."""
import numpy as np
from sklearn.datasets import make_classification, make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error

class Node:
    def __init__(self):
        self.feature = None
        self.threshold = None
        self.left = None
        self.right = None
        self.value = None

class DecisionTree:
    def __init__(self, max_depth=None, min_samples_split=2, task='classification'):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.task = task
        self.root = None

    def fit(self, X, y):
        self.n_classes_ = len(np.unique(y)) if self.task == 'classification' else None
        self.root = self._grow(X, y, depth=0)

    def _grow(self, X, y, depth):
        node = Node()
        if len(y) < self.min_samples_split or (self.max_depth and depth >= self.max_depth):
            node.value = self._leaf_value(y)
            return node

        best_feat, best_thresh = self._best_split(X, y)
        if best_feat is None:
            node.value = self._leaf_value(y)
            return node

        left_idx = X[:, best_feat] <= best_thresh
        right_idx = ~left_idx
        if np.sum(left_idx) == 0 or np.sum(right_idx) == 0:
            node.value = self._leaf_value(y)
            return node

        node.feature = best_feat
        node.threshold = best_thresh
        node.left = self._grow(X[left_idx], y[left_idx], depth + 1)
        node.right = self._grow(X[right_idx], y[right_idx], depth + 1)
        return node

    def _best_split(self, X, y):
        best_gain = -1
        best_feat, best_thresh = None, None
        n, d = X.shape
        for f in range(d):
            thresholds = np.unique(X[:, f])
            for t in thresholds:
                left = y[X[:, f] <= t]
                right = y[X[:, f] > t]
                if len(left) < 1 or len(right) < 1:
                    continue
                gain = self._impurity(y) - (len(left)*self._impurity(left) + len(right)*self._impurity(right)) / len(y)
                if gain > best_gain:
                    best_gain = gain
                    best_feat = f
                    best_thresh = t
        return best_feat, best_thresh

    def _impurity(self, y):
        if self.task == 'classification':
            p = np.bincount(y.astype(int)) / len(y)
            return 1 - np.sum(p**2)
        else:
            return np.var(y)

    def _leaf_value(self, y):
        if self.task == 'classification':
            return np.bincount(y.astype(int)).argmax()
        else:
            return y.mean()

    def predict(self, X):
        return np.array([self._traverse(x, self.root) for x in X])

    def _traverse(self, x, node):
        if node.value is not None:
            return node.value
        if x[node.feature] <= node.threshold:
            return self._traverse(x, node.left)
        return self._traverse(x, node.right)

if __name__ == "__main__":
    X, y = make_classification(n_samples=200, n_features=5, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    dt = DecisionTree(max_depth=5)
    dt.fit(X_train, y_train)
    print(f"Decision Tree (classif) Accuracy: {accuracy_score(y_test, dt.predict(X_test)):.4f}")

    Xr, yr = make_regression(n_samples=200, n_features=5, noise=0.1, random_state=42)
    Xr_tr, Xr_te, yr_tr, yr_te = train_test_split(Xr, yr, test_size=0.2, random_state=42)
    dtr = DecisionTree(max_depth=5, task='regression')
    dtr.fit(Xr_tr, yr_tr)
    print(f"Decision Tree (regr) MSE: {mean_squared_error(yr_te, dtr.predict(Xr_te)):.4f}")

    from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
    print(f"sklearn classif: {accuracy_score(y_test, DecisionTreeClassifier(max_depth=5).fit(X_train, y_train).predict(X_test)):.4f}")
