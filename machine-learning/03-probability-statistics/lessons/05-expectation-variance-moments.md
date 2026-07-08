# Lesson 05: Expectation, Variance, Moments

## Learning Objectives

After completing this lesson, you will be able to:
- Compute expectations for discrete, continuous, and general random variables
- Apply LOTUS to compute expectations of transformed variables
- Calculate variance, skewness, and kurtosis
- Use moment generating functions to characterize distributions
- Understand Jensen's inequality and its implications in ML

## Expectation (Expected Value)

### Definition

For a discrete random variable $X$ with PMF $p(x)$:
$$E[X] = \sum_{x} x \, p(x)$$

For a continuous random variable $X$ with PDF $f(x)$:
$$E[X] = \int_{-\infty}^{\infty} x \, f(x) \, dx$$

In general (Lebesgue integral):
$$E[X] = \int_{\Omega} X(\omega) \, dP(\omega)$$

The expectation is the **probability-weighted average** of all possible values. It need not exist (e.g., Cauchy distribution) and need not be a possible value.

### Linearity of Expectation

For any random variables $X, Y$ and constants $a, b$:
$$E[aX + b] = aE[X] + b$$
$$E[X + Y] = E[X] + E[Y]$$

**Crucially, linearity holds regardless of dependence!** This is one of the most powerful properties in probability.

### Law of the Unconscious Statistician (LOTUS)

For a measurable function $g$:
$$E[g(X)] = \int g(x) \, f_X(x) \, dx$$

No need to derive the distribution of $g(X)$ first. This works for both discrete and continuous:
- Discrete: $E[g(X)] = \sum_x g(x) p(x)$
- Continuous: $E[g(X)] = \int g(x) f_X(x) dx$

## Moments

### Raw Moments

The $k$-th raw moment of $X$ is:
$$\mu'_k = E[X^k]$$

The first raw moment is the mean $\mu = E[X]$.

### Central Moments

The $k$-th central moment is:
$$\mu_k = E[(X - \mu)^k]$$

The second central moment is the variance: $\text{Var}(X) = \mu_2 = E[(X-\mu)^2]$.

### Moment Generating Function (MGF)

$$M_X(t) = E[e^{tX}]$$

Properties:
- $M_X(0) = 1$
- $M_X^{(k)}(0) = E[X^k]$ (the $k$-th derivative at 0 gives the $k$-th raw moment)
- If MGFs exist and match in a neighborhood of 0, the distributions are identical
- For independent $X, Y$: $M_{X+Y}(t) = M_X(t) M_Y(t)$

**Common MGFs:**
| Distribution | MGF $M(t)$ |
|-------------|------------|
| Bernoulli($p$) | $1-p+pe^t$ |
| Binomial($n,p$) | $(1-p+pe^t)^n$ |
| Poisson($\lambda$) | $\exp(\lambda(e^t-1))$ |
| Normal($\mu,\sigma^2$) | $\exp(\mu t + \sigma^2 t^2/2)$ |
| Exponential($\lambda$) | $\lambda/(\lambda-t)$ for $t<\lambda$ |
| Gamma($\alpha,\beta$) | $\left(\frac{\beta}{\beta-t}\right)^\alpha$ for $t<\beta$ |

### Characteristic Function

More general than MGF (always exists):
$$\phi_X(t) = E[e^{itX}]$$

## Variance and Standard Deviation

$$\text{Var}(X) = E[(X - \mu)^2] = E[X^2] - (E[X])^2$$

Standard deviation: $\sigma_X = \sqrt{\text{Var}(X)}$

### Properties of Variance

1. $\text{Var}(aX + b) = a^2 \text{Var}(X)$
2. $\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) + 2\text{Cov}(X, Y)$
3. If $X \perp Y$, then $\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y)$
4. $\text{Var}(X) = 0 \iff P(X = c) = 1$ for some constant $c$

## Skewness and Kurtosis

### Skewness

$$\gamma_1 = E\left[\left(\frac{X - \mu}{\sigma}\right)^3\right] = \frac{\mu_3}{\sigma^3}$$

- **$\gamma_1 > 0$:** Right-tailed (positive skew) — e.g., Exponential, Log-normal
- **$\gamma_1 < 0$:** Left-tailed (negative skew)
- **$\gamma_1 = 0$:** Symmetric — e.g., Normal, t-distribution

### Kurtosis

$$\gamma_2 = E\left[\left(\frac{X - \mu}{\sigma}\right)^4\right] - 3 = \frac{\mu_4}{\sigma^4} - 3$$

The "-3" makes the Normal distribution have **excess kurtosis** of 0 (it has kurtosis 3).

