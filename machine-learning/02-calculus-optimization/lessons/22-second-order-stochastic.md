# 22. Second-Order Stochastic Methods

## Introduction

Second-order stochastic methods approximate curvature information using only stochastic gradients and Hessian-vector products, bringing Newton-like convergence to large-scale optimization.

## Motivation

First-order methods are oblivious to curvature. Preconditioning with curvature information can dramatically accelerate convergence, especially for ill-conditioned problems.

## AdaHessian

AdaHessian uses Hutchinson's trace estimator to compute Hessian diagonals:

```
v ∼ Rademacher (entries ±1 with prob 1/2)
Hv ≈ (∇f(x + σv) - ∇f(x - σv)) / (2σ)  # Hessian-vector product
d = (Hv) ⊙ v  # diagonal estimate (unbiased)
```

```python
import numpy as np

def hessian_vector_product(grad_f, x, v, sigma=0.01):
    """Compute H(x)v via finite differences."""
    grad_plus = grad_f(x + sigma * v)
    grad_minus = grad_f(x - sigma * v)
    return (grad_plus - grad_minus) / (2 * sigma)

def adahessian_step(grad_f, x, m, v, t, lr=0.15, beta1=0.9, beta2=0.999):
    """Single AdaHessian update (diagonal approximation)."""
    g = grad_f(x)
    m = beta1 * m + (1 - beta1) * g

    # Hutchinson estimate of Hessian diagonal
    rademacher = np.random.choice([-1, 1], size=len(x))
    hv = hessian_vector_product(grad_f, x, rademacher)
    d = hv * rademacher  # diagonal estimate
    d = np.abs(d)  # ensure positivity
    v = beta2 * v + (1 - beta2) * d**2

    m_hat = m / (1 - beta1**t)
    v_hat = v / (1 - beta2**t)
    x = x - lr * m_hat / (np.sqrt(v_hat) + 1e-8)

    return x, m, v
```

## Stochastic L-BFGS

Stochastic L-BFGS maintains curvature pairs using subsampled gradients:

```python
def stochastic_lbfgs(grad_f, x0, batch_size=10, m=5, n_epochs=20):
    """Simplified stochastic L-BFGS."""
    n = len(x0)
    x = x0.copy()
    s_list = []
    y_list = []

    for epoch in range(n_epochs):
        g = grad_f(x)  # full or minibatch gradient

        # Compute direction using two-loop recursion
        if len(s_list) > 0:
            q = g.copy()
            alphas = []
            for s, y in reversed(s_list):
                rho = 1.0 / (y @ s)
                alpha = rho * (s @ q)
                alphas.append(alpha)
                q = q - alpha * y
            r = q * (s_list[-1][0] @ y_list[-1][0]) / (y_list[-1][0] @ y_list[-1][0])
            for (s, y), alpha in zip(s_list, reversed(alphas)):
                rho = 1.0 / (y @ s)
                beta = rho * (y @ r)
                r = r + (alpha - beta) * s
            d = -r
        else:
            d = -g

        # Line search and update
        x_new = x + 1.0 * d
        g_new = grad_f(x_new)
        s = x_new - x
        y = g_new - g

        if len(s_list) >= m:
            s_list.pop(0)
            y_list.pop(0)
        s_list.append((s, y))
        x = x_new

    return x
```

## Trade-offs

- **AdaHessian**: O(d) per iteration, good for deep networks
- **Stochastic L-BFGS**: O(md) per iteration, good for medium-scale
- **Full Newton**: O(d³) per iteration, impractical for large d

Second-order stochastic methods bridge the gap between first-order methods and full Newton, offering faster convergence for ill-conditioned problems at reasonable cost.
