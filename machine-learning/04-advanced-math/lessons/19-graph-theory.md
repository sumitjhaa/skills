# 04.19 Graph Theory and Spectral Graph Theory

## Motivation
Graphs model relational data: social networks, molecular structures, and the internet. Spectral graph theory connects graph properties to eigenvalues of graph matrices, powering clustering, embeddings, and graph neural networks. The graph Laplacian and its spectral decomposition are the foundation for spectral clustering, manifold learning (Laplacian eigenmaps), and graph convolutional networks.

## Learning Objectives
- Define the graph Laplacian and its normalised variants.
- State and apply Cheeger's inequality connecting the spectral gap to graph conductance.
- Implement spectral clustering and Laplacian eigenmaps.
- Understand graph convolution in the spectral and spatial domains.

## Math Foundation

### Graph Matrices
For an undirected graph $G = (V, E)$ with $n = |V|$ nodes and $m = |E|$ edges:
- **Adjacency matrix** $A \in \mathbb{R}^{n \times n}$: $A_{ij} = 1$ if $(i,j) \in E$, 0 otherwise.
- **Degree matrix** $D = \text{diag}(d_1, \dots, d_n)$ where $d_i = \sum_j A_{ij}$.
- **Combinatorial Laplacian**: $L = D - A$.
- **Normalised Laplacian**: $\mathcal{L} = D^{-1/2} L D^{-1/2} = I - D^{-1/2} A D^{-1/2}$.

### Properties of the Laplacian
1. **Quadratic form**: $x^\top L x = \sum_{(i,j) \in E} (x_i - x_j)^2$.
2. **Eigenvalues**: $0 = \lambda_1 \le \lambda_2 \le \dots \le \lambda_n$.
3. **Multiplicity of $\lambda_1 = 0$**: equals the number of connected components.
4. **Eigenvector of $\lambda_1$**: the constant vector $\mathbf{1}$.
5. **$\lambda_2$ (algebraic connectivity)**: measures how well-connected the graph is — larger $\lambda_2$ means harder to cut.

### Cheeger Inequality
The conductance (isoperimetric number) of a graph is:

$$h_G = \min_{S \subseteq V, |S| \le |V|/2} \frac{|\partial S|}{|S|}$$

where $|\partial S|$ is the number of edges leaving $S$. Cheeger's inequality bounds $h_G$ in terms of $\lambda_2$:

$$\frac{\lambda_2}{2} \le h_G \le \sqrt{2 \lambda_2}$$

For the normalised Laplacian, the inequality becomes $h_G \ge \lambda_2 / 2$ and $h_G \le \sqrt{2 \lambda_2}$.

### Spectral Clustering
The normalised cut (NCut) minimises:

$$\text{NCut}(S, \bar{S}) = \text{Cut}(S, \bar{S}) \left( \frac{1}{\text{vol}(S)} + \frac{1}{\text{vol}(\bar{S})} \right)$$

Spectral clustering solves a relaxed version: use the eigenvectors of $\mathcal{L}$ corresponding to the $k$ smallest eigenvalues as a $k$-dimensional embedding, then cluster with $k$-means.

## Python Implementation

```python
import numpy as np
from sklearn.cluster import KMeans

def laplacian(A, normalized=True):
    """Compute graph Laplacian from adjacency matrix."""
    D = np.diag(np.sum(A, axis=1))
    L = D - A
    if normalized:
        D_inv_sqrt = np.diag(1.0 / np.sqrt(np.maximum(np.diag(D), 1e-10)))
        L = D_inv_sqrt @ L @ D_inv_sqrt
    return L

def spectral_clustering(A, n_clusters=3):
    """Spectral clustering via normalised Laplacian."""
    L = laplacian(A, normalized=True)
    eigenvalues, eigenvectors = np.linalg.eigh(L)
    # take eigenvectors of smallest eigenvalues (excluding the first constant one)
    X = eigenvectors[:, 1:n_clusters+1]
    # normalise rows
    X = X / np.linalg.norm(X, axis=1, keepdims=True)
    kmeans = KMeans(n_clusters=n_clusters, n_init=10)
    return kmeans.fit_predict(X)

def laplacian_eigenmaps(A, n_components=2):
    """Laplacian Eigenmaps dimensionality reduction."""
    L = laplacian(A, normalized=True)
    eigenvalues, eigenvectors = np.linalg.eigh(L)
    return eigenvectors[:, 1:n_components+1]

def cheeger_conductance(A, labels):
    """Estimate conductance for a bipartition."""
    n = len(A)
    S = np.where(labels == 0)[0]
    vol_S = np.sum(np.sum(A[S], axis=1))
    vol_total = np.sum(A)
    cut = np.sum(A[S][:, np.where(labels == 1)[0]])
    return cut / min(vol_S, vol_total - vol_S)

# Example: cluster a simple graph (two moons as graph)
np.random.seed(42)
n_per_moon = 20
theta1 = np.linspace(0, np.pi, n_per_moon)
moon1 = np.column_stack([np.cos(theta1), np.sin(theta1)]) + np.random.randn(n_per_moon, 2) * 0.1
theta2 = np.linspace(np.pi, 2*np.pi, n_per_moon)
moon2 = np.column_stack([np.cos(theta2), np.sin(theta2)]) + np.array([1, 0]) + np.random.randn(n_per_moon, 2) * 0.1
X = np.vstack([moon1, moon2])

# Build adjacency (k-nearest neighbours)
from sklearn.neighbors import kneighbors_graph
A = kneighbors_graph(X, n_neighbors=5, mode='connectivity').toarray()
A = (A + A.T) / 2  # symmetrise
A = (A > 0).astype(float)

labels = spectral_clustering(A, n_clusters=2)
print("Cluster sizes:", np.bincount(labels))
print(f"Conductance: {cheeger_conductance(A, labels):.3f}")

# Laplacian eigenmaps embedding
embed = laplacian_eigenmaps(A, n_components=2)
print(f"Embedding shape: {embed.shape}")
```

