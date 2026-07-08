# 28. Bayesian Optimization

## Introduction

Bayesian optimization (BO) optimizes expensive black-box functions where evaluations are costly (e.g., hyperparameter tuning, experimental design). It builds a probabilistic surrogate model and selects evaluation points via an acquisition function.

## Gaussian Process Surrogate

A GP prior over functions: `f ∼ GP(m(x), k(x, x'))` with:

- Mean function `m(x)` (often zero)
- Covariance kernel `k(x, x')` (e.g., RBF, Matern)

After observing data `D = {(x_i, y_i)}`, the posterior is:

```
f(x) | D ∼ N(μ(x), σ²(x))
```

```python
import numpy as np
from scipy.linalg import cholesky, solve_triangular

def gp_posterior(X_train, y_train, X_test, sigma_noise=1e-3, length_scale=1.0):
    """GP posterior mean and variance."""
    def rbf(x1, x2):
        dist2 = np.sum((x1[:, None] - x2[None, :])**2, axis=-1)
        return np.exp(-dist2 / (2 * length_scale**2))

    K = rbf(X_train, X_train) + sigma_noise * np.eye(len(X_train))
    K_s = rbf(X_train, X_test)
    K_ss = rbf(X_test, X_test) + sigma_noise * np.eye(len(X_test))

    L = cholesky(K, lower=True)
    alpha = solve_triangular(L.T, solve_triangular(L, y_train, lower=True))

    mu = K_s.T @ alpha
    v = solve_triangular(L, K_s, lower=True)
    var = np.diag(K_ss) - np.sum(v**2, axis=0)

    return mu, np.sqrt(var)
```

## Acquisition Functions

### Expected Improvement (EI)

```
EI(x) = E[max(0, f(x) - f(x_best))]
       = (μ(x) - f*)Φ(z) + σ(x)φ(z)  where z = (μ(x) - f*)/σ(x)
```

### Upper Confidence Bound (UCB)

```
UCB(x) = μ(x) + κ · σ(x)
```

```python
def expected_improvement(mu, sigma, f_best):
    """Expected Improvement acquisition function."""
    imp = mu - f_best
    Z = imp / (sigma + 1e-10)
    ei = imp * norm.cdf(Z) + sigma * norm.pdf(Z)
    ei[sigma < 1e-10] = 0
    return ei

def bayesian_optimization(f, bounds, n_init=5, n_iter=20):
    """Simple Bayesian optimization loop."""
    dim = len(bounds)
    X = np.random.uniform(bounds[:, 0], bounds[:, 1], (n_init, dim))
    y = np.array([f(x) for x in X])

    for i in range(n_iter):
        # Fit GP and maximize acquisition
        X_candidates = np.random.uniform(bounds[:, 0], bounds[:, 1], (1000, dim))
        mu, sigma = gp_posterior(X, y, X_candidates)
        f_best = y.min()
        ei = expected_improvement(mu, sigma, f_best)
        x_next = X_candidates[ei.argmax()]

        # Evaluate and update
        y_next = f(x_next)
        X = np.vstack([X, x_next.reshape(1, -1)])
        y = np.hstack([y, y_next])

    return X, y
```

## Applications

- **Hyperparameter tuning**: Learning rates, architecture choices
- **A/B testing**: Finding optimal website design
- **Material design**: Optimizing material properties
- **Robot control**: Learning walking gaits

BO excels when evaluations cost more than the optimization overhead (typically > 1 minute per evaluation).
