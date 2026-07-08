# Lesson 05.22: t-SNE / UMAP / LargeVis

## Learning Objectives
- Understand non-linear dimensionality reduction for visualization
- Derive t-SNE gradient and crowding problem solution
- Compare UMAP's fuzzy topological approach
- Analyze tradeoffs in preserving local vs global structure

## t-SNE (t-distributed Stochastic Neighbor Embedding)

### Stochastic Neighbor Embedding (SNE)
High-dimensional similarities (Gaussian):

$$P_{j|i} = \frac{\exp(-\|x_i - x_j\|^2 / 2\sigma_i^2)}{\sum_{k \neq i} \exp(-\|x_i - x_k\|^2 / 2\sigma_i^2)}$$

Low-dimensional similarities (Gaussian in SNE):

$$Q_{j|i} = \frac{\exp(-\|y_i - y_j\|^2)}{\sum_{k \neq i} \exp(-\|y_i - y_k\|^2)}$$

Minimize: $C = \sum_i \sum_j P_{j|i} \log \frac{P_{j|i}}{Q_{j|i}}$

### Key t-SNE Innovations

**Symmetric SNE**: Use joint probabilities $P_{ij} = \frac{P_{i|j} + P_{j|i}}{2n}$, simplifying gradient:

$$\frac{\partial C}{\partial y_i} = 4 \sum_j (P_{ij} - Q_{ij})(y_i - y_j)$$

**Heavy-tailed Student-t distribution** (df=1, Cauchy) in low-D:

$$Q_{ij} = \frac{(1 + \|y_i - y_j\|^2)^{-1}}{\sum_{k \neq l} (1 + \|y_k - y_l\|^2)^{-1}}$$

This solves the **crowding problem**: moderate distances in high-D can't be faithfully represented in low-D. The Cauchy distribution has heavier tails, pushing moderately distant points farther apart in low-D.

**Perplexity-based $\sigma_i$**: Binary search for $\sigma_i$ such that each point has targeted perplexity (typically 5-50):

$$\text{Perp}(P_i) = 2^{H(P_i)}, \quad H(P_i) = -\sum_j P_{j|i} \log_2 P_{j|i}$$

### t-SNE Gradient
$$\frac{\partial C}{\partial y_i} = 4 \sum_j (P_{ij} - Q_{ij})(y_i - y_j)(1 + \|y_i - y_j\|^2)^{-1}$$

Interpretation: attractive force ($P_{ij} > Q_{ij}$) pulls points together, repulsive force ($P_{ij} < Q_{ij}$) pushes them apart.

## UMAP (Uniform Manifold Approximation and Projection)

### Key Differences from t-SNE
1. **Graph-based**: Build weighted $k$-NN graph from high-D data
2. **Fuzzy simplicial sets**: Apply normalized Laplacian $L = D^{-1/2}(D-A)D^{-1/2}$ for spectral initialization
3. **Cross-entropy optimization**: Optimize cross-entropy of fuzzy set membership
4. **Global structure**: Better preserved than t-SNE due to spectral initialization

### Mathematical Formulation
High-D: $\phi(i,j) = \exp\left(-\frac{\max(0, d_{ij} - \rho_i)}{\sigma_i}\right)$
Low-D: $\psi(i,j) = \frac{1}{1 + a\|y_i - y_j\|^{2b}}$

Minimize: $\sum_{i,j} \phi_{ij} \log \frac{\phi_{ij}}{\psi_{ij}} + (1-\phi_{ij}) \log \frac{1-\phi_{ij}}{1-\psi_{ij}}$

### Parameters
- `n_neighbors`: Controls local vs global balance (small = local, large = global)
- `min_dist`: Minimum distance between embedded points (small = tighter clusters)
- `n_components`: Target dimension (default 2)

## LargeVis
- Approximate k-NN graph via random projection trees (fast)
- Negative sampling for optimization (scalable)
- Linear-time inference $O(n)$ after graph construction
- Hybrid: t-SNE-like objective with efficient graph-based optimization

## Comparison

| Method | Complexity | Memory | Global Structure | Local Detail | Parameters |
|--------|-----------|--------|-----------------|--------------|------------|
| t-SNE (Barnes-Hut) | $O(n \log n)$ | $O(n)$ | Poor | Excellent | perplexity |
| UMAP | $O(n \log n)$ | $O(n)$ | Good | Good | n_neighbors, min_dist |
| LargeVis | $O(n)$ | $O(n)$ | Moderate | Good | neg_samples |

## Code: t-SNE-like Gradient Computation

```python
import numpy as np
from scipy.spatial.distance import pdist, squareform

def tsne_grad(Y, P, alpha=1.0):
    """Compute t-SNE gradient"""
    n = Y.shape[0]
    dists = squareform(pdist(Y))
    Q = 1.0 / (1.0 + dists**2)
    np.fill_diagonal(Q, 0)
    Q /= np.sum(Q)
    PQ = P - Q
    grad = np.zeros_like(Y)
    for i in range(n):
        diff = Y[i] - Y
        grad[i] = 4 * np.sum((PQ[i, :, None] * diff).T * (1.0 / (1.0 + dists[i, :]**2))[:, None], axis=0)
    return grad
```

## Practical Considerations
- **Non-determinism**: t-SNE/UMAP give different results each run (different random seed)
- **Perplexity selection**: Try several values (5, 30, 50) — no single correct value
- **Dimensionality reduction first**: Apply PCA to $d \leq 50$ before t-SNE for speed and noise reduction
- **t-SNE vs UMAP**: t-SNE for local structure emphasis, UMAP for better global structure
- **Distance preservation**: Neither preserves distances — only neighborhood structure
- **Cluster interpretation**: Cluster size in t-SNE is not meaningful (density is distorted)
- **Large datasets**: UMAP scales better ($O(n \log n)$ vs Barnes-Hut t-SNE)

## Interpretability Guidelines
1. t-SNE preserves local neighborhoods (nearby points stay nearby)
2. t-SNE does NOT preserve cluster sizes or distances between clusters
3. Random noise can produce apparent clusters — always run multiple times
4. UMAP better at preserving global topology than t-SNE
5. Both are primarily visualization tools, not for feature extraction

## References
- van der Maaten & Hinton, "Visualizing Data using t-SNE" (JMLR, 2008)
- van der Maaten, "Accelerating t-SNE using Tree-Based Algorithms" (JMLR, 2014)
- McInnes, Healy, Melville, "UMAP: Uniform Manifold Approximation and Projection" (JOSS, 2018)
- Tang et al., "LargeVis: Visualizing Large-scale and High-dimensional Data" (WWW, 2016)
- Wattenberg, Viégas, Johnson, "How to Use t-SNE Effectively" (Distill, 2016)
