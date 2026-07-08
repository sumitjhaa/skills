"""k-NN (brute force, KD-tree, Ball tree) from scratch."""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from collections import Counter

class BruteKNN:
    def __init__(self, k=5):
        self.k = k
    def fit(self, X, y):
        self.X = X; self.y = y
    def predict(self, X):
        preds = []
        for x in X:
            dists = np.sum((self.X - x)**2, axis=1)
            idx = np.argsort(dists)[:self.k]
            preds.append(Counter(self.y[idx]).most_common(1)[0][0])
        return np.array(preds)

class KDTree:
    def __init__(self, k=5):
        self.k = k
    class Node:
        def __init__(self, point, label, left=None, right=None, axis=0):
            self.point = point; self.label = label
            self.left = left; self.right = right; self.axis = axis

    def fit(self, X, y):
        self.data = np.column_stack([X, y])
        self.tree = self._build(self.data)

    def _build(self, data, depth=0):
        if len(data) == 0: return None
        axis = depth % (data.shape[1] - 1)
        idx = np.argsort(data[:, axis])
        data = data[idx]
        mid = len(data) // 2
        return self.Node(data[mid, :-1], int(data[mid, -1]),
                         self._build(data[:mid], depth+1),
                         self._build(data[mid+1:], depth+1), axis)

    def predict(self, X):
        return np.array([self._predict_one(x) for x in X])

    def _predict_one(self, x):
        best = []
        self._search(self.tree, x, best)
        labels = [l for _, l in best]
        return Counter(labels).most_common(1)[0][0]

    def _search(self, node, x, best, depth=0):
        if node is None: return
        dist = np.sum((node.point - x)**2)
        if len(best) < self.k:
            best.append((dist, node.label))
            best.sort(key=lambda p: p[0])
        elif dist < best[-1][0]:
            best[-1] = (dist, node.label)
            best.sort(key=lambda p: p[0])
        axis = node.axis
        diff = x[axis] - node.point[axis]
        if diff <= 0:
            self._search(node.left, x, best, depth+1)
            if len(best) < self.k or diff**2 < best[-1][0]:
                self._search(node.right, x, best, depth+1)
        else:
            self._search(node.right, x, best, depth+1)
            if len(best) < self.k or diff**2 < best[-1][0]:
                self._search(node.left, x, best, depth+1)

class BallTreeKNN:
    def __init__(self, k=5, leaf_size=20):
        self.k = k; self.leaf_size = leaf_size
    class Node:
        def __init__(self, points, labels, left=None, right=None, center=None, radius=0):
            self.points = points; self.labels = labels
            self.left = left; self.right = right
            self.center = center; self.radius = radius
            self.is_leaf = left is None

    def fit(self, X, y):
        self.data = np.column_stack([X, y])
        self.tree = self._build(self.data)

    def _build(self, data):
        if len(data) <= self.leaf_size:
            return self.Node(data[:, :-1], data[:, -1].astype(int), center=data[:, :-1].mean(axis=0))
        center = data[:, :-1].mean(axis=0)
        radius = np.max(np.sqrt(np.sum((data[:, :-1] - center)**2, axis=1)))
        idx = np.argsort(np.sum((data[:, :-1] - center)**2, axis=1))
        mid = len(data) // 2
        return self.Node(data[idx[:mid], :-1], data[idx[:mid], -1].astype(int),
                         self._build(data[idx[:mid]]),
                         self._build(data[idx[mid:]]),
                         center, radius)

    def predict(self, X):
        return np.array([self._predict_one(x) for x in X])

    def _predict_one(self, x):
        best = []
        self._search(self.tree, x, best)
        labels = [l for _, l in best]
        return Counter(labels).most_common(1)[0][0]

    def _search(self, node, x, best):
        if node is None: return
        if node.is_leaf:
            for p, l in zip(node.points, node.labels):
                d = np.sum((p - x)**2)
                if len(best) < self.k:
                    best.append((d, l)); best.sort(key=lambda p: p[0])
                elif d < best[-1][0]:
                    best[-1] = (d, l); best.sort(key=lambda p: p[0])
            return
        d_center = np.sqrt(np.sum((node.center - x)**2))
        if len(best) >= self.k and d_center - node.radius >= np.sqrt(best[-1][0]):
            return
        self._search(node.left, x, best)
        self._search(node.right, x, best)

if __name__ == "__main__":
    X, y = make_classification(n_samples=300, n_features=10, random_state=42)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

    brute = BruteKNN(k=5)
    brute.fit(X_tr, y_tr)
    print(f"Brute k-NN: {accuracy_score(y_te, brute.predict(X_te)):.4f}")

    kd = KDTree(k=5)
    kd.fit(X_tr, y_tr)
    print(f"KD-Tree k-NN: {accuracy_score(y_te, kd.predict(X_te)):.4f}")

    bt = BallTreeKNN(k=5, leaf_size=20)
    bt.fit(X_tr, y_tr)
    print(f"Ball Tree k-NN: {accuracy_score(y_te, bt.predict(X_te)):.4f}")

    from sklearn.neighbors import KNeighborsClassifier
    print(f"sklearn k-NN: {accuracy_score(y_te, KNeighborsClassifier(5).fit(X_tr, y_tr).predict(X_te)):.4f}")
