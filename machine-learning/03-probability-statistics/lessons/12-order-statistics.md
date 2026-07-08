# Lesson 12: Order Statistics

## Learning Objectives

After completing this lesson, you will be able to:
- Derive the distribution of individual order statistics
- Compute joint distributions of multiple order statistics
- Apply extreme value theory to model maxima and minima
- Use quantiles and sample quantiles for robust statistics
- Implement order-statistic-based methods in Python

## Definitions

For a random sample $X_1, X_2, \dots, X_n$, the **order statistics** are the sorted values:
$$X_{(1)} \leq X_{(2)} \leq \cdots \leq X_{(n)}$$

- $X_{(1)}$: sample minimum
- $X_{(n)}$: sample maximum
- $X_{(k)}$: $k$-th order statistic
- **Sample median:** $X_{((n+1)/2)}$ for odd $n$; average of $X_{(n/2)}$ and $X_{(n/2+1)}$ for even $n$

## Distribution of a Single Order Statistic

### CDF of $X_{(k)}$

$$F_{X_{(k)}}(x) = P(X_{(k)} \leq x) = \sum_{j=k}^{n} \binom{n}{j} F(x)^j (1-F(x))^{n-j}$$

This is the probability that at least $k$ of the $n$ observations are $\leq x$.

### PDF of $X_{(k)}$

For a continuous distribution with CDF $F$ and PDF $f$:
$$f_{X_{(k)}}(x) = \frac{n!}{(k-1)!(n-k)!} F(x)^{k-1} f(x) [1-F(x)]^{n-k}$$

**Derivation:** To have $X_{(k)} \in (x, x+dx)$, we need exactly $k-1$ observations below $x$, one in $(x, x+dx)$, and $n-k$ above $x+dx$.

### Special Cases

- **Minimum ($k=1$):** $f_{X_{(1)}}(x) = n f(x) [1-F(x)]^{n-1}$
- **Maximum ($k=n$):** $f_{X_{(n)}}(x) = n f(x) F(x)^{n-1}$
- **Median:** $f_{X_{((n+1)/2)}}(x)$ centers on $f(x)$ as $n$ grows

## Joint Distribution of Two Order Statistics

For $1 \leq i < j \leq n$:
$$f_{X_{(i)}, X_{(j)}}(x, y) = \frac{n!}{(i-1)!(j-i-1)!(n-j)!} F(x)^{i-1} f(x) [F(y)-F(x)]^{j-i-1} f(y) [1-F(y)]^{n-j}$$

for $x < y$.

### Range

$$R_n = X_{(n)} - X_{(1)}$$
$$f_{R_n}(r) = \int_{-\infty}^{\infty} n(n-1) f(x) f(x+r) [F(x+r) - F(x)]^{n-2} dx$$

## Asymptotic Distribution of Order Statistics

### Central Order Statistics ($k = \lfloor np \rfloor$)

For quantile $p \in (0, 1)$, as $n \to \infty$:
$$\sqrt{n} (X_{(\lfloor np \rfloor)} - F^{-1}(p)) \xrightarrow{d} \mathcal{N}\left(0, \frac{p(1-p)}{f(F^{-1}(p))^2}\right)$$

### Extreme Value Theory

As $n \to \infty$, properly normalized maxima converge to one of three distributions (the **extreme value distributions**):

**Fisher-Tippett-Gnedenko Theorem:** If there exist sequences $a_n > 0$, $b_n$ such that $(X_{(n)} - b_n)/a_n$ converges in distribution, then the limit is one of:

1. **Gumbel ($\xi = 0$):** $F(x) = \exp(-e^{-(x-\mu)/\sigma})$
   - For light-tailed distributions (Normal, Exponential, Gamma)
   
2. **Fréchet ($\xi > 0$):** $F(x) = \exp(-(x/\sigma)^{-\alpha})$
   - For heavy-tailed distributions (t, Pareto, Cauchy)
   - $\alpha = 1/\xi$ is the tail index
   
3. **Weibull ($\xi < 0$):** $F(x) = \exp(-(-(x-\mu)/\sigma)^\alpha)$
   - For bounded distributions (Uniform, Beta)

The **generalized extreme value (GEV)** distribution unifies all three:
$$F(x) = \exp\left(-\left[1 + \xi\left(\frac{x-\mu}{\sigma}\right)\right]^{-1/\xi}\right)$$

