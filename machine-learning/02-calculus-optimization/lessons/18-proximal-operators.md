# 18. Proximal Operators

## Introduction

Proximal operators generalize projection and are the building blocks of proximal gradient methods, which handle non-smooth regularizers like L1 and nuclear norm.

## Definition

The proximal operator of a (possibly non-smooth) function `g` is:

```
prox_g(x) = argmin_u { g(u) + (1/2)‖u - x‖² }
```

## Common Proximal Operators

### L1 Norm (Soft Thresholding)

```
prox_{λ‖·‖₁}(x) = S_λ(x) = sign(x) · max(|x| - λ, 0)
```

```python
import numpy as np

def soft_threshold(x, lam):
    """Proximal operator of λ‖·‖₁."""
    return np.sign(x) * np.maximum(np.abs(x) - lam, 0)

x = np.array([1.5, -0.5, 0.3, -2.0])
lam = 1.0
print(f"Soft-thresholded: {soft_threshold(x, lam)}")
```

### L2 Norm

```
prox_{λ‖·‖}(x) = (1 - λ/‖x‖)_+ · x
```

```python
def prox_l2(x, lam):
    """Proximal operator of λ‖·‖₂."""
    norm = np.linalg.norm(x)
    if norm <= lam:
        return np.zeros_like(x)
    return (1 - lam / norm) * x
```

### Indicator Function

```
prox_{I_C}(x) = Π_C(x)  # projection onto C
```

## Proximal Gradient Descent (ISTA)

For minimizing `f(x) + g(x)` where `f` is smooth and `g` is non-smooth:

```
x_{t+1} = prox_{ηg}(x_t - η∇f(x_t))
```

```python
def proximal_gradient(f, grad_f, prox_g, x0, lr=0.1, n_iter=100):
    x = x0.copy()
    for i in range(n_iter):
        x = prox_g(x - lr * grad_f(x), lr)
    return x

# Example: L1-regularized least squares (LASSO)
# f(x) = (1/2)‖Ax - b‖², g(x) = λ‖x‖₁
A = np.random.randn(20, 50)
x_true = np.zeros(50)
x_true[:5] = np.random.randn(5)
b = A @ x_true + 0.1 * np.random.randn(20)

grad_f = lambda x: A.T @ (A @ x - b)
prox_g = lambda x, eta: soft_threshold(x, eta * 0.1)  # λ = 0.1

x_est = proximal_gradient(lambda x: 0.5 * np.linalg.norm(A @ x - b)**2,
                           grad_f, prox_g, np.zeros(50), lr=0.5, n_iter=200)
print(f"Recovery error: {np.linalg.norm(x_est - x_true):.4f}")
```

## FISTA: Fast ISTA

FISTA adds Nesterov momentum to proximal gradient, achieving O(1/k²) convergence instead of O(1/k).
