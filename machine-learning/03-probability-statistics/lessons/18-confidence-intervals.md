# Lesson 18: Confidence Intervals

## Learning Objectives

After completing this lesson, you will be able to:
- Construct and interpret frequentist confidence intervals
- Construct and interpret Bayesian credible intervals
- Distinguish between confidence and credible intervals
- Apply bootstrap methods for nonparametric intervals
- Compute intervals for common parameters (mean, proportion, regression coefficients)

## Frequentist Confidence Intervals

### Definition

A $100(1-\alpha)\%$ confidence interval for $\theta$ is a random interval $[L(X), U(X)]$ such that:
$$P_\theta(L(X) \leq \theta \leq U(X)) = 1 - \alpha \quad \forall \theta \in \Theta$$

**Key:** The probability refers to the **procedure** (across repeated samples), not the specific interval. For a single realized interval $[l, u]$, either $\theta \in [l, u]$ or not — there is no probability statement.

### Pivotal Quantities

A **pivot** $Q(X, \theta)$ has a distribution that does not depend on $\theta$ (or any nuisance parameters).

**Example (Normal mean, known variance):**
$$Q = \frac{\sqrt{n}(\bar{X} - \mu)}{\sigma} \sim \mathcal{N}(0, 1)$$

Find $z_{\alpha/2}$ such that $P(-z_{\alpha/2} \leq Q \leq z_{\alpha/2}) = 1 - \alpha$, then:
$$P\left(\bar{X} - z_{\alpha/2}\frac{\sigma}{\sqrt{n}} \leq \mu \leq \bar{X} + z_{\alpha/2}\frac{\sigma}{\sqrt{n}}\right) = 1 - \alpha$$

### Common Intervals

| Parameter | Interval |
|-----------|----------|
| Normal mean (known $\sigma^2$) | $\bar{X} \pm z_{\alpha/2} \cdot \sigma/\sqrt{n}$ |
| Normal mean (unknown $\sigma^2$) | $\bar{X} \pm t_{\alpha/2, n-1} \cdot s/\sqrt{n}$ |
| Proportion | $\hat{p} \pm z_{\alpha/2} \sqrt{\hat{p}(1-\hat{p})/n}$ |
| Difference of means | $(\bar{X}_1 - \bar{X}_2) \pm t_{\alpha/2, \nu} \cdot s_p \sqrt{1/n_1 + 1/n_2}$ |
| Regression coefficient | $\hat{\beta}_j \pm t_{\alpha/2, n-p} \cdot \text{SE}(\hat{\beta}_j)$ |

### Wald Intervals

In general, for an asymptotically normal estimator:
$$\hat{\theta} \pm z_{\alpha/2} \cdot \text{SE}(\hat{\theta})$$

## Bayesian Credible Intervals

### Definition

A $100(1-\alpha)\%$ credible interval $[a, b]$ satisfies:
$$P(\theta \in [a, b] \mid X = x) = 1 - \alpha$$

### Types

1. **Equal-tailed interval:** $[\pi_{\theta|x}^{-1}(\alpha/2), \pi_{\theta|x}^{-1}(1-\alpha/2)]$
2. **Highest Posterior Density (HPD):** The shortest interval containing $1-\alpha$ posterior probability. Advantage: every point inside has higher density than every point outside.

### Interpretation

**Credible:** "There is a 95% probability that $\theta$ falls in this interval, given the observed data."
**Confidence:** "95% of intervals constructed this way will contain the true $\theta$."

## Bootstrap Confidence Intervals

### Normal Bootstrap

$$\hat{\theta} \pm z_{\alpha/2} \cdot \widehat{\text{SE}}_{\text{boot}}$$

where $\widehat{\text{SE}}_{\text{boot}}$ is the standard deviation of bootstrap estimates.

### Percentile Bootstrap

$$[\hat{\theta}^*_{(\alpha/2)}, \hat{\theta}^*_{(1-\alpha/2)}]$$

where $\hat{\theta}^*_{(q)}$ is the $q$-th quantile of bootstrap estimates.

### BCa (Bias-Corrected and Accelerated)

