# 26. Canonical Polyadic with Constraints

## Introduction

Adding constraints to CP decomposition improves interpretability and can capture domain knowledge. Common constraints include orthogonality, nonnegativity, and sparsity.

## Orthogonal CP

Orthogonality constraints on factors simplify interpretation and ensure uniqueness:

min ||**X** − [[A, B, C]]||²  subject to  AᵀA = I, BᵀB = I, CᵀC = I

```python
def orthogonal_cp(X, rank, max_iter=100):
    I, J, K = X.shape
    A, _ = np.linalg.qr(np.random.randn(I, rank))
    B, _ = np.linalg.qr(np.random.randn(J, rank))
    C, _ = np.linalg.qr(np.random.randn(K, rank))
    # ALS with orthogonal projections
    for _ in range(max_iter):
        A, _ = np.linalg.qr(...)
        B, _ = np.linalg.qr(...)
        C, _ = np.linalg.qr(...)
    return A, B, C
```

## Sparse CP

Sparsity (L1 regularization) encourages many factor entries to be zero:

min ||**X** − [[A, B, C]]||² + λ(||A||₁ + ||B||₁ + ||C||₁)

```python
def sparse_cp(X, rank, lam=0.1, max_iter=100):
    # ALS with soft-thresholding
    for _ in range(max_iter):
        A = soft_threshold(A_new, lam)
        B = soft_threshold(B_new, lam)
        C = soft_threshold(C_new, lam)
    return A, B, C
```

## Nonnegative CP

All factor entries are constrained to be nonnegative, producing parts-based representations (covered in lesson 25).

## Applications

- **Orthogonal CP**: Signal separation, clustering
- **Sparse CP**: Feature selection, interpretable models
- **Nonnegative CP**: Topic modeling, spectral unmixing

## What You'll Implement

- Orthogonal CP decomposition
- Sparse CP with L1 regularization
- Nonnegative CP multiplicative updates
- Comparison of constrained vs unconstrained CP
- Factor interpretability analysis
- Convergence behavior under constraints
