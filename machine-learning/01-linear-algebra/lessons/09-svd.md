# 09. Singular Value Decomposition (SVD)

## Introduction

Every real m×n matrix A can be decomposed as:

A = U Σ Vᵀ

Where:
- U is m×m orthogonal (left singular vectors)
- Σ is m×n diagonal (singular values σ₁ ≥ σ₂ ≥ ... ≥ σᵣ > 0)
- Vᵀ is n×n orthogonal (right singular vectors)

The SVD reveals the rank, range, nullspace, and optimal low-rank approximation of A.

## Full SVD

```python
import numpy as np
from scipy.linalg import svd

A = np.random.randn(6, 4)
U, s, Vt = svd(A, full_matrices=True)
print(f"U shape: {U.shape}, s: {s}, Vt shape: {Vt.shape}")
```

## Truncated SVD

Keep only the top k singular values:

```python
def truncated_svd(A, k):
    U, s, Vt = svd(A, full_matrices=False)
    return U[:, :k], s[:k], Vt[:k, :]
```

This is optimal for low-rank approximation (Eckart–Young theorem).

## Randomized SVD

For large matrices, the randomized SVD uses random sampling:

```python
def randomized_svd(A, k, n_oversamples=10, n_iter=2):
    m, n = A.shape
    p = min(k + n_oversamples, n)
    Omega = np.random.randn(n, p)
    Y = A @ Omega
    for _ in range(n_iter):
        Y = A @ (A.T @ Y)
    Q, _ = np.linalg.qr(Y)
    B = Q.T @ A
    Ub, s, Vt = svd(B, full_matrices=False)
    U = Q @ Ub[:, :k]
    return U, s[:k], Vt[:k, :]
```

## Applications

### PCA (Principal Component Analysis)

```python
def pca_svd(X, k):
    X_centered = X - X.mean(axis=0)
    U, s, Vt = svd(X_centered, full_matrices=False)
    components = Vt[:k]
    scores = X_centered @ components.T
    var_explained = (s[:k]**2) / (s**2).sum()
    return scores, components, var_explained
```

### Compression

```python
def compress(A, k):
    U, s, Vt = svd(A, full_matrices=False)
    return U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]
```

### Denoising

Low-rank approximation removes noise by thresholding small singular values:

```python
def denoise(A, threshold):
    U, s, Vt = svd(A, full_matrices=False)
    s_denoised = np.where(s > threshold, s, 0)
    return U @ np.diag(s_denoised) @ Vt
```

## Hard Thresholding

For low-rank matrix denoising, there are theoretically optimal thresholds based on the noise level.

## What You'll Implement

- Full SVD computation (via numpy/scipy)
- Truncated SVD
- Randomized SVD (Halko–Martinsson–Tropp algorithm)
- PCA via SVD with variance explained
- Image compression using truncated SVD
- Image denoising via singular value thresholding
- Comparison of SVD algorithms on large matrices
