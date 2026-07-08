# Lesson 14: Maximum A Posteriori (MAP) Estimation

## Learning Objectives

After completing this lesson, you will be able to:
- Derive the MAP estimate from posterior distribution
- Understand the relationship between MAP estimation and regularization
- Compare MAP with MLE in terms of bias, variance, and invariance
- Identify when MAP estimation is preferable to MLE
- Implement MAP estimation for common models

## Bayesian Framework

### Setup

In Bayesian inference, we treat the parameter $\theta$ as a random variable with **prior distribution** $\pi(\theta)$. Given data $x$, the **posterior distribution** is:

$$\pi(\theta \mid x) = \frac{f(x \mid \theta) \pi(\theta)}{m(x)} \propto f(x \mid \theta) \pi(\theta)$$

where $m(x) = \int f(x \mid \theta) \pi(\theta) d\theta$ is the marginal likelihood.

## MAP Estimate

The **Maximum A Posteriori** estimate is the mode of the posterior:

$$\hat{\theta}_{\text{MAP}} = \arg\max_{\theta} \pi(\theta \mid x) = \arg\max_{\theta} [\log f(x \mid \theta) + \log \pi(\theta)]$$

The marginal likelihood $m(x)$ is constant with respect to $\theta$, so it does not affect the maximization.

### Connection to Regularization

MAP estimation reveals the regularization interpretation of common priors:

| Prior | $\log \pi(\theta)$ | Regularization | Penalty |
|-------|---------------------|----------------|---------|
| Normal$(0, \tau^2)$ | $-\frac{1}{2\tau^2} \|\theta\|_2^2 + \text{const}$ | L2 (Ridge) | $\lambda \|\theta\|_2^2$, $\lambda = \frac{1}{2\tau^2}$ |
| Laplace$(0, b)$ | $-\frac{1}{b} \|\theta\|_1 + \text{const}$ | L1 (Lasso) | $\lambda \|\theta\|_1$, $\lambda = \frac{1}{b}$ |
| Horseshoe | Complex shrinkage profile | Adaptive shrinkage | Non-convex penalty |

### Example: Linear Regression

For $y_i = \theta^\top x_i + \epsilon_i$ with $\epsilon_i \sim \mathcal{N}(0, \sigma^2)$:

- **MLE (no prior):** Minimizes $\|y - X\theta\|_2^2$
- **MAP with Normal prior (Ridge):** Minimizes $\|y - X\theta\|_2^2 + \lambda \|\theta\|_2^2$, closed form:
  $$\hat{\theta}_{\text{ridge}} = (X^\top X + \lambda I)^{-1} X^\top y$$

- **MAP with Laplace prior (Lasso):** Minimizes $\|y - X\theta\|_2^2 + \lambda \|\theta\|_1$, solved via coordinate descent

## Examples

### Beta-Binomial

Model: $X \sim \text{Binomial}(n, \theta)$, prior $\theta \sim \text{Beta}(\alpha, \beta)$:

Posterior: $\theta \mid x \sim \text{Beta}(\alpha + x, \beta + n - x)$

$$\hat{\theta}_{\text{MAP}} = \frac{\alpha + x - 1}{\alpha + \beta + n - 2}$$
$$\hat{\theta}_{\text{MLE}} = \frac{x}{n}$$

When $\alpha = \beta = 1$ (Uniform prior), $\hat{\theta}_{\text{MAP}} = x/n = \hat{\theta}_{\text{MLE}}$.

### Normal-Normal

Model: $X_i \sim \mathcal{N}(\theta, \sigma^2)$, prior $\theta \sim \mathcal{N}(\mu_0, \tau^2)$:

Posterior: $\theta \mid x \sim \mathcal{N}(\mu_n, \sigma_n^2)$ where:
$$\mu_n = \frac{\frac{n}{\sigma^2}\bar{x} + \frac{1}{\tau^2}\mu_0}{\frac{n}{\sigma^2} + \frac{1}{\tau^2}}, \quad \sigma_n^2 = \frac{1}{\frac{n}{\sigma^2} + \frac{1}{\tau^2}}$$

The MAP is $\mu_n$ — a **weighted average** of the sample mean and prior mean.

### Bayesian Logistic Regression

No closed form. The MAP is found via optimization:
$$\ell(\theta) = \sum_{i=1}^n [y_i \log \sigma(\theta^\top x_i) + (1-y_i) \log(1-\sigma(\theta^\top x_i))] - \frac{\lambda}{2} \|\theta\|_2^2$$

## Comparison with MLE

| Aspect | MLE | MAP |
|--------|-----|-----|
| Prior knowledge | Not used | Incorporated via prior |
| Shrinkage | None | Shrinks estimate toward prior mean |
| Uncertainty | Fisher information only | Posterior includes prior uncertainty |
| Reparametrization invariance | Invariant | Not invariant |
| Asymptotics | Unbiased, efficient | Biased (shrinks toward prior) |
| Small-sample behavior | Can be extreme | More stable (shrinkage) |
| Bayesian interpretation | Limiting case as prior → flat | Mode of posterior |

