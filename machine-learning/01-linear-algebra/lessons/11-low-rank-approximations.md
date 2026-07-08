# 11. Low-Rank Approximations and the Eckart–Young Theorem

## Introduction

The Eckart–Young theorem states that the best rank-k approximation to a matrix A in both Frobenius and spectral norms is given by the truncated SVD:

Aₖ = Uₖ Σₖ Vₖᵀ

where we keep only the k largest singular values and corresponding vectors.

## Eckart–Young Theorem

||A − Aₖ||_F = √(σₖ₊₁² + ... + σᵣ²)
||A − Aₖ||₂ = σₖ₊₁

```python
import numpy as np
from scipy.linalg import svd

A = np.random.randn(10, 8)
U, s, Vt = svd(A, full_matrices=False)
k = 3
Ak = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]

error_frob = np.linalg.norm(A - Ak, 'fro')
error_spec = np.linalg.norm(A - Ak, 2)
expected_frob = np.sqrt(np.sum(s[k:]**2))
expected_spec = s[k]
```

## Matrix Completion

Given only a subset of entries, find the lowest-rank matrix consistent with observations. The nuclear norm ||A||_* is minimized as a convex surrogate for rank:

min ||X||_*  subject to  Xᵢⱼ = Aᵢⱼ for (i,j) ∈ Ω

## Nuclear Norm Minimization

```python
def nuclear_norm_minimization(A_observed, mask, max_iter=500, tol=1e-6):
    X = np.zeros_like(A_observed)
    for _ in range(max_iter):
        U, s, Vt = svd(X, full_matrices=False)
        s = np.maximum(s - 1, 0)
        X_new = U @ np.diag(s) @ Vt
        X_new[mask] = A_observed[mask]
        if np.linalg.norm(X_new - X) < tol:
            break
        X = X_new
    return X
```

## Applications

- **Recommendation systems**: Predict missing user-item ratings
- **Image compression**: Store only top k singular values
- **Denoising**: Remove noise by truncating small singular values
- **Latent semantic analysis**: Find low-dimensional document topics

## What You'll Implement

- Truncated SVD for low-rank approximation
- Verify Eckart–Young theorem
- Nuclear norm minimization for matrix completion
- Image compression with controllable rank
- Compare approximation quality across ranks
