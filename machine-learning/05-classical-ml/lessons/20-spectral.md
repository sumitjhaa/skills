# Lesson 05.20: Spectral Clustering

## Learning Objectives
- Understand spectral relaxation of normalized cut
- Implement spectral clustering with graph Laplacians
- Analyze the role of similarity graph construction
- Apply to non-convex cluster shapes

## Graph Representation
Build similarity graph $G = (V, E)$ where vertices = data points:

### Common Similarity Graphs
- **$\varepsilon$-neighborhood**: $W_{ij} = 1$ if $\|x_i - x_j\| < \varepsilon$, else 0
- **$k$-nearest neighbors**: $W_{ij} = 1$ if $x_i$ is among $k$NN of $x_j$ or vice versa
- **Fully connected**: $W_{ij} = \exp\left(-\frac{\|x_i - x_j\|_2^2}{2\sigma^2}\right)$ (RBF kernel)

RBF graph typically gives best results; $\sigma$ controls locality.

## Graph Laplacians

### Unnormalized Laplacian
$$L = D - W$$

where $D_{ii} = \sum_j W_{ij}$ is the degree matrix.

Properties:
- $L$ is symmetric positive semidefinite
- Smallest eigenvalue = 0 with eigenvector $\mathbf{1}$ (constant)
- Number of zero eigenvalues = number of connected components

### Normalized Laplacians
- **Symmetric**: $L_{\text{sym}} = I - D^{-1/2} W D^{-1/2}$
- **Random walk**: $L_{\text{rw}} = I - D^{-1} W$

Both have the same eigenvalues. $L_{\text{rw}}$ is directly related to the random walk on the graph.

## Algorithm (Normalized Cut)
1. Build similarity graph $W$ (RBF kernel)
2. Compute normalized Laplacian $L_{\text{sym}} = I - D^{-1/2} W D^{-1/2}$
3. Find $k$ smallest eigenvectors of $L_{\text{sym}}$
4. Form $U \in \mathbb{R}^{n \times k}$ with eigenvectors as columns
5. Normalize rows: $U_{ij} \leftarrow U_{ij} / \sqrt{\sum_j U_{ij}^2}$
6. Run k-means on rows of $U$ to get cluster assignments

## Why It Works
The normalized cut objective:

$$\text{NCut}(A, \bar{A}) = \text{cut}(A,\bar{A})\left(\frac{1}{\text{vol}(A)} + \frac{1}{\text{vol}(\bar{A})}\right)$$

Minimizing NCut is NP-hard. Spectral relaxation solves the continuous relaxation:

$$\min_{f \in \mathbb{R}^n} \frac{f^\top L f}{f^\top D f} \quad \text{s.t.} \quad f \perp D\mathbf{1}$$

The solution is the eigenvector of $L_{\text{rw}}$ with smallest non-zero eigenvalue. This is the Rayleigh quotient for the generalized eigenvalue problem $L f = \lambda D f$.

## Choosing $\sigma$ (Kernel Width)
- **Median heuristic**: $\sigma = \text{median}(\{ \|x_i - x_j\| : i < j \})$ — adapts to data scale
- **Local scaling**: Per-point $\sigma_i = \|x_i - x_{i_k}\|$ (distance to $k$th NN), then $W_{ij} = \exp(-\|x_i-x_j\|^2 / (\sigma_i \sigma_j))$
- **Multiple scales**: Combine multiple $\sigma$ values for multi-scale data

## Code: Spectral Clustering

```python
import numpy as np
from scipy.linalg import eigh
from sklearn.cluster import KMeans

class SpectralClustering:
    def __init__(self, n_clusters=3, gamma=1.0):
        self.n_clusters = n_clusters
        self.gamma = gamma

    def fit(self, X):
        n = X.shape[0]
        # Build similarity matrix (RBF)
        sq_dists = np.sum(X**2, axis=1, keepdims=True) + np.sum(X**2, axis=1) - 2 * X @ X.T
        W = np.exp(-self.gamma * sq_dists)
        np.fill_diagonal(W, 0)
        # Normalized Laplacian
        D = np.diag(1.0 / np.sqrt(np.sum(W, axis=1) + 1e-10))
        L_sym = np.eye(n) - D @ W @ D
        # Eigen decomposition
        eigvals, eigvecs = eigh(L_sym, subset_by_index=[0, self.n_clusters - 1])
        # Normalize rows
        U = eigvecs / (np.linalg.norm(eigvecs, axis=1, keepdims=True) + 1e-10)
        # K-means on spectral embedding
        self.labels_ = KMeans(n_clusters=self.n_clusters, n_init=10).fit_predict(U)
        return self
```

## Practical Considerations
- **Eigendecomposition cost**: $O(n^3)$ — use Nyström approximation for large $n$
- **Nyström method**: Sample $m \ll n$ landmark points, approximate eigenvectors in $O(m^3 + nm^2)$
- **Choice of $k$**: Use eigengap heuristic (gap between $\lambda_k$ and $\lambda_{k+1}$)
- **Large $n$**: Use sparse eigen-solvers (ARPACK) exploiting neighborhood graph sparsity
- **$k=2$ case**: The second eigenvector (Fiedler vector) directly gives bipartition by sign

### Scalability Tricks
- **Landmark-based**: Cluster $m \ll n$ points, assign rest via nearest landmark
- **Approximate nearest neighbors**: Build sparse $W$ from approximate k-NN
- **Multiscale**: Downsample, cluster, upsample with constrained propagation

## Properties
- Finds non-convex, arbitrarily shaped clusters
- Can separate nested circles (e.g., two moons, concentric circles)
- $O(n^3)$ eigendecomposition is main bottleneck
- Sensitive to similarity graph construction ($\sigma$ choice)
- Related to manifold learning (Laplacian Eigenmaps)

## References
- Shi & Malik, "Normalized Cuts and Image Segmentation" (IEEE TPAMI, 2000)
- Ng, Jordan, Weiss, "On Spectral Clustering: Analysis and an Algorithm" (NIPS 2001)
- von Luxburg, "A Tutorial on Spectral Clustering" (Statistics and Computing, 2007)
- Bengio et al., "Out-of-Sample Extensions for LLE, Isomap, MDS, Eigenmaps, and Spectral Clustering" (NIPS 2003)
