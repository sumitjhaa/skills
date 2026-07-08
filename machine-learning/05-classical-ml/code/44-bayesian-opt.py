"""Bayesian Optimization with GP surrogate and EI."""
import numpy as np
import matplotlib.pyplot as plt

def rbf_kernel(x1, x2, l=1.0, sf=1.0):
    sq = np.sum(x1**2, axis=1)[:, None] + np.sum(x2**2, axis=1)[None, :] - 2*x1@x2.T
    return sf**2 * np.exp(-0.5/l**2 * sq)

class GP:
    def __init__(self, sigma_n=1e-2):
        self.sigma_n = sigma_n
    def fit(self, X, y):
        self.X, self.y = X, y
        K = rbf_kernel(X, X) + self.sigma_n**2 * np.eye(X.shape[0])
        self.L = np.linalg.cholesky(K)
        self.alpha = np.linalg.solve(self.L.T, np.linalg.solve(self.L, y))
    def predict(self, X_test):
        Ks = rbf_kernel(self.X, X_test)
        mu = Ks.T @ self.alpha
        v = np.linalg.solve(self.L, Ks)
        cov = rbf_kernel(X_test, X_test) - v.T @ v
        return mu.ravel(), np.sqrt(np.maximum(np.diag(cov), 0))

def expected_improvement(mu, sigma, f_best, xi=0.01):
    imp = f_best - mu - xi
    Z = imp / (sigma + 1e-10)
    return imp * sp_stats.norm.cdf(Z) + sigma * sp_stats.norm.pdf(Z)

import scipy.stats as sp_stats

class BayesianOptimization:
    def __init__(self, f, bounds, n_init=5, n_iter=20):
        self.f = f
        self.bounds = np.array(bounds)
        self.n_init = n_init
        self.n_iter = n_iter
        self.gp = GP()

    def optimize(self):
        X = np.random.uniform(self.bounds[:, 0], self.bounds[:, 1], (self.n_init, 1))
        y = np.array([self.f(x) for x in X])

        for i in range(self.n_iter):
            self.gp.fit(X, y)
            xs = np.linspace(self.bounds[0, 0], self.bounds[0, 1], 200).reshape(-1, 1)
            mu, sigma = self.gp.predict(xs)
            ei = expected_improvement(mu, sigma, y.max())
            x_next = xs[np.argmax(ei)]
            y_next = self.f(x_next)
            X = np.vstack([X, [x_next]])
            y = np.append(y, y_next)
            print(f"  Iter {i+1}: x={x_next[0]:.4f}, y={y_next:.4f}, best={y.max():.4f}")

        best_idx = np.argmax(y)
        return X[best_idx], y[best_idx]

if __name__ == "__main__":
    def f(x):
        return np.sin(3*x[0]) * np.exp(-0.5*x[0])

    np.random.seed(42)
    bo = BayesianOptimization(f, bounds=[(-3, 3)], n_init=3, n_iter=10)
    x_best, y_best = bo.optimize()
    print(f"\nBest found: x={x_best[0]:.4f}, f(x)={y_best:.4f}")
    print(f"True optimum: x≈{np.pi/6:.4f}, f(x)≈{1:.4f}")
