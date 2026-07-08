# 23. Natural Gradient Descent

## Introduction

Natural gradient descent respects the geometry of the parameter space, providing invariance to reparameterization and faster convergence in probabilistic models.

## Beyond Euclidean Geometry

Standard gradient descent moves in the direction of steepest descent under the Euclidean metric:

```
Δx = argmin_{‖d‖=1} f(x + d) ≈ -∇f(x)
```

Natural gradient uses the Fisher information metric, which measures distances in distribution space rather than parameter space:

```
Δx_{NG} = -F(x)⁻¹ · ∇f(x)
```

where `F(x)` is the Fisher information matrix:

```
F(x) = E_{p(y|x)} [∇log p(y|x) · ∇log p(y|x)ᵀ]
```

```python
import numpy as np

def natural_gradient(grad_log_p, fisher, x0, lr=0.1, n_iter=100):
    """Natural gradient descent."""
    x = x0.copy()
    for i in range(n_iter):
        g = grad_log_p(x)
        F = fisher(x)
        x = x - lr * np.linalg.solve(F, g)
    return x
```

## Fisher Information as Metric

The KL divergence between two distributions parameterized by `θ` and `θ'`:

```
KL(p_θ || p_θ') ≈ (1/2)(θ - θ')ᵀ F(θ)(θ - θ')
```

Natural gradient moves in the direction that causes the largest change in the objective per unit change in KL divergence.

## Connection to Second-Order Methods

For maximum likelihood estimation with correct model specification, the Fisher is the expected Hessian of the negative log-likelihood. Natural gradient is thus a form of adaptive preconditioning specific to probabilistic models.

## Example: Natural Gradient for Bernoulli

```python
def bernoulli_ng(X, y, x0, lr=0.5, n_iter=100):
    """Natural gradient for Bernoulli GLM."""
    n, d = X.shape
    x = x0.copy()

    for i in range(n_iter):
        p = 1 / (1 + np.exp(-X @ x))
        grad = X.T @ (p - y)

        # Fisher: F = Xᵀ diag(p(1-p)) X
        W = np.diag(p * (1 - p))
        F = X.T @ W @ X

        x = x - lr * np.linalg.solve(F + 1e-8 * np.eye(d), grad)

    return x
```

## Applications

- **Variational inference**: Efficient VI with natural gradients
- **Reinforcement learning**: TRPO and PPO use natural gradients
- **Gradient boosting**: Natural gradient boosting
- **Deep learning**: KFAC approximates the Fisher with a Kronecker factorization
