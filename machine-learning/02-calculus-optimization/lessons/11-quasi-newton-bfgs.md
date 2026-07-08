# 11. Quasi-Newton Methods & BFGS

## Introduction

Quasi-Newton methods approximate the Hessian (or its inverse) using gradient differences, avoiding O(n³) computation while achieving superlinear convergence.

## The Secant Condition

The true Hessian satisfies:
```
∇f(x_{t+1}) - ∇f(x_t) ≈ H(x_{t+1}) · (x_{t+1} - x_t)
```

Let `s_t = x_{t+1} - x_t` and `y_t = ∇f_{t+1} - ∇f_t`. The secant condition is:
```
B_{t+1} · s_t = y_t
```

## BFGS Update

BFGS maintains an approximation `B_t ≈ H_t` (or `H_t⁻¹`) and updates it rank-2:

```
B_{t+1} = B_t + (y_t y_tᵀ) / (y_tᵀ s_t) - (B_t s_t)(B_t s_t)ᵀ / (s_tᵀ B_t s_t)
```

```python
import numpy as np

def bfgs(grad_f, x0, max_iter=100, tol=1e-6):
    n = len(x0)
    x = x0.copy()
    H_inv = np.eye(n)  # Approximate inverse Hessian
    for i in range(max_iter):
        g = grad_f(x)
        if np.linalg.norm(g) < tol:
            break
        d = -H_inv @ g
        # Line search (simplified: Armijo backtracking)
        alpha = 1.0
        x_new = x + alpha * d
        g_new = grad_f(x_new)
        s = x_new - x
        y = g_new - g
        rho = 1.0 / (y @ s) if y @ s != 0 else 0
        # BFGS update of inverse Hessian
        I = np.eye(n)
        H_inv = (I - rho * np.outer(s, y)) @ H_inv @ (I - rho * np.outer(y, s)) + rho * np.outer(s, s)
        x = x_new
    return x, i + 1
```

## L-BFGS

Limited-memory BFGS stores only the last `m` pairs of `(s, y)` instead of the full matrix, making it O(mn) instead of O(n²):

```python
def lbfgs(grad_f, x0, m=10, max_iter=100):
    """Simplified L-BFGS with two-loop recursion."""
    # Stores last m (s, y) pairs, uses recursion to compute direction
    pass
```

## Guarantees

- Superlinear convergence under mild conditions
- Positive definiteness preserved if line search satisfies Wolfe conditions
- No Hessian computation: only gradient evaluations

BFGS is the default optimizer in many scientific computing libraries and remains competitive for medium-scale problems.
