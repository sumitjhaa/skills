"""Semi-Supervised Learning (self-training, label propagation) from scratch."""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score

class LogisticRegression:
    def __init__(self):
        self.w = None
    def fit(self, X, y):
        n, d = X.shape; X = np.c_[np.ones(n), X]; self.w = np.zeros(d+1)
        for _ in range(200):
            p = 1/(1+np.exp(-X @ self.w)); grad = X.T @ (p-y)/n; self.w -= 0.1*grad
    def predict_proba(self, X):
        X = np.c_[np.ones(X.shape[0]), X]; p = 1/(1+np.exp(-X @ self.w))
        return np.c_[1-p, p]
    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)

def self_training(X_labeled, y_labeled, X_unlabeled, n_rounds=10, threshold=0.9):
    model = LogisticRegression()
    X_l, y_l = X_labeled.copy(), y_labeled.copy()
    X_u = X_unlabeled.copy()

    for _ in range(n_rounds):
        model.fit(X_l, y_l)
        probs = model.predict_proba(X_u)
        conf = np.max(probs, axis=1)
        best = np.argmax(conf)
        if conf[best] < threshold: break
        X_l = np.vstack([X_l, X_u[best]])
        y_l = np.append(y_l, model.predict(X_u[best].reshape(1, -1)))
        X_u = np.delete(X_u, best, axis=0)
        if len(X_u) == 0: break

    model.fit(X_l, y_l)
    return model

def label_propagation(X, y_labeled, alpha=0.8, max_iter=100):
    n = X.shape[0]
    dist = np.sum(X**2, axis=1)[:, None] + np.sum(X**2, axis=1)[None, :] - 2 * X @ X.T
    sigma = np.median(dist)
    W = np.exp(-dist / (2 * sigma**2))
    np.fill_diagonal(W, 0)
    D = np.diag(W.sum(axis=1))
    D_inv = np.linalg.inv(D + 1e-10)
    S = D_inv @ W

    Y = np.zeros((n, 2))
    Y[y_labeled >= 0, :] = 0
    for i, lbl in enumerate(y_labeled):
        if lbl >= 0:
            Y[i, int(lbl)] = 1

    for _ in range(max_iter):
        Y_new = alpha * S @ Y + (1-alpha) * Y
        Y = Y_new.copy()
        for i, lbl in enumerate(y_labeled):
            if lbl >= 0:
                Y[i] = 0; Y[i, int(lbl)] = 1

    return np.argmax(Y, axis=1)

if __name__ == "__main__":
    X, y = make_classification(n_samples=300, n_features=10, random_state=42)

    labeled = np.random.choice(300, 20, replace=False)
    unlabeled = [i for i in range(300) if i not in labeled]
    y_labeled = np.full(300, -1)
    y_labeled[labeled] = y[labeled]

    model = self_training(X[labeled], y[labeled], X[unlabeled])
    print(f"Self-training accuracy: {accuracy_score(y, model.predict(X)):.4f}")

    pseudo_labels = label_propagation(X, y_labeled)
    print(f"Label propagation accuracy: {accuracy_score(y, pseudo_labels):.4f}")

    model2 = LogisticRegression()
    model2.fit(X[labeled], y[labeled])
    print(f"Supervised baseline (20 labels): {accuracy_score(y, model2.predict(X)):.4f}")