- **$\gamma_2 > 0$:** Leptokurtic — heavier tails than Normal (e.g., t-distribution, Laplace)
- **$\gamma_2 < 0$:** Platykurtic — lighter tails than Normal (e.g., Uniform)

## Jensen's Inequality

For a convex function $\phi$:
$$E[\phi(X)] \geq \phi(E[X])$$

For a concave function $\phi$:
$$E[\phi(X)] \leq \phi(E[X])$$

**ML Implications:**
- $\log$ is concave, so $E[\log X] \leq \log E[X]$ — used in EM algorithm and variational inference (ELBO)
- $x^2$ is convex, so $E[X^2] \geq (E[X])^2$ — equivalent to variance being non-negative
- Used to derive the EM algorithm's guarantee of convergence

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Empirical moments from samples
np.random.seed(42)
samples = np.random.gamma(shape=2.0, scale=2.0, size=10000)

mean_emp = np.mean(samples)
var_emp = np.var(samples, ddof=1)  # unbiased
skew_emp = stats.skew(samples)
kurt_emp = stats.kurtosis(samples)  # excess kurtosis

print(f"Empirical moments:")
print(f"  Mean:     {mean_emp:.3f}  (theoretical: 4.0)")
print(f"  Variance: {var_emp:.3f}  (theoretical: 8.0)")
print(f"  Skewness: {skew_emp:.3f}  (theoretical: {np.sqrt(2):.3f})")
print(f"  Kurtosis: {kurt_emp:.3f}  (theoretical: 3.0)")

# LOTUS: E[X^2] from samples
E_X2_emp = np.mean(samples**2)
E_X2_formula = var_emp + mean_emp**2
print(f"\nE[X^2] via LOTUS: {E_X2_emp:.3f}")
print(f"E[X^2] via Var + E[X]^2: {E_X2_formula:.3f}")

# Jensen's inequality visualization
xs = np.linspace(0.1, 5, 100)
plt.figure(figsize=(10, 4))

plt.subplot(121)
plt.plot(xs, np.log(xs), label='log(x)')
plt.axvline(x=mean_emp, color='r', linestyle='--', label=f'E[X]={mean_emp:.2f}')
plt.axhline(y=np.log(mean_emp), color='g', linestyle='--', label=f'log(E[X])={np.log(mean_emp):.2f}')
plt.axhline(y=np.mean(np.log(samples)), color='orange', linestyle=':', label=f'E[log(X)]={np.mean(np.log(samples)):.2f}')
plt.legend()
plt.title("Jensen: log is concave → E[log(X)] ≤ log(E[X])")

plt.subplot(122)
plt.plot(xs, xs**2, label='x²')
plt.axvline(x=mean_emp, color='r', linestyle='--', label=f'E[X]={mean_emp:.2f}')
plt.axhline(y=mean_emp**2, color='g', linestyle='--', label=f'(E[X])²={mean_emp**2:.2f}')
plt.axhline(y=np.mean(samples**2), color='orange', linestyle=':', label=f'E[X²]={np.mean(samples**2):.2f}')
plt.legend()
plt.title("Jensen: x² is convex → E[X²] ≥ (E[X])²")

plt.tight_layout()
plt.show()
```

## Visualization

Plot a distribution's PDF with vertical lines at $\mu$, $\mu \pm \sigma$, $\mu \pm 2\sigma$. The area between $\mu \pm \sigma$ for any distribution is at least 0% but can be as high as 100% (Chebyshev's inequality guarantees at least $1-1/k^2$ within $k$ standard deviations). Show a second plot with the skewness visualization: a right-skewed distribution (Gamma), symmetric (Normal), and left-skewed (mirrored Gamma).

## Practical Considerations

- **Existence of moments:** Not all distributions have finite moments (Cauchy has no mean). Always check before computing sample moments.
- **Numerical stability:** Computing variance as $E[X^2] - (E[X])^2$ can suffer from catastrophic cancellation. Use the stable two-pass algorithm or Welford's online algorithm.
- **MGF is a Laplace transform:** It may not exist for all $t$ (e.g., Cauchy has no MGF). Use characteristic functions for theoretical work.
- **High-dimensional moments:** The mean vector and covariance matrix are first- and second-order moments. For many ML algorithms, higher moments are ignored (Gaussian assumption), but heavy-tailed or skewed data may need more sophisticated models.

## References

- Billingsley, P. (1995). *Probability and Measure*
- Casella, G., & Berger, R. L. (2002). *Statistical Inference*
- Wasserman, L. (2004). *All of Statistics*