Adjusts for bias and skewness. Let $z_0 = \Phi^{-1}(p_{\text{bias}})$ where $p_{\text{bias}} = \frac{\#\{\hat{\theta}^*_b < \hat{\theta}\}}{B}$, and $a$ (acceleration) estimated via jackknife. Then:
$$\alpha_1 = \Phi\left(z_0 + \frac{z_0 + z_{\alpha/2}}{1 - a(z_0 + z_{\alpha/2})}\right)$$
$$\alpha_2 = \Phi\left(z_0 + \frac{z_0 + z_{1-\alpha/2}}{1 - a(z_0 + z_{1-\alpha/2})}\right)$$
$$[\hat{\theta}^*_{(\alpha_1)}, \hat{\theta}^*_{(\alpha_2)}]$$

## Likelihood-Ratio-Based Intervals

For a scalar parameter $\theta$, a $100(1-\alpha)\%$ confidence interval is:
$$\{\theta: \ell(\theta) \geq \ell(\hat{\theta}) - \chi^2_{1, 1-\alpha} / 2\}$$

This is **invariant** to reparametrization (unlike Wald intervals).

## Comparison

| Aspect | Confidence Interval | Credible Interval |
|--------|-------------------|-------------------|
| Probability statement | About procedure | About parameter |
| Requires prior | No | Yes |
| Coverage guarantee | Yes (by construction) | If prior is correct |
| Interpretation | "95% of intervals..." | "95% probability..." |
| Repeated sampling | Meaningful | Not necessary |
| Nuisance parameters | Profile likelihood | Marginalize out |

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# CI for normal mean
np.random.seed(42)
n = 50
data = np.random.normal(5.0, 2.0, n)
x_bar = np.mean(data)
se = np.std(data, ddof=1) / np.sqrt(n)

# t-interval
ci_t = (x_bar - stats.t.ppf(0.975, n-1) * se,
        x_bar + stats.t.ppf(0.975, n-1) * se)
print(f"95% t-interval: [{ci_t[0]:.3f}, {ci_t[1]:.3f}]")

# Coverage simulation
n_sims = 10000
covers_t = np.zeros(n_sims)
for i in range(n_sims):
    sample = np.random.normal(5.0, 2.0, n)
    xb = np.mean(sample)
    s = np.std(sample, ddof=1)
    se_ = s / np.sqrt(n)
    low = xb - stats.t.ppf(0.975, n-1) * se_
    high = xb + stats.t.ppf(0.975, n-1) * se_
    covers_t[i] = (low <= 5.0 <= high)
print(f"Empirical coverage: {covers_t.mean():.3f}")

# Bootstrap percentile CI for median
def bootstrap_ci(data, stat_func, n_boot=10000, alpha=0.05):
    boot_stats = np.zeros(n_boot)
    n = len(data)
    for b in range(n_boot):
        boot_sample = np.random.choice(data, size=n, replace=True)
        boot_stats[b] = stat_func(boot_sample)
    return np.percentile(boot_stats, [100*alpha/2, 100*(1-alpha/2)])

ci_median = bootstrap_ci(data, np.median)
print(f"95% bootstrap CI for median: [{ci_median[0]:.3f}, {ci_median[1]:.3f}]")

# Bayesian credible interval
# Normal-Normal: prior N(0, 100), data N(5, 4)
mu_0, tau2 = 0, 100
sigma2 = 4
mu_n = (mu_0/tau2 + n*x_bar/sigma2) / (1/tau2 + n/sigma2)
sigma2_n = 1 / (1/tau2 + n/sigma2)
credible = (mu_n - stats.norm.ppf(0.975) * np.sqrt(sigma2_n),
            mu_n + stats.norm.ppf(0.975) * np.sqrt(sigma2_n))
print(f"95% credible interval: [{credible[0]:.3f}, {credible[1]:.3f}]")

# Visualization: comparing intervals
fig, ax = plt.subplots(figsize=(10, 4))
methods = ['t-interval', 'Bootstrap CI', 'Credible interval']
lows = [ci_t[0], ci_median[0], credible[0]]
highs = [ci_t[1], ci_median[1], credible[1]]
colors = ['blue', 'green', 'red']
for i, (m, l, h, c) in enumerate(zip(methods, lows, highs, colors)):
    ax.plot([l, h], [i, i], 'o-', color=c, lw=3)
    ax.text(l, i+0.1, f'{l:.3f}', ha='center', fontsize=9)
    ax.text(h, i+0.1, f'{h:.3f}', ha='center', fontsize=9)
ax.set_yticks(range(len(methods)))
ax.set_yticklabels(methods)
ax.axvline(x=5.0, color='k', linestyle='--', label='True mean')
ax.legend()
ax.set_title('95% Intervals Comparison')
plt.tight_layout()
plt.show()
```

## Visualization

Create a "coverage plot" showing 100 confidence intervals (horizontal lines) from 100 simulated datasets, with the true value as a vertical line. Intervals that miss the true value are highlighted in red — about 5 of 100 should miss for a 95% CI. A second panel shows a Bayesian credible interval with the full posterior distribution and the HPD region shaded.

## Practical Considerations

- **Wald intervals can misbehave:** For proportions near 0 or 1, Wald intervals can extend outside $[0,1]$. Use Wilson score or Clopper-Pearson (exact) intervals instead.
- **Coverage vs width:** Narrower is better, but only if coverage is maintained. Bootstrap percentile intervals sometimes undercover for small $n$.
- **Transformation:** If $\hat{\theta}$ has skewed sampling distribution, construct the CI on a transformed scale (e.g., log for odds ratios) and back-transform.
- **Fieller's theorem:** For ratios of parameters, use Fieller's interval instead of delta method (which can give infinite intervals).

## References

- Neyman, J. (1937). "Outline of a theory of statistical estimation based on the classical theory of probability"
- Efron, B. & Tibshirani, R. J. (1993). *An Introduction to the Bootstrap*
- DiCiccio, T. J. & Efron, B. (1996). "Bootstrap confidence intervals"
- Casella, G. & Berger, R. L. (2002). *Statistical Inference*
