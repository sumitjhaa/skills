# Lesson 37: Bayesian Nonparametrics

## Learning Objectives

After completing this lesson, you will be able to:
- Understand the Dirichlet process as a distribution over distributions
- Apply stick-breaking and Chinese restaurant process constructions
- Implement Dirichlet process mixture models for density estimation
- Recognize other Bayesian nonparametric models (IBP, HDP, Beta process)
- Use BNP models for clustering with unknown number of clusters

## Dirichlet Process

### Definition

A **Dirichlet Process (DP)** $DP(\alpha, G_0)$ is a distribution over probability measures, characterized by:
- $\alpha > 0$: **concentration parameter** (controls dispersion around $G_0$)
- $G_0$: **base measure** (center of the process)

**Finite-dimensional distributions:** For any finite partition $(A_1, \dots, A_k)$ of the sample space $\Theta$:
$$(G(A_1), \dots, G(A_k)) \sim \text{Dir}(\alpha G_0(A_1), \dots, \alpha G_0(A_k))$$

### Properties

- $E[G(A)] = G_0(A)$ (centered at base measure)
- $\text{Var}(G(A)) = \frac{G_0(A)(1-G_0(A))}{\alpha + 1}$ (variance controlled by $\alpha$)
- As $\alpha \to \infty$, $G \to G_0$ (concentrates at base measure)
- As $\alpha \to 0$, $G$ concentrates on a single atom

## Stick-Breaking Construction

### Sethuraman's Representation

$$G = \sum_{k=1}^{\infty} \pi_k \delta_{\theta_k}$$

where:
$$\pi_k = \beta_k \prod_{j < k} (1 - \beta_j), \quad \beta_k \sim \text{Beta}(1, \alpha)$$
$$\theta_k \sim G_0$$

The stick-breaking weights $\{\pi_k\}$ satisfy $\sum_{k=1}^\infty \pi_k = 1$ almost surely.

### Infinite Sum

Draws from a DP are **almost surely discrete** (countable sum of point masses), even if $G_0$ is continuous. This discreteness is essential for clustering but can be undesirable for density estimation.

## Chinese Restaurant Process (CRP)

### Sequential Sampling

The CRP describes the marginal distribution of $\theta_1, \dots, \theta_n$ after integrating out $G \sim DP(\alpha, G_0)$:

- Customer 1 sits at table 1, orders dish $\theta_1 \sim G_0$
- Customer $n$:
  - Sits at existing table $k$ with probability $\frac{n_k}{\alpha + n - 1}$
  - Starts a new table with probability $\frac{\alpha}{\alpha + n - 1}$ and orders $\theta_n \sim G_0$

### Exchangeability

The CRP is **exchangeable** — the order of customers does not affect the joint distribution. This is critical for MCMC inference.

### Clustering Properties

- Expected number of clusters: $E[K_n] = \alpha \log(1 + n/\alpha)$ for large $n$
- Rich-get-richer: large clusters attract more points (power-law behavior)

## Dirichlet Process Mixture (DPM)

### Model

$$y_i \sim F(\theta_i)$$
$$\theta_i \sim G$$
$$G \sim DP(\alpha, G_0)$$

### Infinite Mixture Interpretation

Marginalizing over $G$:
$$y_i \sim \sum_{k=1}^\infty \pi_k f(y_i \mid \theta_k^*)$$

The DPM is an infinite mixture model with:
- Infinite number of components (practically truncated)
- Component weights $\pi_k$ from stick-breaking
- Component parameters $\theta_k^*$ from base measure

### Inference

**Collapsed Gibbs sampler:**
- Integrate out $G$ analytically
- Sample cluster assignments using CRP
- Sample cluster parameters from conditional posterior

**Truncated stick-breaking:**
- Fix maximum $K$ (large, e.g., 50)
- Use finite approximation with stick-breaking prior

## Other Models

### Indian Buffet Process (IBP)

Prior over infinite binary matrices — each row is an observation, each column is a latent feature.
- Each observation has a finite but unbounded number of features
- Used for factor models and feature discovery

### Hierarchical Dirichlet Process (HDP)

Multiple DPs sharing a common base measure:
$$G_j \sim DP(\alpha, G_0), \quad G_0 \sim DP(\gamma, H)$$

- Group-specific distributions share atoms
- Used for topic modeling (HDP-LDA), multi-task learning

### Beta Process

Prior for survival analysis and feature selection.
$$B \sim BP(c, B_0)$$
- $B$ is a random measure on [0,1]
- Atoms correspond to features with associated probabilities

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Stick-breaking construction
def stick_breaking(alpha, n_atoms=50):
    beta = np.random.beta(1, alpha, n_atoms)
    pi = np.zeros(n_atoms)
    remaining = 1.0
    for k in range(n_atoms):
        pi[k] = beta[k] * remaining
        remaining -= pi[k]
    return pi

