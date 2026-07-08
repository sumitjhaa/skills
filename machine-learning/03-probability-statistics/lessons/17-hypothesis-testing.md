# Lesson 17: Hypothesis Testing

## Learning Objectives

After completing this lesson, you will be able to:
- Formulate null and alternative hypotheses for statistical tests
- Distinguish Type I and Type II errors and compute power
- Apply the Neyman-Pearson lemma for optimal tests
- Conduct Wald, score, and likelihood ratio tests
- Interpret p-values correctly and avoid common pitfalls

## Neyman-Pearson Framework

### Hypotheses

- **Null hypothesis** $H_0$: Default position, typically "no effect"
- **Alternative hypothesis** $H_1$: What we want to detect

### Types of Errors

| Decision | $H_0$ True | $H_0$ False |
|----------|-----------|-------------|
| Fail to reject $H_0$ | Correct ($1-\alpha$) | Type II error ($\beta$) |
| Reject $H_0$ | Type I error ($\alpha$) | Correct ($1-\beta$) |

- **Type I error ($\alpha$):** False positive — rejecting a true null
- **Type II error ($\beta$):** False negative — failing to reject a false null
- **Power ($1-\beta$):** Probability of correctly rejecting a false null

### Test Function

A test is a function $\phi(x) = P(\text{reject } H_0 \mid X = x)$, typically $\phi(x) = 1\{T(x) > c\}$.

## Neyman-Pearson Lemma

For testing simple $H_0: \theta = \theta_0$ vs $H_1: \theta = \theta_1$, the **most powerful test** at level $\alpha$ rejects $H_0$ when:
$$\frac{L(\theta_1 \mid x)}{L(\theta_0 \mid x)} > k$$

where $k$ is chosen so that $P(\text{reject} \mid H_0) = \alpha$.

## Common Parametric Tests

### Z-test (Known Variance)

$$Z = \frac{\bar{X} - \mu_0}{\sigma / \sqrt{n}} \sim \mathcal{N}(0, 1) \text{ under } H_0$$

Reject $H_0$ if $|Z| > z_{\alpha/2}$ (two-sided).

### t-test (Unknown Variance)

$$t = \frac{\bar{X} - \mu_0}{s / \sqrt{n}} \sim t_{n-1} \text{ under } H_0$$

where $s^2 = \frac{1}{n-1}\sum (X_i - \bar{X})^2$ is the sample variance.

**Welch's t-test** (unequal variances): Adjust degrees of freedom using Satterthwaite approximation.

### F-test for Variance Ratio

$$F = \frac{s_1^2}{s_2^2} \sim F_{n_1-1, n_2-1} \text{ under } H_0: \sigma_1^2 = \sigma_2^2$$

### Chi-squared Goodness-of-Fit

$$\chi^2 = \sum_{i=1}^k \frac{(O_i - E_i)^2}{E_i} \sim \chi^2_{k-1-m} \text{ under } H_0$$

where $m$ is the number of estimated parameters.

## Three Asymptotic Test Paradigms

### Wald Test

$$W = \frac{(\hat{\theta} - \theta_0)^2}{\text{Var}(\hat{\theta})} \xrightarrow{d} \chi^2_1 \text{ under } H_0$$

- Requires only the unconstrained MLE $\hat{\theta}$
- Simple to compute (estimate and standard error)
- **Not invariant** to reparametrization

### Score Test (Lagrange Multiplier)

$$\text{LM} = \frac{S(\theta_0)^2}{I(\theta_0)} \xrightarrow{d} \chi^2_1 \text{ under } H_0$$

where $S(\theta_0)$ is the score function at $\theta_0$.

- Requires only the constrained estimate $\theta_0$
- **Invariant** to reparametrization
- Also called Rao's score test

### Likelihood Ratio Test (LRT)

$$\text{LRT} = -2 \log \frac{L(\theta_0)}{L(\hat{\theta})} \xrightarrow{d} \chi^2_{df} \text{ under } H_0$$

