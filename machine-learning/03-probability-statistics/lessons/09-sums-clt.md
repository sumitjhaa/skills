# Lesson 09: Sums of Random Variables & Central Limit Theorem

## Learning Objectives

After completing this lesson, you will be able to:
- Compute the distribution of sums via convolution
- Use MGFs to derive distributions of sums
- Understand cumulants and their properties
- Apply the Central Limit Theorem to approximate distributions
- Quantify the CLT approximation error using Berry-Esseen

## Convolution

### Continuous Case

If $X \perp Y$ have PDFs $f_X$ and $f_Y$, the PDF of $Z = X + Y$ is the convolution:
$$f_Z(z) = (f_X * f_Y)(z) = \int_{-\infty}^{\infty} f_X(x) f_Y(z - x) \, dx$$

**Derivation:** $F_Z(z) = P(X + Y \leq z) = \int_{-\infty}^{\infty} \int_{-\infty}^{z-x} f_X(x) f_Y(y) \, dy \, dx$. Differentiate to get the convolution formula.

### Discrete Case

For discrete variables with PMFs $p_X$ and $p_Y$:
$$p_Z(z) = \sum_x p_X(x) p_Y(z - x)$$

### Examples

**Sum of two independent Normals:** If $X \sim \mathcal{N}(\mu_1, \sigma_1^2)$ and $Y \sim \mathcal{N}(\mu_2, \sigma_2^2)$ with $X \perp Y$:
$$X + Y \sim \mathcal{N}(\mu_1 + \mu_2, \sigma_1^2 + \sigma_2^2)$$

**Sum of two independent Poissons:** If $X \sim \text{Poisson}(\lambda_1)$ and $Y \sim \text{Poisson}(\lambda_2)$ with $X \perp Y$:
$$X + Y \sim \text{Poisson}(\lambda_1 + \lambda_2)$$

**Sum of two independent Gammas (same rate):** If $X \sim \text{Gamma}(\alpha_1, \beta)$ and $Y \sim \text{Gamma}(\alpha_2, \beta)$ with $X \perp Y$:
$$X + Y \sim \text{Gamma}(\alpha_1 + \alpha_2, \beta)$$

## Moment Generating Functions

The MGF of $X$ is $M_X(t) = E[e^{tX}]$.

### Key Property

For independent $X$ and $Y$:
$$M_{X+Y}(t) = E[e^{t(X+Y)}] = E[e^{tX} e^{tY}] = E[e^{tX}] E[e^{tY}] = M_X(t) M_Y(t)$$

### MGF Uniqueness

If $M_X(t) = M_Y(t)$ for all $t$ in some neighborhood of 0, then $X$ and $Y$ have the same distribution. This is the basis for using MGFs to prove distributional results.

### MGF of Sample Mean

For i.i.d. $X_1, \dots, X_n$ with MGF $M_X$:
$$M_{\bar{X}_n}(t) = M_X(t/n)^n$$

### Cumulant Generating Function

$$K_X(t) = \log M_X(t)$$

The $k$-th **cumulant** $\kappa_k$ is $K^{(k)}(0)$:

- $\kappa_1 = E[X]$ (mean)
- $\kappa_2 = \text{Var}(X)$
- $\kappa_3 = E[(X-\mu)^3]$ (third central moment)
- $\kappa_4 = E[(X-\mu)^4] - 3\sigma^4$ (fourth cumulant = excess kurtosis × variance²)

**Properties:**
- For independent $X, Y$: $K_{X+Y}(t) = K_X(t) + K_Y(t)$ and $\kappa_k^{(X+Y)} = \kappa_k^{(X)} + \kappa_k^{(Y)}$
- Cumulants beyond the second are zero for the Normal distribution

## Central Limit Theorem

### Lindeberg-Levy CLT

Let $X_1, X_2, \dots, X_n$ be i.i.d. with $E[X_i] = \mu$ and $\text{Var}(X_i) = \sigma^2 < \infty$. Then:
$$\frac{\sqrt{n}(\bar{X}_n - \mu)}{\sigma} \xrightarrow{d} \mathcal{N}(0, 1)$$

Equivalently:
$$\frac{\sum_{i=1}^n X_i - n\mu}{\sigma\sqrt{n}} \xrightarrow{d} \mathcal{N}(0, 1)$$

**Proof sketch:** Standardize so mean=0, var=1. The MGF of the standardized sum converges to $e^{t^2/2}$ (the MGF of N(0,1)) as $n \to \infty$, using Taylor expansion.

### Multivariate CLT

For i.i.d. random vectors $X_i \in \mathbb{R}^d$ with mean $\mu$ and covariance $\Sigma$:
$$\sqrt{n}(\bar{X}_n - \mu) \xrightarrow{d} \mathcal{N}_d(0, \Sigma)$$

