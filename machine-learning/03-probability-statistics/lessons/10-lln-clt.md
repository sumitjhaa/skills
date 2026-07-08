# Lesson 10: Laws of Large Numbers & Central Limit Theorem

## Learning Objectives

After completing this lesson, you will be able to:
- Distinguish between Weak and Strong Laws of Large Numbers
- Understand the four modes of convergence and their relationships
- Apply the CLT for inference and approximation
- Recognize when LLN and CLT fail (heavy tails, infinite variance)

## Laws of Large Numbers

### Weak Law of Large Numbers (WLLN)

Let $X_1, X_2, \dots$ be i.i.d. with $E[X_i] = \mu < \infty$. For any $\epsilon > 0$:
$$\lim_{n \to \infty} P\left(|\bar{X}_n - \mu| > \epsilon\right) = 0$$

where $\bar{X}_n = \frac{1}{n} \sum_{i=1}^n X_i$. This says $\bar{X}_n$ **converges in probability** to $\mu$.

**Proof (under finite variance):** By Chebyshev's inequality:
$$P(|\bar{X}_n - \mu| > \epsilon) \leq \frac{\text{Var}(\bar{X}_n)}{\epsilon^2} = \frac{\sigma^2}{n\epsilon^2} \to 0$$

The WLLN holds under the weaker condition $E[|X|] < \infty$ (Khinchin's WLLN), proved using characteristic functions.

### Strong Law of Large Numbers (SLLN)

Let $X_1, X_2, \dots$ be i.i.d. with $E[X_i] = \mu < \infty$. Then:
$$P\left(\lim_{n \to \infty} \bar{X}_n = \mu\right) = 1$$

This says $\bar{X}_n$ **converges almost surely** to $\mu$. The SLLN is strictly stronger than the WLLN — it guarantees that every sample path converges, not just that the probability of large deviations vanishes.

**Proof (Kolmogorov):** Uses Kolmogorov's inequality and the Kronecker lemma. The key step is bounding $P(\sup_{k \geq n} |\bar{X}_k - \mu| > \epsilon)$.

### Relationship Between WLLN and SLLN

- SLLN $\implies$ WLLN (almost sure convergence implies convergence in probability)
- Converse is false: For any sequence converging in probability but not almost surely, there exist counterexamples
- SLLN requires essentially the same moment conditions as WLLN ($E[|X|] < \infty$)

## Modes of Convergence

Understanding the hierarchy of convergence modes is essential for asymptotic statistics.

| Mode | Notation | Definition | Intuition |
|------|----------|------------|-----------|
| Almost sure | $X_n \xrightarrow{a.s.} X$ | $P(\lim_{n \to \infty} X_n = X) = 1$ | Every sequence eventually converges |
| In probability | $X_n \xrightarrow{p} X$ | $\lim_{n \to \infty} P(|X_n - X| > \epsilon) = 0$ | Probability of large deviation vanishes |
| In distribution | $X_n \xrightarrow{d} X$ | $\lim_{n \to \infty} F_n(x) = F(x)$ at continuity points | CDFs converge |
| In $L^p$ | $X_n \xrightarrow{L^p} X$ | $\lim_{n \to \infty} E[|X_n - X|^p] = 0$ | Mean absolute deviation vanishes |

### Hierarchy

$$\text{Almost sure} \implies \text{In probability} \implies \text{In distribution}$$
$$\text{In } L^p \implies \text{In probability}$$

**Key fact:** Convergence in probability does not imply almost sure convergence, but there exists a subsequence $n_k$ such that $X_{n_k} \xrightarrow{a.s.} X$.

### Counterexamples

- **Probability $\not\Rightarrow$ Almost sure:** $X_n = 1$ with probability $1/n$, 0 otherwise. $X_n \xrightarrow{p} 0$ but $P(X_n \to 0) = 0$ (since Borel-Cantelli implies infinitely many 1s).
- **Distribution $\not\Rightarrow$ Probability:** $X_n = X$ and $X'_n = -X$ where $P(X=1) = P(X=-1) = 0.5$. Both have the same distribution but $X_n - X'_n$ does not converge to 0.

## Central Limit Theorem (Detailed)

### Lindeberg-Levy CLT

Let $X_1, \dots, X_n$ be i.i.d. with $E[X_i] = \mu$, $\text{Var}(X_i) = \sigma^2 < \infty$:
$$\sqrt{n}(\bar{X}_n - \mu) \xrightarrow{d} \mathcal{N}(0, \sigma^2)$$

### Multivariate CLT

For i.i.d. random vectors $X_i \in \mathbb{R}^d$ with mean $\mu$ and covariance $\Sigma$:
$$\sqrt{n}(\bar{X}_n - \mu) \xrightarrow{d} \mathcal{N}_d(0, \Sigma)$$

### Delta Method

For a differentiable function $g: \mathbb{R}^d \to \mathbb{R}^k$:
$$\sqrt{n}(g(\bar{X}_n) - g(\mu)) \xrightarrow{d} \mathcal{N}(0, \nabla g(\mu)^\top \Sigma \nabla g(\mu))$$

**ML Connection:** The delta method gives asymptotic standard errors for transformed parameters (e.g., log-odds to probability, variance to standard deviation).

### Cramér-Wold Device

To prove multivariate convergence, it suffices to check univariate convergence of all linear combinations: $X_n \xrightarrow{d} X$ iff $t^\top X_n \xrightarrow{d} t^\top X$ for all $t \in \mathbb{R}^d$.

## Applications in Machine Learning

| Application | LLN | CLT |
|-------------|-----|-----|
| Monte Carlo estimation | $\bar{f}_n \to E[f(X)]$ | $\sqrt{n}(\bar{f}_n - \mu) \to N(0, \sigma^2)$ |
| SGD convergence | $\theta_n \to \theta^*$ | $\sqrt{n}(\theta_n - \theta^*) \to N(0, V)$ |
| Bootstrap | Bootstrap distribution $\to$ sampling dist. | Bootstrap CLT |
| MLE asymptotics | $\hat{\theta}_n \xrightarrow{p} \theta_0$ | $\sqrt{n}(\hat{\theta}_n - \theta_0) \to N(0, I^{-1})$ |
| Cross-validation | CV estimate $\to$ true risk | CV risk confidence intervals |

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# LLN demonstration: running average
np.random.seed(42)
n_max = 10000
data = np.random.exponential(scale=2.0, size=n_max)
running_mean = np.cumsum(data) / np.arange(1, n_max + 1)

plt.figure(figsize=(10, 5))
plt.plot(running_mean, lw=1, label='Running mean')
plt.axhline(y=2.0, color='r', linestyle='--', lw=2, label='True mean')
plt.xscale('log')
plt.xlabel('n')
plt.ylabel(r'$\bar{X}_n$')
plt.title('Strong Law of Large Numbers: Running Mean Converges')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

# CLT: convergence in distribution
# Generate sample means for n=30, show distribution
n_trials = 10000
n = 30
sample_means = np.mean(np.random.exponential(scale=2.0, size=(n_trials, n)), axis=1)
z = np.sqrt(n) * (sample_means - 2.0) / 2.0  # standardized

plt.figure(figsize=(10, 5))
plt.hist(z, bins=80, density=True, alpha=0.7, label=f'Sample means (n={n})')
xs = np.linspace(-4, 4, 200)
plt.plot(xs, stats.norm.pdf(xs), 'r-', lw=2, label='N(0,1)')
plt.legend()
plt.title('Central Limit Theorem: Standardized Sample Means')
plt.show()

# Delta method: log-transformed mean
log_mean = np.log(sample_means)
z_log = np.sqrt(n) * (log_mean - np.log(2.0)) * 2.0  # approx var = (sigma/mu)^2
plt.figure(figsize=(10, 5))
plt.hist(z_log, bins=80, density=True, alpha=0.7, label='Log-transformed')
xs = np.linspace(-4, 4, 200)
plt.plot(xs, stats.norm.pdf(xs), 'r-', lw=2, label='N(0,1)')
plt.legend()
plt.title('Delta Method: log(mean) is asymptotically normal')
plt.show()
```

## Visualization

Create a three-panel figure: (1) LLN: running mean of Cauchy samples (does not converge) vs Exponential samples (converges to mean=2), using log-scale for n; (2) CLT: Q-Q plot of standardized sample means (n=30) against normal quantiles; (3) Convergence rate: standard deviation of $\bar{X}_n$ plotted against $1/\sqrt{n}$ on log-log scale, confirming $O(1/\sqrt{n})$ rate.

## Practical Considerations

- **Finite variance is required** for the standard CLT. The Cauchy distribution has no mean and no variance — sums of Cauchy are Cauchy, not normal. The t-distribution with df ≤ 2 has infinite variance.
- **Heavy-tailed data** in practice may have near-infinite variance. Consider using robust standard errors or subsampling.
- **Dependent data:** Time series data violates the i.i.d. assumption. Use autocorrelation-robust standard errors (Newey-West) or block bootstrap.
- **Rate of convergence:** The error in LLN approximation decays as $1/\sqrt{n}$ (from CLT). Doubling precision requires 4× more data.

## References

- Etemadi, N. (1981). "An elementary proof of the strong law of large numbers"
- Durrett, R. (2019). *Probability: Theory and Examples*
- Van der Vaart, A. W. (2000). *Asymptotic Statistics*
