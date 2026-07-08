# Lesson 38: Approximate Bayesian Computation (ABC)

## Learning Objectives

After completing this lesson, you will be able to:
- Understand when ABC is necessary (intractable likelihood)
- Implement rejection ABC and ABC-MCMC
- Choose summary statistics and tolerance thresholds
- Apply regression adjustment to improve ABC estimates
- Diagnose ABC accuracy and calibration

## Motivation

### Intractable Likelihood

Many models have likelihoods $f(x \mid \theta)$ that cannot be evaluated pointwise but can be **simulated from**:
- Ecological models (population dynamics)
- Epidemiological models (disease spread)
- Stochastic financial models
- Agent-based models

ABC bypasses likelihood evaluation by comparing simulated data to observed data.

## Rejection ABC

### Basic Algorithm

1. Sample $\theta^*$ from prior $\pi(\theta)$
2. Simulate data $x^*$ from $f(x \mid \theta^*)$
3. Accept $\theta^*$ if $d(x^*, x_{\text{obs}}) \leq \varepsilon$

### Output

The accepted samples approximate:
$$\pi(\theta \mid d(x, x_{\text{obs}}) \leq \varepsilon)$$

As $\varepsilon \to 0$ (and $n \to \infty$), this converges to the true posterior $\pi(\theta \mid x_{\text{obs}})$.

### Acceptance Rate

The acceptance rate equals $P(d(x, x_{\text{obs}}) \leq \varepsilon)$. For high-dimensional $x$, this can be extremely low. This is why summary statistics are crucial.

## Summary Statistics

### Need for Summaries

When $x$ is high-dimensional (e.g., time series, images), comparing full data vectors is computationally infeasible and requires tiny $\varepsilon$.

### Choosing Summary Statistics

Use $S(x)$ that capture relevant features:
- **Sufficient statistics** (if known): optimal but rarely available for complex models
- **Domain-specific:** mean, variance, autocorrelation, quantiles, spectral density
- **Automatic:** Random forests, neural network embeddings, moment networks

### Pitfall

Insufficient statistics lose information. The ABC posterior then approximates $\pi(\theta \mid S(x_{\text{obs}}))$, which can be very different from $\pi(\theta \mid x_{\text{obs}})$.

## ABC-MCMC

### Algorithm

1. Initialize $\theta^{(0)}$
2. For iteration $t$:
   a. Propose $\theta^* \sim q(\cdot \mid \theta^{(t)})$
   b. Simulate $x^* \sim f(x \mid \theta^*)$
   c. Accept $\theta^{(t+1)} = \theta^*$ with probability:
      $$\min\left(1, \frac{\pi(\theta^*)}{\pi(\theta^{(t)})} \cdot \frac{q(\theta^{(t)} \mid \theta^*)}{q(\theta^* \mid \theta^{(t)})} \cdot I(d(S(x^*), S(x_{\text{obs}})) \leq \varepsilon)\right)$$
   d. Otherwise $\theta^{(t+1)} = \theta^{(t)}$

### Challenges

- Chain can get stuck if $\varepsilon$ is too small (low acceptance)
- MCMC may not explore the full posterior if proposal is poor
- Convergence diagnostics are difficult (likelihood not available)

## ABC-SMC (Sequential Monte Carlo)

### Population-Based Approach

1. Start with tolerance $\varepsilon_1$ (large), sample $N$ particles from prior
2. For generation $t = 2, \dots, T$:
   a. Perturb each particle using kernel $K(\theta \mid \theta^*)$
   b. Simulate data, accept if $d(S(x^*), S(x_{\text{obs}})) \leq \varepsilon_t$
   c. Weight particles by importance weights
   d. Resample $N$ particles with replacement
3. Progressively reduce $\varepsilon_t \to \varepsilon_T$

### Advantages

- Better exploration than ABC-MCMC
- Naturally parallelizable
- Provides an estimate of marginal likelihood

## Choosing Tolerance $\varepsilon$

| Method | Description |
|--------|-------------|
| Fixed quantile | Accept top $p\%$ (e.g., 0.1%) of simulations |
| Cross-validation | Test different $\varepsilon$ on held-out data |
| Diagnostic plots | Posterior vs $\varepsilon$ — stable region indicates convergence |
| $\varepsilon$-calibration | Accept fixed number of simulations per batch |

### Bias-Variance Tradeoff

- **Small $\varepsilon$:** Less bias, lower acceptance rate (more computation)
- **Large $\varepsilon$:** More bias (poor approximation), higher acceptance

## Regression Adjustment

### Beaumont et al. (2002)

After obtaining accepted samples $(\theta_i, S(x_i^*))$, fit:
$$\theta_i = \mu + \beta^\top (S(x_i^*) - S(x_{\text{obs}})) + \varepsilon_i$$

