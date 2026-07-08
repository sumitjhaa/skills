# 23. Matrix Completion

## Introduction

Matrix completion recovers missing entries of a low-rank matrix from partial observations. It is the mathematical foundation of recommendation systems (e.g., Netflix Prize).

## Problem Formulation

Given observed entries P_Ω(A), find X that minimizes rank(X) subject to Xᵢⱼ = Aᵢⱼ for (i,j) ∈ Ω.

Since rank minimization is NP-hard, we relax to nuclear norm:

min ||X||_*  subject to  P_Ω(X) = P_Ω(A)

## Singular Value Thresholding (SVT)

The SVT algorithm iteratively shrinks singular values and projects onto observed entries:

```python
def svt(A_obs, mask, tau, delta, max_iter=500):
    X = np.zeros_like(A_obs)
    for k in range(max_iter):
        U, s, Vt = np.linalg.svd(X, full_matrices=False)
        s = np.maximum(s - tau, 0)
        X = U @ np.diag(s) @ Vt
        X[mask] += delta * (A_obs[mask] - X[mask])
    return X
```

## Riemannian Optimization

Treat the low-rank manifold as a Riemannian manifold and use geodesic steps:

```python
def riemannian_completion(A_obs, mask, rank, max_iter=100):
    m, n = A_obs.shape
    U = np.random.randn(m, rank)
    V = np.random.randn(n, rank)
    for _ in range(max_iter):
        X = U @ V.T
        grad = np.zeros((m, n))
        grad[mask] = X[mask] - A_obs[mask]
        U -= 0.01 * grad @ V
        V -= 0.01 * grad.T @ U
    return U @ V.T
```

## What You'll Implement

- SVT algorithm from scratch
- Riemannian optimization for matrix completion
- Comparison of SVT vs Riemannian
- Phase transition analysis (fraction observed vs rank)
- Recommendation system demo (synthetic)
- Nuclear norm minimization convergence visualization
