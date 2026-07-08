# 05. The Hessian Matrix

## Introduction

The Hessian captures second-order information about a function — its curvature. This is essential for understanding convexity, saddle points, and second-order optimization methods.

## Definition

For a scalar-valued function `f: ℝⁿ → ℝ`, the Hessian H(f) is an n×n matrix of second partial derivatives:

```
H(f) = ∇²f = 
[ ∂²f/∂x₁²    ∂²f/∂x₁∂x₂  ...  ∂²f/∂x₁∂xₙ ]
[ ∂²f/∂x₂∂x₁  ∂²f/∂x₂²    ...  ∂²f/∂x₂∂xₙ ]
[   ...          ...       ...     ...       ]
[ ∂²f/∂xₙ∂x₁  ∂²f/∂xₙ∂x₂  ...  ∂²f/∂xₙ²   ]
```

For functions with continuous second partials (C²), the Hessian is symmetric (Clairaut's theorem): ∂²f/∂xᵢ∂xⱼ = ∂²f/∂xⱼ∂xᵢ.

## Computing the Hessian

```python
import numpy as np

def hessian(f, x, h=1e-5):
    """Compute Hessian using central differences."""
    n = len(x)
    H = np.zeros((n, n))
    f0 = f(x)
    for i in range(n):
        for j in range(n):
            x_pp = x.copy(); x_pp[i] += h; x_pp[j] += h
            x_pm = x.copy(); x_pm[i] += h; x_pm[j] -= h
            x_mp = x.copy(); x_mp[i] -= h; x_mp[j] += h
            x_mm = x.copy(); x_mm[i] -= h; x_mm[j] -= h
            H[i, j] = (f(x_pp) - f(x_pm) - f(x_mp) + f(x_mm)) / (4 * h**2)
    return H

f = lambda x: x[0]**2 + 3*x[1]**2 + 2*x[0]*x[1]
x = np.array([1.0, 2.0])
H = hessian(f, x)
print(f"Hessian:\n{H}")
```

## Convexity Test

A function is convex if its Hessian is positive semidefinite (all eigenvalues ≥ 0) everywhere:

```python
eigvals = np.linalg.eigvalsh(H)
print(f"Eigenvalues: {eigvals}")
print(f"Convex: {np.all(eigvals >= -1e-10)}")
```

## Hessian in Optimization

- At a local minimum: ∇f = 0, H ≻ 0 (positive definite)
- At a local maximum: ∇f = 0, H ≺ 0 (negative definite)
- At a saddle point: ∇f = 0, H has both positive and negative eigenvalues

The condition number of the Hessian (ratio of largest to smallest eigenvalue) determines how ill-conditioned the optimization problem is — this is why second-order methods can help.
