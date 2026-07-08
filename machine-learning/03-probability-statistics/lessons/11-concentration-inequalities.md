# Lesson 11: Concentration Inequalities

## Learning Objectives

After completing this lesson, you will be able to:
- Apply Markov and Chebyshev inequalities for basic tail bounds
- Use Chernoff bounds for exponential concentration
- Apply Hoeffding, Bernstein, and McDiarmid inequalities
- Understand the role of concentration in learning theory
- Derive generalization bounds for ML models

## Markov's Inequality

### Statement

For a non-negative random variable $X \geq 0$ with $E[X] < \infty$ and $a > 0$:
$$P(X \geq a) \leq \frac{E[X]}{a}$$

**Proof:** $E[X] = \int_0^\infty x f(x) dx \geq \int_a^\infty x f(x) dx \geq a \int_a^\infty f(x) dx = a P(X \geq a)$

### Sharpness

Markov's inequality is tight but weak — it gives a linear decay bound for any non-negative variable. For example, if $X = a$ with probability $p$ and 0 otherwise, equality holds.

## Chebyshev's Inequality

### Statement

For a random variable $X$ with mean $\mu$ and variance $\sigma^2$, and $k > 0$:
$$P(|X - \mu| \geq k\sigma) \leq \frac{1}{k^2}$$

### Application to Sample Mean

$$P(|\bar{X}_n - \mu| \geq \epsilon) \leq \frac{\sigma^2}{n\epsilon^2}$$

### Proof

Apply Markov to $Y = (X - \mu)^2$ with $a = k^2\sigma^2$:
$$P((X-\mu)^2 \geq k^2\sigma^2) \leq \frac{E[(X-\mu)^2]}{k^2\sigma^2} = \frac{1}{k^2}$$

### Limitations

- Requires knowledge of variance (or at least an upper bound)
- Gives polynomial ($1/k^2$) decay — much weaker than exponential bounds for light-tailed variables

## Chernoff Bound

### General Method

For any random variable $X$:
$$P(X \geq a) = P(e^{tX} \geq e^{ta}) \leq \frac{E[e^{tX}]}{e^{ta}} = e^{-ta} M_X(t)$$

Optimizing over $t > 0$:
$$P(X \geq a) \leq \inf_{t > 0} e^{-ta} M_X(t)$$

### Chernoff for Binomial

For $X \sim \text{Binomial}(n, p)$:
$$P(X \geq (1+\delta)np) \leq \left(\frac{e^\delta}{(1+\delta)^{1+\delta}}\right)^{np}$$
$$P(X \leq (1-\delta)np) \leq \left(\frac{e^{-\delta}}{(1-\delta)^{1-\delta}}\right)^{np}$$

Simplified forms:
$$P(|X - np| \geq \delta np) \leq 2e^{-np\delta^2/3} \quad \text{for } \delta \in (0,1]$$

## Hoeffding's Inequality

### Statement

Let $X_1, \dots, X_n$ be independent with $a_i \leq X_i \leq b_i$ almost surely. Then for $t > 0$:
$$P\left(\left|\bar{X}_n - E[\bar{X}_n]\right| \geq t\right) \leq 2 \exp\left(-\frac{2n^2 t^2}{\sum_{i=1}^n (b_i - a_i)^2}\right)$$

### Special Case: Bounded Variables

If $X_i \in [0, 1]$:
$$P(|\bar{X}_n - \mu| \geq t) \leq 2e^{-2nt^2}$$

### Proof Sketch

Apply Chernoff bound using Hoeffding's lemma: For any random variable $X$ with $a \leq X \leq b$ and $E[X] = 0$, $E[e^{tX}] \leq e^{t^2(b-a)^2/8}$.

## Bernstein's Inequality

### Statement

Let $X_1, \dots, X_n$ be independent with $E[X_i] = 0$, $|X_i| \leq c$, and $\text{Var}(X_i) \leq \sigma_i^2$. Then:
$$P\left(\left|\frac{1}{n}\sum_{i=1}^n X_i\right| \geq t\right) \leq 2 \exp\left(-\frac{nt^2}{2\bar{\sigma}^2 + 2ct/3}\right)$$

where $\bar{\sigma}^2 = \frac{1}{n}\sum \sigma_i^2$.

### Key Insight

Bernstein's inequality adapts to the variance — when $t$ is small (relative to variance), the bound behaves like $e^{-nt^2/(2\sigma^2)}$ (Gaussian tail). When $t$ is large, it behaves like $e^{-3nt/(2c)}$ (exponential tail).

## McDiarmid's Inequality (Bounded Differences)

### Statement

Let $f: \mathcal{X}^n \to \mathbb{R}$ satisfy the **bounded differences property**:
$$\sup_{x_1, \dots, x_n, x'_i} |f(x_1, \dots, x_i, \dots, x_n) - f(x_1, \dots, x'_i, \dots, x_n)| \leq c_i$$

