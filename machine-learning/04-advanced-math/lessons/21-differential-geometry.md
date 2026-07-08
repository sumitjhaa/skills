# 04.21 Differential Geometry: Manifolds, Tangent Spaces, Curvature

## Motivation
Many real-world data lie on low-dimensional manifolds embedded in high-dimensional space. Differential geometry provides the language to describe curvature, geodesics, and intrinsic coordinates — essential for manifold learning, geometric deep learning, and physics-informed ML. Concepts like geodesic distances, parallel transport, and curvature are increasingly used in representation learning and generative models on non-Euclidean spaces.

## Learning Objectives
- Define smooth manifolds, tangent spaces, and Riemannian metrics.
- Compute geodesics and understand the exponential map.
- Distinguish between Riemann, sectional, and Ricci curvature.
- Apply differential geometry to manifold learning and optimisation on manifolds.

## Math Foundation

### Smooth Manifolds
A smooth $n$-manifold $M$ is a Hausdorff, second-countable topological space locally homeomorphic to $\mathbb{R}^n$ via smooth transition maps. This means every point $p \in M$ has a neighbourhood $U$ and a homeomorphism $\phi: U \to \phi(U) \subseteq \mathbb{R}^n$ (a chart), and overlapping charts are smoothly compatible.

### Tangent Space
At each point $p \in M$, the tangent space $T_p M$ is an $n$-dimensional vector space of directional derivatives at $p$. A tangent vector $v \in T_p M$ can be thought of as the velocity of a curve $\gamma(t)$ through $p$:
$$\gamma(0) = p, \quad \dot{\gamma}(0) = v$$

The tangent bundle $TM = \bigsqcup_{p \in M} T_p M$ is a $2n$-dimensional manifold connecting all tangent spaces.

### Riemannian Metric
A Riemannian metric $g$ assigns an inner product $g_p: T_p M \times T_p M \to \mathbb{R}$ that varies smoothly with $p$. In local coordinates $(x^1, \dots, x^n)$:

$$g = \sum_{i,j} g_{ij}(x) dx^i \otimes dx^j$$

where $g_{ij}(x) = g_p(\partial_i, \partial_j)$ is a positive-definite symmetric matrix for each $x$.

### Geodesics
A geodesic is a curve $\gamma(t)$ that locally minimises length. It satisfies the geodesic equation:

$$\ddot{\gamma}^k + \sum_{i,j} \Gamma_{ij}^k \dot{\gamma}^i \dot{\gamma}^j = 0$$

where $\Gamma_{ij}^k$ are the Christoffel symbols (connection coefficients):

$$\Gamma_{ij}^k = \frac12 \sum_l g^{kl} \left( \frac{\partial g_{lj}}{\partial x^i} + \frac{\partial g_{il}}{\partial x^j} - \frac{\partial g_{ij}}{\partial x^l} \right)$$

### Exponential Map
For $v \in T_p M$, let $\gamma_v(t)$ be the unique geodesic with $\gamma_v(0) = p$ and $\dot{\gamma}_v(0) = v$. The exponential map is:

$$\exp_p(v) = \gamma_v(1)$$

The exponential map is a local diffeomorphism from a neighbourhood of $0$ in $T_p M$ to a neighbourhood of $p$ in $M$. The inverse $\exp_p^{-1}$ gives the Riemannian log map.

### Curvature
- **Riemann curvature tensor** $R(X,Y)Z = \nabla_X \nabla_Y Z - \nabla_Y \nabla_X Z - \nabla_{[X,Y]} Z$. Measures the non-commutativity of parallel transport.
- **Sectional curvature** $K(X,Y) = \frac{g(R(X,Y)Y, X)}{g(X,X)g(Y,Y) - g(X,Y)^2}$. Extends Gaussian curvature to higher dimensions.
- **Ricci curvature** $\text{Ric}(v,w) = \sum_i g(R(e_i, v)w, e_i)$ where $e_i$ is an orthonormal basis. Averages sectional curvature over directions.
- **Scalar curvature** $S = \sum_i \text{Ric}(e_i, e_i)$.
- **Gauss-Bonnet theorem**: $\int_M K dA = 2\pi \chi(M)$ — total curvature equals topology.

## Python Implementation

