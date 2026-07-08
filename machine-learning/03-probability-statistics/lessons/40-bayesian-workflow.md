# Lesson 40: Full Bayesian Workflow

## Learning Objectives

After completing this lesson, you will be able to:
- Apply the iterative Bayesian modeling cycle
- Conduct prior and posterior predictive checks
- Compare models using WAIC, LOO-CV, and Bayes factors
- Diagnose MCMC convergence
- Perform sensitivity analysis and communicate results

## The Bayesian Modeling Cycle

### Iterative Process (Gelman et al., 2020)

1. **Model building:** Translate domain knowledge into likelihood, prior, and model structure
2. **Prior predictive simulation:** Simulate from the prior, check if generated data is realistic
3. **Inference:** Compute posterior using MCMC, variational inference, or Laplace approximation
4. **Posterior predictive checks:** Simulate from the posterior, compare with observed data
5. **Model comparison:** Evaluate predictive performance, compare competing models
6. **Sensitivity analysis:** Check robustness to prior, likelihood, and data choices
7. **Application:** Prediction, decision-making, reporting

## Step 1: Model Building

### Components

- **Likelihood:** $f(y \mid \theta)$ — the data generating process
- **Prior:** $\pi(\theta)$ — prior knowledge about parameters
- **Structure:** Hierarchical, latent variables, missing data, measurement error

### Prior Elicitation

- Domain expert knowledge (translate to parameter scale)
- Weakly informative priors (regularize without dominating)
- Reference priors (Jeffreys, maximal data information)

## Step 2: Prior Predictive Checks

### Purpose

Check whether the prior generates plausible data before seeing the observations.

### Method

1. Sample $\theta^{(s)} \sim \pi(\theta)$
2. Sample $y^{(s)} \sim f(y \mid \theta^{(s)})$
3. Compare $y^{(s)}$ to domain knowledge:
   - Are extreme values plausible?
   - Are correlations in the right direction?
   - Are the range and scale realistic?

### Example

In a hierarchical model with $\mu \sim \mathcal{N}(0, 100)$, $\sigma \sim \text{HC}(5)$, simulate group means — would groups differ by 200 units? If not, the prior is too diffuse.

## Step 3: Posterior Inference

### Algorithms

| Method | When to Use | Pros | Cons |
|--------|-------------|------|------|
| HMC/NUTS | Complex models, small-to-medium data | Efficient exploration | Tuning required |
| Gibbs sampling | Conjugate conditional distributions | No tuning | Slow convergence |
| Variational inference | Large data, fast approximation | Fast, scalable | Approximate posterior |
| Laplace approx | Quick exploration, large $n$ | Very fast | Gaussian-only posterior |

### Convergence Diagnostics

- $\hat{R} < 1.01$ for all parameters (split $\hat{R}$)
- Effective sample size (ESS) $> 100$ per parameter
- Bulk ESS and tail ESS
- Trace plots show good mixing (no drift, no stuck chains)
- Rank histograms should be uniform

## Step 4: Posterior Predictive Checks

### Method

1. Sample $\theta^{(s)}$ from posterior $\pi(\theta \mid y)$
2. Sample $y_{\text{rep}}^{(s)} \sim f(y \mid \theta^{(s)})$ (replicated data)
3. Compare $y_{\text{rep}}$ to observed $y$

### Test Statistics

Compute discrepancy measure $T(y)$ and compare to posterior predictive distribution:
$$\text{Bayesian } p\text{-value} = P(T(y_{\text{rep}}) \geq T(y) \mid y)$$

- $p \approx 0.5$: good fit
- $p \approx 0$ or $p \approx 1$: systematic discrepancy

**Examples:** Mean, variance, skewness, min, max, autocorrelation, chi-squared statistic.

### Graphical Checks

- Histogram/density of $y_{\text{rep}}$ with $y$ overlaid
- Scatterplot of $T(y_{\text{rep}})$ vs $T(y)$
- PIT histogram (should be uniform for well-calibrated model)

## Step 5: Model Comparison

### Information Criteria

| Method | Formula | Pros | Cons |
|--------|---------|------|------|
| WAIC | $-2(\text{lppd} - p_{\text{eff}})$ | Fully Bayesian | Requires posterior draws |
| LOO-CV via PSIS | $\sum \log p(y_i \mid y_{-i})$ | Robust | Pareto $k$ diagnostics |
| Bayes factor | $m_1(y) / m_2(y)$ | Interpretable scale | Prior-sensitive |

### Leave-One-Out Cross-Validation

LOO-CV estimates out-of-sample predictive accuracy:
$$\text{elpd}_{\text{loo}} = \sum_{i=1}^n \log p(y_i \mid y_{-i})$$

**PSIS (Pareto Smoothed Importance Sampling):** Approximate LOO without refitting the model $n$ times. The Pareto $k$ diagnostic identifies influential observations ($k > 0.7$ indicates unreliable approximation).

## Step 6: Sensitivity Analysis

### Prior Sensitivity

- Perturb hyperparameters (e.g., double the scale)
- Replace with alternative weakly informative priors
- Check posterior stability

### Likelihood Sensitivity

