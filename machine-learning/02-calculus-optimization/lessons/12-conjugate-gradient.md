# 12. Conjugate Gradient Methods

## Introduction

Conjugate gradient (CG) methods solve linear systems `Ax = b` where A is symmetric positive definite, without explicitly inverting A. CG can also be adapted for nonlinear optimization.

## Conjugate Directions

A set of directions `{d₀, ..., d_{n-1}}` is A-conjugate (A-orthogonal) if:

```
dᵢᵀ A dⱼ = 0  for i ≠ j
```

Searching along conjugate directions ensures each step does not spoil previous progress.

## Linear CG Algorithm

To solve `Ax = b`:

```
r₀ = b - Ax₀
d₀ = r₀
for k = 0, ..., n-1:
    α_k = (r_kᵀ r_k) / (d_kᵀ A d_k)
    x_{k+1} = x_k + α_k d_k
    r_{k+1} = r_k - α_k A d_k
    β_k = (r_{k+1}ᵀ r_{k+1}) / (r_kᵀ r_k)
    d_{k+1} = r_{k+1} + β_k d_k
```

```python
import numpy as np

def conjugate_gradient(A, b, x0=None, max_iter=None, tol=1e-10):
    n = len(b)
    x = np.zeros(n) if x0 is None else x0.copy()
    r = b - A @ x
    d = r.copy()
    rs_old = r @ r
    iterations = min(max_iter, n) if max_iter else n

    for i in range(iterations):
        Ad = A @ d
        alpha = rs_old / (d @ Ad)
        x = x + alpha * d
        r = r - alpha * Ad
        rs_new = r @ r
        if np.sqrt(rs_new) < tol:
            break
        beta = rs_new / rs_old
        d = r + beta * d
        rs_old = rs_new
    return x, i + 1
```

## Nonlinear Conjugate Gradient

For minimizing general `f(x)`, we replace the residual with the negative gradient:

```
d₀ = -∇f(x₀)
d_{k+1} = -∇f(x_{k+1}) + β_k d_k
```

Common β choices: Fletcher-Reeves, Polak-Ribière, Hestenes-Stiefel.

```python
def nonlinear_cg(grad_f, x0, max_iter=100, tol=1e-6):
    x = x0.copy()
    g = grad_f(x)
    d = -g
    for i in range(max_iter):
        if np.linalg.norm(g) < tol:
            break
        # Line search for alpha
        alpha = 1.0
        x_new = x + alpha * d
        g_new = grad_f(x_new)
        beta = (g_new @ g_new) / (g @ g)  # Fletcher-Reeves
        d = -g_new + beta * d
        x, g = x_new, g_new
    return x
```

CG is memory-efficient (no matrix storage) and converges in at most n iterations for quadratic functions.