where $df = \dim(\Theta) - \dim(\Theta_0)$ (Wilks' theorem).

- Requires both constrained and unconstrained estimates
- **Invariant** to reparametrization
- Often the most powerful among the three

## P-values

### Definition

$$p\text{-value} = P(T(X) \geq t_{\text{obs}} \mid H_0)$$

The probability, under $H_0$, of observing a test statistic as or more extreme than the one observed.

### Common Misinterpretations

| Incorrect | Correct |
|-----------|---------|
| "The probability $H_0$ is true" | "Probability of data given $H_0$" |
| "1 - p = probability $H_1$ is true" | Nothing about $H_1$ probability |
| "p < 0.05 means large effect" | Small p-value can arise from large $n$ with tiny effect |

### p-hacking

Data dredging practices that inflate significance:
- Multiple testing without correction
- Optional stopping (collect data until p < 0.05)
- Post-hoc hypothesis selection
- Failing to report all tests conducted

## Multiple Testing Corrections

| Method | Procedure | Control |
|--------|-----------|---------|
| Bonferroni | $\alpha / m$ | FWER |
| Holm | Sequential Bonferroni | FWER |
| Benjamini-Hochberg | Sort p-values, compare to $(i/m)\alpha$ | FDR |
| Storey's q-value | Estimate $\pi_0$, control FDR | FDR |

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Power analysis for t-test
np.random.seed(42)
n, d = 30, 0.5  # sample size, Cohen's d
alpha = 0.05

# Simulate many experiments
n_sims = 10000
p_vals = np.zeros(n_sims)
for i in range(n_sims):
    control = np.random.normal(0, 1, n)
    treatment = np.random.normal(d, 1, n)
    _, p_vals[i] = stats.ttest_ind(treatment, control)

power_empirical = np.mean(p_vals < alpha)
print(f"Empirical power (n={n}, d={d}): {power_empirical:.3f}")

# Theoretical power
ncp = d * np.sqrt(n / 2)  # non-centrality parameter
t_crit = stats.t.ppf(1 - alpha/2, 2*n - 2)
power_theoretical = 1 - stats.nct.cdf(t_crit, 2*n-2, ncp) + stats.nct.cdf(-t_crit, 2*n-2, ncp)
print(f"Theoretical power: {power_theoretical:.3f}")

# Multiple testing demonstration
m = 1000
true_effects = np.zeros(m)
true_effects[:50] = 0.5  # 5% have real effect
p_vals_multi = np.zeros(m)
for i in range(m):
    if true_effects[i] > 0:
        x = np.random.normal(true_effects[i], 1, 30)
        y = np.random.normal(0, 1, 30)
    else:
        x = np.random.normal(0, 1, 30)
        y = np.random.normal(0, 1, 30)
    _, p_vals_multi[i] = stats.ttest_ind(x, y)

# Bonferroni correction
alpha_bonf = alpha / m
discoveries_raw = p_vals_multi < alpha
discoveries_bonf = p_vals_multi < alpha_bonf

# BH correction
p_sorted = np.sort(p_vals_multi)
bh_threshold = np.arange(1, m+1) / m * alpha
reject_bh = p_sorted < bh_threshold

print(f"\nTrue positives: {true_effects.sum():.0f}")
print(f"Raw discoveries: {discoveries_raw.sum()}")
print(f"Bonferroni discoveries: {discoveries_bonf.sum()}")
print(f"BH discoveries: {reject_bh.sum()}")
```

## Visualization

Plot power curves for the t-test as a function of $n$ (sample size) for different effect sizes $d = 0.2, 0.5, 0.8$ (small, medium, large by Cohen's convention). Power increases with $n$ and $d$. Superimpose the empirical power from simulation. A second plot shows a volcano plot (log p-value vs effect size) for a multiple testing scenario, with Bonferroni and BH thresholds marked.

## Practical Considerations

- **p-values are not the effect size:** With large $n$, trivial effects become statistically significant. Always report effect sizes (Cohen's d, $\eta^2$, $R^2$).
- **Equivalence testing:** When you want to prove $H_0$ (no effect), use TOST (two one-sided tests) instead of failing to reject $H_0$.
- **Bayesian alternatives:** Bayes factors provide evidence for $H_0$ vs $H_1$ on a symmetric scale, avoiding the "absence of evidence vs evidence of absence" problem.
- **Pre-registration:** Pre-register your analysis plan to avoid p-hacking and confirmatory bias.

## References

- Neyman, J. & Pearson, E. S. (1933). "On the problem of the most efficient tests of statistical hypotheses"
- Lehmann, E. L. & Romano, J. P. (2005). *Testing Statistical Hypotheses*
- Wasserstein, R. L. & Lazar, N. A. (2016). "The ASA Statement on p-Values"
- Benjamin, D. J., et al. (2018). "Redefine statistical significance"
