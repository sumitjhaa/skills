# Lesson 05.52: Robust Statistics

## Learning Objectives
- Understand breakdown point and influence functions
- Implement M-estimators (Huber, Tukey bisquare)
- Apply robust regression via IRLS
- Compare robust covariance estimation (MCD, MVE)

## Motivation
Standard statistics (mean, variance, OLS) are highly sensitive to outliers. A single extreme value can make them arbitrarily wrong.

**Example**: Mean of $\{1, 2, 3, 4, 1000\}$ is 202 — not representative of 4 out of 5 points.

## M-Estimators
Generalize MLE by minimizing:

$$\hat{\theta} = \arg\min_\theta \sum_i \rho(x_i; \theta)$$

Solved by: $\sum_i \psi(x_i; \theta) = 0$ where $\psi(x, \theta) = \frac{\partial}{\partial \theta} \rho(x, \theta)$

### Common $\rho$ Functions

| Estimator | $\rho(x)$ | $\psi(x)$ | Weight $w(x) = \psi(x)/x$ |
|-----------|-----------|-----------|---------------------------|
| Least squares | $x^2/2$ | $x$ | 1 |
| Huber | $\begin{cases} x^2/2 & |x| \leq c \\ c|x| - c^2/2 & |x| > c \end{cases}$ | $\max(-c, \min(c, x))$ | $\min(1, c/|x|)$ |
| Tukey bisquare | $\begin{cases} \frac{c^2}{6}[1-(1-(x/c)^2)^3] & |x| \leq c \\ c^2/6 & |x| > c \end{cases}$ | $x[1-(x/c)^2]^2$ for $|x| \leq c$ | $[1-(x/c)^2]^2$ for $|x| \leq c$ |
| L1 (median) | $|x|$ | $\text{sign}(x)$ | $1/|x|$ |

**Huber**: Combines L2 (near 0) with L1 (far). Redescends to constant — robust but efficient.
**Tukey bisquare**: Redescending $\psi$ — can reject extreme outliers completely.

## Breakdown Point
Maximum fraction of contamination an estimator can tolerate without giving arbitrarily extreme values:

| Estimator | Breakdown Point |
|-----------|----------------|
| Mean | 0% |
| Median | 50% |
| Trimmed mean (50%) | 50% |
| Huber M-estimator | 50% (with robust scale) |
| Tukey bisquare | 50% |
| MAD (median absolute deviation) | 50% |

## Influence Function
Measures sensitivity to an infinitesimal contamination at point $x$:

$$\text{IF}(x; T, F) = \lim_{\varepsilon \to 0} \frac{T((1-\varepsilon)F + \varepsilon \delta_x) - T(F)}{\varepsilon}$$

- **B-robust**: Bounded IF (Huber, Tukey)
- **Efficient**: Low variance at Gaussian model
- **Tradeoff**: Robustness vs efficiency

## Robust Regression

### IRLS for M-Estimation
$$\beta^{(t+1)} = (X^\top W^{(t)} X)^{-1} X^\top W^{(t)} y$$

where $W_{ii}^{(t)} = \frac{\psi(r_i^{(t)} / \hat{\sigma})}{r_i^{(t)} / \hat{\sigma}}$ and $r_i = y_i - x_i^\top \beta$

**Robust scale estimate**: MAD of residuals: $\hat{\sigma} = \text{median}(|r_i - \text{median}(r_i)|) / 0.6745$

### MM-Estimator
Two-stage: 50% breakdown + 95% Gaussian efficiency
1. S-estimator for high breakdown
2. M-step with Tukey bisquare for efficiency

## Code: Robust Regression with Huber

```python
import numpy as np

def huber_psi(r, c=1.345):
    """Huber psi function"""
    return np.where(np.abs(r) <= c, r, c * np.sign(r))

def huber_weight(r, c=1.345):
    """Huber weight function"""
    return np.where(np.abs(r) <= c, 1.0, c / np.abs(r))

def robust_regression(X, y, c=1.345, max_iter=100, tol=1e-6):
    n, d = X.shape
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    for _ in range(max_iter):
        residuals = y - X @ beta
        sigma = np.median(np.abs(residuals)) / 0.6745
        r_scaled = residuals / sigma
        W = np.diag(huber_weight(r_scaled, c))
        beta_new = np.linalg.solve(X.T @ W @ X, X.T @ W @ y)
        if np.linalg.norm(beta_new - beta) < tol:
            break
        beta = beta_new
    return beta
```

## Robust Covariance Estimation

### MCD (Minimum Covariance Determinant)
1. Find subset of $h = \lfloor \alpha n \rfloor$ points with minimum covariance determinant
2. Compute mean and covariance of this subset
3. Reweight using Mahalanobis distances

**Algorithm**: FAST-MCD (Rousseeuw & Van Driessen) — random subsets + C-step concentration.

### MVE (Minimum Volume Ellipsoid)
Smallest ellipsoid covering $h$ points — computationally expensive. MCD preferred.

## Practical Considerations
- **Always check residuals**: No robust method works if data fundamentally violates assumptions
- **Huber vs Tukey**: Huber for general use (better efficiency), Tukey for extreme outliers
- **Robust standard errors**: Use sandwich estimator (Huber-White) for inference after robust regression
- **High-dimensional data**: Regularized robust methods (e.g., sparse M-estimation)
- **Tuning constant**: $c = 1.345$ for 95% Huber efficiency, $c = 4.685$ for 95% Tukey efficiency

## Applications
- **Finance**: Asset returns have heavy tails — robust covariance for portfolio optimization
- **Genomics**: Gene expression data contains outliers from measurement error
- **Signal processing**: Robust mean for noise removal
- **Quality control**: Robust process monitoring

## References
- Huber, "Robust Statistics" (Wiley, 1981)
- Hampel, Ronchetti, Rousseeuw, Stahel, "Robust Statistics: The Approach Based on Influence Functions" (Wiley, 1986)
- Rousseeuw & Leroy, "Robust Regression and Outlier Detection" (Wiley, 1987)
- Rousseeuw & Van Driessen, "A Fast Algorithm for the Minimum Covariance Determinant Estimator" (Technometrics, 1999)
- Maronna, Martin, Yohai, "Robust Statistics: Theory and Methods" (Wiley, 2006)
