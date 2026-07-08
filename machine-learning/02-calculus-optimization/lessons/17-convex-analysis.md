# 17. Convex Analysis

## Introduction

Convexity is the "sweet spot" of optimization — convex problems have global minima, strong duality, and efficient algorithms. Understanding convexity is essential for designing and analyzing optimization methods.

## Convex Sets

A set `C` is convex if for all `x, y ∈ C` and `θ ∈ [0, 1]`:

```
θx + (1-θ)y ∈ C
```

Examples: hyperplanes, halfspaces, norm balls, positive semidefinite cone.

## Convex Functions

A function `f` is convex if its domain is convex and for all `x, y ∈ dom(f)`, `θ ∈ [0, 1]`:

```
f(θx + (1-θ)y) ≤ θf(x) + (1-θ)f(y)
```

```python
import numpy as np

def check_convexity(f, x_range, n_points=100):
    """Check convexity via Jensen's inequality."""
    xs = np.linspace(x_range[0], x_range[1], n_points)
    for i in range(n_points - 1):
        for j in range(i + 1, n_points):
            x, y = xs[i], xs[j]
            for theta in np.linspace(0, 1, 10):
                lhs = f(theta * x + (1 - theta) * y)
                rhs = theta * f(x) + (1 - theta) * f(y)
                if lhs > rhs + 1e-10:
                    return False
    return True

f = lambda x: x**2  # convex
g = lambda x: np.sin(x)  # not convex on [-π, π]
print(f"x² convex: {check_convexity(f, [-2, 2])}")
print(f"sin(x) convex on [-π, π]: {check_convexity(g, [-np.pi, np.pi])}")
```

## First-Order Condition

For differentiable convex `f`:

```
f(y) ≥ f(x) + ∇f(x)ᵀ(y - x)  for all x, y
```

The gradient provides a global underestimator. This is the basis of gradient descent analysis.

## Second-Order Condition

For twice-differentiable `f`:

```
∇²f(x) ≽ 0  for all x ∈ dom(f)
```

## Subgradients

For non-differentiable convex functions, subgradients generalize gradients:

```
∂f(x) = {g | f(y) ≥ f(x) + gᵀ(y - x) for all y}
```

```python
# Subgradient of f(x) = |x|
def subgrad_abs(x):
    if x > 0: return np.array([1])
    if x < 0: return np.array([-1])
    return np.array([np.random.uniform(-1, 1)])  # any value in [-1, 1]

# Subgradient method for f(x) = |x|
x = 5.0
for _ in range(100):
    x -= 0.1 * subgrad_abs(x)
print(f"Subgradient method converges to: {x:.6f}")
```

## Convexity-Preserving Operations

- Non-negative weighted sums
- Composition with affine function
- Pointwise maximum
- Partial minimization
