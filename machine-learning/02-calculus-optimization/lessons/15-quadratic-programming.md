# 15. Quadratic Programming

## Introduction

Quadratic programming (QP) minimizes a quadratic objective subject to linear constraints. It is the core optimization problem for support vector machines, portfolio optimization, and model predictive control.

## Standard Form

```
minimize    (1/2) xᵀQx + cᵀx
subject to  Ax ≤ b
            Aₑq x = bₑq
```

where `Q` is symmetric positive semidefinite (convex QP) or indefinite (non-convex QP).

## Convex QP

When `Q ≽ 0`, the problem is convex and has a unique global minimum.

```python
import numpy as np
from scipy.optimize import minimize

# minimize (x₁ - 1)² + (x₂ - 2)² = xᵀQx/2 + cᵀx
# where Q = 2I, c = [-2, -4]
Q = np.array([[2, 0], [0, 2]])
c = np.array([-2, -4])

def qp_objective(x):
    return 0.5 * x @ Q @ x + c @ x

constraints = [
    {'type': 'ineq', 'fun': lambda x: 1 - x[0] - x[1]},  # x₁ + x₂ ≤ 1
    {'type': 'ineq', 'fun': lambda x: x[0]},               # x₁ ≥ 0
    {'type': 'ineq', 'fun': lambda x: x[1]},               # x₂ ≥ 0
]

result = minimize(qp_objective, x0=[0, 0], constraints=constraints)
print(f"Optimal: x={result.x}, f(x)={result.fun:.6f}")
```

## Active Set Methods

Active set methods maintain a set of constraints that are tight (active) at the current iterate. They solve equality-constrained QP subproblems and adjust the active set:

```python
# Conceptual active set iteration:
# 1. Solve equality-constrained QP with current active set
# 2. Check if multipliers for active inequalities are non-negative
# 3. Remove constraints with negative multipliers
# 4. Add violated constraints to active set
```

## Support Vector Machines

The SVM dual is a convex QP:

```
maximize    Σᵢ αᵢ - ½ Σᵢ Σⱼ αᵢ αⱼ yᵢ yⱼ K(xᵢ, xⱼ)
subject to  0 ≤ αᵢ ≤ C
            Σᵢ αᵢ yᵢ = 0
```

## Sequential Quadratic Programming

SQP solves general nonlinear constrained problems by approximating them as QP subproblems:

```python
from scipy.optimize import minimize
# SLSQP is the default method for constrained problems
result = minimize(lambda x: (x[0]-1)**2 + (x[1]-2)**2,
                  x0=[0, 0],
                  method='SLSQP',
                  constraints={'type': 'eq', 'fun': lambda x: x[0] + x[1] - 1})
```
