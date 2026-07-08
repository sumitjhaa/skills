# 06. Implicit Differentiation

## Introduction

Implicit differentiation handles functions defined implicitly by equations (e.g., `x² + y² = 1`) rather than explicitly as `y = f(x)`. It is widely used in differentiable optimization layers and implicit neural representations.

## Implicit Function Theorem

For an equation `F(x, y) = 0` where `∂F/∂y ≠ 0`, we can differentiate both sides:

```
d/dx [F(x, y(x))] = 0
∂F/∂x + (∂F/∂y)·(dy/dx) = 0
dy/dx = -(∂F/∂x) / (∂F/∂y)
```

```python
import numpy as np

F = lambda x, y: x**2 + y**2 - 1  # Circle equation

def dydx_implicit(F, x, y, h=1e-7):
    """dy/dx using implicit differentiation."""
    dF_dx = (F(x + h, y) - F(x - h, y)) / (2 * h)
    dF_dy = (F(x, y + h) - F(x, y - h)) / (2 * h)
    return -dF_dx / dF_dy

# At point (0, 1): dy/dx should be 0 (horizontal tangent)
print(f"dy/dx at (0, 1): {dydx_implicit(F, 0, 1):.6f}")

# At point (1/√2, 1/√2): dy/dx should be -1
x0 = 1/np.sqrt(2)
print(f"dy/dx at (1/√2, 1/√2): {dydx_implicit(F, x0, x0):.6f}")
```

## Multiple Variables

For `F(x₁, ..., xₙ, y) = 0`:

```
∂y/∂xᵢ = -(∂F/∂xᵢ) / (∂F/∂y)
```

## Implicit Layers in ML

Modern deep learning uses implicit differentiation to differentiate through optimization problems, ODE solvers, and fixed-point iterations without storing the entire computation graph:

```python
# Differentiate through a fixed point: z* = f(z*, θ)
# Using implicit differentiation: dz*/dθ = (I - ∂f/∂z)⁻¹ · ∂f/∂θ
```

This is the foundation of deep equilibrium models, neural ODEs, and differentiable optimization layers.
