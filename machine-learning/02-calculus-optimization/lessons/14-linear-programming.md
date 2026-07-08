# 14. Linear Programming

## Introduction

Linear programming optimizes a linear objective subject to linear equality and inequality constraints. It is fundamental to operations research and appears in ML for resource allocation, adversarial robustness, and optimal transport.

## Standard Form

```
minimize    cᵀx
subject to  Ax = b
            x ≥ 0
```

where `c ∈ ℝⁿ`, `A ∈ ℝ^{m×n}`, `b ∈ ℝᵐ`.

## Simplex Method

The simplex method traverses vertices of the feasible polytope. Each vertex corresponds to a basic feasible solution (n-m variables set to zero, the rest determined by Ax = b).

```python
import numpy as np
from scipy.optimize import linprog

# minimize -3x₁ - 2x₂ subject to x₁ + x₂ ≤ 4, 2x₁ + x₂ ≤ 6, x₁, x₂ ≥ 0
c = [-3, -2]
A = [[1, 1], [2, 1]]
b = [4, 6]
bounds = [(0, None), (0, None)]

result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
print(f"Optimal: x={result.x}, f(x)={-result.fun:.4f}")
```

## Duality

Every LP has a dual problem. For the primal `min cᵀx s.t. Ax = b, x ≥ 0`, the dual is:

```
maximize    bᵀy
subject to  Aᵀy ≤ c
```

Weak duality: `bᵀy ≤ cᵀx` for all feasible primal/dual pairs.
Strong duality: At optimality, `bᵀy* = cᵀx*`.

## Interior Point Methods

IPMs follow the central path through the interior of the feasible region:

```python
# Using scipy's interior point method
result_ip = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='interior-point')
print(f"IP solution: x={result_ip.x}, f(x)={-result_ip.fun:.4f}")
```

## Applications in ML

- **Adversarial robustness**: Computing minimum adversarial perturbations
- **Optimal transport**: Earth mover's distance
- **Resource-constrained learning**: Training under budget constraints
- **Reinforcement learning**: Linear programming for MDPs
