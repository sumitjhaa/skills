# Lesson 30: Empirical Processes

## Learning Objectives

After completing this lesson, you will be able to:
- Define the empirical distribution function and its properties
- Apply the Glivenko-Cantelli theorem for uniform convergence
- Use DKW inequality for finite-sample confidence bands
- Understand the Kolmogorov-Smirnov test
- Connect empirical process theory to statistical learning

## Empirical Distribution Function

### Definition

$$F_n(x) = \frac{1}{n} \sum_{i=1}^n I(X_i \leq x)$$

For each fixed $x$, $n F_n(x) \sim \text{Binomial}(n, F(x))$. By the WLLN and CLT:
$$F_n(x) \xrightarrow{p} F(x)$$
$$\sqrt{n}(F_n(x) - F(x)) \xrightarrow{d} \mathcal{N}(0, F(x)(1-F(x)))$$

## Glivenko-Cantelli Theorem

### Statement

$$\sup_{x \in \mathbb{R}} |F_n(x) - F(x)| \xrightarrow{a.s.} 0$$

The empirical CDF converges **uniformly** to the true CDF almost surely. This is a much stronger statement than pointwise convergence.

### Proof Sketch

The key insight is that the supremum occurs at one of the jump points of $F_n$. Using the Dvoretzky-Kiefer-Wolfowitz inequality, we can bound the tail probability and apply Borel-Cantelli.

## Dvoretzky-Kiefer-Wolfowitz (DKW) Inequality

### Statement

$$P\left(\sup_{x \in \mathbb{R}} |F_n(x) - F(x)| > \varepsilon\right) \leq 2e^{-2n\varepsilon^2}$$

This holds for any $n$, any $\varepsilon > 0$, and any distribution $F$ (the constant 2 is sharp).

### Confidence Bands

Using DKW, we can construct **confidence bands** for $F$:
$$L(x) = \max\{F_n(x) - \varepsilon_n, 0\}$$
$$U(x) = \min\{F_n(x) + \varepsilon_n, 1\}$$
where $\varepsilon_n = \sqrt{\frac{\log(2/\alpha)}{2n}}$ gives a $100(1-\alpha)\%$ band.

These are **simultaneous** confidence bands (valid for all $x$ simultaneously), unlike pointwise confidence intervals (valid for one $x$ at a time).

## Kolmogorov-Smirnov (KS) Test

### Test Statistic

$$D_n = \sup_{x \in \mathbb{R}} |F_n(x) - F_0(x)|$$

Under $H_0: F = F_0$, the distribution of $\sqrt{n} D_n$ converges to the **Kolmogorov distribution**:
$$\lim_{n \to \infty} P(\sqrt{n} D_n \leq t) = 1 - 2 \sum_{k=1}^\infty (-1)^{k-1} e^{-2k^2 t^2}$$

### One-Sample KS Test

- $H_0$: Sample comes from $F_0$
- Reject $H_0$ if $\sqrt{n} D_n > K_\alpha$ (critical value from Kolmogorov distribution)

### Two-Sample KS Test

- Compares two empirical distributions: $D_{n,m} = \sup_x |F_n(x) - G_m(x)|$
- Tests $H_0$: Both samples come from the same distribution

### Limitations

- KS test is most sensitive near the center of the distribution, less sensitive in the tails
- Parameters of $F_0$ must be fully specified (no estimation)
- Lilliefors test corrects for estimated parameters (e.g., Normal with estimated $\mu, \sigma$)

## Empirical Process

### Definition

The **empirical process** is:
$$\mathbb{G}_n(f) = \sqrt{n}(P_n - P)(f) = \sqrt{n} \left(\frac{1}{n}\sum_{i=1}^n f(X_i) - \int f \, dP\right)$$

For a fixed $f$, $\mathbb{G}_n(f) \xrightarrow{d} \mathcal{N}(0, \text{Var}_P(f))$ by CLT.

### Donsker's Theorem

The empirical process $\mathbb{G}_n$ converges weakly to a **Brownian bridge** $\mathbb{G}$ — a Gaussian process with:
$$E[\mathbb{G}(f)] = 0$$
$$\text{Cov}(\mathbb{G}(f), \mathbb{G}(g)) = \text{Cov}_P(f, g)$$

### Donsker Classes

A class of functions $\mathcal{F}$ is **Donsker** if $\mathbb{G}_n$ converges weakly to $\mathbb{G}$ uniformly over $\mathcal{F}$. This requires the class to be "not too large" — measured by entropy or VC dimension.

## VC Dimension and Uniform Convergence

### Vapnik-Chervonenkis (VC) Theory

For a class $\mathcal{C}$ of sets with VC dimension $V$:
$$E\left[\sup_{C \in \mathcal{C}} |P_n(C) - P(C)|\right] \leq C_0 \sqrt{\frac{V}{n}}$$

