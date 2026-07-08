"""Active Learning (uncertainty sampling, query-by-committee) from scratch."""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score

class LogisticRegression:
    def __init__(self):
        self.w = None
    def fit(self, X, y):
        n, d = X.shape
        X = np.c_[np.ones(n), X]
        self.w = np.zeros(d+1)
        lr = 0.1
        for _ in range(200):
            p = 1 / (1 + np.exp(-X @ self.w))
            grad = X.T @ (p - y) / n
            self.w -= lr * grad
    def predict_proba(self, X):
        X = np.c_[np.ones(X.shape[0]), X]
        p = 1 / (1 + np.exp(-X @ self.w))
        return np.c_[1-p, p]
    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)

def uncertainty_sampling(model, X_pool):
    probs = model.predict_proba(X_pool)
    uncertainty = 1 - np.max(probs, axis=1)
    return np.argmax(uncertainty)

def margin_sampling(model, X_pool):
    probs = model.predict_proba(X_pool)
    sorted_probs = np.sort(probs, axis=1)
    margins = sorted_probs[:, -1] - sorted_probs[:, -2]
    return np.argmin(margins)

def entropy_sampling(model, X_pool):
    probs = model.predict_proba(X_pool)
    entropy = -np.sum(probs * np.log(probs + 1e-15), axis=1)
    return np.argmax(entropy)

if __name__ == "__main__":
    X, y = make_classification(n_samples=500, n_features=10, random_state=42)

    labeled_idx = np.random.choice(500, 10, replace=False)
    unlabeled_idx = np.array([i for i in range(500) if i not in labeled_idx])

    strategies = {
        'Uncertainty': uncertainty_sampling,
        'Margin': margin_sampling,
        'Entropy': entropy_sampling
    }

    for name, strategy in strategies.items():
        lab = labeled_idx.copy()
        unl = unlabeled_idx.copy()
        model = LogisticRegression()
        model.fit(X[lab], y[lab])

        accs = [accuracy_score(y, model.predict(X))]
        for _ in range(20):
            pick = strategy(model, X[unl])
            lab = np.append(lab, unl[pick])
            unl = np.delete(unl, pick)
            model.fit(X[lab], y[lab])
            accs.append(accuracy_score(y, model.predict(X)))

        print(f"{name} sampling: final accuracy {accs[-1]:.4f} (started {accs[0]:.4f})")
