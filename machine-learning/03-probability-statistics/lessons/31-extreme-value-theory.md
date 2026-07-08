# Lesson 31: Extreme Value Theory

## Learning Objectives

After completing this lesson, you will be able to:
- Model block maxima using the Generalized Extreme Value (GEV) distribution
- Model peaks over threshold using the Generalized Pareto Distribution (GPD)
- Estimate return levels for rare events
- Select appropriate thresholds for POT models
- Apply EVT in finance, climate, and reliability engineering

## Block Maxima Approach

### Fisher-Tippett-Gnedenko Theorem

Let $M_n = \max\{X_1, \dots, X_n\}$ for i.i.d. $X_i$. If there exist sequences $a_n > 0$, $b_n$ such that:
$$\frac{M_n - b_n}{a_n} \xrightarrow{d} G$$

then $G$ belongs to the **Generalized Extreme Value (GEV)** family:
$$G(z) = \exp\left\{-\left[1 + \xi\left(\frac{z - \mu}{\sigma}\right)\right]_{+}^{-1/\xi}\right\}$$

### GEV Parameters

- $\mu \in \mathbb{R}$: **location** parameter
- $\sigma > 0$: **scale** parameter
- $\xi \in \mathbb{R}$: **shape** parameter (tail index)

### Three Types

| $\xi$ | Type | Domain | Examples |
|-------|------|--------|----------|
| $\xi \to 0$ | Gumbel | $\mathbb{R}$ | Normal, Exponential, Gamma, Lognormal |
| $\xi > 0$ | Fréchet | $(\mu - \sigma/\xi, \infty)$ | t, Pareto, Cauchy, stable |
| $\xi < 0$ | (Reversed) Weibull | $(-\infty, \mu - \sigma/\xi)$ | Uniform, Beta |

## Peaks Over Threshold (POT)

### Pickands-Balkema-de Haan Theorem

For a sufficiently high threshold $u$, the distribution of excesses $Y = X - u \mid X > u$ converges to the **Generalized Pareto Distribution (GPD)**:
$$H(y) = 1 - \left(1 + \frac{\xi y}{\tilde{\sigma}}\right)_{+}^{-1/\xi}$$

where $\tilde{\sigma} = \sigma + \xi(u - \mu)$.

### GPD Parameters

- $\tilde{\sigma} > 0$: scale parameter (depends on threshold)
- $\xi \in \mathbb{R}$: shape parameter (same as GEV)

### Mean Excess Function

$$e(u) = E[X - u \mid X > u]$$

For GPD with $\xi < 1$: $e(u) = \frac{\tilde{\sigma} + \xi u}{1 - \xi}$

If the mean excess plot is approximately linear above a threshold, the GPD model is appropriate.

## Return Levels

### GEV Return Level

The $m$-observation return level $z_m$ (level exceeded once every $m$ observations):
$$z_m = 
\begin{cases}
\mu - \frac{\sigma}{\xi} \left[1 - (-\log(1 - 1/m))^{-\xi}\right], & \xi \neq 0 \\
\mu - \sigma \log(-\log(1 - 1/m)), & \xi = 0
\end{cases}$$

### GPD Return Level

For the $m$-observation return level:
$$z_m = u + \frac{\tilde{\sigma}}{\xi} \left[(m \zeta_u)^\xi - 1\right]$$

where $\zeta_u = P(X > u)$.

### Return Level Plot

Plot $z_m$ against $-\log(-\log(1 - 1/m))$ on a logarithmic scale. For Gumbel ($\xi = 0$), the plot is linear. Convex shape indicates $\xi > 0$ (Fréchet), concave indicates $\xi < 0$ (Weibull).

## Threshold Selection

### For GEV

- Choose block size (e.g., annual maxima for climate data)
- Trade-off: larger blocks reduce variance but increase bias
- Typical blocks: year, quarter, month (depending on data frequency)

### For GPD

- Choose threshold $u$
- **Mean residual life plot:** $\{(u, \bar{e}(u)) : u \geq 0\}$ — choose $u$ where plot becomes approximately linear
- **Parameter stability:** Fit GPD at multiple thresholds — if $\xi$ and $\tilde{\sigma}_u$ (reparameterized) stabilize, choose the lowest such $u$

## Estimation

### Methods

| Method | Pros | Cons |
|--------|------|------|
| Maximum Likelihood | Efficient, flexible | Irregular for $\xi < -0.5$ |
| Probability-Weighted Moments | Works for $\xi < 0.5$ | Less efficient |
| Bayesian | Incorporates prior uncertainty | Computationally intensive |

### Profile Likelihood

For confidence intervals, profile likelihood is preferred over Wald (Wald intervals can extend outside the parameter space for $\xi$).

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import minimize

# Generate data with heavy tails
np.random.seed(42)
n = 5000
data = np.random.standard_t(df=3, size=n)  # heavy-tailed, ξ ≈ 1/3

# Block maxima (block size = 100)
block_size = 100
n_blocks = n // block_size
block_maxima = np.max(data[:n_blocks * block_size].reshape(-1, block_size), axis=1)

