# Lesson 19: Bootstrap

## Learning Objectives

After completing this lesson, you will be able to:
- Implement nonparametric bootstrap for standard error estimation
- Compute bootstrap confidence intervals (normal, percentile, BCa)
- Understand parametric bootstrap for model-based inference
- Identify when bootstrap fails and use jackknife alternatives
- Apply bootstrap for hypothesis testing

## Nonparametric Bootstrap

### Core Idea

The bootstrap treats the **empirical distribution** $\hat{F}_n$ as an estimate of the true population distribution $F$. We resample from $\hat{F}_n$ to approximate the sampling distribution of a statistic.

### Algorithm

1. Given original data $x_1, \dots, x_n$, compute observed statistic $\hat{\theta} = s(x)$
2. For $b = 1, \dots, B$:
   a. Sample $x^*_1, \dots, x^*_n$ **with replacement** from $\{x_1, \dots, x_n\}$
   b. Compute $\hat{\theta}^*_b = s(x^*)$
3. The empirical distribution of $\{\hat{\theta}^*_1, \dots, \hat{\theta}^*_B\}$ approximates the sampling distribution of $\hat{\theta}$

### Why It Works

The bootstrap approximates the sampling distribution of $\hat{\theta}$ under $F$ by its sampling distribution under $\hat{F}_n$. As $n \to \infty$, $\hat{F}_n \to F$ (by Glivenko-Cantelli), so the bootstrap distribution converges to the true sampling distribution (under regularity conditions).

### Standard Error Estimation

$$\widehat{\text{SE}}_{\text{boot}}(\hat{\theta}) = \sqrt{\frac{1}{B-1} \sum_{b=1}^B (\hat{\theta}^*_b - \bar{\hat{\theta}}^*)^2}$$

where $\bar{\hat{\theta}}^* = \frac{1}{B} \sum_{b=1}^B \hat{\theta}^*_b$.

### Bias Estimation

$$\widehat{\text{Bias}}_{\text{boot}} = \bar{\hat{\theta}}^* - \hat{\theta}$$

Bias-corrected estimate: $\hat{\theta}_{\text{BC}} = 2\hat{\theta} - \bar{\hat{\theta}}^*$

## Bootstrap Confidence Intervals

### Normal Interval

$$\hat{\theta} \pm z_{\alpha/2} \cdot \widehat{\text{SE}}_{\text{boot}}$$

**Requires:** Approximately normal sampling distribution.

### Percentile Interval

$$[\hat{\theta}^*_{(\alpha/2)}, \hat{\theta}^*_{(1-\alpha/2)}]$$

where $\hat{\theta}^*_{(q)}$ is the $q$-th quantile of bootstrap replications.

**Requires:** Existence of a monotone transformation $g$ such that $g(\hat{\theta}) - g(\theta)$ is symmetric about 0.

### BCa Interval (Bias-Corrected and Accelerated)

Adjusts the percentile endpoints for bias and skewness:

