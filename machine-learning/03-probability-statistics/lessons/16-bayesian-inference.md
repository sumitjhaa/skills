# Lesson 16: Bayesian Inference

## Learning Objectives

After completing this lesson, you will be able to:
- Apply Bayes' theorem to compute posterior distributions
- Work with conjugate prior-likelihood pairs
- Compute prior and posterior predictive distributions
- Understand the philosophical differences between Bayesian and frequentist inference
- Implement Bayesian inference for standard models

## Bayes' Theorem

### Core Equation

$$\pi(\theta \mid x) = \frac{f(x \mid \theta) \pi(\theta)}{m(x)}$$

Where:
- $\pi(\theta)$: **prior** — beliefs about $\theta$ before seeing data
- $f(x \mid \theta)$: **likelihood** — probability of data given $\theta$
- $m(x) = \int f(x \mid \theta) \pi(\theta) d\theta$: **marginal likelihood** (evidence)
- $\pi(\theta \mid x)$: **posterior** — updated beliefs after seeing data

### Sequential Updating

Bayesian updating is sequential: the posterior after one batch of data becomes the prior for the next batch.

If we have two independent datasets $x_1$ and $x_2$:
$$\pi(\theta \mid x_1, x_2) \propto f(x_2 \mid \theta) \cdot f(x_1 \mid \theta) \cdot \pi(\theta) = f(x_2 \mid \theta) \cdot \pi(\theta \mid x_1)$$

This sequential property makes Bayesian inference natural for online learning.

## Conjugate Models

A prior is **conjugate** to a likelihood if the posterior belongs to the same family as the prior.

### Beta-Binomial

$$X \mid \theta \sim \text{Binomial}(n, \theta)$$
$$\theta \sim \text{Beta}(\alpha, \beta)$$
$$\theta \mid x \sim \text{Beta}(\alpha + x, \beta + n - x)$$

**Interpretation:** $\alpha$ and $\beta$ are "prior successes" and "prior failures". The posterior updates these counts.

### Gamma-Poisson

$$X_i \mid \lambda \sim \text{Poisson}(\lambda)$$
$$\lambda \sim \text{Gamma}(\alpha, \beta)$$
$$\lambda \mid x \sim \text{Gamma}(\alpha + \sum x_i, \beta + n)$$

### Normal-Normal

$$X_i \mid \mu \sim \mathcal{N}(\mu, \sigma^2) \text{ (known } \sigma^2)$$
$$\mu \sim \mathcal{N}(\mu_0, \tau^2)$$
$$\mu \mid x \sim \mathcal{N}\left(\frac{\mu_0/\tau^2 + n\bar{x}/\sigma^2}{1/\tau^2 + n/\sigma^2}, \frac{1}{1/\tau^2 + n/\sigma^2}\right)$$

The posterior mean is a **precision-weighted average** of prior mean and sample mean.

### Dirichlet-Multinomial

$$X \mid \theta \sim \text{Multinomial}(n, \theta)$$
$$\theta \sim \text{Dirichlet}(\alpha)$$
$$\theta \mid x \sim \text{Dirichlet}(\alpha + x)$$

## Predictive Distributions

### Prior Predictive

$$m(x) = \int f(x \mid \theta) \pi(\theta) d\theta$$

This is the marginal likelihood — the probability of the data averaged over the prior. Used for model comparison (Bayes factors).

### Posterior Predictive

For a new observation $\tilde{x}$:
$$f(\tilde{x} \mid x) = \int f(\tilde{x} \mid \theta) \pi(\theta \mid x) d\theta$$

The posterior predictive accounts for **parameter uncertainty** — it averages predictions over all plausible $\theta$ values, weighted by their posterior probability.

### Posterior Predictive Examples

- **Beta-Binomial:** Beta-Binomial distribution
- **Gamma-Poisson:** Negative Binomial distribution
- **Normal-Normal:** Normal distribution with variance $\sigma^2 + \sigma_n^2$

## Bayesian vs Frequentist Inference

| Aspect | Bayesian | Frequentist |
|--------|----------|-------------|
| Parameter | Random variable (has distribution) | Fixed constant |
| Probability | Degree of belief (subjective) | Long-run frequency |
| Inference | Posterior distribution | Sampling distribution |
| Uncertainty | Credible interval (e.g., 95% posterior interval) | Confidence interval (covers in 95% of repeated samples) |
| Prior | Required | Not used |
| Interpretation of 95% interval | "95% probability that $\theta$ lies in this interval" | "95% of such intervals contain the true $\theta$" |
| Model comparison | Bayes factors | Likelihood ratio tests |
| Computation | MCMC, VI, conjugate updates | Optimization, bootstrap |

### When They Agree

With large samples and uninformative priors, Bayesian and frequentist results converge (Bernstein-von Mises theorem):
$$\pi(\theta \mid x) \approx \mathcal{N}(\hat{\theta}_{\text{MLE}}, n^{-1} I(\hat{\theta}_{\text{MLE}})^{-1})$$

## Bayesian Computation

### Conjugate Models

Closed-form posteriors, exact inference. Limited to a small set of models.

### Markov Chain Monte Carlo (MCMC)