## Visualization
Plot the two-moon graph with spectral clustering labels shown as colours — spectral clustering separates the non-convex moons that $k$-means on raw data cannot. A second panel shows the Laplacian eigenmaps embedding (coordinates from the second and third eigenvectors), where the two moons become linearly separable. A third panel shows the eigenvalue spectrum of the Laplacian — the gap after $\lambda_2$ indicates a good cut.

## Connections to Machine Learning

### Graph Neural Networks
GCN (Kipf & Welling 2017) uses a first-order approximation of spectral graph convolution:

$$H^{(l+1)} = \sigma\left( \tilde{D}^{-1/2} \tilde{A} \tilde{D}^{-1/2} H^{(l)} W^{(l)} \right)$$

where $\tilde{A} = A + I$ adds self-loops. This is a spatial message-passing layer: each node aggregates feature information from its neighbours, weighted by degree normalisation.

### Graph Attention Networks (GAT)
GAT replaces the fixed normalised adjacency with learned attention coefficients:

$$h_i' = \sigma\left( \sum_{j \in \mathcal{N}(i)} \alpha_{ij} W h_j \right), \quad \alpha_{ij} = \frac{\exp(\text{LeakyReLU}(a^\top [W h_i \| W h_j]))}{\sum_{k \in \mathcal{N}(i)} \exp(\text{LeakyReLU}(a^\top [W h_i \| W h_k]))}$$

Attention allows each node to weight its neighbours differently, improving capacity on heterogeneous graphs.

### Laplacian Regularisation in Semi-Supervised Learning
Propagate labels via the graph Laplacian:

$$\min_{f} \sum_{i=1}^n \ell(y_i, f_i) + \lambda \sum_{(i,j) \in E} (f_i - f_j)^2$$

The second term is $f^\top L f$, encouraging smoothness on the graph. The solution for a linear model is $\hat{f} = (I + \lambda L)^{-1} y$, analogous to kernel ridge regression with the Laplacian kernel.

### PageRank as a Graph Diffusion
PageRank's stationary distribution satisfies:

$$\pi = \alpha \pi P + (1-\alpha) \frac{1}{n} \mathbf{1}^\top$$

where $P = D^{-1} A$ is the random walk transition matrix. The solution $\pi$ can be expressed as $\pi = (1-\alpha) \frac{1}{n} \mathbf{1}^\top (I - \alpha P)^{-1}$, which is equivalent to a graph diffusion process.

## Practical Considerations

### Choosing the Right Laplacian
- **Combinatorial $L = D - A$**: eigenvalues scale with degree; eigenvectors localise on high-degree nodes.
- **Normalised $\mathcal{L} = D^{-1/2} L D^{-1/2}$**: eigenvalues in $[0, 2]$; better for graphs with varying degree.
- **Random walk $L_{rw} = D^{-1} L$**: eigenvalues same as $\mathcal{L}$; eigenvectors directly give cluster memberships.

### Scaling Graph Methods
- Standard spectral clustering is $O(n^3)$ due to eigendecomposition.
- **Nyström approximation**: sample $m \ll n$ landmark nodes, approximate $L \approx L_{nm} L_{mm}^{-1} L_{mn}$.
- **Lanczos method**: compute only the $k$ smallest eigenvalues in $O(k n^2)$.
- For GNNs on large graphs, use neighbour sampling (GraphSAGE) or cluster-GCN.

## References
- Chung, *Spectral Graph Theory*, AMS 1997
- Hamilton, *Graph Representation Learning*, Morgan & Claypool 2020
- Von Luxburg, "A Tutorial on Spectral Clustering," *Statistics and Computing*, 2007
- Kipf & Welling, "Semi-Supervised Classification with Graph Convolutional Networks," *ICLR 2017*
- Veličković et al., "Graph Attention Networks," *ICLR 2018*
- Belkin & Niyogi, "Laplacian Eigenmaps for Dimensionality Reduction and Data Representation," *Neural Computation*, 2003
