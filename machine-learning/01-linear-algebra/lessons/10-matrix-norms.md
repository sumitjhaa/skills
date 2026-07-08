# 10. Matrix Norms: Frobenius, Spectral, Nuclear, Induced

## Introduction

Matrix norms measure the "size" of a matrix. They are essential for understanding convergence, stability, and conditioning.

## Frobenius Norm

||A||_F = √(Σᵢⱼ aᵢⱼ²) = √(tr(AᵀA))

```python
import numpy as np
A = np.random.randn(5, 5)
frob = np.sqrt(np.sum(A**2))
frob_np = np.linalg.norm(A, 'fro')
```

The Frobenius norm is the ℓ₂ norm of the vectorized matrix. It is submultiplicative: ||AB||_F ≤ ||A||_F ||B||_F.

## Spectral Norm (ℓ₂ induced norm)

||A||₂ = σₘₐₓ(A) = max singular value

```python
spectral = np.linalg.norm(A, 2)
# Equivalent to largest singular value
_, s, _ = np.linalg.svd(A)
spectral_svd = s[0]
```

The spectral norm measures the maximum amplification of a vector's length.

## Nuclear Norm (Trace Norm)

||A||_* = Σᵢ σᵢ(A) = sum of singular values

```python
nuclear = np.linalg.norm(A, 'nuc')
```

The nuclear norm is the tightest convex relaxation of the rank function, making it useful for matrix completion.

## Induced p-norms

||A||ₚ = sup_{||x||ₚ=1} ||Ax||ₚ

```python
def induced_norm(A, p):
    from scipy.linalg import norm
    return norm(A, p)
```

Common induced norms:
- ||A||₁ = max column sum
- ||A||_∞ = max row sum
- ||A||₂ = spectral norm

## Relationships

- ||A||₂ ≤ ||A||_F ≤ √(r) ||A||₂ (where r = rank)
- ||A||_* ≥ ||A||_F ≥ ||A||₂
- For rank-1: ||A||_F = ||A||_* = ||A||₂

```python
A = np.array([[1, 0], [0, 0]])
frob = np.linalg.norm(A, 'fro')
spec = np.linalg.norm(A, 2)
nuc = np.linalg.norm(A, 'nuc')
print(f"Rank-1: frob={frob:.2f}, spec={spec:.2f}, nuc={nuc:.2f}")
```

## What You'll Implement

- Frobenius norm from scratch
- Spectral norm via SVD
- Nuclear norm via SVD
- Induced 1-norm and ∞-norm
- Verify norm inequalities and relationships
- Visualize norm relationships for random matrices
