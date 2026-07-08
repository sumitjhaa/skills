"""Robust Statistics (Huber, Median, IRLS) from scratch."""
import numpy as np

def huber_rho(x, c=1.345):
    x = np.asarray(x)
    out = np.where(np.abs(x) <= c, 0.5 * x**2, c * (np.abs(x) - 0.5 * c))
    return out

def huber_psi(x, c=1.345):
    return np.clip(x, -c, c)

def tukey_psi(x, c=4.685):
    out = np.where(np.abs(x) <= c, x * (1 - (x/c)**2)**2, 0)
    return out

def robust_mean(x, method='huber', c=1.345, max_iter=50):
    mu = np.median(x)
    for _ in range(max_iter):
        r = x - mu
        mad = np.median(np.abs(r)) / 0.6745 + 1e-10
        r_std = r / mad
        if method == 'huber':
            w = huber_psi(r_std, c) / r_std
        else:
            w = tukey_psi(r_std, c) / r_std
        w = np.where(np.isnan(w), 1, w)
        mu_new = np.sum(w * x) / np.sum(w)
        if abs(mu_new - mu) < 1e-6: break
        mu = mu_new
    return mu

class RobustLinearRegression:
    def __init__(self, c=1.345, max_iter=50):
        self.c = c
        self.max_iter = max_iter

    def fit(self, X, y):
        n, d = X.shape
        X = np.c_[np.ones(n), X]
        self.beta = np.linalg.lstsq(X, y, rcond=None)[0]
        for _ in range(self.max_iter):
            r = y - X @ self.beta
            s = np.median(np.abs(r)) / 0.6745 + 1e-10
            w = huber_psi(r / s, self.c) / (r / s + 1e-10)
            w = np.nan_to_num(w, nan=1.0)
            W = np.diag(w)
            self.beta = np.linalg.solve(X.T @ W @ X, X.T @ W @ y)
        self.intercept_ = self.beta[0]
        self.coef_ = self.beta[1:]

    def predict(self, X):
        return X @ self.coef_ + self.intercept_

if __name__ == "__main__":
    np.random.seed(42)
    x = np.random.randn(100)
    x[:5] = x[:5] + 100  # outliers

    print(f"Mean: {x.mean():.2f} (bad with outliers)")
    print(f"Median: {np.median(x):.2f} (robust)")
    print(f"Huber robust mean: {robust_mean(x, 'huber'):.2f}")
    print(f"Tukey robust mean: {robust_mean(x, 'tukey'):.2f}")

    X = np.random.randn(100, 3)
    y = X @ np.array([1.5, -2.0, 0.5]) + np.random.randn(100) * 0.3
    y[:5] += 50  # outliers

    rr = RobustLinearRegression(c=1.345)
    rr.fit(X, y)
    from sklearn.linear_model import LinearRegression
    lr = LinearRegression().fit(X, y)
    print(f"\nRobust LR coefs: {rr.coef_}")
    print(f"OLS LR coefs: {lr.coef_}")
    print(f"True coefs: [1.5, -2.0, 0.5]")