## Sample Quantiles

The $p$-th sample quantile ($0 < p < 1$) is:
$$\hat{Q}_n(p) = X_{(\lceil np \rceil)}$$

Many alternative definitions exist (nine common types in statistical software).

### Quantile Function

$$Q(p) = F^{-1}(p) = \inf\{x: F(x) \geq p\}$$

### Properties of Sample Quantiles

- **Consistent:** $\hat{Q}_n(p) \xrightarrow{p} Q(p)$
- **Asymptotically normal:** $\sqrt{n}(\hat{Q}_n(p) - Q(p)) \xrightarrow{d} \mathcal{N}(0, \frac{p(1-p)}{f(Q(p))^2})$
- **Robust:** The median ($p=0.5$) is robust to outliers; the IQR ($Q(0.75)-Q(0.25)$) is a robust scale measure

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# PDF of k-th order statistic for standard normal
def order_stat_pdf(x, k, n):
    """PDF of k-th order statistic for N(0,1) sample of size n."""
    F = stats.norm.cdf(x)
    f = stats.norm.pdf(x)
    coeff = np.math.factorial(n) / (np.math.factorial(k-1) * np.math.factorial(n-k))
    return coeff * F**(k-1) * f * (1-F)**(n-k)

n = 10
xs = np.linspace(-3, 3, 500)
plt.figure(figsize=(10, 6))
for k in [1, 2, 5, 9, 10]:
    pdf_vals = order_stat_pdf(xs, k, n)
    plt.plot(xs, pdf_vals, label=f'X({k})')
plt.legend()
plt.title(f'Order Statistics PDFs for N(0,1), n={n}')
plt.grid(alpha=0.3)
plt.show()

# Extreme value: GEV fitting to block maxima
blocks = 1000
block_size = 100
block_maxima = np.max(np.random.normal(0, 1, (blocks, block_size)), axis=1)

plt.figure(figsize=(10, 4))
plt.hist(block_maxima, bins=50, density=True, alpha=0.7)
xs = np.linspace(2, 5, 100)
# Normalize for Gumbel: a_n = 1/sqrt(2 log n), b_n = sqrt(2 log n)
n = block_size
a_n = 1 / np.sqrt(2 * np.log(n))
b_n = np.sqrt(2 * np.log(n)) - (np.log(np.log(n)) + np.log(4*np.pi)) / (2 * np.sqrt(2 * np.log(n)))
plt.plot(xs, stats.gumbel_r.pdf((xs - b_n) / a_n) / a_n, 'r-', lw=2, label='Gumbel fit')
plt.legend()
plt.title('Block Maxima of Normal Samples Converge to Gumbel')
plt.show()

# Robust statistics using order statistics
data = np.concatenate([np.random.normal(0, 1, 95), np.random.normal(10, 1, 5)])
print(f"Sample mean: {np.mean(data):.3f} (corrupted)")
print(f"Sample median: {np.median(data):.3f} (robust)")
print(f"Sample 10% trimmed mean: {stats.trim_mean(data, 0.1):.3f}")
```

## Visualization

Create a multi-panel figure: (1) PDFs of $X_{(1)}, X_{(5)}, X_{(10)}$ for $n=10$ standard normal samples, showing how the distribution shifts from minimum to median to maximum; (2) PDF of the sample range for uniform samples; (3) Q-Q plot of block maxima against the Gumbel distribution to validate extreme value theory.

## Practical Considerations

- **Robust estimation:** Order statistics-based estimators (median, trimmed mean, IQR) are resistant to outliers. The median has a 50% breakdown point.
- **Extreme value theory in ML:** Used for anomaly detection (rare events), financial risk modeling (VaR), and climate science (extreme weather).
- **Sample quantile accuracy:** The variance of sample quantiles depends on $1/f(Q(p))^2$ — quantiles in low-density regions are estimated with high uncertainty.
- **QQ plots:** Plot sample quantiles against theoretical quantiles to check distributional assumptions. Deviations from the diagonal indicate departures.

## References

- David, H. A. & Nagaraja, H. N. (2003). *Order Statistics*
- Coles, S. (2001). *An Introduction to Statistical Modeling of Extreme Values*
- Embrechts, P., Klüppelberg, C., & Mikosch, T. (1997). *Modelling Extremal Events*
