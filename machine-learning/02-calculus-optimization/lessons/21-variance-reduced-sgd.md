# 21. Variance-Reduced SGD

## Introduction

Standard SGD has high variance due to random minibatches, leading to slow convergence. Variance-reduced methods maintain gradient estimates with progressively lower variance, achieving faster convergence.

## The Variance Problem

For SGD: `∇f_S(x) = (1/|S|) Σ_{i∈S} ∇f_i(x)`

```
Var[∇f_S(x)] = (1/|S|) · Var[∇f_i(x)]
```

The variance prevents convergence to the exact optimum — SGD only converges to a neighborhood.

## SVRG (Stochastic Variance Reduced Gradient)

SVRG maintains a snapshot gradient computed periodically on the full dataset:

```
μ = ∇f(x_0)  # full gradient at snapshot
For each epoch:
  For each minibatch:
    g = ∇f_S(x) - ∇f_S(x_0) + μ
    x = x - η · g
```

```python
import numpy as np

def svrg(grad_f, grad_fi, data, x0, lr=0.01, epoch_size=100, n_epochs=50):
    """SVRG for minimizing f(x) = (1/N)Σ f_i(x)."""
    x = x0.copy()
    N = len(data)

    for epoch in range(n_epochs):
        x_tilde = x.copy()
        mu = grad_f(x_tilde, data)  # full gradient

        for t in range(epoch_size):
            i = np.random.randint(N)
            g = grad_fi(x, data[i]) - grad_fi(x_tilde, data[i]) + mu
            x = x - lr * g

    return x
```

Key insight: `g` is an unbiased estimate of `∇f(x)` with variance that decreases as `x → x_tilde`.

## SAGA

SAGA stores the gradient for each data point and updates it after each step:

```
g = ∇f_i(x) - g_i_old + (1/N) Σ_j g_j_old
g_i_old = ∇f_i(x)
```

```python
def saga(grad_fi, data, x0, lr=0.01, n_epochs=50):
    N = len(data)
    x = x0.copy()
    g_old = [grad_fi(x0, d) for d in data]  # stored gradients
    g_mean = np.mean(g_old, axis=0)

    for epoch in range(n_epochs):
        for i in np.random.permutation(N):
            g_i = grad_fi(x, data[i])
            g = g_i - g_old[i] + g_mean
            x = x - lr * g
            g_mean += (g_i - g_old[i]) / N
            g_old[i] = g_i

    return x
```

## Convergence Comparison

| Method | Convergence rate | Storage | Variance |
|--------|-----------------|---------|----------|
| SGD | O(1/√t) + noise | O(1) | High |
| SVRG | O(1/t) | O(d) | Decaying |
| SAGA | O(1/t) | O(Nd) | Decaying |
| SARAH | O(1/t) | O(d) | Monotonic |

Variance-reduced methods achieve linear convergence for strongly convex functions, matching full-gradient methods while using only stochastic gradients.