# Fit GEV by MLE
def gev_nll(params, data):
    mu, sigma, xi = params
    if sigma <= 0:
        return np.inf
    z = (data - mu) / sigma
    if xi == 0:
        nll = -np.sum(-np.log(sigma) - z - np.exp(-z))
    else:
        t = 1 + xi * z
        if np.any(t <= 0):
            return np.inf
        nll = -np.sum(-np.log(sigma) - (1 + 1/xi) * np.log(t) - t**(-1/xi))
    return nll

result = minimize(gev_nll, x0=[np.mean(block_maxima), np.std(block_maxima), 0.1],
                  args=(block_maxima,), method='Nelder-Mead')
mu_hat, sigma_hat, xi_hat = result.x
print(f"GEV MLE: μ={mu_hat:.3f}, σ={sigma_hat:.3f}, ξ={xi_hat:.3f}")

# Return level plot
return_periods = np.array([2, 5, 10, 20, 50, 100, 500, 1000])
if xi_hat == 0:
    z_m = mu_hat - sigma_hat * np.log(-np.log(1 - 1/return_periods))
else:
    z_m = mu_hat - (sigma_hat/xi_hat) * (1 - (-np.log(1 - 1/return_periods))**(-xi_hat))

# Empirical return levels
sorted_max = np.sort(block_maxima)
empirical_rp = n_blocks / (np.arange(n_blocks, 0, -1))
empirical_rl = sorted_max

plt.figure(figsize=(12, 4))

plt.subplot(131)
plt.plot(np.log(return_periods), z_m, 'bo-', label='GEV fit')
plt.plot(np.log(empirical_rp[:50]), empirical_rl[-50:], 'rx', label='Empirical')
plt.xlabel('log(Return period)')
plt.ylabel('Return level')
plt.legend()
plt.title('Return Level Plot')

# POT / GPD approach
threshold = np.percentile(data, 90)
excesses = data[data > threshold] - threshold

def gpd_nll(params, data):
    sigma, xi = params
    if sigma <= 0:
        return np.inf
    t = 1 + xi * data / sigma
    if np.any(t <= 0):
        return np.inf
    nll = -np.sum(-np.log(sigma) - (1 + 1/xi) * np.log(t))
    return nll

result_gpd = minimize(gpd_nll, x0=[np.std(excesses), 0.3],
                      args=(excesses,), method='Nelder-Mead')
sigma_gpd, xi_gpd = result_gpd.x
print(f"\nGPD MLE (threshold={threshold:.2f}): σ={sigma_gpd:.3f}, ξ={xi_gpd:.3f}")

# Q-Q plot for GPD
plt.subplot(132)
sorted_excess = np.sort(excesses)
theoretical = stats.genpareto.ppf(np.arange(1, len(excesses)+1)/(len(excesses)+1),
                                   xi_gpd, scale=sigma_gpd)
plt.scatter(theoretical, sorted_excess, alpha=0.5)
plt.plot(theoretical, theoretical, 'r--')
plt.xlabel('Theoretical quantiles')
plt.ylabel('Empirical quantiles')
plt.title('GPD Q-Q Plot')

# Mean excess plot
plt.subplot(133)
thresholds = np.percentile(data, np.linspace(50, 99, 50))
mean_excess = [np.mean(data[data > t] - t) for t in thresholds]
plt.plot(thresholds, mean_excess, 'b-')
plt.xlabel('Threshold u')
plt.ylabel('Mean excess e(u)')
plt.title('Mean Excess Plot')
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

## Visualization

Create a three-panel figure: (1) Return level plot with confidence intervals (from profile likelihood); (2) Parameter stability plot (estimates of $\xi$ and reparameterized $\sigma$ for increasing thresholds); (3) QQ-plot for GPD fit. The return level plot is the most important — it shows the expected frequency of extreme events and is the primary output for risk assessment.

## Practical Considerations

- **Extrapolation risk:** EVT extrapolates beyond the observed range. Return levels for $m > 2n$ (beyond twice the data length) should be treated with caution.
- **Threshold uncertainty:** The choice of threshold is the most important modeling decision. Use a range of thresholds in sensitivity analysis.
- **Stationarity:** Climate change and economic regime shifts violate the stationarity assumption. Use time-varying GEV parameters (e.g., $\mu(t) = \mu_0 + \mu_1 t$).
- **Dependence:** EVT assumes independence of extremes. For clustered extremes (e.g., storms), decluster or use extremal index.
- **Multivariate EVT:** For multiple correlated extremes, use max-stable processes or copulas with extreme value dependence.

## References

- Fisher, R. A. & Tippett, L. H. C. (1928). "Limiting forms of the frequency distribution of the largest or smallest member of a sample"
- Gnedenko, B. V. (1943). "Sur la distribution limite du terme maximum d'une série aléatoire"
- Pickands, J. (1975). "Statistical inference using extreme order statistics"
- Davison, A. C. & Smith, R. L. (1990). "Models for exceedances over high thresholds"
- Coles, S. (2001). *An Introduction to Statistical Modeling of Extreme Values*
