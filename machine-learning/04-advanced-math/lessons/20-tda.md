# 04.20 Algebraic Topology and Topological Data Analysis

## Motivation
Topology studies shape and connectivity. TDA extracts topological features (holes, loops, connected components) from data, providing robust, coordinate-free descriptors for point clouds, images, and networks. Unlike Euclidean methods, topological features are invariant under continuous deformations — making them ideal for analysing data with varying geometry but consistent shape.

## Learning Objectives
- Construct simplicial complexes (Čech, Vietoris–Rips) from point cloud data.
- Compute persistent homology and interpret persistence diagrams/barcodes.
- Understand the stability theorem for persistence diagrams.
- Apply TDA for point cloud classification, shape analysis, and time-series analysis.

## Math Foundation

### Simplicial Complexes
A simplicial complex $K$ is a set of simplices (points, edges, triangles, tetrahedra, ...) closed under taking faces:
- A $k$-simplex $\sigma = [v_0, \dots, v_k]$ is the convex hull of $k+1$ affinely independent points.
- A face of $\sigma$ is a simplex formed by a subset of its vertices.
- $K$ must contain all faces of every simplex in $K$.

### Building Complexes from Point Clouds
- **Čech complex** $\check{C}_\epsilon(X)$: includes simplex $\sigma$ if the $\epsilon$-balls around its vertices have non-empty intersection. Captures the topology of the union of $\epsilon$-balls.
- **Vietoris–Rips complex** $VR_\epsilon(X)$: includes simplex $\sigma$ if all pairwise distances $\le 2\epsilon$. Cheaper to compute (only distances needed).
- **Alpha complex**: subcomplex of the Delaunay triangulation; exactly captures the union of $\epsilon$-balls in $\mathbb{R}^d$.

### Homology
Homology groups $H_k(K)$ capture:
- $H_0$: connected components (rank = number of components)
- $H_1$: loops/cycles (rank = number of independent 1D holes)
- $H_2$: voids/cavities (rank = number of 2D holes)

The $k$-th Betti number $\beta_k = \text{rank}(H_k)$ counts the number of $k$-dimensional holes. The Euler characteristic is $\chi = \sum_{k=0}^\infty (-1)^k \beta_k$.

### Persistent Homology
As $\epsilon$ increases from 0 to $\infty$, the complexes form a filtration:

$$K_0 \subseteq K_{\epsilon_1} \subseteq K_{\epsilon_2} \subseteq \dots \subseteq K_\infty$$

Persistent homology tracks the birth and death of homology classes across the filtration. Each feature is encoded as a pair $(\epsilon_{\text{birth}}, \epsilon_{\text{death}})$.

- **Persistence diagram**: 2D plot where each feature is a point $(\text{birth}, \text{death})$. Features near the diagonal are short-lived (noise); features far from the diagonal are persistent (signal).
- **Barcode**: each feature is shown as an interval $[\text{birth}, \text{death}]$.

### Stability Theorem
The bottleneck distance between persistence diagrams is bounded by the Hausdorff distance between the underlying spaces:

$$d_B(\text{Dgm}(X), \text{Dgm}(Y)) \le d_H(X, Y)$$

This ensures that small perturbations to the data cause only small perturbations to the persistence diagrams — a crucial robustness guarantee.

## Python Implementation

```python
import numpy as np
try:
    from ripser import ripser
    from persim import plot_diagrams
    HAVE_PERSISTENCE = True
except ImportError:
    HAVE_PERSISTENCE = False

def compute_persistence(point_cloud, max_dim=2):
    """Compute persistent homology of a point cloud via Vietoris-Rips."""
    if not HAVE_PERSISTENCE:
        # Fallback: simulate persistence computation (sketch only)
        print("Install ripser for actual computation: pip install ripser")
        return None
    
    diagrams = ripser(point_cloud, maxdim=max_dim)['dgms']
    return diagrams

def persistence_statistics(diagrams):
    """Extract summary statistics from persistence diagrams."""
    stats = {}
    for dim, dgm in enumerate(diagrams):
        if len(dgm) == 0:
            continue
        births = dgm[:, 0]
        deaths = dgm[:, 1]
        lifetimes = deaths - births
        finite = np.isfinite(deaths) & (lifetimes > 0)
        if finite.any():
            stats[f'H{dim}_max_life'] = np.max(lifetimes[finite])
            stats[f'H{dim}_sum_life'] = np.sum(lifetimes[finite])
            stats[f'H{dim}_num_features'] = np.sum(finite)
            stats[f'H{dim}_mean_birth'] = np.mean(births[finite])
    return stats

def persistence_image(dgm, x_range=(0, 1), y_range=(0, 1), resolution=(20, 20), sigma=0.05):
    """Convert a persistence diagram to a persistence image (vectorisation)."""
    finite = np.isfinite(dgm[:, 1])
    dgm = dgm[finite]
    # transform death-birth to birth+death coordinates
    pts = np.column_stack([dgm[:, 0], dgm[:, 1] - dgm[:, 0]])
    
    x_lin = np.linspace(x_range[0], x_range[1], resolution[0])
    y_lin = np.linspace(y_range[0], y_range[1], resolution[1])
    img = np.zeros(resolution)
    
    for x, y in pts:
        if x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]:
            gauss = np.exp(-((x_lin - x)**2 + (y_lin[:, None] - y)**2) / (2 * sigma**2))
            img += gauss
    
    return img

# Example: circle vs. noisy circle
np.random.seed(42)
theta = np.linspace(0, 2*np.pi, 50)
circle = np.column_stack([np.cos(theta), np.sin(theta)])
noisy_circle = circle + np.random.randn(50, 2) * 0.1

if HAVE_PERSISTENCE:
    dgm_circle = compute_persistence(circle)
    dgm_noisy = compute_persistence(noisy_circle)
    print("Circle H1 features:", persistence_statistics(dgm_circle))
    print("Noisy circle H1 features:", persistence_statistics(dgm_noisy))
else:
    print("Skipping persistence computation (ripser not installed)")
```

