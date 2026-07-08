# 04.12 Monte Carlo Estimation

## Motivation
Monte Carlo methods use random sampling to compute intractable integrals. They are the workhorse of Bayesian inference (marginal likelihoods, posterior expectations), reinforcement learning (policy evaluation), and probabilistic machine learning (MC dropout, particle filters). The core insight is that expectations under complex distributions can be approximated by averaging over samples.

## Learning Objectives
- Understand the Law of Large Numbers and Central Limit Theorem for Monte Carlo estimates.
- Implement and compare variance reduction techniques: importance sampling, control variates, antithetic variates.
- Apply Monte Carlo to Bayesian marginal likelihood estimation and model comparison.
- Recognise when quasi-Monte Carlo or sequential Monte Carlo is preferred.

## Math Foundation

### Crude Monte Carlo
For a target distribution $p(x)$ and a function $f$, the expectation is approximated by:

$$\mathbb{E}_p[f(X)] \approx \frac{1}{N} \sum_{i=1}^N f(x_i), \quad x_i \sim p$$

The estimator is unbiased: $\mathbb{E}[\bar{f}_N] = \mathbb{E}_p[f]$, and its variance is $\sigma_f^2 / N$ where $\sigma_f^2 = \text{Var}_p(f)$.

### Convergence Rates
By the **Law of Large Numbers**, $\bar{f}_N \xrightarrow{a.s.} \mathbb{E}_p[f]$ as $N \to \infty$. By the **Central Limit Theorem**:

$$\sqrt{N}(\bar{f}_N - \mu) \xrightarrow{d} \mathcal{N}(0, \sigma_f^2)$$

The error decays as $O(N^{-1/2})$ regardless of the dimension of $X$ — the fundamental advantage of Monte Carlo over grid-based integration.

### Importance Sampling
When sampling from $p$ is difficult, we sample from a proposal $q$ and reweight:

$$\mathbb{E}_p[f(X)] = \mathbb{E}_q\left[ f(X) \frac{p(X)}{q(X)} \right] \approx \frac{1}{N} \sum_{i=1}^N f(x_i) w(x_i), \quad x_i \sim q$$

where $w(x) = p(x)/q(x)$ are the importance weights. The variance of the estimator depends on the mismatch between $p$ and $q$:

$$\text{Var}_q(\bar{f}) = \frac{1}{N} \left( \mathbb{E}_q[f^2 w^2] - \mu^2 \right)$$

The optimal proposal (zero variance) is $q^*(x) \propto |f(x)| p(x)$, which is typically intractable.

### Self-Normalised Importance Sampling
When $p$ is known only up to a normalising constant $p(x) = \tilde{p}(x)/Z$, use normalised weights:

$$\mathbb{E}_p[f(X)] \approx \sum_{i=1}^N f(x_i) \frac{\tilde{w}_i}{\sum_j \tilde{w}_j}, \quad \tilde{w}_i = \frac{\tilde{p}(x_i)}{q(x_i)}$$

This estimator is biased for finite $N$ but consistent as $N \to \infty$.

## Variance Reduction Techniques

### Control Variates
If we know $\mathbb{E}_q[g(X)] = \mu_g$ for some function $g$ correlated with $f$, we construct:

$$\hat{f}_{\text{CV}} = \frac{1}{N} \sum_{i=1}^N [f(x_i) - \beta (g(x_i) - \mu_g)]$$

The optimal $\beta^* = \text{Cov}(f,g) / \text{Var}(g)$ minimises the variance to $(1 - \rho_{fg}^2) \sigma_f^2/N$.

### Antithetic Variates
Generate negatively correlated pairs: if $x_i \sim p$ and $x_i' = T(x_i)$ such that $\text{Cov}(f(x_i), f(x_i')) < 0$, then:

$$\bar{f}_{\text{AV}} = \frac{1}{N} \sum_{i=1}^{N/2} \frac{f(x_i) + f(T(x_i))}{2}$$

Common choices: $T(x) = 2\mu - x$ for symmetric distributions, or use paired uniform samples $(u, 1-u)$.

### Rao-Blackwellisation
When a conditional expectation is tractable, integrate out some variables analytically:

$$\mathbb{E}[f(X,Y)] = \mathbb{E}[\mathbb{E}[f(X,Y)|X]]$$

The inner conditional expectation has lower variance than the crude MC estimate. Example: in a mixture model, integrate out the cluster assignment and sample only the parameters.

## Python Implementation

