# 16. Semidefinite Programming

## Introduction

Semidefinite programming (SDP) optimizes a linear objective subject to linear matrix inequality (LMI) constraints. It generalizes linear and quadratic programming and is central to control theory, combinatorial optimization, and kernel methods.

## Standard Form

```
minimize    C · X
subject to  Aᵢ · X = bᵢ,  i = 1, ..., m
            X ≽ 0
```

where `C · X = trace(CᵀX) = Σᵢⱼ Cᵢⱼ Xᵢⱼ` is the Frobenius inner product, and `X ≽ 0` means X is positive semidefinite.

## Example: Minimum Eigenvalue Problem

```python
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import minimize

# Find minimum eigenvalue of a matrix via SDP
A = np.array([[3, 1], [1, 2]])

# min λ such that A - λI ≽ 0
# Equivalent to: max t such that A - tI ≽ 0
# Check via eigenvalues directly
eigvals = eigh(A, eigvals_only=True)
print(f"Minimum eigenvalue: {eigvals[0]:.6f}")
```

## SDP for Max-Cut

The Max-Cut SDP relaxation finds a provably good approximation:

```
maximize    ¼ Σᵢⱼ Wᵢⱼ (1 - Xᵢⱼ)
subject to   Xᵢᵢ = 1
             X ≽ 0
```

The optimal value of this SDP upper-bounds the true Max-Cut value (Goemans-Williamson guarantee: ≥ 0.878 approximation ratio).

## Applications in ML

- **Kernel learning**: Finding the optimal kernel matrix
- **Metric learning**: Learning Mahalanobis distance matrices
- **Dimensionality reduction**: Maximum variance unfolding
- **Robust optimization**: Worst-case performance bounds

```python
# Example: SDP for sensor network localization
# Given noisy distances between nearby sensors and some anchors
# Find sensor positions that satisfy distance constraints
```

## Solving SDPs

While CVXOPT and MOSEK provide robust SDP solvers, for small problems we can formulate SDPs using eigendecomposition. The constraint `X ≽ 0` is equivalent to all eigenvalues of X being non-negative.
