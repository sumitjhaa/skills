# 04.14 Riemannian Hamiltonian Monte Carlo

## Motivation
Standard HMC uses a fixed mass matrix, ignoring the geometry of the parameter space. Riemannian HMC (RHMC) adapts the kinetic energy using a position-dependent metric derived from the Fisher information or Hessian, enabling efficient exploration of strongly curved, ill-conditioned posteriors common in hierarchical models, Bayesian neural networks, and latent Gaussian models.

## Learning Objectives
- Understand the Hamiltonian dynamics on a Riemannian manifold with a position-dependent metric.
- Derive the generalised leapfrog integrator for RHMC.
- Contrast RHMC with standard HMC in terms of efficiency per gradient evaluation.
- Apply RHMC to strongly correlated posteriors where standard HMC mixes slowly.

## Math Foundation

### Hamiltonian on a Riemannian Manifold
For a target distribution $\pi(\theta)$ on a Riemannian manifold with metric $G(\theta)$ (a positive-definite matrix for each $\theta$), the Hamiltonian is:

$$H(\theta, p) = -\log \pi(\theta) + \frac12 p^\top G(\theta)^{-1} p + \frac12 \log |G(\theta)|$$

The kinetic energy $K(\theta, p) = \frac12 p^\top G(\theta)^{-1} p$ defines a geodesic motion on the manifold. The additional $\frac12 \log |G(\theta)|$ term arises from transforming the uniform measure on $(\theta, p)$ to the canonical measure.

### Equations of Motion
The dynamics are given by Hamilton's equations:

$$\dot{\theta} = \nabla_p H = G(\theta)^{-1} p$$

$$\dot{p} = -\nabla_\theta H = \nabla_\theta \log \pi(\theta) - \frac12 \text{tr}\left(G(\theta)^{-1} \frac{\partial G(\theta)}{\partial \theta}\right) + \frac12 p^\top G(\theta)^{-1} \frac{\partial G(\theta)}{\partial \theta} G(\theta)^{-1} p$$

The first term in $\dot{p}$ is the standard gradient. The second term (the "Christoffel correction") accounts for the curvature of the metric. The third term is a centripetal force — without it, the dynamics would not preserve the Hamiltonian.

### Metric Choices
- **Fisher information metric**: $G(\theta) = \mathcal{I}(\theta)$ — natural from information geometry; the resulting dynamics are related to natural gradient descent.
- **Hessian of negative log-posterior**: $G(\theta) = -\nabla^2 \log \pi(\theta) + \epsilon I$ — captures local curvature; requires computing Hessians.
- **Empirical Fisher**: $G(\theta) = \frac{1}{n} \sum_{i=1}^n \nabla \log p(y_i|x_i,\theta) \nabla \log p(y_i|x_i,\theta)^\top$ — cheaper than the true Fisher.
- **SoftAbs metric**: smooth the absolute values of Hessian eigenvalues: $\text{SoftAbs}(\lambda) = \lambda \coth(\lambda/\epsilon)$, ensuring positive-definiteness.

### Generalised Leapfrog Integrator
Because $G$ depends on $\theta$, the standard leapfrog integrator requires an implicit step:

1. $p(t + \epsilon/2) = p(t) - \frac{\epsilon}{2} \nabla_\theta H(\theta(t), p(t + \epsilon/2))$ (implicit in $p$)
2. $\theta(t + \epsilon) = \theta(t) + \frac{\epsilon}{2} (G(\theta(t))^{-1} + G(\theta + \epsilon))^{-1}) p(t + \epsilon/2)$ (requires fixed-point iteration)

In practice, a simplified explicit integrator (e.g., using the metric at the midpoint) works well with small $\epsilon$.

## Python Implementation