# Draw from DP
alpha = 2.0
G0_mean, G0_var = 0, 5
K = 50

pi = stick_breaking(alpha, K)
theta = np.random.normal(G0_mean, np.sqrt(G0_var), K)

# Sample from DP prior
n_samples = 1000
G_samples = np.random.choice(theta, size=n_samples, p=pi)

plt.figure(figsize=(12, 4))
plt.subplot(121)
plt.stem(range(1, K+1), pi)
plt.xlabel('Atom index')
plt.ylabel('Weight π_k')
plt.title(f'Stick-breaking weights (α={alpha})')

plt.subplot(122)
plt.hist(G_samples, bins=30, density=True, alpha=0.7)
xs = np.linspace(-6, 6, 200)
plt.plot(xs, stats.norm.pdf(xs, G0_mean, np.sqrt(G0_var)), 'r--', label='G₀')
plt.legend()
plt.title(f'DP(α={alpha}, G₀) draw')
plt.tight_layout()
plt.show()

# DPM for density estimation
np.random.seed(42)
true_data = np.concatenate([
    np.random.normal(-3, 0.5, 200),
    np.random.normal(1, 0.3, 300),
    np.random.normal(4, 0.8, 100)
])

# Collapsed Gibbs sampler for DPM (simplified)
def dpm_gibbs(data, alpha=1.0, n_iter=500):
    n = len(data)
    z = np.zeros(n, dtype=int)  # cluster assignments

    for _ in range(n_iter):
        for i in range(n):
            z[i] = -1  # remove i
            # Count clusters
            unique_z = np.unique(z[z >= 0])
            n_z = np.array([(z == k).sum() for k in unique_z])

            if len(unique_z) == 0:
                z[i] = 0
                continue

            # Compute cluster probabilities
            probs = np.zeros(len(unique_z) + 1)  # +1 for new cluster
            for j, k in enumerate(unique_z):
                # Likelihood p(y_i | cluster k) — conjugate Normal-Normal
                cluster_data = data[(z == k) | (np.arange(n) == i)]
                # Simple: use distance to cluster mean
                probs[j] = n_z[j] * stats.norm.pdf(data[i], loc=np.mean(cluster_data), scale=1.0)
            # New cluster probability
            probs[-1] = alpha * stats.norm.pdf(data[i], loc=0, scale=3.0)

            probs /= probs.sum()
            k_new = np.random.choice(len(probs), p=probs)
            if k_new < len(unique_z):
                z[i] = unique_z[k_new]
            else:
                z[i] = unique_z.max() + 1 if len(unique_z) > 0 else 0

    return z

z_est = dpm_gibbs(true_data, alpha=2.0)
n_clusters = len(np.unique(z_est))
print(f"Estimated clusters: {n_clusters}")

plt.figure(figsize=(10, 4))
for k in np.unique(z_est):
    plt.hist(true_data[z_est == k], bins=20, density=True, alpha=0.5, label=f'Cluster {k}')
plt.xlabel('x')
plt.ylabel('Density')
plt.legend()
plt.title('DPM Clustering Result')
plt.show()
```

## Visualization

Create a figure showing the stick-breaking construction: the sticks (bars) with their lengths representing $\pi_k$, and the cumulative sum showing $\sum_{k=1}^K \pi_k \to 1$. A second figure shows DP prior draws: multiple random distributions from $DP(\alpha, G_0)$, showing how $\alpha$ controls variability.

## Practical Considerations

- **Posterior computation:** Collapsed Gibbs samplers for DPMs are relatively simple but can be slow to converge. Use multiple chains and check $\hat{R}$.
- **Label switching:** Mixture components are unidentifiable under label permutations. The posterior mean is not meaningful — use clustering summaries (VI, Binder's loss).
- **Concentration parameter:** $\alpha$ has a strong influence on the number of clusters. Place a prior on $\alpha$ (e.g., Gamma) and learn it from data.
- **Scalability:** Standard DPM inference is $O(n^2)$ per iteration. For large $n$, use variational inference or subsampling approaches.

## References

- Ferguson, T. S. (1973). "A Bayesian analysis of some nonparametric problems"
- Sethuraman, J. (1994). "A constructive definition of Dirichlet priors"
- Blackwell, D. & MacQueen, J. B. (1973). "Ferguson distributions via Polya urn schemes"
- Neal, R. M. (2000). "Markov chain sampling methods for Dirichlet process mixture models"
- Teh, Y. W., et al. (2006). "Hierarchical Dirichlet processes"