1. **Bias correction:** $z_0 = \Phi^{-1}\left(\frac{\#\{\hat{\theta}^*_b < \hat{\theta}\}}{B}\right)$
2. **Acceleration $a$:** Estimated via jackknife:
   $$a = \frac{\sum_{i=1}^n (\hat{\theta}_{(\cdot)} - \hat{\theta}_{(i)})^3}{6\left[\sum_{i=1}^n (\hat{\theta}_{(\cdot)} - \hat{\theta}_{(i)})^2\right]^{3/2}}$$
   where $\hat{\theta}_{(i)}$ is the estimate with $i$-th observation removed, and $\hat{\theta}_{(\cdot)}$ is their mean.
3. **Adjusted quantiles:**
   $$\alpha_1 = \Phi\left(z_0 + \frac{z_0 + z_{\alpha/2}}{1 - a(z_0 + z_{\alpha/2})}\right)$$
   $$\alpha_2 = \Phi\left(z_0 + \frac{z_0 + z_{1-\alpha/2}}{1 - a(z_0 + z_{1-\alpha/2})}\right)$$
   $$\text{CI} = [\hat{\theta}^*_{(\alpha_1)}, \hat{\theta}^*_{(\alpha_2)}]$$

## Parametric Bootstrap

When we assume a parametric model $F_\theta$:

1. Estimate $\hat{\theta}$ from data (e.g., MLE)
2. For $b = 1, \dots, B$:
   a. Sample $x^*_1, \dots, x^*_n \sim F_{\hat{\theta}}$
   b. Compute $\hat{\theta}^*_b$ from $x^*$
3. Use distribution of $\hat{\theta}^*$ for inference

**Use case:** When the parametric model is trusted and $n$ is small.

## Jackknife

### Leave-One-Out Resampling

For $i = 1, \dots, n$:
- Remove observation $i$, compute $\hat{\theta}_{(i)}$ from remaining $n-1$ observations

### Pseudo-values

$$\tilde{\theta}_i = n\hat{\theta} - (n-1)\hat{\theta}_{(i)}$$

The mean of pseudo-values, $\bar{\tilde{\theta}}$, is the **jackknife estimate** of $\theta$.

### Jackknife Standard Error

$$\widehat{\text{SE}}_{\text{jack}} = \sqrt{\frac{n-1}{n} \sum_{i=1}^n (\hat{\theta}_{(i)} - \bar{\hat{\theta}}_{(\cdot)})^2}$$

### Limitations

- Less general than bootstrap (works for smooth statistics only)
- Deterministic (no Monte Carlo variability)
- Can fail for non-smooth statistics (median, quantiles)

## Bootstrap Hypothesis Testing

### Bootstrap p-value

**Algorithm (one-sided, $H_0: \theta = \theta_0$):**
1. Compute $\hat{\theta}$ from original data
2. Shift bootstrap distribution so it's centered at $\theta_0$: $\tilde{\theta}^*_b = \hat{\theta}^*_b - \bar{\hat{\theta}}^* + \theta_0$
3. $p = \frac{1 + \#\{\tilde{\theta}^*_b \geq \hat{\theta}\}}{B+1}$

## When Bootstrap Fails

| Scenario | Problem | Alternative |
|----------|---------|-------------|
| Extreme order statistics | Bootstrap distribution inconsistent | Subsampling |
| Non-smooth functionals | Bootstrap fails for $\max\{X_i\}$ | m-out-of-n bootstrap |
| Heavy tails (infinite variance) | Bootstrap not consistent | Subsampling |
| Small $n$ | Bootstrap too discrete | Smoothed bootstrap |
| Dependent data | i.i.d. bootstrap invalid | Block bootstrap |
| High-dimensional $p \gg n$ | Bootstrap inconsistent | Mulitplier bootstrap |

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Bootstrap for correlation coefficient
np.random.seed(42)
n = 50
x = np.random.normal(0, 1, n)
y = 0.7 * x + 0.3 * np.random.normal(0, 1, n)

def pearson_corr(data):
    x, y = data[:, 0], data[:, 1]
    return np.corrcoef(x, y)[0, 1]

data = np.column_stack([x, y])
r_obs = pearson_corr(data)

# Bootstrap
B = 10000
boot_stats = np.zeros(B)
for b in range(B):
    idx = np.random.choice(n, size=n, replace=True)
    boot_stats[b] = pearson_corr(data[idx])

# Standard error
se_boot = np.std(boot_stats, ddof=1)
print(f"Observed r = {r_obs:.4f}")
print(f"Bootstrap SE = {se_boot:.4f}")

# Bias
bias_boot = np.mean(boot_stats) - r_obs
print(f"Bootstrap bias = {bias_boot:.4f}")

# Percentile CI
ci_perc = np.percentile(boot_stats, [2.5, 97.5])
print(f"95% percentile CI: [{ci_perc[0]:.4f}, {ci_perc[1]:.4f}]")

# Plot
plt.figure(figsize=(12, 4))

plt.subplot(131)
plt.scatter(x, y, alpha=0.6)
plt.title(f'Data: r = {r_obs:.3f}')

plt.subplot(132)
plt.hist(boot_stats, bins=50, density=True, alpha=0.7, color='steelblue')
plt.axvline(r_obs, color='r', lw=2, label='Observed')
plt.axvline(ci_perc[0], color='g', linestyle='--', label='95% CI')
plt.axvline(ci_perc[1], color='g', linestyle='--')
plt.xlabel('Correlation')
plt.ylabel('Density')
plt.legend()
plt.title('Bootstrap Distribution')

plt.subplot(133)
plt.boxplot(boot_stats, vert=False)
plt.xlabel('Correlation')
plt.title('Bootstrap Boxplot')

plt.tight_layout()
plt.show()

# Parametric bootstrap for Exponential
sample = np.random.exponential(scale=2.0, size=30)
lam_hat = 1.0 / np.mean(sample)

B = 10000
boot_parametric = np.zeros(B)
for b in range(B):
    boot_sample = np.random.exponential(scale=1/lam_hat, size=30)
    boot_parametric[b] = 1.0 / np.mean(boot_sample)

ci_param = np.percentile(boot_parametric, [2.5, 97.5])
print(f"\nParametric bootstrap 95% CI for λ: [{ci_param[0]:.4f}, {ci_param[1]:.4f}]")
print(f"MLE λ = {lam_hat:.4f}")
```

## Visualization

Create a four-panel figure: (1) Original data with scatterplot; (2) Bootstrap distribution histogram with observed statistic and CI marked; (3) QQ-plot of bootstrap statistics vs normal quantiles (checking normality assumption for normal bootstrap); (4) Comparison of normal, percentile, and BCa confidence intervals for a skewed statistic (e.g., ratio or correlation).

## Practical Considerations

- **Number of bootstrap replications:** For standard errors, $B = 1000$ is typically sufficient. For confidence intervals, $B = 10000$ or more. For BCa intervals, use $B \geq 5000$.
- **Computational cost:** Bootstrap can be expensive for large $n$ and complex statistics. Consider the **bag of little bootstraps** or **subsampling** for scalability.
- **Stratified bootstrap:** For stratified data, resample within each stratum to preserve the stratification structure.
- **Balanced bootstrap:** Each observation appears exactly $B$ times across all bootstrap samples — reduces variance.

## References

- Efron, B. (1979). "Bootstrap methods: Another look at the jackknife"
- Efron, B. & Tibshirani, R. J. (1993). *An Introduction to the Bootstrap*
- Davison, A. C. & Hinkley, D. V. (1997). *Bootstrap Methods and Their Application*
- Shao, J. & Tu, D. (1995). *The Jackknife and Bootstrap*