- Replace Normal with t-distribution (robust to outliers)
- Use mixture models for multi-modal data

### Data Sensitivity

- Leave-one-out influence analysis
- Subset analysis (by group, time period)
- Add synthetic data to stress-test

## Step 7: Reporting

### Essential Elements

- **Full model specification:** Likelihood, priors, hyperparameters, data
- **Convergence diagnostics:** $\hat{R}$, ESS, trace plots
- **Posterior summaries:** Mean, SD, quantiles, ROPE
- **Predictive performance:** WAIC/LOO with SE
- **Sensitivity results:** Key quantities under alternative assumptions

### Communication

- Visualize posterior distributions (density plots, interval plots)
- Report practical significance (not just statistical significance)
- Acknowledge limitations and assumptions

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pymc as pm
import arviz as az

# Generate example data
np.random.seed(42)
n = 100
x = np.random.normal(0, 1, n)
y = 0.8 * x + np.random.normal(0, 0.5, n)

# Build model
with pm.Model() as model:
    # Priors
    alpha = pm.Normal('alpha', mu=0, sigma=10)
    beta = pm.Normal('beta', mu=0, sigma=5)
    sigma = pm.HalfCauchy('sigma', beta=5)

    # Likelihood
    mu = alpha + beta * x
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y)

    # Prior predictive
    prior_pred = pm.sample_prior_predictive(samples=50)

    # Inference
    trace = pm.sample(1000, tune=1000, chains=4, random_seed=42)

    # Posterior predictive
    posterior_pred = pm.sample_posterior_predictive(trace)

# Convert to arviz for diagnostics
idata = az.from_pymc(
    trace=trace,
    prior=prior_pred,
    posterior_predictive=posterior_pred
)

# Summary
print(az.summary(idata, hdi_prob=0.95))

# Convergence diagnostics
print(f"\nR-hat: {az.rhat(idata)}")
print(f"ESS: {az.ess(idata)}")

# Posterior predictive checks
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Trace plot
az.plot_trace(idata, axes=axes[:, 0])

# Posterior predictive check
ax = axes[0, 1]
y_rep = idata.posterior_predictive['y_obs'].values.flatten()
ax.hist(y_rep, bins=40, density=True, alpha=0.5, label='Replicated')
ax.hist(y, bins=40, density=True, alpha=0.7, label='Observed')
ax.legend()
ax.set_title('Posterior Predictive Check')

# PIT histogram
ax = axes[1, 1]
az.plot_ppc(idata, ax=ax, alpha=0.3)
ax.set_title('PPC with uncertainty')

plt.tight_layout()
plt.show()

# WAIC and LOO
waic = az.waic(idata)
loo = az.loo(idata)
print(f"\nWAIC: {waic.waic:.1f} (SE={waic.se:.1f})")
print(f"LOO: {loo.loo:.1f} (SE={loo.se:.1f})")
print(f"Pareto k values: {loo.pareto_k.values}")

# Sensitivity analysis: try different priors
sensitivities = {}
for prior_scale in [1, 5, 10, 50]:
    with pm.Model() as model_sens:
        alpha = pm.Normal('alpha', mu=0, sigma=prior_scale)
        beta = pm.Normal('beta', mu=0, sigma=prior_scale)
        sigma = pm.HalfCauchy('sigma', beta=prior_scale)
        mu = alpha + beta * x
        y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y)
        trace_sens = pm.sample(500, tune=500, chains=2, random_seed=42,
                                progressbar=False)
    sensitivities[prior_scale] = {
        'alpha': trace_sens.posterior['alpha'].mean().item(),
        'beta': trace_sens.posterior['beta'].mean().item(),
    }

print("\nPrior sensitivity analysis:")
for scale, estimates in sensitivities.items():
    print(f"  Prior SD={scale}: α={estimates['alpha']:.3f}, β={estimates['beta']:.3f}")
```

## Visualization

Create a comprehensive workflow figure showing all steps: (1) Prior predictive distribution — do simulated datasets look plausible? (2) Trace plots and $\hat{R}$ diagnostics; (3) Posterior predictive check: replicated data histogram vs observed; (4) LOO-PIT (probability integral transform) histogram, expected to be uniform.

## Practical Considerations

- **Iterate:** Rarely get the model right the first time. Each iteration of prior/posterior checks may reveal model flaws.
- **Computational cost:** Prior predictive checks are cheap (no inference needed). Posterior predictive checks and LOO require full inference.
- **p-values are not for model selection:** Bayesian p-values measure discrepancy, not "significance." They are useful for model criticism, not model comparison.
- **Reporting negative results:** When sensitivity analysis shows instability, report it. Models with strong prior sensitivity are not trustworthy.

## References

- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd ed.)
- Gelman, A., et al. (2020). "Bayesian workflow"
- Vehtari, A., Gelman, A., & Gabry, J. (2017). "Practical Bayesian model evaluation using leave-one-out cross-validation and WAIC"
- Betancourt, M. (2018). "A conceptual introduction to Hamiltonian Monte Carlo"
- McElreath, R. (2020). *Statistical Rethinking* (2nd ed.)
