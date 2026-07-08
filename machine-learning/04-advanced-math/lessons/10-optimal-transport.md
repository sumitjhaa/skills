# 04.10 Optimal Transport and Wasserstein Distance

## Motivation
Optimal transport provides a geometric framework for comparing probability distributions with a proper metric (Wasserstein distance) that respects the underlying geometry. Unlike KL divergence, Wasserstein distances remain meaningful even for distributions with disjoint support — a critical property for generative modelling, domain adaptation, and single-cell genomics.

## Learning Objectives
- Distinguish between the Monge and Kantorovich formulations of optimal transport.
- Derive the Kantorovich–Rubinstein duality and its role in WGANs.
- Implement the Sinkhorn algorithm for entropic optimal transport.
- Apply optimal transport to domain adaptation, generative modelling, and trajectory inference.

## Math Foundation

### Monge Problem
Given two distributions $P$ on $\mathcal{X}$ and $Q$ on $\mathcal{Y}$, find a transport map $T: \mathcal{X} \to \mathcal{Y}$ that pushes $P$ to $Q$ (i.e., $T_\# P = Q$) and minimises the transportation cost:

$$\inf_{T: T_\# P = Q} \int_{\mathcal{X}} c(x, T(x)) dP(x)$$

The Monge problem may have no solution if $P$ has atoms (a single point cannot be split across multiple destinations).

### Kantorovich Relaxation
Kantorovich relaxed the problem by allowing mass splitting: find a coupling $\gamma \in \Gamma(P,Q)$ (a joint distribution with marginals $P$ and $Q$) minimising:

$$W_c(P,Q) = \inf_{\gamma \in \Gamma(P,Q)} \mathbb{E}_{(X,Y) \sim \gamma}[c(X,Y)]$$

For $c(x,y) = \|x-y\|^p$, the $p$-th power of the $p$-Wasserstein distance is:

$$W_p^p(P,Q) = \inf_{\gamma \in \Gamma(P,Q)} \mathbb{E}[\|X-Y\|^p]$$

### Kantorovich–Rubinstein Duality
For $p=1$ and $c(x,y) = \|x-y\|$, the dual problem is:

$$W_1(P,Q) = \sup_{\|f\|_L \le 1} \mathbb{E}_{x \sim P}[f(x)] - \mathbb{E}_{y \sim Q}[f(y)]$$

where $\|f\|_L$ is the Lipschitz constant of $f$. The optimal $f$ is called the Kantorovich potential. This dual form is the basis for Wasserstein GANs, where a critic network learns $f$ under a Lipschitz constraint (via weight clipping or gradient penalty).

### Wasserstein-2 and the Bures Metric
For $p=2$, the Wasserstein distance between Gaussians $\mathcal{N}(\mu_1, \Sigma_1)$ and $\mathcal{N}(\mu_2, \Sigma_2)$ has closed form:

$$W_2^2 = \|\mu_1 - \mu_2\|^2 + \text{tr}\left( \Sigma_1 + \Sigma_2 - 2 (\Sigma_1^{1/2} \Sigma_2 \Sigma_1^{1/2})^{1/2} \right)$$

The optimal transport map is affine: $T(x) = \mu_2 + A(x - \mu_1)$ where $A = \Sigma_1^{-1/2} (\Sigma_1^{1/2} \Sigma_2 \Sigma_1^{1/2})^{1/2} \Sigma_1^{-1/2}$.

## Entropic Optimal Transport and Sinkhorn

Adding entropy to the transport problem yields a smooth, differentiable approximation:

$$W_{c,\varepsilon}(P,Q) = \min_{\gamma \in \Gamma(P,Q)} \mathbb{E}[c(X,Y)] - \varepsilon H(\gamma)$$

where $H(\gamma) = -\int \gamma(x,y) \log \gamma(x,y) dx dy$ is the Shannon entropy. As $\varepsilon \to 0$, we recover exact OT; as $\varepsilon \to \infty$, the coupling becomes the product of marginals.

### Sinkhorn Algorithm
The optimal $\gamma$ has the form $\gamma_{ij} = u_i K_{ij} v_j$ where $K_{ij} = \exp(-c_{ij}/\varepsilon)$. The algorithm iterates:

1. $u \leftarrow p / (K v)$ (element-wise)
2. $v \leftarrow q / (K^\top u)$

until convergence. This is simply iterative row/column scaling of $K$.

```python
import numpy as np

def sinkhorn(p, q, C, eps=0.1, max_iter=100, tol=1e-8):
    """Sinkhorn algorithm for entropic optimal transport.
    
    Args:
        p: source distribution (n,)
        q: target distribution (m,)
        C: cost matrix (n, m)
        eps: entropic regularisation strength
    Returns:
        gamma: optimal coupling (n, m)
        W: transport cost
    """
    n, m = len(p), len(q)
    K = np.exp(-C / eps)
    u = np.ones(n) / n
    v = np.ones(m) / m
    
    for i in range(max_iter):
        u_prev = u.copy()
        v = q / (K.T @ u + 1e-12)
        u = p / (K @ v + 1e-12)
        if np.max(np.abs(u - u_prev)) < tol:
            break
    
    gamma = np.diag(u) @ K @ np.diag(v)
    W = np.sum(gamma * C)
    return gamma, W

# Example: 1D transport between two distributions
np.random.seed(42)
n = m = 50
p = np.ones(n) / n
q = np.ones(m) / m
x = np.linspace(0, 1, n)[:, None]
y = np.linspace(0.5, 1.5, m)[:, None]  # shifted
C = (x - y.T)**2  # squared Euclidean

gamma, W = sinkhorn(p, q, C, eps=0.01)
print(f"Wasserstein-2^2 ≈ {W:.4f}")

# Closed form for 1D: W_2^2 = int_0^1 |F_p^{-1}(t) - F_q^{-1}(t)|^2 dt
# = |mean shift|^2 since both are uniform on different intervals
print(f"Expected: {(1.0 - 0.5)**2:.4f}")  # mean shift squared
```

## Visualization
Plot the two 1D distributions as histograms and show the optimal transport coupling $\gamma^*$ as a heatmap — the bright diagonal band is shifted, showing mass transported from $[0,1]$ to $[0.5,1.5]$. A second panel displays the transport map $T(x)$ as a line from each source bin to its destination bin(s), with line opacity proportional to transported mass.

## Connections to Machine Learning

### Wasserstein GANs
WGAN replaces the JS divergence in GANs with Wasserstein-1 distance:

$$\min_G \max_{D \in \text{Lip}_1} \mathbb{E}_{x \sim P_{\text{data}}}[D(x)] - \mathbb{E}_{z \sim P_z}[D(G(z))]$$

The discriminator (critic) learns a 1-Lipschitz function $D$, and the generator minimises the Wasserstein distance between the real and generated distributions. The Lipschitz constraint is enforced by weight clipping (original) or gradient penalty (WGAN-GP). WGANs provide meaningful loss curves, stable training, and mode-covering behaviour.

### Domain Adaptation
Optimal transport aligns source and target domains by finding a transport map from source to target features. Methods include:
- **Joint distribution optimal transport** (JDOT): transports source examples to target while preserving labels.
- **Wasserstein distance for domain adaptation**: minimise $W(P_S, P_T)$ with a class-regularised transport plan.
- **OT for label propagation**: transport source labels to target via the optimal coupling, weighted by class proportions.

### Single-Cell Trajectory Inference
In single-cell genomics, cells are unordered snapshots. Wasserstein-2 gives a natural pseudotime: the WFR (Wasserstein-Fisher-Rao) geodesic interpolates between a start cell distribution and an end cell distribution, revealing the most likely developmental path for each cell.

### Flow Matching and Diffusion
Continuous normalising flows and diffusion models can be understood through optimal transport:
- The probability path from noise to data in a diffusion model is a Wasserstein geodesic under the score function drift.
- **Flow matching** directly constructs a vector field that pushes a source distribution to a target, and the optimal vector field minimises a Wasserstein-2 kinetic energy.

## Practical Considerations

### Computational Cost
| Method | Complexity | Use Case |
|--------|-----------|----------|
| Exact OT (network simplex) | $O(n^3 \log n)$ | Small $n$ ($<10^3$) |
| Sinkhorn | $O(n^2 / \varepsilon^2)$ | Medium $n$ ($10^3$-$10^5$) |
| Sliced Wasserstein | $O(n \log n)$ per projection | Large $n$ with approximations |
| Tree-Wasserstein | $O(n \log n)$ | When a tree metric is appropriate |

### Choosing $\varepsilon$ in Sinkhorn
- Small $\varepsilon$ gives near-exact transport but requires many iterations.
- Large $\varepsilon$ converges quickly but is far from exact OT.
- Rule of thumb: $\varepsilon \approx \text{median}(C)/10$ balances accuracy and speed.
- The **Sinkhorn divergence** $\text{S}_\varepsilon(P,Q) = W_{c,\varepsilon}(P,Q) - \frac12 W_{c,\varepsilon}(P,P) - \frac12 W_{c,\varepsilon}(Q,Q)$ corrects for the entropic bias.

### Wasserstein in High Dimensions
Wasserstein distances suffer from the curse of dimensionality — the sample complexity of estimating $W_2$ scales as $O(n^{-1/d})$. Practical workarounds:
- **Sliced Wasserstein**: average 1D Wasserstein distances over random projections.
- **Max-sliced Wasserstein**: take the maximum over projections (adversarial).
- **Kernelised Wasserstein**: embed distributions in an RKHS first.

## References
- Villani, *Optimal Transport: Old and New*, Springer 2009
- Peyré & Cuturi, *Computational Optimal Transport*, FnT ML 2019
- Arjovsky, Chintala, Bottou, "Wasserstein GAN," *ICML 2017*
- Cuturi, "Sinkhorn Distances: Lightspeed Computation of Optimal Transport," *NeurIPS 2013*
- Courty et al., "Optimal Transport for Domain Adaptation," *IEEE TPAMI*, 2017
- Kolouri et al., "Sliced Wasserstein Distance for Learning Gaussian Mixture Models," *CVPR 2016*