### Bias-Variance Tradeoff

MAP adds bias (toward the prior) but reduces variance. This parallels the bias-variance tradeoff in frequentist shrinkage estimation.

## MAP Invariance Issue

Unlike MLE, MAP is **not invariant under reparametrization**. If $\phi = g(\theta)$ and we compute the MAP for $\phi$ using the transformed prior, the result is not generally $g(\hat{\theta}_{\text{MAP}})$.

**Reason:** The mode transforms with the Jacobian: $f_\Phi(\phi) = f_\Theta(g^{-1}(\phi)) \cdot |dg^{-1}/d\phi|$, so the mode changes.

This is a significant limitation — MAP estimates depend on how the model is parameterized.

## Limitations of MAP

1. **No uncertainty quantification:** MAP is a point estimate, not a full posterior distribution
2. **Misleading for multimodal posteriors:** The mode may represent a tiny probability mass
3. **Reparametrization dependence:** Different parameterizations give different answers
4. **Prior sensitivity:** Results depend on prior choice, especially with small data

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats, optimize

# Beta-Binomial MAP
alpha, beta = 2, 5  # prior parameters
n_trials, x_success = 20, 15

theta = np.linspace(0, 1, 200)
prior = stats.beta(alpha, beta).pdf(theta)
likelihood = stats.binom(n_trials, theta).pmf(x_success)
posterior = stats.beta(alpha + x_success, beta + n_trials - x_success).pdf(theta)

theta_map = (alpha + x_success - 1) / (alpha + beta + n_trials - 2)
theta_mle = x_success / n_trials

plt.figure(figsize=(10, 5))
plt.plot(theta, likelihood / likelihood.max(), '--', label='Likelihood (normalized)')
plt.plot(theta, prior / prior.max(), ':', label='Prior (normalized)')
plt.plot(theta, posterior / posterior.max(), '-', label='Posterior (normalized)')
plt.axvline(theta_mle, color='g', linestyle='--', label=f'MLE = {theta_mle:.3f}')
plt.axvline(theta_map, color='r', linestyle='--', label=f'MAP = {theta_map:.3f}')
plt.xlabel('θ')
plt.ylabel('Density (normalized)')
plt.legend()
plt.title('Beta-Binomial: MLE vs MAP')
plt.show()

# Bayesian logistic regression MAP
np.random.seed(42)
n, p = 100, 3
X = np.random.randn(n, p)
true_beta = np.array([0.5, -1.0, 0.0])
y = 1 / (1 + np.exp(-X @ true_beta)) > np.random.uniform(0, 1, n)

def neg_log_posterior(beta, lam=1.0):
    """Negative log posterior for Bayesian logistic regression."""
    logit = X @ beta
    ll = np.sum(y * logit - np.log(1 + np.exp(logit)))
    log_prior = -0.5 * lam * np.sum(beta**2)
    return -(ll + log_prior)

result = optimize.minimize(neg_log_posterior, x0=np.zeros(p), method='BFGS',
                           args=(1.0,))
beta_map = result.x
print(f"MAP estimates: {beta_map}")
print(f"True values:   {true_beta}")

# Comparison with MLE (no prior) - note: unregularized may differ
result_mle = optimize.minimize(
    lambda b: -np.sum(y * (X @ b) - np.log(1 + np.exp(X @ b))),
    x0=np.zeros(p), method='BFGS')
print(f"MLE estimates:  {result_mle.x}")
```

## Visualization

Create a three-panel figure: (1) Beta-Binomial posterior with MLE and MAP marked, showing shrinkage toward prior mean; (2) Ridge regression coefficient paths as $\lambda$ varies, illustrating MAP's bias-variance tradeoff; (3) Comparison of MLE and MAP for small sample sizes ($n=5, 10, 30$) showing MAP's improved stability.

## Practical Considerations

- **MAP as a compromise:** MAP is useful when you want to incorporate prior knowledge but don't need full Bayesian inference (posterior uncertainty). It's computationally cheaper than MCMC.
- **Uninformative priors:** When using flat (improper) priors, MAP = MLE. But improper priors can cause improper posteriors.
- **Jeffreys prior:** The prior $\pi(\theta) \propto \sqrt{I(\theta)}$ is invariant under reparametrization. MAP with Jeffreys prior is reparametrization-invariant.
- **Hierarchical MAP:** For hierarchical models, MAP is computed via empirical Bayes or variational inference.

## References

- Berger, J. O. (1985). *Statistical Decision Theory and Bayesian Analysis*
- Gelman, A., et al. (2013). *Bayesian Data Analysis*
- Murphy, K. P. (2012). *Machine Learning: A Probabilistic Perspective*
