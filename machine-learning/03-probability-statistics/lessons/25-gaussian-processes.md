# Lesson 25: Gaussian Processes

## Learning Objectives

After completing this lesson, you will be able to:
- Define a Gaussian process and its properties
- Choose and combine kernel functions for different data types
- Perform GP regression predictions with uncertainty
- Learn hyperparameters by maximizing marginal likelihood
- Understand computational challenges and scalable approximations

## Definition

A **Gaussian process (GP)** is a collection of random variables $\{f(x): x \in \mathcal{X}\}$ such that any finite subset has a multivariate normal distribution.

A GP is fully specified by:
- **Mean function:** $m(x) = E[f(x)]$
- **Covariance (kernel) function:** $k(x, x') = \text{Cov}(f(x), f(x'))$

$$f(x) \sim \mathcal{GP}(m(x), k(x, x'))$$

## Gaussian Process Regression

### Prior

$$f \sim \mathcal{GP}(0, k(\cdot, \cdot))$$

At training points $X$: $f(X) \sim \mathcal{N}(0, K(X, X))$ where $K_{ij} = k(x_i, x_j)$.

### Likelihood

$$y_i = f(x_i) + \varepsilon_i, \quad \varepsilon_i \sim \mathcal{N}(0, \sigma_n^2)$$
$$y \mid f \sim \mathcal{N}(f, \sigma_n^2 I)$$

### Posterior

For test points $X_*$:
$$f_* \mid X, y, X_* \sim \mathcal{N}(\bar{f}_*, \text{Cov}(f_*))$$

$$\bar{f}_* = K(X_*, X) (K(X, X) + \sigma_n^2 I)^{-1} y$$
$$\text{Cov}(f_*) = K(X_*, X_*) - K(X_*, X) (K + \sigma_n^2 I)^{-1} K(X, X_*)$$

The predictive mean is a linear combination of $n$ kernel functions centered at training points:
$$\bar{f}_*(x_*) = \sum_{i=1}^n \alpha_i k(x_i, x_*), \quad \alpha = (K + \sigma_n^2 I)^{-1} y$$

## Kernel Functions

### Stationary Kernels

$k(x, x') = k(r)$ where $r = \|x - x'\|$.

| Kernel | Formula | Properties |
|--------|---------|------------|
| RBF/SE | $\sigma^2 \exp(-r^2/2\ell^2)$ | Infinitely smooth, $\mathcal{C}^\infty$ |
| Exponential | $\sigma^2 \exp(-r/\ell)$ | Continuous, not differentiable |
| Matérn($\nu$) | $\sigma^2 \frac{2^{1-\nu}}{\Gamma(\nu)} (\sqrt{2\nu}r/\ell)^\nu K_\nu(\sqrt{2\nu}r/\ell)$ | $\lceil \nu \rceil - 1$ times differentiable |
| Rational Quadratic | $\sigma^2 (1 + r^2/2\alpha\ell^2)^{-\alpha}$ | Scale mixture of SE kernels |

### Non-Stationary Kernels

| Kernel | Formula | Use Case |
|--------|---------|----------|
| Linear | $\sigma_0^2 + \sigma_1^2 x^\top x'$ | Linear functions |
| Periodic | $\sigma^2 \exp(-2\sin^2(\pi|x-x'|/p)/\ell^2)$ | Periodic data |
| Polynomial | $(\sigma_0^2 + x^\top x')^d$ | Polynomial functions |

### Kernel Composition

Valid kernels are closed under:
- **Addition:** $k_1 + k_2$ (capture multiple scales)
- **Multiplication:** $k_1 \times k_2$ (capture interactions)
- **Scaling:** $c \cdot k$ for $c > 0$
- **Kronecker product:** For multi-dimensional inputs

## Hyperparameter Learning

### Log Marginal Likelihood

$$\log p(y \mid X, \theta) = -\frac{1}{2} y^\top (K + \sigma_n^2 I)^{-1} y - \frac{1}{2} \log|K + \sigma_n^2 I| - \frac{n}{2} \log 2\pi$$

Three terms:
1. **Data fit:** $-\frac{1}{2} y^\top K_y^{-1} y$ (encourages fit)
2. **Complexity penalty:** $-\frac{1}{2} \log|K_y|$ (penalizes complex models)
3. **Normalization constant:** $-\frac{n}{2} \log 2\pi$

### Gradient-Based Optimization

$$\frac{\partial}{\partial \theta_j} \log p(y \mid X, \theta) = \frac{1}{2} \text{tr}\left((\alpha\alpha^\top - K_y^{-1}) \frac{\partial K_y}{\partial \theta_j}\right)$$

where $\alpha = K_y^{-1} y$ and $K_y = K + \sigma_n^2 I$.

## Computational Issues

### Naive Cost

- Training: $O(n^3)$ (Cholesky decomposition of $K_y$)
- Storage: $O(n^2)$
- Prediction per test point: $O(n)$ (or $O(n^2)$ for variance)

### Scalable Approximations

| Method | Approach | Cost |
|--------|----------|------|
| Subset of Data | Use $m < n$ points | $O(m^3)$ |
| Nyström | Approximate $K$ by low-rank | $O(m^2 n)$ |
| Fully Independent Training Conditional (FITC) | Sparse pseudo-inputs | $O(n m^2)$ |
| Variational Free Energy (VFE) | Variational bound on marginal likelihood | $O(n m^2)$ |
| Stochastic Variational GP | Mini-batch training | $O(m^3)$ per iteration |
| KISS-GP | Kronecker structure | $O(n + m \log m)$ |

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from scipy.optimize import minimize

def rbf_kernel(X1, X2, length_scale=1.0, variance=1.0):
    sq_dist = cdist(X1 / length_scale, X2 / length_scale, 'sqeuclidean')
    return variance * np.exp(-0.5 * sq_dist)

class GaussianProcess:
    def __init__(self, kernel=rbf_kernel, sigma_n=0.1):
        self.kernel = kernel
        self.sigma_n = sigma_n

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y
        n = X.shape[0]
        K = self.kernel(X, X) + self.sigma_n**2 * np.eye(n)
        self.L = np.linalg.cholesky(K)
        self.alpha = np.linalg.solve(self.L.T, np.linalg.solve(self.L, y))
        return self

    def predict(self, X_test, return_std=True):
        K_s = self.kernel(self.X_train, X_test)
        K_ss = self.kernel(X_test, X_test)
        mu = K_s.T @ self.alpha
        if return_std:
            v = np.linalg.solve(self.L, K_s)
            cov = K_ss - v.T @ v
            std = np.sqrt(np.diag(cov) + self.sigma_n**2)
            return mu, std
        return mu

    def negative_log_likelihood(self, params):
        length_scale, variance, sigma_n = params
        kernel = lambda X1, X2: rbf_kernel(X1, X2, length_scale, variance)
        n = self.X_train.shape[0]
        K = kernel(self.X_train, self.X_train) + sigma_n**2 * np.eye(n)
        L = np.linalg.cholesky(K)
        alpha = np.linalg.solve(L.T, np.linalg.solve(L, self.y_train))
        nll = 0.5 * self.y_train.T @ alpha + np.sum(np.log(np.diag(L))) + 0.5 * n * np.log(2*np.pi)
        return nll.flatten()

# Example
np.random.seed(42)
X = np.random.uniform(-5, 5, 20).reshape(-1, 1)
y = np.sin(X).ravel() + np.random.normal(0, 0.1, 20)

gp = GaussianProcess()
gp.fit(X, y)

X_test = np.linspace(-6, 6, 200).reshape(-1, 1)
mu, std = gp.predict(X_test)

plt.figure(figsize=(10, 5))
plt.scatter(X, y, c='r', s=30, label='Training data')
plt.plot(X_test, np.sin(X_test), 'k--', label='True function')
plt.plot(X_test, mu, 'b-', lw=2, label='GP mean')
plt.fill_between(X_test.ravel(), mu - 2*std, mu + 2*std,
                  alpha=0.3, color='b', label='95% CI')
plt.legend()
plt.title('Gaussian Process Regression')
plt.show()

# Hyperparameter optimization
result = minimize(gp.negative_log_likelihood,
                  x0=[1.0, 1.0, 0.1],
                  bounds=((1e-3, 10), (1e-3, 10), (1e-3, 1)),
                  method='L-BFGS-B')
print(f"Optimized length_scale={result.x[0]:.3f}, variance={result.x[1]:.3f}, sigma_n={result.x[2]:.4f}")
```

## Visualization

The key visualization for GP regression shows: (1) Observations as points; (2) GP predictive mean as a curve; (3) 95% credible intervals as a shaded region that expands away from data; (4) The true function (if known). Add a second figure showing random functions drawn from the GP prior (before seeing data) and posterior (after conditioning on data), illustrating how the GP constrains functions to pass near observations.

## Practical Considerations

- **Kernel choice:** The kernel encodes assumptions about function smoothness, periodicity, and stationarity. Use cross-validation or LML for kernel selection.
- **Input scaling:** Standardize inputs to unit variance. Otherwise, length-scale hyperparameters are hard to interpret and optimize.
- **Noise estimation:** The noise variance $\sigma_n^2$ prevents overfitting. For noise-free data, set to a small positive number for numerical stability.
- **Big data:** For $n > 10^4$, use scalable approximations (SVGP, KISS-GP). For $n > 10^6$, consider deep GPs or random feature expansions.

## References

- Rasmussen, C. E. & Williams, C. K. I. (2006). *Gaussian Processes for Machine Learning*
- Duvenaud, D. (2014). "Automatic model construction with Gaussian processes"
- Wilson, A. G. & Nickisch, H. (2015). "Kernel interpolation for scalable structured Gaussian processes"
- Hensman, J., et al. (2013). "Gaussian processes for big data"