```python
import numpy as np

def crude_mc(f, sampler, n_samples=10000):
    """Crude Monte Carlo estimate of E[f(X)]."""
    samples = sampler(n_samples)
    return np.mean(f(samples))

def importance_sampling(f, p_unnorm, q_sampler, q_pdf, n_samples=10000):
    """Self-normalised importance sampling."""
    x = q_sampler(n_samples)
    w = p_unnorm(x) / q_pdf(x)
    w_norm = w / np.sum(w)
    return np.sum(f(x) * w_norm), np.sum(w_norm**2)  # estimate and ESS fraction

def control_variate_estimate(f, g, mu_g, sampler, n_samples=10000):
    """MC with control variate g (known mean mu_g)."""
    x = sampler(n_samples)
    fx = f(x)
    gx = g(x)
    beta = np.cov(fx, gx)[0, 1] / np.var(gx)
    return np.mean(fx - beta * (gx - mu_g))

def effective_sample_size(weights):
    """Kish's effective sample size."""
    w_norm = weights / np.sum(weights)
    return 1.0 / np.sum(w_norm**2)

# Example: estimate E[X^2] for X ~ N(0, 1)
np.random.seed(42)
f = lambda x: x**2

# Crude MC
crude = crude_mc(f, lambda n: np.random.randn(n), 100000)
print(f"Crude MC: {crude:.4f} (true: 1.0)")

# Importance sampling from N(0,2) to target N(0,1)
def q_sampler(n): return np.random.randn(n) * 2
def q_pdf(x): return np.exp(-x**2 / 8) / np.sqrt(8 * np.pi)
p_unnorm = lambda x: np.exp(-x**2 / 2)
is_est, ess_frac = importance_sampling(f, p_unnorm, q_sampler, q_pdf, 100000)
print(f"IS estimate: {is_est:.4f}, ESS fraction: {ess_frac:.4f}")

# Control variate using g(x)=x (mean 0) correlated with f(x)=x^2
cv_est = control_variate_estimate(f, lambda x: x, 0.0, lambda n: np.random.randn(n))
print(f"Control variate: {cv_est:.4f}")
```

## Visualization
Plot the convergence of crude MC as $N$ increases — the error decreases as $O(1/\sqrt{N})$, shown as a log-log plot with a reference line of slope $-1/2$. A second panel compares the variance of crude MC, importance sampling (with a good and bad proposal), and control variate estimators on the same integrand, using box plots across 100 repeated runs.

## Advanced Monte Carlo Methods

### Quasi-Monte Carlo
Replace random samples with deterministic low-discrepancy sequences (Sobol, Halton, Faure). The error rate improves to $O(N^{-1})$ for smooth integrands (Koksma-Hlawka inequality). QMC is particularly effective for financial pricing and Bayesian quadrature.

### Sequential Monte Carlo (Particle Filters)
For state-space models $p(x_{1:T} | y_{1:T})$, SMC maintains a weighted particle approximation that evolves through resampling and mutation steps. Used in:
- Dynamic Bayesian networks (target tracking, robotics)
- POMDPs (partially observable planning)
- Likelihood estimation for complex time series models

### Multi-Level Monte Carlo
For problems with a hierarchy of approximations (e.g., PDE solvers at different mesh resolutions), MLMC combines cheap coarse samples with expensive fine samples to achieve $O(\epsilon^{-2})$ cost with $O(\epsilon^{-2})$ variance, often reducing total cost by orders of magnitude.

## Practical Considerations

### Effective Sample Size
The ESS for importance sampling is:

$$\text{ESS} = \frac{(\sum w_i)^2}{\sum w_i^2}$$

When $\text{ESS} \ll N$, the proposal is poorly matched to the target and the estimate will have high variance. A rule of thumb: aim for $\text{ESS} > 0.1N$.

### Diagnosing Importance Sampling Failure
- **Weight degeneracy**: one weight dominates. The coefficient of variation of the weights CV$(w) > 1$ indicates degeneracy.
- **Pareto-smoothed importance sampling** (PSIS): fit a Pareto distribution to the largest weights and use the fitted shape parameter $k$ to diagnose reliability. $k > 0.7$ indicates the importance sampling estimate may be unreliable.

### When to Use What
- **Crude MC**: simple, robust, when $p$ is easy to sample from.
- **Importance sampling**: when $p$ is expensive or impossible to sample from directly.
- **Control variates**: when a correlated variable with known expectation is available.
- **Antithetic variates**: when the integrand is monotonic in the random variates.
- **QMC**: when the integrand is smooth and $d \le 20$ (QMC loses its edge in high dimensions).
- **MCMC**: when $p$ is complex and high-dimensional (see next lesson).

## References
- Robert & Casella, *Monte Carlo Statistical Methods*, 2nd ed., Springer 2004
- Owen, *Monte Carlo Theory, Methods and Examples*, ongoing monograph
- Rubinstein & Kroese, *Simulation and the Monte Carlo Method*, 3rd ed., Wiley 2016
- Vehtari et al., "Pareto Smoothed Importance Sampling," *JMLR*, 2024
- Lemieux, *Monte Carlo and Quasi-Monte Carlo Sampling*, Springer 2009
