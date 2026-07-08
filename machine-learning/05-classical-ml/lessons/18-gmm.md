# Lesson 05.18: Gaussian Mixture Models

## Learning Objectives
- Derive EM algorithm for GMM parameter estimation
- Implement E-step (responsibilities) and M-step (parameter updates)
- Understand model selection via BIC/AIC
- Analyze covariance types and their tradeoffs

## Model Definition
A Gaussian Mixture Model represents the data as a convex combination of $K$ Gaussian components:

$$p(x) = \sum_{k=1}^K \pi_k \mathcal{N}(x \mid \mu_k, \Sigma_k)$$

where $\sum_{k=1}^K \pi_k = 1$, $\pi_k \geq 0$, and $\mathcal{N}(x \mid \mu, \Sigma) = \frac{1}{(2\pi)^{d/2}|\Sigma|^{1/2}} \exp\left(-\frac12 (x-\mu)^\top \Sigma^{-1} (x-\mu)\right)$

**Latent variable interpretation**: Each observation $x_i$ has a latent component assignment $z_i \in \{1, \dots, K\}$:
- $P(z_i = k) = \pi_k$
- $x_i \mid z_i = k \sim \mathcal{N}(\mu_k, \Sigma_k)$

## EM Algorithm for GMM

### E-Step (Expectation)
Compute responsibilities (posterior probability that point $i$ belongs to component $k$):

$$\gamma_{ik} = P(z_i = k \mid x_i, \theta) = \frac{\pi_k \mathcal{N}(x_i \mid \mu_k, \Sigma_k)}{\sum_{j=1}^K \pi_j \mathcal{N}(x_i \mid \mu_j, \Sigma_j)}$$

### M-Step (Maximization)
Update parameters using weighted statistics:

$$\pi_k^{\text{new}} = \frac{1}{n} \sum_{i=1}^n \gamma_{ik}$$

$$\mu_k^{\text{new}} = \frac{\sum_{i=1}^n \gamma_{ik} x_i}{\sum_{i=1}^n \gamma_{ik}}$$

$$\Sigma_k^{\text{new}} = \frac{\sum_{i=1}^n \gamma_{ik} (x_i - \mu_k^{\text{new}})(x_i - \mu_k^{\text{new}})^\top}{\sum_{i=1}^n \gamma_{ik}}$$

### Log-Likelihood Monitoring
$$\log L(\theta) = \sum_{i=1}^n \log \left( \sum_{k=1}^K \pi_k \mathcal{N}(x_i \mid \mu_k, \Sigma_k) \right)$$

Monotonically increasing under EM (guaranteed). Stop when improvement < tolerance.

## Covariance Types

| Type | Parameters | Shape | Flexibility |
|------|-----------|-------|-------------|
| `spherical` | $\Sigma_k = \sigma_k^2 I$ | $K$ | Circles |
| `diag` | $\Sigma_k = \text{diag}(\sigma_{k1}^2, \dots, \sigma_{kd}^2)$ | $Kd$ | Axis-aligned ellipses |
| `tied` | $\Sigma_k = \Sigma$ (shared) | $d(d+1)/2$ | Same shape/orientation |
| `full` | $\Sigma_k$ unrestricted | $Kd(d+1)/2$ | Arbitrary ellipses |

More flexible types need more data and are more prone to singularities.

## Model Selection

### Bayesian Information Criterion (BIC)
$$\text{BIC} = -2 \log L + k_p \log n$$

$k_p$ = number of free parameters:
- Spherical: $K(d+2) - 1$
- Diag: $K(2d+1) - 1$
- Tied: $Kd + d(d+1)/2 + K - 1$
- Full: $Kd + Kd(d+1)/2 + K - 1$

Lower BIC is better. BIC penalizes complexity more than AIC.

### Variational GMM (VB-GMM)
Place conjugate priors (NIW on $\mu_k, \Sigma_k$, Dirichlet on $\pi$):
- Automatically prunes unnecessary components
- Provides full posterior over parameters
- More stable than MLE for small $n$

## Code: GMM from Scratch

```python
import numpy as np
from scipy.stats import multivariate_normal

class GMM:
    def __init__(self, k=3, covariance_type='full', max_iter=200, tol=1e-4):
        self.k = k
        self.covariance_type = covariance_type
        self.max_iter = max_iter
        self.tol = tol

    def fit(self, X):
        n, d = X.shape
        self.weights = np.ones(self.k) / self.k
        idx = np.random.choice(n, self.k, replace=False)
        self.means = X[idx].copy()
        if self.covariance_type == 'full':
            self.covs = np.array([np.cov(X.T) + 1e-6 * np.eye(d) for _ in range(self.k)])
        elif self.covariance_type == 'diag':
            self.covs = np.array([np.diag(np.var(X, axis=0)) + 1e-6 for _ in range(self.k)])

        log_likelihood = -np.inf
        for iteration in range(self.max_iter):
            # E-step
            gamma = np.zeros((n, self.k))
            for k in range(self.k):
                gamma[:, k] = self.weights[k] * multivariate_normal.pdf(X, self.means[k], self.covs[k])
            gamma /= gamma.sum(axis=1, keepdims=True) + 1e-300

            # M-step
            Nk = gamma.sum(axis=0)
            self.weights = Nk / n
            self.means = (gamma.T @ X) / Nk[:, None]
            if self.covariance_type == 'full':
                for k in range(self.k):
                    diff = X - self.means[k]
                    self.covs[k] = (gamma[:, k, None] * diff).T @ diff / Nk[k] + 1e-6 * np.eye(d)

            # Check convergence
            new_log_likelihood = np.sum(np.log(gamma.sum(axis=1) + 1e-300))
            if abs(new_log_likelihood - log_likelihood) < self.tol:
                break
            log_likelihood = new_log_likelihood
        return self
```

## Practical Considerations
- **Singularities**: When $\Sigma_k$ becomes singular (e.g., component collapses to one point), add small regularization term
- **Initialization**: Multiple restarts (5-20) with different random seeds; use k-means for warm-start
- **High $d$**: Full covariance is $O(d^2)$ per component — use diagonal or factor analysis for $d > 100$
- **Large $n$**: Use online EM (incremental updates) or mini-batch training
- **Non-Gaussian data**: GMM can still approximate complex densities with enough components
- **Identifiability**: Components can be relabeled (permutation symmetry) — add small prior for identifiability

## Key Properties
- Soft clustering (probabilistic memberships)
- Can model complex, multi-modal distributions
- EM converges to local optimum (not global)
- $O(nKd^2)$ per iteration for full covariance
- Generative model: can sample new data from fitted distribution

## References
- Dempster, Laird, Rubin, "Maximum Likelihood from Incomplete Data via the EM Algorithm" (JRSS-B, 1977)
- Bishop, "Pattern Recognition and Machine Learning", Ch. 9
- McLachlan & Peel, "Finite Mixture Models" (2000)
- Murphy, "Probabilistic Machine Learning", Ch. 21