Samples from the posterior using a Markov chain whose stationary distribution is the posterior.
- **Metropolis-Hastings:** Propose-and-accept algorithm
- **Gibbs sampling:** Sample each parameter conditional on all others
- **Hamiltonian Monte Carlo:** Uses gradient information for efficient sampling
- **NUTS:** No-U-Turn Sampler, automated HMC

### Variational Inference

Approximate the posterior with a simpler distribution (e.g., factorized Gaussian) by minimizing KL divergence:
$$q^*(\theta) = \arg\min_q \text{KL}(q(\theta) \| \pi(\theta \mid x))$$

### Laplace Approximation

Approximate the posterior as Gaussian around the MAP:
$$\pi(\theta \mid x) \approx \mathcal{N}(\hat{\theta}_{\text{MAP}}, H(\hat{\theta}_{\text{MAP}})^{-1})$$

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Beta-Binomial: coin flipping
alpha, beta = 2, 2  # prior: Beta(2,2) — symmetric, weak
n_flips = 20
n_heads = 13

# Posterior
alpha_post = alpha + n_heads
beta_post = beta + n_flips - n_heads

theta_grid = np.linspace(0, 1, 500)
prior = stats.beta(alpha, beta).pdf(theta_grid)
posterior = stats.beta(alpha_post, beta_post).pdf(theta_grid)

# Posterior predictive: P(next flip = heads)
pred_heads = alpha_post / (alpha_post + beta_post)
print(f"P(next flip = heads) = {pred_heads:.4f}")

# 95% credible interval
ci_low, ci_high = stats.beta(alpha_post, beta_post).ppf([0.025, 0.975])
print(f"95% credible interval: [{ci_low:.3f}, {ci_high:.3f}]")

plt.figure(figsize=(10, 5))
plt.plot(theta_grid, prior, 'b:', label=f'Beta({alpha},{beta}) prior')
plt.plot(theta_grid, posterior, 'r-', label=f'Beta({alpha_post},{beta_post}) posterior')
plt.fill_between(theta_grid, posterior, where=(theta_grid >= ci_low) & (theta_grid <= ci_high),
                 color='r', alpha=0.3, label='95% CI')
plt.axvline(n_heads/n_flips, color='g', linestyle='--', label=f'MLE = {n_heads/n_flips:.3f}')
plt.xlabel('θ')
plt.ylabel('Density')
plt.legend()
plt.title('Bayesian Inference: Beta-Binomial')
plt.show()

# Normal-Normal: sequential updating
mu_0, tau2 = 0, 10  # prior mean, variance
sigma2 = 4  # known data variance
data = np.random.normal(5, np.sqrt(sigma2), size=10)

def update_normal_normal(mu_n, tau2_n, x):
    """Sequential update for Normal-Normal model."""
    w = tau2_n / (tau2_n + sigma2)  # shrinkage factor
    mu_n1 = mu_n + w * (x - mu_n)
    tau2_n1 = (1 - w) * tau2_n
    return mu_n1, tau2_n1

mu_n, tau2_n = mu_0, tau2
history = [(mu_n, np.sqrt(tau2_n))]
for x in data:
    mu_n, tau2_n = update_normal_normal(mu_n, tau2_n, x)
    history.append((mu_n, np.sqrt(tau2_n)))

history = np.array(history)
plt.figure(figsize=(10, 4))
plt.errorbar(range(len(history)), history[:, 0], yerr=2*history[:, 1],
             fmt='o-', capsize=3)
plt.axhline(y=np.mean(data), color='g', linestyle='--', label=f'Sample mean = {np.mean(data):.2f}')
plt.xlabel('Data points seen')
plt.ylabel('Posterior mean ± 2σ')
plt.legend()
plt.title('Sequential Bayesian Updating: Normal-Normal')
plt.show()
```

## Visualization

Create a four-panel figure showing Bayesian updating: (1) Prior and posterior for Beta-Binomial with increasing data; (2) Sequential Normal-Normal updating with shrinking credible intervals; (3) Prior vs posterior predictive distributions; (4) Comparison of 95% credible interval and 95% confidence interval for a Normal mean, illustrating the different interpretations.

## Practical Considerations

- **Prior sensitivity:** Always check how sensitive your conclusions are to prior choice. Use sensitivity analysis with different priors.
- **Proper vs improper priors:** An improper prior (e.g., Uniform on $\mathbb{R}$) can yield a proper posterior if enough data is available. But improper priors can also yield improper posteriors.
- **Model checking:** Use posterior predictive checks — simulate data from the posterior predictive and compare to observed data. Systematic discrepancies suggest model misspecification.
- **Bayesian computation is hard:** For complex models, MCMC can be slow and convergence is difficult to diagnose. Consider variational inference for large-scale problems.
- **Reporting:** Report the full posterior (or summaries like mean, median, credible intervals), not just MAP estimates.

## References

- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd ed.)
- McElreath, R. (2020). *Statistical Rethinking*
- Berger, J. O. (1985). *Statistical Decision Theory and Bayesian Analysis*
- Bernardo, J. M. & Smith, A. F. M. (2000). *Bayesian Theory*