### Lindeberg-Feller CLT

For independent (not necessarily identically distributed) random variables $X_1, \dots, X_n$ with $E[X_i] = \mu_i$ and $\text{Var}(X_i) = \sigma_i^2$, let $s_n^2 = \sum \sigma_i^2$. The **Lindeberg condition**:
$$\frac{1}{s_n^2} \sum_{i=1}^n E[(X_i - \mu_i)^2 \cdot 1\{|X_i - \mu_i| > \epsilon s_n\}] \to 0 \quad \forall \epsilon > 0$$

ensures $\frac{1}{s_n} \sum (X_i - \mu_i) \xrightarrow{d} \mathcal{N}(0, 1)$.

## Berry-Esseen Theorem

Provides a **rate of convergence** for the CLT:

$$\sup_{x \in \mathbb{R}} \left| P\left( \frac{\sqrt{n}(\bar{X}_n - \mu)}{\sigma} \leq x \right) - \Phi(x) \right| \leq \frac{C \cdot \rho}{\sigma^3 \sqrt{n}}$$

where $\rho = E[|X - \mu|^3]$ is the third absolute moment and $C \approx 0.4748$ (universal constant).

## Applications in ML

### Stochastic Gradient Descent

The noise in SGD gradients can be approximated as Gaussian via CLT. This justifies using Gaussian assumptions in Bayesian SGD and learning rate schedules.

### Bootstrap

The bootstrap approximates the sampling distribution of a statistic via resampling. The CLT justifies bootstrap for means and smooth functionals.

### Monte Carlo Estimation

$$\bar{X}_n = \frac{1}{n} \sum_{i=1}^n f(X_i) \to E[f(X)]$$
Using CLT: $\bar{X}_n \pm z_{\alpha/2} \cdot \sigma/\sqrt{n}$ is a confidence interval for $E[f(X)]$.

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# CLT demonstration: sum of Exponential(1) variables
# Theoretical: Gamma(n, 1) with mean=n, variance=n
# Standardized: (sum - n) / sqrt(n) -> N(0,1)

n_samples = 10000
n_vars_list = [1, 2, 5, 30]

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

for idx, n in enumerate(n_vars_list):
    # Generate sums of n exponential(1) variables
    samples = np.random.exponential(scale=1, size=(n_samples, n)).sum(axis=1)
    # Standardize
    z = (samples - n) / np.sqrt(n)

    ax = axes[idx // 2, idx % 2]
    ax.hist(z, bins=80, density=True, alpha=0.7, label=f'n={n}')
    xs = np.linspace(-4, 4, 200)
    ax.plot(xs, stats.norm.pdf(xs), 'r-', lw=2, label='N(0,1)')
    ax.legend()
    ax.set_title(f'Sum of {n} Exponential(1) variables')

plt.tight_layout()
plt.show()

# Berry-Esseen bound demonstration
rho = stats.expon.moment(3)  # E[|X-1|^3] for Exp(1)
sigma = 1.0
for n in [1, 5, 30, 100]:
    bound = 0.4748 * rho / (sigma**3 * np.sqrt(n))
    print(f"n={n}: Berry-Esseen bound = {bound:.4f}")
```

## Visualization

Create a 2×2 grid showing histograms of standardized sums for $n = 1, 2, 5, 30$ with the standard normal PDF overlaid. For $n=1$, the distribution is Exponential (highly skewed). For $n=2$, it's a Gamma(2,1) (less skewed). By $n=30$, the histogram is nearly indistinguishable from the normal. A second figure shows the Q-Q plot for $n=30$, confirming approximate normality (points follow the diagonal line).

## Practical Considerations

- **How large is "large enough"?** For symmetric, unimodal distributions, $n \approx 30$ often suffices. For heavily skewed distributions, you may need $n > 100$. For heavy-tailed distributions (Cauchy), the CLT may not apply at all.
- **Outliers violate CLT assumptions:** If the variance is infinite (Cauchy) or heavy-tailed with finite variance (t with df=2), convergence is slow or absent.
- **Dependent data:** The CLT requires independence (or at least weak dependence). For time series, use specialized CLTs for stationary processes.
- **Multivariate CLT:** The dimension $d$ must be fixed as $n \to \infty$. High-dimensional CLTs (where $d/n \to c$) are more complex.

## References

- Feller, W. (1971). *An Introduction to Probability Theory and Its Applications*, Vol. II
- Durrett, R. (2019). *Probability: Theory and Examples*
- Berry, A. C. (1941). "The accuracy of the Gaussian approximation"
- Esseen, C. G. (1942). "On the Liapunoff limit of error in the theory of probability"