## Visualization
Plot the persistence diagrams for a clean circle (one persistent $H_1$ point far from diagonal) and a noisy circle (still one persistent $H_1$ point but more short-lived features near the diagonal). A second panel shows the barcode representation. A third panel shows the persistence image — a 2D heatmap that discretises the diagram for input to ML classifiers.

## Connections to Machine Learning

### Vectorisation for ML
Persistence diagrams are not directly compatible with standard ML algorithms. Vectorisation methods include:
- **Persistence images**: 2D histogram weighted by lifetime, convolved with a Gaussian kernel.
- **Persistence landscapes**: sequence of functions $\lambda_k(t) = \sup\{\ell : \text{feature } (\ell, t) \text{ persists}\}$.
- **Persistence curves**: summary curves (e.g., total lifetime, number of features) as a function of $\epsilon$.
- **Persistence Fisher kernel**: kernel on the space of persistence diagrams.

### TDA for Time Series
Use delay embeddings (Takens' embedding) to reconstruct the attractor from a scalar time series:

$$x(t) \mapsto (x(t), x(t-\tau), \dots, x(t-(d-1)\tau))$$

Apply persistent homology to the embedded point cloud:
- **Periodic signals**: produce a persistent $H_1$ loop (circle).
- **Chaotic signals**: produce complex topology with multiple $H_1$ features.
- **Random noise**: produce features close to the diagonal.

This is used for anomaly detection, physiological signal classification (EEG, ECG), and distinguishing dynamical regimes.

### Shape Analysis and Molecular Modelling
- **Protein structure comparison**: persistence diagrams of distance-based filtrations on 3D protein coordinates capture secondary and tertiary structure; used for fold classification.
- **Material science**: persistent homology of nanoporous materials predicts adsorption properties from the topological features of the pore network.
- **3D shape retrieval**: persistence diagrams are robust to deformations and noise, making them effective shape descriptors.

### Network Analysis
- **Graph persistence**: build a filtration by thresholding edge weights (e.g., correlation between nodes). Persistent $H_0$ reveals hierarchical community structure; persistent $H_1$ reveals feedback loops.
- **Mapper**: summarise high-dimensional data as a simplicial complex by clustering in overlapping bins of a filter function (e.g., density). Used for disease subtype discovery in genomics.

## Practical Considerations

### Computational Complexity
- Vietoris–Rips: $O(N^2)$ for the distance matrix, then $O(N^3)$ for persistence (worst case). Practical for $N \le 10^4$ with optimised libraries (Ripser, Gudhi).
- Persistence simplification: reduce point cloud or subsample landmarks.
- Distributed persistence: available in DIPHA and PHAT for large datasets.

### Choosing the Filtration
- **Distance-based** (Čech, VR): when the data is a point cloud in a metric space.
- **Function-based** (sublevel/superlevel sets): when the data has a function defined on it (e.g., grayscale image, density estimate).
- **Graph-based**: when the data is relational with weighted edges.

### Interpreting Persistence
- **Persistent features** (far from diagonal): likely signal, robust to noise.
- **Ephemeral features** (near diagonal): likely noise or sampling artefacts.
- **Multiple persistent $H_1$ features**: complex cyclic structure (e.g., torus, multiple loops).
- **Infinite death**: features that never die within the filtration range.

## References
- Edelsbrunner & Harer, *Computational Topology: An Introduction*, AMS 2010
- Carlsson, "Topology and Data," *Bull. Amer. Math. Soc.*, 2009
- Adams et al., "Persistence Images: A Stable Vector Representation of Persistent Homology," *JMLR*, 2017
- Bubenik, "Statistical Topological Data Analysis using Persistence Landscapes," *JMLR*, 2015
- Chazal & Michel, "An Introduction to Topological Data Analysis: Fundamental and Practical Aspects for Data Scientists," *Foundations and Trends in ML*, 2021
