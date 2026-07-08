# Lesson 05.23: Isomap / LLE / Laplacian Eigenmaps

## Learning Objectives
- Understand manifold assumption in dimensionality reduction
- Implement Isomap with geodesic distances
- Derive locally linear embedding optimization
- Apply Laplacian eigenmaps for spectral embedding

## Isomap (Isometric Mapping)
Preserves global geometric structure via geodesic distances:

1. **Build neighborhood graph**: Connect each point to its $k$ nearest neighbors (or $\varepsilon$-ball)
2. **Compute geodesic distances**: Shortest paths via Floyd-Warshall ($O(n^3)$) or Dijkstra ($O(kn \log n)$)
3. **Multidimensional scaling (MDS)**: Apply MDS to geodesic distance matrix $D_G$
   - Double-center: $B = -\frac12 J D_G^2 J$ where $J = I - \frac{1}{n}\mathbf{1}\mathbf{1}^\top$
   - Eigendecompose $B$, take top $d'$ eigenvectors

**Key insight**: Geodesic distances along the manifold approximate Euclidean distances in the intrinsic coordinates.

**Complexity**: $O(n^3)$ (eigendecomposition of doubly-centered $D_G$) — use landmarks for scaling.

## LLE (Locally Linear Embedding)
Preserves local geometric structure:

1. **Find neighbors**: For each $x_i$, find $k$ nearest neighbors
2. **Compute reconstruction weights**: Minimize

   $$\min_W \sum_{i=1}^n \left\| x_i - \sum_{j=1}^k W_{ij} x_{n_j(i)} \right\|_2^2$$

   s.t. $\sum_j W_{ij} = 1$ (translation invariance), $W_{ij} = 0$ if $j$ not neighbor of $i$

   **Closed form**: For each $i$, solve $G_i w_i = \mathbf{1}$ where $G_i[j,l] = (x_i - x_{n_j(i)})^\top (x_i - x_{n_l(i)})$, then normalize $w_i = w_i / \sum w_i$

3. **Compute embedding**: Find $Y \in \mathbb{R}^{n \times d'}$ minimizing

   $$\min_Y \sum_{i=1}^n \left\| y_i - \sum_{j=1}^k W_{ij} y_{n_j(i)} \right\|_2^2$$

   s.t. $Y^\top Y = I$ and $\sum_i y_i = 0$

   Solution: eigenvectors of $M = (I-W)^\top (I-W)$ with smallest non-zero eigenvalues (ignore the zero eigenvalue with eigenvector $\mathbf{1}$).

## Laplacian Eigenmaps
Preserves local relationships via spectral graph theory:

1. **Build similarity graph**: $W_{ij} = \exp(-\|x_i - x_j\|^2 / t)$ or 1 for k-NN adjacency
2. **Compute Laplacian**: $L = D - W$ (or normalized $L_{\text{sym}} = I - D^{-1/2} W D^{-1/2}$)
3. **Solve generalized eigenvalue problem**: $L y = \lambda D y$
4. **Embedding**: Eigenvectors with smallest non-zero eigenvalues (ordered by $\lambda_1 \leq \lambda_2 \leq \dots$)

**Connection to spectral clustering**: Same eigenvectors, but Laplacian Eigenmaps uses them directly as coordinates (spectral clustering applies k-means).

## Comparison

| Method | Type | Preserves | Complexity | Key parameter |
|--------|------|-----------|------------|---------------|
| Isomap | Global | Geodesic distances | $O(n^3)$ | $k$ (neighbors) |
| LLE | Local | Linear patches | $O(n^3)$ | $k$ (neighbors) |
| Laplacian Eigenmaps | Local | Graph adjacency | $O(n^3)$ | $k$ or $t$ |
| Hessian LLE | Local | Local isometry | $O(n^3)$ | $k$ |

## Code: LLE from Scratch

```python
import numpy as np
from scipy.spatial import KDTree
from scipy.linalg import eigh

def lle(X, n_components=2, k=12):
    n, d = X.shape
    tree = KDTree(X)
    W = np.zeros((n, n))
    for i in range(n):
        idx = tree.query(X[i], k=k+1)[1][1:]  # exclude self
        Z = X[idx] - X[i]  # center at x_i
        G = Z @ Z.T  # local Gram matrix
        G += 1e-3 * np.eye(k)  # regularization
        w = np.linalg.solve(G, np.ones(k))
        w /= w.sum()
        W[i, idx] = w
    M = (np.eye(n) - W).T @ (np.eye(n) - W)
    eigvals, eigvecs = eigh(M, subset_by_index=[1, n_components])
    return eigvecs  # (n x n_components)
```

## Practical Considerations

### Neighborhood Size $k$
- Too small: graph disconnected, embedding fails globally
- Too large: manifold assumption violated, local structure smoothed
- Rule of thumb: $k = 2 \cdot \text{intrinsic\_dim}$ or 10-20 for typical data
- Adaptive neighborhood: use locally varying $k$ based on density

### Robustness Issues
- **Isomap**: Topological instability (short-circuit edges) → add landmark filtering
- **LLE**: Requires $k > d$ for local Gram matrix to be full rank; weight regularization helps
- **Laplacian Eigenmaps**: Sensitive to kernel width $t$; median distance heuristic helps

### Out-of-Sample Extension
- Isomap: Use triangulation with $k$ nearest landmarks
- LLE: Compute weights for new point with its neighbors, apply to embedding
- Laplacian Eigenmaps: Nyström formula: $y_{\text{new}} = \frac{1}{\lambda} \sum_i K(x_{\text{new}}, x_i) y_i$

## Limitations
- All $O(n^3)$ due to eigendecomposition — use landmarks for $n > 10^4$
- Sensitive to manifold sampling density (holes cause issues)
- Struggle with manifolds of varying intrinsic dimension
- Isomap fails on non-convex manifolds (e.g., Swiss roll with hole)
- LLE can produce degenerate embeddings with non-uniform sampling

## References
- Tenenbaum, de Silva, Langford, "A Global Geometric Framework for Nonlinear Dimensionality Reduction" (Science, 2000)
- Roweis & Saul, "Nonlinear Dimensionality Reduction by Locally Linear Embedding" (Science, 2000)
- Belkin & Niyogi, "Laplacian Eigenmaps for Dimensionality Reduction and Data Representation" (Neural Computation, 2003)
- Saul & Roweis, "Think Globally, Fit Locally" (JMLR, 2003)
- de Silva & Tenenbaum, "Global Versus Local Methods in Nonlinear Dimensionality Reduction" (NIPS 2002)
