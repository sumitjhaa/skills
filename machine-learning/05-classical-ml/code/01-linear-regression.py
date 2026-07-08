"""Linear Regression: OLS, Ridge, Lasso, ElasticNet from scratch."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

class OLS:
    def __init__(self, fit_intercept=True):
        self.fit_intercept = fit_intercept
    def fit(self, X, y):
        if self.fit_intercept:
            X = np.c_[np.ones(X.shape[0]), X]
        self.coef_ = np.linalg.lstsq(X, y, rcond=None)[0]
        if self.fit_intercept:
            self.intercept_ = self.coef_[0]
            self.coef_ = self.coef_[1:]
    def predict(self, X):
        if self.fit_intercept:
            return X @ self.coef_ + self.intercept_
        return X @ self.coef_

class Ridge:
    def __init__(self, alpha=1.0, fit_intercept=True):
        self.alpha = alpha
        self.fit_intercept = fit_intercept
    def fit(self, X, y):
        if self.fit_intercept:
            X = np.c_[np.ones(X.shape[0]), X]
        n_features = X.shape[1]
        I = np.eye(n_features)
        if self.fit_intercept:
            I[0, 0] = 0
        self.coef_ = np.linalg.solve(X.T @ X + self.alpha * I, X.T @ y)
        if self.fit_intercept:
            self.intercept_ = self.coef_[0]
            self.coef_ = self.coef_[1:]
    def predict(self, X):
        if self.fit_intercept:
            return X @ self.coef_ + self.intercept_
        return X @ self.coef_

class Lasso:
    def __init__(self, alpha=1.0, max_iter=1000, tol=1e-4):
        self.alpha = alpha
        self.max_iter = max_iter
        self.tol = tol
    def _soft_threshold(self, x, gamma):
        return np.sign(x) * np.maximum(np.abs(x) - gamma, 0)
    def fit(self, X, y):
        n, d = X.shape
        X_mean = X.mean(axis=0)
        y_mean = y.mean()
        Xc = X - X_mean
        yc = y - y_mean
        beta = np.zeros(d)
        for _ in range(self.max_iter):
            beta_old = beta.copy()
            for j in range(d):
                r = yc - Xc @ beta + Xc[:, j] * beta[j]
                rho = Xc[:, j] @ r
                z = Xc[:, j] @ Xc[:, j]
                beta[j] = self._soft_threshold(rho, self.alpha) / max(z, 1e-12)
            if np.max(np.abs(beta - beta_old)) < self.tol:
                break
        self.coef_ = beta
        self.intercept_ = y_mean - X_mean @ beta
    def predict(self, X):
        return X @ self.coef_ + self.intercept_

class ElasticNet:
    def __init__(self, alpha=1.0, l1_ratio=0.5, max_iter=1000, tol=1e-4):
        self.alpha = alpha
        self.l1_ratio = l1_ratio
        self.max_iter = max_iter
        self.tol = tol
    def _soft_threshold(self, x, gamma):
        return np.sign(x) * np.maximum(np.abs(x) - gamma, 0)
    def fit(self, X, y):
        n, d = X.shape
        X_mean = X.mean(axis=0)
        y_mean = y.mean()
        Xc = X - X_mean
        yc = y - y_mean
        beta = np.zeros(d)
        L1 = self.alpha * self.l1_ratio
        L2 = self.alpha * (1 - self.l1_ratio)
        for _ in range(self.max_iter):
            beta_old = beta.copy()
            for j in range(d):
                r = yc - Xc @ beta + Xc[:, j] * beta[j]
                rho = Xc[:, j] @ r
                z = Xc[:, j] @ Xc[:, j]
                beta[j] = self._soft_threshold(rho, L1) / (z + L2)
            if np.max(np.abs(beta - beta_old)) < self.tol:
                break
        self.coef_ = beta
        self.intercept_ = y_mean - X_mean @ beta
    def predict(self, X):
        return X @ self.coef_ + self.intercept_

if __name__ == "__main__":
    X, y = make_regression(n_samples=200, n_features=5, noise=0.1, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    ols = OLS()
    ols.fit(X_train, y_train)
    print(f"OLS MSE: {mean_squared_error(y_test, ols.predict(X_test)):.4f}")

    ridge = Ridge(alpha=1.0)
    ridge.fit(X_train, y_train)
    print(f"Ridge MSE: {mean_squared_error(y_test, ridge.predict(X_test)):.4f}")

    lasso = Lasso(alpha=1.0)
    lasso.fit(X_train, y_train)
    print(f"Lasso MSE: {mean_squared_error(y_test, lasso.predict(X_test)):.4f}")
    print(f"Lasso sparsity: {np.sum(np.abs(lasso.coef_) < 1e-6)}/{len(lasso.coef_)}")

    enet = ElasticNet(alpha=1.0, l1_ratio=0.5)
    enet.fit(X_train, y_train)
    print(f"ElasticNet MSE: {mean_squared_error(y_test, enet.predict(X_test)):.4f}")

    from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
    print(f"\nsklearn OLS MSE: {mean_squared_error(y_test, LinearRegression().fit(X_train, y_train).predict(X_test)):.4f}")
    print(f"sklearn Ridge MSE: {mean_squared_error(y_test, Ridge(alpha=1.0).fit(X_train, y_train).predict(X_test)):.4f}")
    print(f"sklearn Lasso MSE: {mean_squared_error(y_test, Lasso(alpha=1.0).fit(X_train, y_train).predict(X_test)):.4f}")
