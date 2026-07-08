# Lesson 05.01: Linear Regression (OLS, Ridge, Lasso, ElasticNet)

## Learning Objectives
- Derive OLS closed-form solution and understand Gauss-Markov assumptions
- Implement Ridge, Lasso, and ElasticNet regressions
- Understand bias-variance tradeoff across regularizations
- Analyze regularization paths

## Mathematical Foundation

### Ordinary Least Squares (OLS)
Given design matrix $X \in \mathbb{R}^{n \times d}$ and targets $y \in \mathbb{R}^n$, OLS minimizes residual sum of squares:

$$\hat{\beta} = \arg\min_\beta \|y - X\beta\|_2^2$$

Setting gradient to zero:

$$\nabla_\beta \|y - X\beta\|_2^2 = -2X^\top(y - X\beta) = 0$$

$$X^\top X \hat{\beta} = X^\top y$$

Closed-form solution exists when $X^\top X$ is invertible (full column rank):

$$\hat{\beta} = (X^\top X)^{-1} X^\top y$$

### Geometric Interpretation
The OLS solution projects $y$ onto the column space of $X$:

$$\hat{y} = X\hat{\beta} = X(X^\top X)^{-1} X^\top y = H y$$

where $H$ is the hat matrix. $\hat{y}$ is the orthogonal projection of $y$ onto $\text{Col}(X)$.

### Gauss-Markov Theorem
Under assumptions (linearity, exogeneity, homoscedasticity, uncorrelated errors), OLS is BLUE (Best Linear Unbiased Estimator):

$$\text{Var}(\hat{\beta}) = \sigma^2 (X^\top X)^{-1}$$

### Gradient Descent View
For large $n$ where closed-form is expensive ($O(nd^2 + d^3)$):

$$\nabla_\beta L = -2X^\top(y - X\beta)$$

Update rule with learning rate $\eta$:

$$\beta_{t+1} = \beta_t - \eta \nabla_\beta L$$

Stochastic variants sample mini-batches for scalability.

## Ridge Regression (L2 Regularization)
Adds $\ell_2$ penalty to control variance:

$$\hat{\beta}_\text{ridge} = \arg\min_\beta \|y - X\beta\|_2^2 + \lambda \|\beta\|_2^2$$

Closed form remains available:

$$\hat{\beta}_\text{ridge} = (X^\top X + \lambda I)^{-1} X^\top y$$

### Bias-Variance in Ridge
- $\lambda = 0$: OLS (unbiased, high variance)
- $\lambda \to \infty$: $\hat{\beta} \to 0$ (high bias, zero variance)
- Optimal $\lambda$ balances test error via cross-validation

Ridge shrinks coefficients but never to exactly zero. Solutions are equivariant under scaling of features (should standardize first).

## Lasso Regression (L1 Regularization)
$$\hat{\beta}_\text{lasso} = \arg\min_\beta \frac{1}{2n} \|y - X\beta\|_2^2 + \lambda \|\beta\|_1$$

No closed-form solution. Solved via coordinate descent or LARS.

### Coordinate Descent for Lasso
Update one coordinate at a time keeping others fixed:

$$\beta_j \leftarrow \frac{S(\rho_j, \lambda)}{\|X_{\cdot j}\|_2^2}$$

where $\rho_j = \sum_i X_{ij} (y_i - \sum_{k \neq j} X_{ik} \beta_k)$ and $S(z, \gamma) = \text{sign}(z)(|z| - \gamma)_+$ is the soft-thresholding operator.

### Regularization Path
As $\lambda$ decreases, more variables enter the model sequentially. This produces a piecewise-linear solution path efficiently computed by LARS (Least Angle Regression).

## ElasticNet
Mixes L1 and L2 penalties:

$$\hat{\beta}_\text{enet} = \arg\min_\beta \frac{1}{2n} \|y - X\beta\|_2^2 + \lambda \left(\frac{1-\alpha}{2} \|\beta\|_2^2 + \alpha \|\beta\|_1\right)$$

- $\alpha = 1$: Lasso
- $\alpha = 0$: Ridge
- $0 < \alpha < 1$: ElasticNet

ElasticNet handles correlated features better than Lasso (which picks one arbitrarily from a correlated group), performing group selection.

## Code: Linear Regression from Scratch

```python
import numpy as np
from scipy import linalg

def ols_closed_form(X, y):
    """Closed-form OLS solution"""
    return linalg.solve(X.T @ X, X.T @ y)

def ridge_closed_form(X, y, lam):
    """Closed-form Ridge solution"""
    n, d = X.shape
    return linalg.solve(X.T @ X + lam * np.eye(d), X.T @ y)

def soft_threshold(z, gamma):
    """Soft-thresholding operator for Lasso"""
    return np.sign(z) * np.maximum(np.abs(z) - gamma, 0)

def lasso_coordinate_descent(X, y, lam, max_iter=1000, tol=1e-4):
    """Lasso via coordinate descent"""
    n, d = X.shape
    beta = np.zeros(d)
    XtX = np.sum(X**2, axis=0)
    for _ in range(max_iter):
        beta_old = beta.copy()
        for j in range(d):
            residual = y - X @ beta + X[:, j] * beta[j]
            rho_j = X[:, j] @ residual
            beta[j] = soft_threshold(rho_j, lam * n) / XtX[j]
        if np.max(np.abs(beta - beta_old)) < tol:
            break
    return beta
```

## Visualization
Plot three panels: (1) OLS fit with confidence bands, (2) Ridge regularization path (coefficient magnitude vs $\lambda$), (3) Lasso path showing variable selection as $\lambda$ decreases. The Lasso path piecewise-linear shape demonstrates the selection property.

## Practical Considerations
- **Feature scaling**: Standardize all features before Ridge/Lasso/ElasticNet
- **Multicollinearity**: Lasso picks one variable arbitrarily; ElasticNet or Ridge preferred
- **$n < d$**: OLS undefined, Ridge/Lasso still work
- **Intercept**: Center $y$ and $X$, intercept = $\bar{y}$ after centering
- **$\lambda$ selection**: Use cross-validation (sklearn's `RidgeCV`, `LassoCV`)
- **Numerical stability**: Use SVD or Cholesky for OLS; avoid computing $(X^\top X)^{-1}$ explicitly
- **Large $n$**: Use SGD or mini-batch gradient descent over closed form

## Key Properties
- OLS: unbiased, BLUE under Gauss-Markov assumptions, $O(nd^2)$
- Ridge: biased but lower variance, closed-form, handles collinearity
- Lasso: biased, sparse solutions, automatic feature selection, $O(nd)$ per iteration
- ElasticNet: handles correlated features, group selection effect

## References
- Hastie, Tibshirani, Friedman, "The Elements of Statistical Learning", Ch. 3
- Murphy, "Probabilistic Machine Learning", Ch. 11
- Tibshirani, "Regression Shrinkage and Selection via the Lasso" (JRSS-B, 1996)
- Zou & Hastie, "Regularization and Variable Selection via the Elastic Net" (JRSS-B, 2005)