Adjusted samples:
$$\theta_i^* = \theta_i - \beta^\top (S(x_i^*) - S(x_{\text{obs}}))$$

### Benefits

- Reduces the bias from non-zero $\varepsilon$
- Effectively "projects" accepted samples toward the region where $S(x^*) \approx S(x_{\text{obs}})$
- Can use local linear regression or neural networks

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LinearRegression

# Simulator: g-and-k distribution (intractable likelihood)
# This is a standard ABC benchmark
def gk_simulator(theta, n=100):
    """Simulate from g-and-k distribution."""
    A, B, g, k = theta
    z = np.random.normal(0, 1, n)
    # Transformation
    x = A + B * (1 + 0.8 * (1 - np.exp(-g * z)) / (1 + np.exp(-g * z))) * \
        (1 + z**2)**k * z
    return x

def gk_summary(x):
    """Summary statistics for g-and-k distribution."""
    return np.array([
        np.median(x),
        np.percentile(x, 25) - np.percentile(x, 75),  # IQR (note: reversed sign)
        np.percentile(x, 25),
        np.percentile(x, 75),
    ])

# True parameters
theta_true = np.array([3.0, 1.0, 2.0, 0.5])
x_obs = gk_simulator(theta_true, n=500)
S_obs = gk_summary(x_obs)

# Rejection ABC
n_sim = 50000
prior_bounds = np.array([
    [0, 10],    # A
    [0, 5],     # B
    [0, 5],     # g
    [0, 2],     # k
])

thetas = np.random.uniform(prior_bounds[:, 0], prior_bounds[:, 1],
                            size=(n_sim, 4))
S_sim = np.zeros((n_sim, 4))

for i in range(n_sim):
    x_sim = gk_simulator(thetas[i], n=500)
    S_sim[i] = gk_summary(x_sim)

# Normalize summaries
S_mean = S_sim.mean(axis=0)
S_std = S_sim.std(axis=0)
S_sim_norm = (S_sim - S_mean) / S_std
S_obs_norm = (S_obs - S_mean) / S_std

# Distance
distances = np.sqrt(((S_sim_norm - S_obs_norm)**2).sum(axis=1))

# Accept top 1%
epsilon = np.percentile(distances, 1)
accepted = distances <= epsilon

print(f"Acceptance rate: {accepted.mean():.4f}")
print(f"True parameters: {theta_true}")
print(f"ABC posterior means: {thetas[accepted].mean(axis=0)}")

# Regression adjustment
reg = LinearRegression().fit(S_sim[accepted], thetas[accepted])
theta_adjusted = thetas[accepted] - \
    (S_sim[accepted] - S_obs) @ reg.coef_.T

print(f"Adjusted posterior means: {theta_adjusted.mean(axis=0)}")

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
param_names = ['A (location)', 'B (scale)', 'g (skewness)', 'k (kurtosis)']

for i, (ax, name) in enumerate(zip(axes.flatten(), param_names)):
    ax.hist(thetas[accepted, i], bins=30, density=True, alpha=0.5,
            label='Raw ABC', color='blue')
    ax.hist(theta_adjusted[:, i], bins=30, density=True, alpha=0.5,
             label='Adjusted', color='red')
    ax.axvline(theta_true[i], color='green', lw=2, label=f'True={theta_true[i]}')
    ax.set_xlabel(name)
    ax.set_ylabel('Density')
    ax.legend(fontsize=8)

plt.suptitle('ABC Posterior for g-and-k Distribution')
plt.tight_layout()
plt.show()
```

## Visualization

Create a four-panel figure showing: (1) ABC posterior vs true value for each parameter; (2) Distance distribution (most simulations are far from observed data); (3) Posterior vs $\varepsilon$ to check convergence; (4) P-P plot for calibration check. The regression-adjusted posterior should be tighter and less biased.

## Practical Considerations

- **Curse of dimensionality:** ABC works poorly when the summary statistic dimension exceeds 5-10. Use dimension reduction.
- **Sufficiency:** Without sufficient statistics, ABC targets the wrong posterior. Use many summary statistics and hope they're "approximately sufficient."
- **Likelihood-free inference:** ABC is one of several likelihood-free methods. Others include synthetic likelihood, BOLFI, and neural likelihood estimation.
- **Validation:** Always validate ABC using known data (simulate from known $\theta$, apply ABC, check coverage).

## References

- Tavaré, S., et al. (1997). "Inferring coalescence times from DNA sequence data"
- Beaumont, M. A., Zhang, W., & Balding, D. J. (2002). "Approximate Bayesian computation in population genetics"
- Sisson, S. A., Fan, Y., & Tanaka, M. M. (2007). "Sequential Monte Carlo without likelihoods"
- Marin, J. M., et al. (2012). "Approximate Bayesian computational methods"
- Csilléry, K., et al. (2010). "Approximate Bayesian computation (ABC) in practice"
