# 04.13 Markov Chain Monte Carlo (MCMC)

## Motivation
MCMC methods construct a Markov chain whose stationary distribution is the target posterior, enabling sampling from complex, high-dimensional distributions where direct sampling is impossible. They are the primary inference engine for Bayesian models, from hierarchical linear models to deep probabilistic programs.

## Learning Objectives
- Implement and analyse the Metropolis–Hastings algorithm.
- Derive Gibbs sampling as a special case of Metropolis–Hastings.
- Understand Hamiltonian Monte Carlo and the No-U-Turn Sampler.
- Diagnose convergence via trace plots, Gelman–Rubin $\hat{R}$, and effective sample size.

## Math Foundation

### Metropolis–Hastings Algorithm
Goal: sample from target $\pi(x) = \tilde{\pi}(x)/Z$ where $Z$ may be unknown. Given current state $x$, propose $x' \sim q(\cdot|x)$ and accept with probability:

$$\alpha(x, x') = \min\left(1, \frac{\tilde{\pi}(x') q(x|x')}{\tilde{\pi}(x) q(x'|x)}\right)$$

This satisfies detailed balance with respect to $\pi$:

$$\pi(x) q(x'|x) \alpha(x,x') = \pi(x') q(x|x') \alpha(x',x)$$

### Common Proposal Distributions
- **Random walk Metropolis**: $q(x'|x) = \mathcal{N}(x, \sigma^2 I)$. The scale $\sigma$ strongly affects efficiency: too small → high acceptance but slow exploration; too large → low acceptance, chain sticks.
- **Independent Metropolis**: $q(x'|x) = q(x')$ (proposal independent of current state). Simpler but less efficient; requires $q$ to be a good approximation of $\pi$.
- **Langevin-adjusted proposals**: $q(x'|x) = \mathcal{N}(x + \frac{\epsilon^2}{2} \nabla \log \pi(x), \epsilon^2 I)$. Uses gradient information to propose moves toward high-probability regions.

### Gibbs Sampling
For a multivariate target $\pi(x_1, \dots, x_d)$, sample each coordinate in turn from its full conditional:

$$x_i^{(t+1)} \sim \pi(x_i | x_1^{(t+1)}, \dots, x_{i-1}^{(t+1)}, x_{i+1}^{(t)}, \dots, x_d^{(t)})$$

Gibbs sampling is a special case of Metropolis–Hastings where the proposal for coordinate $i$ is the full conditional, giving acceptance probability $\alpha = 1$. It is particularly effective when the full conditionals are tractable (e.g., conditionally conjugate models like LDA, Gaussian mixture models).

## Hamiltonian Monte Carlo

### Physics Analogy
HMC introduces auxiliary momentum variables $r \sim \mathcal{N}(0, M)$ and simulates Hamiltonian dynamics on the joint state $(x, r)$ with energy:

$$H(x, r) = -\log \pi(x) + \frac12 r^\top M^{-1} r$$

Hamilton's equations:

$$\frac{dx}{dt} = M^{-1} r, \quad \frac{dr}{dt} = \nabla_x \log \pi(x)$$

Integrating these dynamics (e.g., via leapfrog discretisation) produces proposals that are far from the current state but have high acceptance probability because the Hamiltonian is approximately conserved.

### Leapfrog Integration
The discrete-time dynamics that preserve the symplectic structure:

$$r(t + \epsilon/2) = r(t) + \frac{\epsilon}{2} \nabla \log \pi(x(t))$$
$$x(t + \epsilon) = x(t) + \epsilon M^{-1} r(t + \epsilon/2)$$
$$r(t + \epsilon) = r(t + \epsilon/2) + \frac{\epsilon}{2} \nabla \log \pi(x(t + \epsilon))$$

After $L$ leapfrog steps, the proposed state $(x', r')$ is accepted with probability $\min(1, \exp(H(x,r) - H(x',r')))$.

### No-U-Turn Sampler (NUTS)
Choosing the integration time $L$ adaptively: NUTS runs the leapfrog integrator forward and backward until the trajectory starts to turn back (a "U-turn"), then samples from the resulting path. This eliminates the need to tune $L$ and is the default sampler in Stan and PyMC.

## Python Implementation

```python
import numpy as np
from scipy.stats import multivariate_normal

def metropolis_hastings(log_target, proposal, n_samples=10000, x0=0.0, proposal_std=1.0):
    """Metropolis-Hastings with Gaussian random walk proposal."""
    x = x0
    samples = np.zeros(n_samples)
    accepted = 0
    
    for i in range(n_samples):
        x_prop = x + proposal_std * np.random.randn(*np.atleast_1d(x).shape)
        log_alpha = log_target(x_prop) - log_target(x)
        if np.log(np.random.rand()) < log_alpha:
            x = x_prop
            accepted += 1
        samples[i] = x
    
    return samples, accepted / n_samples

def gibbs_gmm(data, n_components, n_samples=2000):
    """Gibbs sampling for a Gaussian mixture model with known variance.
    Full conditionals are tractable: conjugate Dirichlet-Normal-Wishart."""
    n, d = data.shape
    # initialise
    z = np.random.randint(0, n_components, size=n)
    mu = np.random.randn(n_components, d) * 2
    pi = np.ones(n_components) / n_components
    
    samples_mu = np.zeros((n_samples, n_components, d))
    samples_pi = np.zeros((n_samples, n_components))
    
    for t in range(n_samples):
        # sample cluster assignments
        log_probs = np.log(pi[None, :]) - 0.5 * np.sum((data[:, None, :] - mu[None, :, :])**2, axis=2)
        log_probs -= log_probs.max(axis=1, keepdims=True)  # stability
        probs = np.exp(log_probs)
        probs /= probs.sum(axis=1, keepdims=True)
        z = np.array([np.random.choice(n_components, p=probs[i]) for i in range(n)])
        
        # sample pi
        counts = np.bincount(z, minlength=n_components)
        pi = np.random.dirichlet(counts + 1.0)
        
        # sample mu (conjugate normal prior => normal posterior)
        prior_var = 5.0
        for k in range(n_components):
            mask = z == k
            nk = mask.sum()
            if nk > 0:
                x_mean = data[mask].mean(axis=0)
                post_var = 1.0 / (nk + 1.0/prior_var)
                post_mean = post_var * (nk * x_mean + 0)
                mu[k] = np.random.randn(d) * np.sqrt(post_var) + post_mean
            else:
                mu[k] = np.random.randn(d) * np.sqrt(prior_var)
        
        samples_mu[t] = mu
        samples_pi[t] = pi
    
    return samples_mu, samples_pi

# Example: N(0, 1) target with random walk MH
log_target = lambda x: -0.5 * x**2
samples, acc = metropolis_hastings(log_target, None, n_samples=10000, proposal_std=1.5)
print(f"Acceptance rate: {acc:.3f}")
print(f"Sample mean: {samples.mean():.3f} (true: 0), std: {samples.std():.3f} (true: 1)")
```

## Visualization
Plot trace plots for a 2D Gaussian target with random walk MH (high autocorrelation) and HMC (low autocorrelation). Overlay the empirical autocorrelation function for both methods — HMC decorrelates much faster. A second panel shows 2D scatter plots of the posterior samples with overlaid contour of the true target, showing better coverage from HMC.

## Convergence Diagnostics

### Trace Plots
Visualise the sampled values over iterations. Look for:
- **Stable mean and variance**: the chain should meander around a constant mean.
- **No trend or drift**: low-frequency oscillations indicate incomplete burn-in.
- **Good mixing**: the chain traverses the full support, not stuck in one region.

### Gelman–Rubin $\hat{R}$
Run $M \ge 4$ chains from overdispersed starting points. The potential scale reduction factor is:

$$\hat{R} = \sqrt{\frac{\text{Var}(\text{pooled})}{\text{Var}(\text{within})}}$$

Values $\hat{R} < 1.01$ indicate convergence. $\hat{R} > 1.1$ suggests the chains have not yet converged or the target has multiple modes.

### Effective Sample Size (ESS)
Due to autocorrelation, $N$ MCMC samples contain less information than $N$ independent samples:

$$\text{ESS} = \frac{N}{1 + 2 \sum_{k=1}^\infty \rho_k}$$

where $\rho_k$ is the autocorrelation at lag $k$. ESS $< N/10$ suggests poor mixing. Stan reports ESS separately for the bulk (mean) and tails (extreme quantiles).

## Practical Considerations

### Burn-in and Thinning
- **Burn-in**: discard the first $B$ samples (e.g., $B = N/2$) to remove dependence on the initial state. However, if the chain converges quickly, burn-in wastes samples.
- **Thinning**: keep every $k$-th sample to reduce autocorrelation. Often unnecessary if storage is not a concern — better to keep all samples and accept the autocorrelation.

### Adaptive MCMC
- **Adaptive Metropolis**: adapt the proposal covariance using the empirical covariance of past samples (Roberts & Rosenthal 2009).
- **Robust adaptive Metropolis**: uses a scaled identity matrix if the chain is short.
- **Warning**: adaptation must satisfy **diminishing adaptation** (the adaptation amount $\to 0$ as $t \to \infty$) to preserve ergodicity.

### Tuning Guidelines
| Algorithm | Key Parameter | Target Acceptance |
|-----------|--------------|-------------------|
| Random walk MH | Proposal std $\sigma$ | 0.234 (optimal) |
| MALA | Step size $\epsilon$ | 0.574 (optimal) |
| HMC | Step size $\epsilon$, steps $L$ | $\epsilon$ tuned to 0.65-0.8 |
| NUTS | Target acceptance $\delta$ | 0.8 (default in Stan) |

## References
- Brooks, Gelman, Jones & Meng, *Handbook of Markov Chain Monte Carlo*, CRC Press 2011
- Betancourt, "A Conceptual Introduction to Hamiltonian Monte Carlo," *arXiv:1701.02434*, 2017
- Gelman et al., *Bayesian Data Analysis*, 3rd ed., CRC Press 2013
- Hoffman & Gelman, "The No-U-Turn Sampler: Adaptively Setting Path Lengths in Hamiltonian Monte Carlo," *JMLR*, 2014
- Roberts & Rosenthal, "Optimal Scaling of Random Walk Metropolis Algorithms," *Bernoulli*, 2001