```python
import numpy as np

def christoffel_symbols(g, dg):
    """Compute Christoffel symbols of the first kind.
    g: metric matrix at a point (n x n)
    dg: list of n matrices, dg[k] = partial g / partial x^k
    """
    n = g.shape[0]
    g_inv = np.linalg.inv(g)
    Gamma = np.zeros((n, n, n))  # Gamma^k_{ij}
    for k in range(n):
        for i in range(n):
            for j in range(n):
                Gamma[k, i, j] = 0.5 * sum(
                    g_inv[k, l] * (dg[l][i, j] + dg[i][j, l] - dg[j][i, l]) 
                    for l in range(n)
                )
    return Gamma

def geodesic_equation(Gamma, x0, v0, t_span, n_steps=100):
    """Integrate geodesic equation via Euler method.
    x0: initial position (n,)
    v0: initial velocity (n,)
    """
    dt = (t_span[1] - t_span[0]) / n_steps
    n = len(x0)
    x = x0.copy()
    v = v0.copy()
    traj = [x.copy()]
    
    for _ in range(n_steps):
        # x dot = v
        x_new = x + dt * v
        # v dot = -Gamma v v
        acc = np.zeros(n)
        for k in range(n):
            acc[k] = -sum(Gamma[k, i, j] * v[i] * v[j] 
                          for i in range(n) for j in range(n))
        v_new = v + dt * acc
        x, v = x_new, v_new
        traj.append(x.copy())
    
    return np.array(traj)

def geodesic_distance_sphere(theta1, phi1, theta2, phi2):
    """Great-circle distance on S^2 (unit sphere).
    Input: (theta, phi) in radians."""
    c = np.sin(theta1)*np.sin(theta2)*np.cos(phi1-phi2) + np.cos(theta1)*np.cos(theta2)
    return np.arccos(np.clip(c, -1.0, 1.0))

def parallel_transport_sphere(theta, phi, v, dtheta, dphi):
    """Parallel transport a vector on S^2 along direction (dtheta, dphi).
    Simplified: assumes small step on sphere."""
    # For a sphere, parallel transport rotates the vector in the tangent plane
    # This is a simplified illustration only
    # The actual computation requires solving the parallel transport ODE
    return v  # placeholder

# Example: geodesic on the unit sphere
# Point 1: (theta=0, phi=0) -> North pole
# Point 2: (theta=pi/2, phi=0) -> Equator
dist = geodesic_distance_sphere(0, 0, np.pi/2, 0)
print(f"Geodesic distance from North pole to Equator: {dist:.4f} (expected: pi/2 = {np.pi/2:.4f})")

# Metric on the sphere in (theta, phi) coordinates
def sphere_metric(theta, phi):
    g = np.array([[1.0, 0.0], [0.0, np.sin(theta)**2]])
    return g

print(f"Metric determinant at equator: {np.linalg.det(sphere_metric(np.pi/2, 0)):.4f}")
print(f"Metric determinant at North pole: {np.linalg.det(sphere_metric(0.01, 0)):.4f} (degenerate)")
```

## Visualization
Plot a 2D manifold (e.g., a sphere or torus) with its tangent space shown at several points as planes. Overlaid geodesics are shown as great circles on the sphere. A second panel shows the curvature scalar as a heatmap on the manifold — positive on spheres, zero on flat tori, negative on hyperbolic surfaces.

## Connections to Machine Learning

### Manifold Learning
- **ISOMAP**: geodesic distances via graph shortest paths, then MDS to embed in low dimensions.
- **Locally Linear Embedding (LLE)**: preserves local linear relationships (tangent space structure).
- **Laplacian Eigenmaps**: preserves local neighbourhood structure via the graph Laplacian.
- **UMAP**: learns a fuzzy simplicial set representation and optimises a low-dimensional embedding with cross-entropy.
- **t-SNE**: minimises KL divergence between high- and low-dimensional pairwise similarities; does not preserve global geometry but excels at visualisation.

All these methods assume the data lies near a low-dimensional manifold, and they differ in how they approximate distances / tangent spaces / topology on that manifold.

### Geometric Deep Learning
Geometric DL generalises convolutional neural networks to non-Euclidean domains:
- **Manifold convolution**: aggregate features in geodesic neighbourhoods via local charts.
- **Geodesic convolution**: $f * g(x) = \int_{B_r(x)} f(y) g(\log_x(y)) d\omega(y)$ where $\log_x$ is the Riemannian log map.
- **Parallel transport**: align features across a manifold by transporting tangent vectors along geodesics.
- **Gauge equivariant CNNs**: layers equivariant to local frame changes on a manifold.

### Optimisation on Manifolds
Riemannian SGD optimises a loss $L(\theta)$ over parameters $\theta$ that lie on a manifold (e.g., Stiefel manifold for orthogonal constraints):

1. Compute Euclidean gradient $\nabla L(\theta_t)$.
2. Project to tangent space: $\text{grad} L(\theta_t) = \text{Proj}_{T_{\theta_t} M}(\nabla L(\theta_t))$.
3. Update along geodesic: $\theta_{t+1} = \exp_{\theta_t}(-\eta \text{ grad} L(\theta_t))$.

Common manifolds: sphere (normalised vectors), Stiefel (orthogonal matrices), Grassmann (subspaces), SPD (positive-definite matrices), and the Pareto simplex.

### Physics-Informed ML
- PINNs embed PDE constraints into loss functions on spatiotemporal manifolds.
- Metric-based regularisation encourages the learned representation to respect the physical geometry (e.g., conservation laws as isometries).
- Neural manifolds: learn an embedding space where distance corresponds to meaningful similarity (e.g., time to transition in dynamical systems).

## Practical Considerations

### Computing Geodesics
- For known metrics (sphere, hyperbolic space), closed-form geodesics exist.
- For data manifolds, approximate geodesic distances via graph shortest paths (ISOMAP).
- For learned metrics, use the geodesic ODE with neural network approximating the metric.
- Heat method (Crane et al. 2013): compute geodesic distances by solving a heat equation and normalising gradients.

### Curse of Dimensionality
- Manifold learning methods assume the intrinsic dimension $d \ll D$ (ambient).
- Estimating $d$: correlation dimension, MLE of intrinsic dimension (Levina & Bickel), or PCA scree plot.
- Noisy high-D data can obscure the manifold structure — denoising (autoencoders, diffusion maps) is often necessary.

## References
- do Carmo, *Riemannian Geometry*, Birkhäuser 1992
- Lee, *Introduction to Smooth Manifolds*, 2nd ed., Springer 2012
- Lee, *Riemannian Manifolds: An Introduction to Curvature*, Springer 1997
- Bronstein et al., "Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges," *arXiv:2104.13478*, 2021
- Absil, Mahony, Sepulchre, *Optimization Algorithms on Matrix Manifolds*, Princeton 2008
- Tenenbaum, de Silva, Langford, "A Global Geometric Framework for Nonlinear Dimensionality Reduction," *Science*, 2000
