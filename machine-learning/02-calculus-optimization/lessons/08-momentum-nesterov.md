# 08. Momentum & Nesterov Accelerated Gradient

## Introduction

Standard gradient descent can be slow in ravines where the surface curves steeply in one direction. Momentum methods accelerate convergence by accumulating a velocity vector.

## Momentum

The momentum update mimics physical inertia:

```
v_{t+1} = β·v_t + ∇f(x_t)
x_{t+1} = x_t - η·v_{t+1}
```

where `β ∈ [0, 1)` is the momentum coefficient (typically 0.9).

```python
import numpy as np

def momentum_gd(grad_f, x0, lr=0.01, beta=0.9, n_iter=100):
    x = x0.copy()
    v = np.zeros_like(x)
    for i in range(n_iter):
        v = beta * v + grad_f(x)
        x = x - lr * v
    return x
```

Momentum dampens oscillations in high-curvature directions and accelerates movement in low-curvature directions.

## Nesterov Accelerated Gradient (NAG)

NAG computes the gradient at a lookahead position:

```
v_{t+1} = β·v_t + ∇f(x_t - η·β·v_t)
x_{t+1} = x_t - η·v_{t+1}
```

```python
def nesterov_gd(grad_f, x0, lr=0.01, beta=0.9, n_iter=100):
    x = x0.copy()
    v = np.zeros_like(x)
    for i in range(n_iter):
        lookahead = x - lr * beta * v
        v = beta * v + grad_f(lookahead)
        x = x - lr * v
    return x
```

NAG achieves a convergence rate of O(1/t²) for convex functions, improving on standard momentum's O(1/t).

## Comparison

```python
rosenbrock = lambda x: (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

def grad_rosenbrock(x):
    dx = -2*(1 - x[0]) - 400*x[0]*(x[1] - x[0]**2)
    dy = 200*(x[1] - x[0]**2)
    return np.array([dx, dy])

x0 = np.array([-1.5, 1.5])
# Compare standard GD, momentum, and NAG
```

For convex quadratic functions, Nesterov's method achieves the optimal convergence rate among first-order methods.
