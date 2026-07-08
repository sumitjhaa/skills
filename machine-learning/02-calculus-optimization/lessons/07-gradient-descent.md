# 07. Gradient Descent

## Introduction

Gradient descent is the foundational optimization algorithm in machine learning. It iteratively moves parameters in the direction of steepest descent of the loss function.

## Algorithm

Given a function `f: ℝⁿ → ℝ`:

```
x_{t+1} = x_t - η · ∇f(x_t)
```

where `η > 0` is the learning rate (step size).

```python
import numpy as np

def gradient_descent(f, grad_f, x0, lr=0.1, n_iter=100):
    x = x0.copy()
    trajectory = [x.copy()]
    for i in range(n_iter):
        x = x - lr * grad_f(x)
        trajectory.append(x.copy())
    return x, np.array(trajectory)

f = lambda x: x**2 + 3*x + 2
grad_f = lambda x: 2*x + 3

x_opt, traj = gradient_descent(f, grad_f, x0=np.array([10.0]), lr=0.1, n_iter=50)
print(f"Optimal x: {x_opt[0]:.6f} (exact: -1.5)")
print(f"Minimum value: {f(x_opt):.6f} (exact: {-0.25})")
```

## Learning Rate Selection

The learning rate is critical:

- **Too small**: Slow convergence
- **Too large**: Divergence or oscillation

```python
# Convergence behavior with different learning rates
for lr in [0.01, 0.1, 0.5, 1.0]:
    x_opt, traj = gradient_descent(f, grad_f, np.array([10.0]), lr=lr, n_iter=20)
    print(f"lr={lr}: final x={x_opt[0]:.4f}, f(x)={f(x_opt):.4f}, steps={len(traj)}")
```

## Gradient Descent for Linear Regression

For `f(w) = (1/2m)‖Xw - y‖²`, the gradient is:

```
∇f(w) = (1/m) Xᵀ (Xw - y)
```

```python
def linear_regression_gd(X, y, lr=0.01, n_iter=100):
    m, n = X.shape
    w = np.zeros(n)
    for i in range(n_iter):
        grad = X.T @ (X @ w - y) / m
        w = w - lr * grad
    return w
```

## Convergence Analysis

For an L-smooth, µ-strongly convex function, gradient descent converges linearly:

```
f(x_t) - f(x*) ≤ (1 - µ/L)ᵗ · [f(x₀) - f(x*)]
```

This motivates the condition number `κ = L/µ` — smaller is better.