### Statistical Learning Connection

Empirical risk minimization:
$$\hat{f}_n = \arg\min_{f \in \mathcal{F}} \hat{R}_n(f)$$
$$\hat{R}_n(f) = \frac{1}{n} \sum \ell(y_i, f(x_i))$$

Uniform convergence of empirical risks to true risks:
$$P\left(\sup_{f \in \mathcal{F}} |\hat{R}_n(f) - R(f)| > \varepsilon\right) \leq 2 \cdot \mathcal{N}(\mathcal{F}, \varepsilon) \cdot e^{-n\varepsilon^2/2}$$

where $\mathcal{N}(\mathcal{F}, \varepsilon)$ is the covering number of $\mathcal{F}$.

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ECDF with DKW confidence bands
np.random.seed(42)
n = 100
data = np.random.exponential(scale=2.0, n)

# ECDF
x_sorted = np.sort(data)
y_ecdf = np.arange(1, n+1) / n

# DKW 95% confidence bands
alpha = 0.05
epsilon = np.sqrt(np.log(2/alpha) / (2*n))
lower = np.maximum(y_ecdf - epsilon, 0)
upper = np.minimum(y_ecdf + epsilon, 1)

plt.figure(figsize=(10, 6))
plt.step(x_sorted, y_ecdf, where='post', lw=2, label='ECDF')
plt.fill_between(x_sorted, lower, upper, step='post', alpha=0.3,
                 label='95% DKW band')
xs = np.linspace(0, 12, 200)
plt.plot(xs, stats.expon.cdf(xs, scale=2.0), 'r--', lw=2,
         label='True Exp(2) CDF')
plt.xlabel('x')
plt.ylabel('F(x)')
plt.legend()
plt.title(f'ECDF with DKW 95% Confidence Bands (n={n})')
plt.show()

# KS Test
ks_stat, ks_pval = stats.kstest(data, 'expon', args=(0, 2.0))
print(f"KS test: D = {ks_stat:.4f}, p = {ks_pval:.4f}")

# Two-sample KS test
data2 = np.random.exponential(scale=2.5, n)
ks_2samp = stats.ks_2samp(data, data2)
print(f"Two-sample KS: D = {ks_2samp.statistic:.4f}, p = {ks_2samp.pvalue:.4f}")

# Empirical process: compare bootstrap distribution of sup|F_n - F|
n_boot = 1000
sup_stats = np.zeros(n_boot)
for b in range(n_boot):
    boot_sample = np.random.choice(data, size=n, replace=True)
    boot_ecdf = np.searchsorted(np.sort(boot_sample), x_sorted) / n
    sup_stats[b] = np.max(np.abs(boot_ecdf - y_ecdf))

plt.figure(figsize=(10, 4))
plt.hist(sup_stats, bins=50, density=True, alpha=0.7)
plt.axvline(x=ks_stat, color='r', lw=2, label=f'Observed D = {ks_stat:.3f}')
plt.xlabel('sup|F_n - F|')
plt.ylabel('Density')
plt.legend()
plt.title('Bootstrap Distribution of KS Statistic')
plt.show()
```

## Visualization

Plot the ECDF as a step function with the DKW simultaneous confidence band. Overlay the true CDF (if known). The band should contain the true CDF with high probability at all $x$. Add a second plot showing how the band width shrinks as $n$ increases — specifically, $\varepsilon_n \propto \sqrt{\log(1/\alpha)/n}$.

## Practical Considerations

- **DKW bands are conservative:** They are simultaneous bands valid for all $x$, so pointwise coverage exceeds $1-\alpha$. This is a small price for the guarantee.
- **Empirical process in ML:** Uniform convergence of empirical risks (via VC dimension or Rademacher complexity) is the foundation of PAC learning.
- **KS test power:** The KS test has low power for detecting differences in the tails. Use Anderson-Darling for better tail sensitivity.
- **Donsker theorem requires continuity:** For discrete distributions, the empirical process still converges but the limit process is different.
- **Computational considerations:** Computing $D_n$ for large $n$ is $O(n \log n)$ (sorting). For $n > 10^5$, consider approximations.

## References

- Glivenko, V. (1933). "Sulla determinazione empirica delle leggi di probabilità"
- Cantelli, F. P. (1933). "Sulla determinazione empirica delle leggi di probabilità"
- Dvoretzky, A., Kiefer, J., & Wolfowitz, J. (1956). "Asymptotic minimax character of the sample distribution function"
- Kolmogorov, A. N. (1933). "Sulla determinazione empirica di una legge di distribuzione"
- Smirnov, N. V. (1939). "On the estimation of the discrepancy between empirical curves"
- van der Vaart, A. W. & Wellner, J. A. (1996). *Weak Convergence and Empirical Processes*
