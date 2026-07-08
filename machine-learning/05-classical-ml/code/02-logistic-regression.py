"""Logistic Regression from scratch with Newton-Raphson and IRLS."""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, log_loss

def sigmoid(z):
    z = np.clip(z, -500, 500)
    return 1.0 / (1.0 + np.exp(-z))

class LogisticRegression:
    def __init__(self, lr=0.01, max_iter=1000, tol=1e-6, method='newton'):
        self.lr = lr
        self.max_iter = max_iter
        self.tol = tol
        self.method = method

    def fit(self, X, y):
        n, d = X.shape
        X = np.c_[np.ones(n), X]
        self.w = np.zeros(d + 1)
        y = y.astype(float)

        if self.method == 'newton':
            for i in range(self.max_iter):
                p = sigmoid(X @ self.w)
                grad = X.T @ (p - y)
                W = np.diag(p * (1 - p) + 1e-10)
                H = X.T @ W @ X
                try:
                    self.w -= np.linalg.solve(H, grad)
                except np.linalg.LinAlgError:
                    self.w -= self.lr * grad
                if np.linalg.norm(grad) < self.tol:
                    print(f"Newton converged in {i+1} iterations")
                    break
        else:
            for i in range(self.max_iter):
                p = sigmoid(X @ self.w)
                grad = X.T @ (p - y)
                self.w -= self.lr * grad
                if np.linalg.norm(grad) < self.tol:
                    break
        self.intercept_ = self.w[0]
        self.coef_ = self.w[1:]

    def predict_proba(self, X):
        X = np.c_[np.ones(X.shape[0]), X]
        p = sigmoid(X @ self.w)
        return np.c_[1 - p, p]

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)

if __name__ == "__main__":
    X, y = make_classification(n_samples=500, n_features=20, n_informative=10,
                                n_clusters_per_class=1, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    lr = LogisticRegression(method='newton')
    lr.fit(X_train, y_train)
    print(f"Accuracy: {accuracy_score(y_test, lr.predict(X_test)):.4f}")
    print(f"Log-loss: {log_loss(y_test, lr.predict_proba(X_test)[:, 1]):.4f}")

    from sklearn.linear_model import LogisticRegression as SKLR
    sk = SKLR(max_iter=1000).fit(X_train, y_train)
    print(f"\nsklearn Accuracy: {accuracy_score(y_test, sk.predict(X_test)):.4f}")
