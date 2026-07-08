# Lesson 05.02: Logistic Regression

## Learning Objectives
- Derive logistic regression from generalized linear model perspective
- Implement Newton-Raphson (IRLS) and gradient descent optimization
- Understand multiclass softmax extension
- Apply regularization for high-dimensional settings

## Mathematical Foundation

### Binary Logistic Regression
Model the probability of class 1 given features $x$:

$$P(y=1|x) = \sigma(w^\top x) = \frac{1}{1 + e^{-w^\top x}}$$

where $\sigma(z)$ is the logistic sigmoid function. The log-odds (logit) is linear:

$$\log\frac{P(y=1|x)}{P(y=0|x)} = w^\top x$$

### Likelihood and Loss
For dataset $\{(x_i, y_i)\}_{i=1}^n$ with $y_i \in \{0, 1\}$:

$$L(w) = \prod_{i=1}^n P(y_i|x_i) = \prod_{i=1}^n \sigma(w^\top x_i)^{y_i} (1-\sigma(w^\top x_i))^{1-y_i}$$

Negative log-likelihood (binary cross-entropy):

$$\ell(w) = -\sum_{i=1}^n [y_i \log(\hat{y}_i) + (1-y_i)\log(1-\hat{y}_i)]$$

### Gradient and Hessian
Gradient:

$$\nabla \ell(w) = \sum_{i=1}^n (\sigma(w^\top x_i) - y_i) x_i = X^\top(\hat{y} - y)$$

Hessian:

$$H(w) = \sum_{i=1}^n \sigma(w^\top x_i)(1-\sigma(w^\top x_i)) x_i x_i^\top = X^\top D X$$

where $D_{ii} = \hat{y}_i(1-\hat{y}_i)$. The Hessian is positive semidefinite, making the problem convex.

### Newton-Raphson (IRLS)
Iteratively reweighted least squares update:

$$w_{t+1} = w_t - H^{-1} \nabla \ell = (X^\top D_t X)^{-1} X^\top D_t z_t$$

where $z_t = X w_t + D_t^{-1}(y - \hat{y}_t)$ is the working response. This is equivalent to solving a weighted least squares problem at each iteration.

## Regularization

### L2 Regularization (Ridge Logistic)
Add penalty to loss: $\ell_\text{reg}(w) = \ell(w) + \frac{\lambda}{2}\|w\|_2^2$

Gradient: $\nabla \ell_\text{reg}(w) = X^\top(\hat{y} - y) + \lambda w$

This improves numerical stability and prevents overfitting, especially when $d \gg n$.

### L1 Regularization (Lasso Logistic)
Adds $\lambda\|w\|_1$ penalty. Not differentiable at zero — solved via proximal gradient or coordinate descent with soft-thresholding.

## Multinomial (Softmax) Regression
For $K$ classes:

$$P(y=k|x) = \frac{e^{w_k^\top x}}{\sum_{j=1}^K e^{w_j^\top x}}$$

Parameters: $W \in \mathbb{R}^{K \times d}$ (or $K \times (d+1)$ with bias).

Loss (categorical cross-entropy):

$$\ell(W) = -\sum_{i=1}^n \log P(y_i|x_i) = -\sum_{i=1}^n \left[ w_{y_i}^\top x_i - \log\sum_{j=1}^K e^{w_j^\top x_i} \right]$$

### Identifiability
Softmax has redundant parameters (adding constant to all $w_k$ gives same probabilities). Fix by setting $w_K = 0$ (reference class) or adding regularization.

## Decision Boundary
Logistic regression has a linear decision boundary: $\{x : w^\top x = 0\}$. Non-linear boundaries can be achieved via feature engineering (polynomials, interactions) or kernels.

## Code: Logistic Regression with IRLS

```python
import numpy as np
from scipy.special import expit

def sigmoid(z):
    """Numerically stable sigmoid"""
    return expit(z)

def logistic_IRLS(X, y, max_iter=100, tol=1e-6):
    """Logistic regression via Iteratively Reweighted Least Squares"""
    n, d = X.shape
    w = np.zeros(d)
    for iteration in range(max_iter):
        eta = X @ w
        mu = sigmoid(eta)
        D = np.diag(mu * (1 - mu))
        z = eta + np.linalg.solve(D, y - mu)
        w_new = np.linalg.solve(X.T @ D @ X, X.T @ D @ z)
        if np.linalg.norm(w_new - w) < tol:
            break
        w = w_new
    return w

def logistic_gradient_descent(X, y, lr=0.01, max_iter=1000):
    """Logistic regression via gradient descent"""
    n, d = X.shape
    w = np.zeros(d)
    for _ in range(max_iter):
        grad = X.T @ (sigmoid(X @ w) - y) / n
        w -= lr * grad
    return w
```

## Practical Considerations
- **Separability**: When classes are perfectly separable, logistic weights diverge to infinity. L2 regularization fixes this
- **Imbalanced data**: Adjust class weights or use oversampling
- **Feature scaling**: Gradient descent converges faster with standardized features
- **Calibration**: Logistic regression is naturally well-calibrated
- **Large $n$**: Use SGD; full Hessian is $O(nd^2)$
- **Numerical stability**: Clip sigmoid inputs to avoid overflow: `np.clip(z, -100, 100)`

## Key Points
- No closed-form solution; optimization required
- Convex objective (unique global optimum)
- Linear decision boundary in original feature space
- Extends to multiclass via softmax
- Naturally calibrated probabilities under correct model

## References
- Hosmer, Lemeshow, Sturdivant, "Applied Logistic Regression"
- Bishop, "Pattern Recognition and Machine Learning", Ch. 4
- Murphy, "Probabilistic Machine Learning", Ch. 8
