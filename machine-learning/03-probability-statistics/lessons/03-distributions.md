# Lesson 03: Probability Distributions

## Learning Objectives

After completing this lesson, you will be able to:
- Identify and characterize the key discrete and continuous probability distributions
- Compute moments, MGFs, and other properties for standard distributions
- Choose appropriate distributions for modeling real-world phenomena
- Understand the relationships and connections between distributions
- Apply distribution properties in ML contexts

## Discrete Distributions

### Bernoulli($p$)

Models a single binary trial with success probability $p$.

| Property | Formula |
|----------|---------|
| Support | $\{0, 1\}$ |
| PMF | $P(X = x) = p^x (1-p)^{1-x}$ |
| Mean | $p$ |
| Variance | $p(1-p)$ |
| MGF | $M(t) = 1-p + pe^t$ |

**ML Connection:** Binary classification output; building block for logistic regression.

### Binomial($n, p$)

Sum of $n$ independent Bernoulli($p$) trials — number of successes in $n$ trials.

$$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}, \quad k = 0, 1, \dots, n$$

- Mean: $np$, Variance: $np(1-p)$
- MGF: $M(t) = (1-p + pe^t)^n$
- **Poisson approximation:** If $n$ is large and $p$ is small with $\lambda = np$ moderate, Binomial($n,p$) $\approx$ Poisson($\lambda$)
- **Normal approximation:** If $n$ is large and $p$ is not too close to 0 or 1, Binomial($n,p$) $\approx$ $\mathcal{N}(np, np(1-p))$

### Poisson($\lambda$)

Models the number of events occurring in a fixed interval of time/space, assuming events occur independently at constant rate $\lambda$.

$$P(X = k) = \frac{e^{-\lambda} \lambda^k}{k!}, \quad k = 0, 1, 2, \dots$$

- Mean: $\lambda$, Variance: $\lambda$
- MGF: $M(t) = \exp(\lambda(e^t - 1))$
- **Key property:** Mean = variance (equidispersion)
- **Superposition:** Sum of independent Poissons is Poisson with rate equal to sum of rates

**ML Connection:** Count data modeling (e.g., traffic, website visits, event counts).

### Geometric($p$)

Number of trials until first success in independent Bernoulli trials.

$$P(X = k) = (1-p)^{k-1}p, \quad k = 1, 2, 3, \dots$$

- Mean: $1/p$, Variance: $(1-p)/p^2$
- **Memoryless property:** $P(X > n + m \mid X > m) = P(X > n)$

### Negative Binomial($r, p$)

Number of trials until $r$ successes.

$$P(X = k) = \binom{k-1}{r-1} p^r (1-p)^{k-r}, \quad k = r, r+1, \dots$$

- Mean: $r/p$, Variance: $r(1-p)/p^2$
- Generalizes Geometric ($r = 1$)
- Also used for overdispersed count data (variance > mean)

### Multinomial($n, p_1, \dots, p_k$)

Generalizes binomial to $k$ categories.

$$P(X_1 = n_1, \dots, X_k = n_k) = \frac{n!}{n_1! \cdots n_k!} p_1^{n_1} \cdots p_k^{n_k}$$

- $E[X_i] = np_i$
- $\text{Var}(X_i) = np_i(1-p_i)$
- $\text{Cov}(X_i, X_j) = -np_i p_j$

## Continuous Distributions

### Uniform($a, b$)

Constant density over an interval — "no information" beyond the bounds.

$$f(x) = \frac{1}{b-a}, \quad a \leq x \leq b$$

- Mean: $(a+b)/2$, Variance: $(b-a)^2/12$
- CDF: $F(x) = (x-a)/(b-a)$

### Normal (Gaussian) $\mathcal{N}(\mu, \sigma^2)$

The central distribution of statistics, arising from the Central Limit Theorem.

$$f(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right), \quad x \in \mathbb{R}$$

- Mean: $\mu$, Variance: $\sigma^2$
- MGF: $M(t) = \exp(\mu t + \sigma^2 t^2 / 2)$
- **68-95-99.7 rule:** $P(|X-\mu| < \sigma) \approx 0.68$, $P(|X-\mu| < 2\sigma) \approx 0.95$, $P(|X-\mu| < 3\sigma) \approx 0.997$
- **Standard normal:** $\Phi(z) = P(Z \leq z)$ where $Z \sim \mathcal{N}(0, 1)$
- **Affine transformation:** If $X \sim \mathcal{N}(\mu, \sigma^2)$, then $aX + b \sim \mathcal{N}(a\mu + b, a^2\sigma^2)$

**ML Connection:** Foundation of linear regression (Gaussian errors), VAE priors, weight initialization.

### Exponential($\lambda$)

Models waiting times for a Poisson process.

$$f(x) = \lambda e^{-\lambda x}, \quad x \geq 0$$

- Mean: $1/\lambda$, Variance: $1/\lambda^2$
- **Memoryless:** $P(X > s + t \mid X > s) = P(X > t)$
- **Connection:** If inter-arrival times are Exponential($\lambda$), arrival count is Poisson($\lambda t$)

### Gamma($\alpha, \beta$)

Generalizes Exponential (sum of $\alpha$ independent Exponential($\beta$) variables).

