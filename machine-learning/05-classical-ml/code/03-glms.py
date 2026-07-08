"""Generalized Linear Models (GLMs) from scratch via IRLS."""
import numpy as np
from sklearn.datasets import make_regression, make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score

class GLM:
    def __init__(self, family='gaussian', max_iter=100, tol=1e-6):
        self.family = family
        self.max_iter = max_iter
        self.tol = tol

    def _link(self, mu):
        if self.family == 'gaussian':
            return mu
        elif self.family == 'binomial':
            mu = np.clip(mu, 1e-10, 1 - 1e-10)
            return np.log(mu / (1 - mu))
        elif self.family == 'poisson':
            return np.log(np.maximum(mu, 1e-10))

    def _link_inv(self, eta):
        if self.family == 'gaussian':
            return eta
        elif self.family == 'binomial':
            eta = np.clip(eta, -500, 500)
            return 1.0 / (1.0 + np.exp(-eta))
        elif self.family == 'poisson':
            return np.exp(np.clip(eta, -500, 500))

    def _variance(self, mu):
        if self.family == 'gaussian':
            return np.ones_like(mu)
        elif self.family == 'binomial':
            mu = np.clip(mu, 1e-10, 1 - 1e-10)
            return mu * (1 - mu)
        elif self.family == 'poisson':
            return np.maximum(mu, 1e-10)

    def fit(self, X, y):
        n, d = X.shape
        X = np.c_[np.ones(n), X]
        beta = np.zeros(d + 1)
        mu = self._link_inv(X @ beta)
        for i in range(self.max_iter):
            eta = self._link(mu)
            V = self._variance(mu)
            g_prime = 1.0 / np.maximum(np.abs(self._link_inv(eta) - self._link_inv(eta * 0.999)), 1e-10)
            W = np.diag(1.0 / (V * g_prime**2 + 1e-10))
            z = eta + (y - mu) * g_prime
            beta_new = np.linalg.solve(X.T @ W @ X, X.T @ W @ z)
            if np.linalg.norm(beta_new - beta) < self.tol:
                print(f"IRLS converged in {i+1} iterations")
                break
            beta = beta_new
            mu = self._link_inv(X @ beta)
        self.intercept_ = beta[0]
        self.coef_ = beta[1:]

    def predict(self, X):
        X = np.c_[np.ones(X.shape[0]), X]
        return self._link_inv(X @ np.r_[self.intercept_, self.coef_])

if __name__ == "__main__":
    X, y = make_regression(n_samples=200, n_features=5, noise=0.5, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    glm_g = GLM(family='gaussian')
    glm_g.fit(X_train, y_train)
    print(f"Gaussian GLM MSE: {mean_squared_error(y_test, glm_g.predict(X_test)):.4f}")

    Xb, yb = make_classification(n_samples=500, n_features=10, random_state=42)
    Xb_tr, Xb_te, yb_tr, yb_te = train_test_split(Xb, yb, test_size=0.2, random_state=42)
    glm_b = GLM(family='binomial')
    glm_b.fit(Xb_tr, yb_tr)
    preds = (glm_b.predict(Xb_te) >= 0.5).astype(int)
    print(f"Binomial GLM Accuracy: {accuracy_score(yb_te, preds):.4f}")