Then for independent $X_1, \dots, X_n$:
$$P(|f(X_1, \dots, X_n) - E[f]| \geq t) \leq 2 \exp\left(-\frac{2t^2}{\sum_{i=1}^n c_i^2}\right)$$

### Applications

- **Empirical risk minimization:** $f(X_1, \dots, X_n) = \frac{1}{n}\sum \ell(h, X_i)$ — each point changes risk by at most $c_i = \frac{1}{n} \cdot \text{range}(\ell)$
- **U-statistics:** Kernel density estimation, two-sample tests
- **VC dimension:** Uniform convergence of empirical risks to true risks

## Applications in Learning Theory

### Generalization Bounds

For a hypothesis class $\mathcal{H}$ with VC dimension $d$, with probability $1-\delta$:
$$R(h) \leq \hat{R}_n(h) + \sqrt{\frac{d \log(2n/d) + \log(1/\delta)}{2n}}$$

where $R(h)$ is true risk and $\hat{R}_n(h)$ is empirical risk.

### Rademacher Complexity

For a function class $\mathcal{F}$ with Rademacher complexity $\mathcal{R}_n(\mathcal{F})$:
$$P\left(\sup_{f \in \mathcal{F}} \left|\frac{1}{n}\sum_{i=1}^n f(X_i) - E[f(X)]\right| \geq 2\mathcal{R}_n(\mathcal{F}) + t\right) \leq 2e^{-nt^2/2}$$

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Empirical comparison of concentration bounds
np.random.seed(42)
n = 100
mu, sigma = 0.0, 1.0
samples = np.random.normal(mu, sigma, n)
sample_mean = np.mean(samples)

# Chebyshev bound
eps_grid = np.linspace(0.01, 2.0, 100)
chebyshev_bound = sigma**2 / (n * eps_grid**2)

# Hoeffding bound (assume bounded in [-3, 3])
a, b = -3, 3
hoeffding_bound = 2 * np.exp(-2 * n * eps_grid**2 / (b - a)**2)

# Empirical tail probability
n_trials = 50000
empirical_tails = []
for eps in eps_grid:
    means_bootstrap = np.mean(
        np.random.normal(mu, sigma, (n_trials, n)),
        axis=1
    )
    empirical_tails.append(np.mean(np.abs(means_bootstrap - mu) > eps))

plt.figure(figsize=(10, 6))
plt.plot(eps_grid, chebyshev_bound, '--', label='Chebyshev bound', lw=2)
plt.plot(eps_grid, hoeffding_bound, '-.', label='Hoeffding bound', lw=2)
plt.plot(eps_grid, empirical_tails, '-', label='Empirical tail', lw=2)
plt.yscale('log')
plt.xlabel('ε')
plt.ylabel('P(|X̄ - μ| > ε)')
plt.title('Concentration Inequalities for n=100 Normal Samples')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

# Applications: confidence interval
# Hoeffding-based CI for bounded [0,1] data
n_binom = 200
p_true = 0.3
data = np.random.binomial(1, p_true, n_binom)
mean_est = np.mean(data)
eps = np.sqrt(np.log(2 / 0.05) / (2 * n_binom))
print(f"95% CI: [{mean_est - eps:.3f}, {mean_est + eps:.3f}]")
print(f"True p = {p_true}")
```

## Visualization

Plot tail probability $P(|\bar{X}_n - \mu| > \epsilon)$ against $\epsilon$ on log scale. Show empirical tail (Monte Carlo), Chebyshev bound ($O(1/\epsilon^2)$), and Hoeffding bound ($O(e^{-2n\epsilon^2})$). The exponential decay of Hoeffding is dramatically tighter than Chebyshev's polynomial decay. A second plot shows how bounds tighten as $n$ increases from 10 to 1000.

## Practical Considerations

- **Slud's inequality:** For small $n$ or extreme tails, Hoeffding can be loose. Use exact binomial bounds or Student's t.
- **Union bound:** Combining multiple concentration bounds via union bound (Bonferroni) becomes loose quickly. Use Benjamini-Hochberg or other multiple testing corrections.
- **Empirical Bernstein:** Use the empirical variance to get tighter bounds (Benkeser et al. 2017).
- **Hoeffding vs Bernstein:** When the variance is much smaller than the range, Bernstein gives tighter bounds than Hoeffding.

## References

- Hoeffding, W. (1963). "Probability inequalities for sums of bounded random variables"
- Bernstein, S. (1946). *The Theory of Probabilities*
- McDiarmid, C. (1989). "On the method of bounded differences"
- Boucheron, S., Lugosi, G., & Massart, P. (2013). *Concentration Inequalities: A Nonasymptotic Theory of Independence*
