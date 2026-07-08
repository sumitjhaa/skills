# 34. Compositional Optimization

## Introduction

Compositional optimization minimizes a function composed of multiple nested functions. It generalizes standard optimization and is essential for risk measures, policy gradients, and some meta-learning formulations.

## Problem Formulation

```
minimize    F(x) = f(g(x))
```

More generally:

```
minimize    F(x) = E_ξ [f_ξ(E_η [g_η(x)])]
```

## Stochastic Compositional Gradient Descent

The gradient via the chain rule involves the Jacobian of the inner function:

```
∇F(x) = ∇f(g(x)) · ∇g(x)
```

When the inner function is an expectation, we need to estimate both:

```python
import numpy as np

def compositional_gd(f, g, grad_f, jac_g, x0, lr=0.01, n_iter=100):
    """Gradient descent for F(x) = f(g(x))."""
    x = x0.copy()
    for i in range(n_iter):
        inner = g(x)
        grad = jac_g(x).T @ grad_f(inner)
        x = x - lr * grad
    return x
```

## Two-Timescale Method

When inner and outer functions involve expectations, use separate step sizes:

```
y_{t+1} = y_t - β_t (y_t - g(x_t))  # inner tracking
x_{t+1} = x_t - α_t ∇f(y_{t+1}) · ∇g(x_t)  # outer update
```

```python
def two_timescale_compositional(sample_g, sample_grad_f, sample_jac_g,
                                 x0, n_iter=1000, alpha=0.01, beta=0.1):
    """Two-timescale stochastic compositional optimization."""
    x = x0.copy()
    y = sample_g(x)  # initial inner estimate

    for t in range(n_iter):
        # Update inner estimate
        g_val = sample_g(x)
        y = y - beta * (y - g_val)

        # Update outer variable
        jac = sample_jac_g(x)
        grad = sample_grad_f(y)
        x = x - alpha * jac.T @ grad

    return x
```

## Applications

### Conditional Value-at-Risk (CVaR)

```
CVaR_α(x) = min_t { t + (1/(1-α)) E[max(0, f(x, ξ) - t)] }
```

This is compositional: the inner expectation depends on `t` and `x`.

### Policy Gradient in RL

The expected return is:

```
J(θ) = E_τ [R(τ)] where τ ∼ p_θ(τ)
```

The gradient requires differentiating through the trajectory distribution, which compositionally depends on the policy.

### Robust Optimization

```
min_x max_{δ ∈ Δ} f(x + δ) = min_x f(x + δ*(x))
```

where `δ*(x) = argmax_{δ ∈ Δ} f(x + δ)`.

## Convergence

- Standard SGD on compositional objectives may not converge due to bias
- Two-timescale methods achieve O(1/√T) convergence for concave compositional problems
- Variance-reduced compositional methods achieve O(1/T) for strongly convex cases

Compositional optimization bridges stochastic approximation and nested optimization, with important applications in risk-sensitive learning and reinforcement learning.
