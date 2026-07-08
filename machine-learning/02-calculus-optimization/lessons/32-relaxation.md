# 32. Relaxation Techniques

## Introduction

Relaxation replaces a hard problem with an easier (relaxed) variant whose solution approximates the original. This is essential for combinatorial optimization, integer programming, and non-convex problems.

## Lagrangian Relaxation

Replace hard constraints with penalty terms in the objective:

```
Primal:  min f(x)  s.t.  g(x) = 0
Relaxed: min f(x) + λᵀ g(x)
```

The Lagrangian dual provides a lower bound:

```
d(λ) = min_x L(x, λ) ≤ f(x*)
```

```python
import numpy as np
from scipy.optimize import minimize

# Example: Integer programming via LP relaxation
# min cᵀx s.t. Ax ≤ b, x ∈ {0, 1}ⁿ
# Relax to: min cᵀx s.t. Ax ≤ b, 0 ≤ x ≤ 1
c = np.array([-3, -2])
A = np.array([[1, 1], [2, 1]])
b = np.array([4, 6])

# LP relaxation (ignoring integrality)
result = minimize(lambda x: c @ x, x0=[0, 0],
                  bounds=[(0, 1), (0, 1)],
                  constraints={'type': 'ineq', 'fun': lambda x: b - A @ x})
print(f"Relaxed solution: x={result.x}, objective={result.fun:.4f}")
```

## Convex Relaxation

Replace a non-convex constraint with its convex hull:

### L0 → L1 Relaxation
The L0 "norm" (cardinality) is non-convex. The L1 norm is its tightest convex relaxation.

```python
# Sparse recovery: L0 problem (NP-hard) relaxed to L1 (convex)
# L1-regularized least squares (LASSO)
from scipy.optimize import minimize

A = np.random.randn(20, 50)
x_true = np.zeros(50); x_true[:5] = np.random.randn(5)
b = A @ x_true + 0.05 * np.random.randn(20)

lasso_obj = lambda x: 0.5 * np.linalg.norm(A @ x - b)**2 + 0.1 * np.linalg.norm(x, 1)
x_lasso = minimize(lasso_obj, np.zeros(50), method='L-BFGS-B').x
print(f"Non-zero recovered: {np.sum(np.abs(x_lasso) > 1e-3)}")
```

### Semidefinite Relaxation

For max-cut, the integer constraint `yᵢ ∈ {-1, 1}` is relaxed to `X ≽ 0, Xᵢᵢ = 1`.

```python
# Max-cut SDP relaxation (Goemans-Williamson)
# maximize (1/4) Σᵢⱼ Wᵢⱼ (1 - Xᵢⱼ)
# subject to X ≽ 0, Xᵢᵢ = 1
```

## Randomized Rounding

Convert relaxed solutions to feasible integer solutions:

```python
def randomized_rounding(X):
    """Round SDP solution to ±1 cut assignment."""
    n = X.shape[0]
    L = np.linalg.cholesky(X + 1e-8 * np.eye(n))
    r = np.random.randn(n)
    y = np.sign(L @ r)
    return y
```

## Applications

- **Semantic segmentation**: CRF inference via LP relaxation
- **Graph matching**: Relax permutation matrix to doubly stochastic
- **Community detection**: Modularity maximization via spectral relaxation
- **Neural network verification**: Relax ReLU networks for verification

Relaxation provides tractable approximations with provable guarantees, bridging combinatorial optimization and continuous methods.
