# 14. Non-Negative Matrix Factorization (NMF)

## Introduction

NMF factors a non-negative matrix V ∈ ℝ₊^{m×n} into W ∈ ℝ₊^{m×k} and H ∈ ℝ₊^{k×n} such that V ≈ WH. The non-negativity constraint leads to a parts-based, interpretable representation.

## Multiplicative Update Rules

Minimizing ||V − WH||_F² with non-negativity constraints leads to multiplicative updates:

H ← H * (WᵀV) / (WᵀWH + ε)
W ← W * (VHᵀ) / (WHHᵀ + ε)

```python
import numpy as np

def nmf_multiplicative(V, k, max_iter=200):
    m, n = V.shape
    W = np.abs(np.random.randn(m, k))
    H = np.abs(np.random.randn(k, n))
    for i in range(max_iter):
        H *= (W.T @ V) / (W.T @ (W @ H) + 1e-10)
        W *= (V @ H.T) / (W @ (H @ H.T) + 1e-10)
    return W, H
```

## ALS (Alternating Least Squares)

Fix H, solve for W with non-negativity constraints (using NNLS), then fix W, solve for H:

```python
from scipy.optimize import nnls

def nmf_als(V, k, max_iter=100):
    m, n = V.shape
    W = np.abs(np.random.randn(m, k))
    H = np.abs(np.random.randn(k, n))
    for _ in range(max_iter):
        for i in range(m):
            W[i] = nnls(H.T, V[i])[0]
        for j in range(n):
            H[:, j] = nnls(W, V[:, j])[0]
    return W, H
```

## Topic Models

NMF on a term-document matrix yields topics (W columns) and document topic proportions (H columns):

```python
# V shape: (n_terms, n_docs)
# W: (n_terms, n_topics) - term distributions per topic
# H: (n_topics, n_docs) - topic proportions per document
```

## What You'll Implement

- Multiplicative update NMF
- Alternating least squares NMF
- Topic modeling on text data
- Reconstruction error tracking
- Compare with truncated SVD
- Non-negativity enforcement
