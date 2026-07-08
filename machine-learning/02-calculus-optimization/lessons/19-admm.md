# 19. Alternating Direction Method of Multipliers (ADMM)

## Introduction

ADMM combines the decomposability of dual ascent with the robust convergence of the method of multipliers. It solves problems of the form `f(x) + g(z)` subject to linear equality constraints.

## Problem Formulation

```
minimize    f(x) + g(z)
subject to  Ax + Bz = c
```

## Augmented Lagrangian

```
L_ρ(x, z, y) = f(x) + g(z) + yᵀ(Ax + Bz - c) + (ρ/2)‖Ax + Bz - c‖²
```

## ADMM Updates

```
x^{k+1} = argmin_x L_ρ(x, z^k, y^k)
z^{k+1} = argmin_z L_ρ(x^{k+1}, z, y^k)
y^{k+1} = y^k + ρ(Ax^{k+1} + Bz^{k+1} - c)
```

```python
import numpy as np

def admm_lasso(A, b, lam=0.1, rho=1.0, max_iter=100):
    """ADMM for LASSO: minimize (1/2)‖Ax - b‖² + λ‖x‖₁."""
    m, n = A.shape
    x = np.zeros(n)
    z = np.zeros(n)
    u = np.zeros(n)  # scaled dual variable

    AtA = A.T @ A
    Atb = A.T @ b

    for k in range(max_iter):
        # x update: (AᵀA + ρI)x = Aᵀb + ρ(z - u)
        x = np.linalg.solve(AtA + rho * np.eye(n), Atb + rho * (z - u))

        # z update: soft thresholding
        z = np.sign(x + u) * np.maximum(np.abs(x + u) - lam / rho, 0)

        # dual update
        u = u + (x - z)

        # Check residuals
        r_norm = np.linalg.norm(x - z)
        s_norm = np.linalg.norm(-rho * (z - z_prev)) if k > 0 else 0

    return z
```

## Convergence and Stopping Criteria

ADMM converges to optimality under modest conditions (convex f, g, existence of saddle point). Primal and dual residuals:

```
r_p = Ax + Bz - c      (primal residual)
r_d = ρAᵀB(z - z_prev)  (dual residual)
```

## Applications

- **LASSO and sparse coding**
- **Matrix completion**: `minimize ‖X‖_* + (1/2)‖P_Ω(X - M)‖²`
- **Graphical lasso**: Sparse inverse covariance estimation
- **Consensus optimization**: Distributed averaging
- **Bilinear problems**: Low-rank matrix factorization

```python
# Application: Distributed consensus ADMM
# N agents with local costs f_i, sharing a common variable
# x_i^{k+1} = prox_{f_i}(z^k - u_i^k)
# z^{k+1} = (1/N) Σ_i (x_i^{k+1} + u_i^k)
# u_i^{k+1} = u_i^k + x_i^{k+1} - z^{k+1}
```

ADMM is the workhorse for many large-scale distributed optimization problems in ML.