$$f(x) = \frac{\beta^\alpha}{\Gamma(\alpha)} x^{\alpha-1} e^{-\beta x}, \quad x \geq 0$$

- Mean: $\alpha/\beta$, Variance: $\alpha/\beta^2$
- Special cases: $\alpha = 1$ is Exponential; $\alpha = n/2, \beta = 1/2$ is Chi-squared($n$)

### Beta($\alpha, \beta$)

Distribution on [0,1], conjugate prior for Bernoulli/Binomial.

$$f(x) = \frac{x^{\alpha-1}(1-x)^{\beta-1}}{B(\alpha, \beta)}, \quad 0 \leq x \leq 1$$

- Mean: $\alpha/(\alpha+\beta)$, Variance: $\alpha\beta/((\alpha+\beta)^2(\alpha+\beta+1))$
- Special cases: $\alpha = \beta = 1$ is Uniform(0,1)

**ML Connection:** Prior for probabilities in Bayesian analysis, Thompson sampling.

### Chi-squared($k$)

Sum of $k$ independent squared standard normals.

$$X = \sum_{i=1}^k Z_i^2, \quad Z_i \overset{\text{i.i.d.}}{\sim} \mathcal{N}(0,1)$$

- Mean: $k$, Variance: $2k$
- Used in goodness-of-fit tests, confidence intervals for variance

### Student's $t$-distribution($\nu$)

Heavier tails than normal, arises from estimating variance.

$$f(x) = \frac{\Gamma((\nu+1)/2)}{\sqrt{\nu\pi} \,\Gamma(\nu/2)} \left(1 + \frac{x^2}{\nu}\right)^{-(\nu+1)/2}$$

- Mean: $0$ (for $\nu > 1$), Variance: $\nu/(\nu-2)$ (for $\nu > 2$)
- **Limit:** As $\nu \to \infty$, $t_\nu \to \mathcal{N}(0,1)$
- **ML Connection:** Robust regression (heavier tails reduce outlier influence)

### Fisher $F$-distribution($d_1, d_2$)

Ratio of two independent chi-squared variables.

$$F = \frac{U/d_1}{V/d_2}, \quad U \sim \chi^2_{d_1}, V \sim \chi^2_{d_2}$$

Used in ANOVA and comparing nested models.

## Other Important Distributions

| Distribution | Use Case | Key Property |
|-------------|----------|--------------|
| **Weibull($\lambda, k$)** | Survival analysis, failure times | Flexible hazard rate |
| **Cauchy($x_0, \gamma$)** | Heavy-tailed data | No finite moments |
| **Laplace($\mu, b$)** | L1 regularization | Sharp peak at mean |
| **Log-normal($\mu, \sigma^2$)** | Multiplicative processes | Product of independent factors |
| **Pareto($x_m, \alpha$)** | Wealth distribution, power laws | "80/20 rule" |

## Python Implementation

```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Plot several distributions
xs = np.linspace(-4, 4, 1000)

distributions = {
    'Normal(0,1)': stats.norm(0, 1),
    't(df=1)': stats.t(df=1),
    't(df=3)': stats.t(df=3),
    'Laplace(0,1)': stats.laplace(0, 1),
    'Cauchy(0,1)': stats.cauchy(0, 1),
}

plt.figure(figsize=(12, 6))
for name, dist in distributions.items():
    plt.plot(xs, dist.pdf(xs), label=name, lw=2)
plt.ylim(0, 0.5)
plt.legend()
plt.title("Heavy-tailed distributions compared to Normal")
plt.grid(alpha=0.3)
plt.show()

# Fitting a distribution to data
data = np.random.exponential(scale=2.0, size=1000)
fitted_params = stats.expon.fit(data)
print(f"Fitted Exponential(scale={fitted_params[1]:.3f})")

# Kolmogorov-Smirnov goodness-of-fit test
ks_stat, ks_pval = stats.kstest(data, 'expon', args=fitted_params)
print(f"KS test: stat={ks_stat:.4f}, p-value={ks_pval:.4f}")
```

## Visualization

A grid of PDF plots for all major distributions helps build intuition. Show Normal, t, Exponential, Gamma, Beta, Chi-squared side by side. Include a second plot showing how the shape of the Gamma distribution changes with $\alpha$ (shape) and $\beta$ (rate). A third plot shows the Beta distribution for different $(\alpha, \beta)$ pairs, illustrating its flexibility for modeling probabilities.

## Practical Considerations

- **Choosing a distribution:** Start with domain knowledge (count data → Poisson/Negative Binomial; continuous positive → Exponential/Gamma/Log-normal; bounded → Beta; heavy tails → t/Cauchy).
- **Overdispersion:** If variance >> mean for count data, use Negative Binomial instead of Poisson.
- **Mixture models:** Complex real-world distributions are often mixtures of simpler ones (e.g., Gaussian Mixture Models).
- **Heavy tails:** Many ML models assume normality, but real data often has heavier tails. Consider robust alternatives.

## References

- Johnson, N. L., Kotz, S., & Balakrishnan, N. (1994). *Continuous Univariate Distributions*, Vol. 1 & 2
- Forbes, C., et al. (2011). *Statistical Distributions*
- Krishnamoorthy, K. (2006). *Handbook of Statistical Distributions with Applications*
