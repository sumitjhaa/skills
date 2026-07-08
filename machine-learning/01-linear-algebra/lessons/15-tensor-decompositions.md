# 15. Tensor Decompositions: CP, Tucker, TT, Tensor Ring

## Introduction

Tensors are multi-dimensional arrays. A third-order tensor **X** ∈ ℝ^{I×J×K} generalizes vectors (1-mode) and matrices (2-mode).

## CP Decomposition (CANDECOMP/PARAFAC)

Decomposes a tensor into a sum of rank-1 tensors:

**X** ≈ Σᵣ aᵣ ∘ bᵣ ∘ cᵣ

where ∘ denotes the outer product.

```python
import numpy as np

def cp_decomposition(X, rank, max_iter=100):
    I, J, K = X.shape
    A = np.random.randn(I, rank)
    B = np.random.randn(J, rank)
    C = np.random.randn(K, rank)
    for _ in range(max_iter):
        # Update using ALS
        A = np.linalg.lstsq(...)  # Khatri-Rao products
    return A, B, C
```

## Tucker Decomposition

**X** ≈ **G** ×₁ A ×₂ B ×₃ C

where **G** is the core tensor and A, B, C are factor matrices.

## Tensor Train (TT)

TT represents a high-order tensor as a chain of 3-way cores:

X(i₁,i₂,...,i_d) = G₁(:,i₁,:) G₂(:,i₂,:) ... G_d(:,i_d,:)

## Tensor Ring

Generalizes TT by connecting the ends of the chain into a ring.

## Tensorly Library

```python
import tensorly as tl
from tensorly.decomposition import parafac, tucker

# CP decomposition
factors = parafac(tensor, rank=10)

# Tucker decomposition
core, factors = tucker(tensor, rank=[10, 10, 10])
```

## What You'll Implement

- CP decomposition from scratch (ALS)
- Tucker decomposition
- Tensor train decomposition
- Tensor ring decomposition
- Use tensorly for comparison
- Reconstruction error analysis
