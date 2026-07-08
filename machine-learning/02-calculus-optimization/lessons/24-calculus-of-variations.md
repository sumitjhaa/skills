# 24. Calculus of Variations

## Introduction

Calculus of variations extends optimization from functions to functionals — functions of functions. It is essential for understanding optimal control, physical models, and neural fields.

## Functionals

A functional `F[y]` maps a function `y` to a scalar. The classic problem:

```
F[y] = ∫ₐᵇ L(x, y(x), y'(x)) dx
```

Find `y` that minimizes `F[y]`.

## Euler-Lagrange Equation

For `F[y] = ∫L(x, y, y') dx`, a necessary condition for optimality is:

```
∂L/∂y - d/dx (∂L/∂y') = 0
```

```python
import numpy as np
from scipy.integrate import solve_bvp

# Example: Shortest path between two points
# L = sqrt(1 + y'²) → EL: y'' = 0 → straight line
def shortest_path():
    x = np.linspace(0, 1, 100)
    y = x  # straight line: y = x
    print(f"Shortest path: length = {np.sqrt(1 + 1**2):.4f}")
    return y
```

## Brachistochrone Problem

Find the curve of fastest descent under gravity:

```
L = sqrt((1 + y'²) / (2gy))
EL: y(1 + y'²) = const
```

## Multiple Functions

For `L(x, y₁, ..., yₙ, y₁', ..., yₙ')`:

```
∂L/∂yᵢ - d/dx (∂L/∂yᵢ') = 0  for i = 1, ..., n
```

## Constrained Variational Problems

Using Lagrange multipliers for functionals:

```
F[y] = ∫L dx,  constrained by ∫G dx = constant
```

Leads to the Euler-Lagrange equation for `L - λG`.

## Numerical Solution via Finite Elements

```python
def solve_euler_lagrange(EL_rhs, a, b, ya, yb, n=100):
    """Solve boundary value problem from Euler-Lagrange."""
    # EL equation is a second-order ODE: y'' = EL_rhs(x, y, y')
    # Discretize and solve via finite differences
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = np.linspace(ya, yb, n + 1)

    for iteration in range(1000):
        y_old = y.copy()
        for i in range(1, n):
            yp = (y[i+1] - y[i-1]) / (2 * h)
            ypp = (y[i+1] - 2*y[i] + y[i-1]) / h**2
            y[i] = 0.5 * (y[i+1] + y[i-1] - h**2 * EL_rhs(x[i], y[i], yp))
        if np.max(np.abs(y - y_old)) < 1e-8:
            break
    return x, y
```

## Applications in ML

- **Neural ODEs**: Continuous-depth networks as variational problems
- **Optimal transport**: Monge-Kantorovich formulation
- **Mean-field games**: Large-population multi-agent systems
- **Physics-informed neural networks**: Solving PDEs by minimizing energy functionals
