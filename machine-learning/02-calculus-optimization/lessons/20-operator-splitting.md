# 20. Operator Splitting Methods

## Introduction

Operator splitting decomposes complex monotone inclusion problems into simpler subproblems. These methods underlie ADMM, proximal algorithms, and many modern optimization techniques.

## Monotone Operators

An operator `T: ℝⁿ → ℝⁿ` is monotone if:

```
⟨T(x) - T(y), x - y⟩ ≥ 0  for all x, y
```

The subdifferential ∂f of a convex function is a monotone operator. Finding `x` such that `0 ∈ T(x)` generalizes optimization.

## Douglas-Rachford Splitting

For finding `0 ∈ A(x) + B(x)` where A and B are monotone:

```
x_{k+1} = prox_A(z_k)
y_k = prox_B(2x_{k+1} - z_k)
z_{k+1} = z_k + y_k - x_{k+1}
```

```python
import numpy as np

def douglas_rachford(prox_A, prox_B, z0, n_iter=100):
    """Douglas-Rachford splitting for 0 ∈ A(x) + B(x)."""
    z = z0.copy()
    for k in range(n_iter):
        x = prox_A(z)
        y = prox_B(2 * x - z)
        z = z + (y - x)
    return prox_A(z)  # return the consensus solution
```

## Peaceman-Rachford Splitting

A variant with faster convergence (but may diverge if operators are not firmly nonexpansive):

```
x_{k+1} = prox_A(z_k)
y_k = prox_B(2x_{k+1} - z_k)
z_{k+1} = 2y_k - x_k
```

## Relation to ADMM

ADMM is Douglas-Rachford splitting applied to the dual problem. The x and z updates correspond to proximal steps with respect to f and g.

## Forward-Backward Splitting

For `0 ∈ A(x) + B(x)` where A is cocoercive (single-valued) and B is monotone:

```
x_{k+1} = prox_B(x_k - γA(x_k))
```

This is precisely proximal gradient descent.

```python
# Forward-backward = proximal gradient for f smooth + g non-smooth
def forward_backward(grad_f, prox_g, x0, gamma=0.1, n_iter=100):
    x = x0.copy()
    for k in range(n_iter):
        x = prox_g(x - gamma * grad_f(x), gamma)
    return x
```

## Applications

- **Image denoising**: Total variation regularization
- **Phase retrieval**: Finding signals from magnitude measurements
- **Optimal transport**: Sinkhorn algorithm as operator splitting
- **Distributed optimization**: Network consensus

Operator splitting provides a unified framework for understanding ADMM, proximal gradient, and many other algorithms.
