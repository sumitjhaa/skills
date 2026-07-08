# 10. Newton's Methods

## Introduction

Newton's method uses second-order (curvature) information to achieve faster convergence than first-order methods. It uses the Hessian matrix to find the minimum of a quadratic approximation.

## Newton-Raphson for Root Finding

For finding roots of `f(x) = 0`:

```
x_{t+1} = x_t - f(x_t) / f'(x_t)
```

```python
import numpy as np

def newton_root(f, fp, x0, n_iter=20):
    x = x0
    for i in range(n_iter):
        x = x - f(x) / fp(x)
    return x

f = lambda x: x**2 - 2  # sqrt(2)
fp = lambda x: 2*x
print(f"sqrt(2) ≈ {newton_root(f, fp, 1.5):.10f}")
```

## Newton's Method for Optimization

For minimizing `f(x)`, we find critical points where `∇f(x) = 0`:

```
x_{t+1} = x_t - H(x_t)⁻¹ · ∇f(x_t)
```

```python
def newton_optimize(grad_f, hess_f, x0, n_iter=20):
    x = x0.copy()
    for i in range(n_iter):
        g = grad_f(x)
        H = hess_f(x)
        x = x - np.linalg.solve(H, g)  # H⁻¹g without explicit inverse
    return x

f = lambda x: x[0]**2 + 10*x[1]**2
grad_f = lambda x: np.array([2*x[0], 20*x[1]])
hess_f = lambda x: np.array([[2, 0], [0, 20]])

x0 = np.array([5.0, 1.0])
x_opt = newton_optimize(grad_f, hess_f, x0)
print(f"Optimum: {x_opt}")
```

## Quadratic Convergence

Newton's method converges quadratically near the optimum:

```
‖x_{t+1} - x*‖ ≤ C·‖x_t - x*‖²
```

This doubles the number of correct digits at each iteration — much faster than gradient descent.

## Limitations

- Computing and inverting the Hessian is O(n³) — impractical for large n
- The Hessian must be positive definite (otherwise Newton may diverge)
- Regularized Newton (adding λI to H) helps when H is ill-conditioned

In ML, full Newton is rarely used; instead, quasi-Newton methods (BFGS, L-BFGS) approximate the Hessian.