```python
import numpy as np

def riemannian_hmc(log_prob, grad_log_prob, metric_fn, metric_grad_fn,
                    n_samples=1000, eps=0.1, L=10, theta0=None, d=None):
    """Riemannian Hamiltonian Monte Carlo.
    
    Args:
        log_prob: log target density
        grad_log_prob: gradient of log target
        metric_fn: returns G(theta) and log|G(theta)|
        metric_grad_fn: returns dG/dtheta (list of d x d matrices)
    """
    if theta0 is None:
        theta0 = np.zeros(d)
    theta = theta0.copy()
    samples = np.zeros((n_samples, len(theta)))
    
    for i in range(n_samples):
        # sample momentum
        G, logdet = metric_fn(theta)
        p = np.random.multivariate_normal(np.zeros_like(theta), G)
        
        # leapfrog integration (simplified fixed metric per step)
        theta_cur = theta.copy()
        p_cur = p.copy()
        
        for _ in range(L):
            G_cur, _ = metric_fn(theta_cur)
            p_cur += 0.5 * eps * grad_log_prob(theta_cur)
            # subtract Christoffel and centripetal terms (simplified)
            G_inv = np.linalg.inv(G_cur)
            p_cur -= 0.5 * eps * (0.5 * np.trace(G_inv @ metric_grad_fn(theta_cur, 0))) * np.ones_like(theta_cur)
            # (full Christoffel term omitted for brevity — see Girolami & Calderhead 2011)
            
            theta_cur += eps * G_inv @ p_cur
            
            G_new, _ = metric_fn(theta_cur)
            p_cur += 0.5 * eps * grad_log_prob(theta_cur)
        
        # Metropolis accept/reject
        G_new, logdet_new = metric_fn(theta_cur)
        H_old = -log_prob(theta) + 0.5 * p @ np.linalg.solve(G, p) + 0.5 * logdet
        H_new = -log_prob(theta_cur) + 0.5 * p_cur @ np.linalg.solve(G_new, p_cur) + 0.5 * logdet_new
        
        if np.random.rand() < np.exp(H_old - H_new):
            theta = theta_cur
        
        samples[i] = theta
    
    return samples

# Example: 2D correlated Gaussian (ill-conditioned)
def log_prob_gauss(theta):
    Sigma = np.array([[1.0, 0.99], [0.99, 1.0]])
    return -0.5 * theta @ np.linalg.solve(Sigma, theta)

def grad_log_prob_gauss(theta):
    Sigma = np.array([[1.0, 0.99], [0.99, 1.0]])
    return -np.linalg.solve(Sigma, theta)

def metric_fn(theta):
    G = np.eye(2) * 0.5 + 0.5 * np.outer(theta, theta) / (1 + theta@theta)
    G += 0.01 * np.eye(2)  # regularise
    sign, logdet = np.linalg.slogdet(G)
    return G, logdet

def metric_grad_fn(theta, idx):
    return np.eye(2) * 0.0  # simplified

samples = riemannian_hmc(log_prob_gauss, grad_log_prob_gauss, metric_fn, metric_grad_fn,
                          n_samples=2000, theta0=np.array([2.0, -2.0]))
print(f"Sample mean: {samples.mean(axis=0)}")
print(f"Sample std: {samples.std(axis=0)}")
print(f"ESS (approx): {2000 / (1 + 2*np.mean(np.corrcoef(samples.T))):.0f}")
```

## Visualization
Plot the 2D posterior samples from standard HMC and RHMC as contours. RHMC samples should be more isotropic and less correlated. A second panel shows the metric $G(\theta)$ as ellipses at various points — the ellipses are aligned with the posterior curvature, enabling larger steps in well-conditioned directions.

## Practical Considerations

### Computational Cost
RHMC requires:
- $O(d^3)$ per step to factorise $G(\theta)$ (vs. $O(d^2)$ for fixed metric HMC)
- Gradient of the metric: $O(d^3)$ for the Christoffel symbol
- Total: $O(L d^3)$ per sample — only worthwhile when the ESS increase outweighs the higher per-step cost

### When RHMC Beats Standard HMC
- **Strong posterior correlations**: $\rho > 0.99$ between parameters
- **Heavy tails**: where standard HMC's Gaussian momentum overshoots
- **Hierarchical models**: where the metric varies significantly across the posterior
- **Non-Euclidean parameter spaces**: e.g., covariance matrices, simplexes, spheres

### Simplified Variants
- **Riemannian Langevin dynamics**: first-order integrator, $O(d^2)$ per step, no momentum. Simpler but lower acceptance.
- **Diagonal metric**: use only the diagonal of the Fisher, reducing to $O(d)$ per step. Captures scale but not correlation.
- **Empirical Fisher with Kronecker structure** (K-FAC): $O(d^{1.5})$ per step, good for neural network layers.

## References
- Girolami & Calderhead, "Riemann Manifold Langevin and Hamiltonian Monte Carlo," *JRSS-B*, 2011
- Betancourt, "A Conceptual Introduction to Hamiltonian Monte Carlo," *arXiv:1701.02434*, 2017
- Livingstone & Girolami, "Information-Geometric Markov Chain Monte Carlo Methods," *Stat. Comput.*, 2014
- Betancourt, "The Fundamental Incompatibility of Hamiltonian Monte Carlo and Data Subsampling," *ICML 2015*
