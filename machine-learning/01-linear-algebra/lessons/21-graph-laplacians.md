# 21. Graph Laplacians: Normalized, Unnormalized, Random Walk

## Introduction

The graph Laplacian captures the structure of a graph and is the foundation of spectral clustering, graph partitioning, and manifold learning.

## Unnormalized Laplacian

L = D − A

where D is the degree matrix and A is the adjacency matrix.

```python
import numpy as np

def laplacian(A):
    D = np.diag(A.sum(axis=1))
    return D - A
```

Properties:
- L is symmetric positive semidefinite
- L has eigenvalues 0 = λ₁ ≤ λ₂ ≤ ... ≤ λₙ
- The multiplicity of the zero eigenvalue equals the number of connected components

## Normalized Laplacian

Two common normalizations:

L_sym = D^{-1/2} L D^{-1/2} (symmetric normalized)
L_rw = D^{-1} L (random walk normalized)

```python
def normalized_laplacian(A):
    D_inv_sqrt = np.diag(1 / np.sqrt(A.sum(axis=1)))
    L = np.diag(A.sum(axis=1)) - A
    return D_inv_sqrt @ L @ D_inv_sqrt
```

## Spectral Clustering

1. Compute the graph Laplacian
2. Find the k smallest eigenvectors
3. Cluster the rows using k-means

```python
from sklearn.cluster import KMeans

def spectral_clustering(A, k):
    L = normalized_laplacian(A)
    eigvals, eigvecs = np.linalg.eigh(L)
    X = eigvecs[:, :k]
    return KMeans(n_clusters=k).fit(X).labels_
```

## Cheeger Inequality

The Cheeger constant h_G measures the quality of the best partition:

λ₂/2 ≤ h_G ≤ √(2λ₂)

This connects the second eigenvalue to graph partitioning.

## What You'll Implement

- Unnormalized, normalized, and random walk Laplacians
- Spectral clustering algorithm
- Cheeger inequality verification
- Eigenvalue visualization for connected components
- Compare clustering quality vs k-means on raw data
