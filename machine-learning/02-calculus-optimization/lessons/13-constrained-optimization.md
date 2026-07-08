# 13. Constrained Optimization

## Introduction

Real-world optimization often has constraints: budget limits, resource constraints, physical laws. Constrained optimization finds minima subject to equality and inequality constraints.

## Problem Formulation

```
minimize    f(x)
subject to  gᵢ(x) = 0,  i = 1, ..., m
            hⱼ(x) ≤ 0,  j = 1, ..., p
```

## Lagrange Multipliers

For equality-constrained problems, the Lagrangian is:

```
L(x, λ) = f(x) + Σᵢ λᵢ gᵢ(x)
```

At the optimum: ∇ₓL = 0 and ∇_λL = 0 (stationarity + feasibility).

```python
import numpy as np
from scipy.optimize import minimize

# Example: minimize x² + y² subject to x + y = 1
f = lambda x: x[0]**2 + x[1]**2
cons = {'type': 'eq', 'fun': lambda x: x[0] + x[1] - 1}

result = minimize(f, x0=[0, 0], constraints=cons)
print(f"Optimal: x={result.x}, f(x)={result.fun:.6f}")
```

## KKT Conditions

For inequality constraints, Karush-Kuhn-Tucker conditions:

1. **Stationarity**: ∇f(x*) + Σλᵢ∇gᵢ(x*) + Σμⱼ∇hⱼ(x*) = 0
2. **Primal feasibility**: gᵢ(x*) = 0, hⱼ(x*) ≤ 0
3. **Dual feasibility**: μⱼ ≥ 0
4. **Complementary slackness**: μⱼ hⱼ(x*) = 0

```python
# Example: minimize (x-1)² + (y-2)² subject to x + y ≤ 1, x ≥ 0, y ≥ 0
f = lambda x: (x[0] - 1)**2 + (x[1] - 2)**2
constraints = [
    {'type': 'ineq', 'fun': lambda x: 1 - x[0] - x[1]},  # x + y ≤ 1
    {'type': 'ineq', 'fun': lambda x: x[0]},
    {'type': 'ineq', 'fun': lambda x: x[1]},
]
result = minimize(f, x0=[0, 0], constraints=constraints)
print(f"Optimal: x={result.x}, f(x)={result.fun:.6f}")
```

## Interior Point Methods

IPMs solve constrained problems by adding a barrier function:

```
minimize f(x) - μ Σⱼ log(-hⱼ(x))
```

As μ → 0, the solution approaches the constrained optimum.

## Applications

- Support vector machines (quadratic programming with constraints)
- Resource allocation
- Portfolio optimization
- Optimal transport
