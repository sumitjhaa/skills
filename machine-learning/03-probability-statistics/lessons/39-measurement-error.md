# Lesson 39: Measurement Error

## Learning Objectives

After completing this lesson, you will be able to:
- Distinguish classical and Berkson measurement error
- Understand the impact of measurement error on regression
- Apply SIMEX for bias correction
- Use regression calibration with validation data
- Implement Bayesian approaches to measurement error

## Types of Measurement Error

### Classical Error Model

$$W = X + U, \quad U \perp X, \quad E[U] = 0$$

The observed measurement $W$ equals the true value $X$ plus independent error $U$.

**Impact:** Attenuation bias — regression coefficients are biased toward zero.

### Berkson Error Model

$$X = W + U, \quad U \perp W$$

The true value $X$ equals the assigned/observed $W$ plus error $U$ independent of $W$.

**Impact:** In linear regression, no bias: $E[Y \mid W] = \beta_0 + \beta_1 W$ (same coefficients). But variance is inflated.

### Differential vs Non-Differential Error

- **Non-differential:** $Y \perp W \mid X$ (error independent of outcome given truth)
- **Differential:** Error depends on outcome — more problematic

## Impact on Linear Regression

### Simple Linear Regression

True model: $Y = \beta_0 + \beta_1 X + \varepsilon$
Observed: $W = X + U$, $U \sim (0, \sigma_U^2)$

The observed regression on $W$:
$$\hat{\beta}_1 \xrightarrow{p} \beta_1 \cdot \frac{\sigma_X^2}{\sigma_X^2 + \sigma_U^2} = \beta_1 \cdot \lambda$$

where $\lambda = \sigma_X^2 / (\sigma_X^2 + \sigma_U^2)$ is the **reliability ratio** (attenuation factor).

### Multiple Regression

Attenuation is more complex — coefficients for error-prone variables are biased toward zero, but coefficients for correctly measured variables can be biased in either direction (contamination effect).

### Attenuation Factor Estimation

If validation data (true $X$ measured on a subset) or replication data (multiple $W$ measurements) are available:
$$\hat{\lambda} = \frac{\text{Cov}(W_1, W_2)}{\text{Var}(W)}$$

## Impact on Nonlinear Models

| Model | Effect of Classical Error |
|-------|--------------------------|
| Logistic regression | Bias toward null |
| Poisson regression | Bias toward null |
| Cox regression | Bias toward null |
| Non-parametric regression | Smearing (oversmoothing) |

## SIMEX (Simulation-Extrapolation)

### Algorithm

1. **Simulation:** For each $b \in \{0, \lambda, 2\lambda, \dots, B\lambda\}$:
   a. Generate additional errors $U_b \sim \mathcal{N}(0, b\sigma_U^2)$
   b. Add to $W$: $W_b = W + U_b$
   c. Estimate $\hat{\beta}(b)$ from regression on $W_b$

2. **Extrapolation:** Fit a parametric model $\hat{\beta}(b) = f(b; \gamma)$, extrapolate to $b = -1$:
   $$\hat{\beta}_{\text{SIMEX}} = f(-1; \hat{\gamma})$$

### Advantages

- Works with any regression method
- No distributional assumptions for $X$
- Intuitive — shows the trend as error increases

## Regression Calibration

### Steps

1. **Calibration model:** Estimate $E[X \mid W, Z]$ from validation data or replicates
   - Usually a linear regression: $E[X \mid W] = \gamma_0 + \gamma_1 W$
2. **Imputation:** Replace observed $W$ with predicted $\hat{X} = E[X \mid W]$
3. **Analysis:** Run regression on $\hat{X}$
4. **Variance correction:** Adjust SEs for imputation uncertainty (bootstrapping or sandwich estimator)

### Validation Study Design

- **Internal validation:** Measure $X$ and $W$ on a random subset of the main study
- **External validation:** Use a separate study with both $X$ and $W$
- **Replication:** Multiple $W$ measurements on each subject (no gold standard)

## Bayesian Methods

### Full Probability Model

$$Y \sim f(Y \mid X, \theta)$$
$$W \sim g(W \mid X, \psi)$$
$$X \sim h(X \mid \phi)$$

- All parameters $(\theta, \psi, \phi)$ estimated jointly via MCMC
- Naturally handles uncertainty from measurement error
- Flexible for complex error structures

### Prior Specification

- Prior for $\sigma_U^2$ is crucial — use weakly informative priors (e.g., Half-Cauchy)
- Prior for $X$ can be flexible (mixture of normals, DP)

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Generate data with classical measurement error
np.random.seed(42)
n = 500
sigma_X = 2.0
sigma_U = 1.5
sigma_Y = 1.0

X = np.random.normal(0, sigma_X, n)
U = np.random.normal(0, sigma_U, n)
W = X + U  # observed with error

beta0, beta1 = 2.0, 1.5
Y = beta0 + beta1 * X + np.random.normal(0, sigma_Y, n)

# Naive regression (using W)
reg_naive = LinearRegression().fit(W.reshape(-1, 1), Y)
print(f"True β1 = {beta1}")
print(f"Naive β1 = {reg_naive.coef_[0]:.3f}")
print(f"Attenuation = {reg_naive.coef_[0] / beta1:.3f}")
print(f"Reliability λ = {sigma_X**2 / (sigma_X**2 + sigma_U**2):.3f}")

# SIMEX
def simex(W, Y, sigma_U, n_sim=100, B=2.0, n_steps=10):
    lambda_vals = np.linspace(0, B, n_steps)
    beta_estimates = []

    for lam in lambda_vals:
        beta_b = []
        for _ in range(n_sim):
            U_add = np.random.normal(0, np.sqrt(lam * sigma_U**2), len(W))
            W_b = W + U_add
            reg = LinearRegression().fit(W_b.reshape(-1, 1), Y)
            beta_b.append(reg.coef_[0])
        beta_estimates.append(np.mean(beta_b))

    # Quadratic extrapolation to λ = -1
    coefs = np.polyfit(lambda_vals + 1, beta_estimates, 2)
    beta_simex = np.polyval(coefs, 0)  # evaluate at λ = -1
    return lambda_vals, beta_estimates, beta_simex

lambda_vals, beta_ests, beta_simex = simex(W, Y, sigma_U)

print(f"SIMEX β1 = {beta_simex:.3f}")

# Regression calibration (assuming known reliability)
reliability = sigma_X**2 / (sigma_X**2 + sigma_U**2)
X_cal = W * reliability  # E[X|W] = λW (since both centered)
reg_cal = LinearRegression().fit(X_cal.reshape(-1, 1), Y)
print(f"Regression calibration β1 = {reg_cal.coef_[0]:.3f}")

# Visualization
plt.figure(figsize=(12, 4))

plt.subplot(131)
plt.scatter(X, Y, alpha=0.3, label='True X')
plt.scatter(W, Y, alpha=0.3, marker='x', label='Observed W')
plt.xlabel('X / W')
plt.ylabel('Y')
plt.legend()
plt.title('True vs Observed Relationship')

plt.subplot(132)
plt.plot(lambda_vals + 1, beta_ests, 'bo-', label='Simulated estimates')
plt.axhline(y=beta1, color='g', linestyle='--', label=f'True β₁={beta1}')
plt.axhline(y=beta_simex, color='r', linestyle='--', label=f'SIMEX β₁={beta_simex:.3f}')
plt.axvline(x=0, color='k', linestyle=':')
plt.xlabel('λ + 1')
plt.ylabel('Estimated β₁')
plt.legend()
plt.title('SIMEX: Extrapolation to λ=-1')

plt.subplot(133)
methods = ['True', 'Naive', 'Calibration', 'SIMEX']
estimates = [beta1, reg_naive.coef_[0], reg_cal.coef_[0], beta_simex]
colors = ['green', 'red', 'blue', 'purple']
for i, (m, e, c) in enumerate(zip(methods, estimates, colors)):
    plt.bar(i, e, color=c, alpha=0.7)
plt.axhline(y=beta1, color='k', linestyle='--')
plt.xticks(range(len(methods)), methods)
plt.ylabel('β₁ estimate')
plt.title('Method Comparison')

plt.tight_layout()
plt.show()
```

## Visualization

Create the SIMEX extrapolation plot: points showing estimates at each error inflation level, the fitted quadratic curve, and the extrapolated estimate at $\lambda = -1$ (the "no error" point). The plot should show a clear trend that extrapolates back to the truth. Add a "true vs observed" scatterplot showing attenuation.

## Practical Considerations

- **Multiple error-prone variables:** Measurement error in one variable contaminates coefficients for others. Use multivariate methods.
- **Error variance known?** Rarely. Use replicates, validation data, or sensitivity analysis over a range of plausible $\sigma_U^2$ values.
- **Instrumental variables:** If a valid instrument $Z$ is available (correlated with $X$, independent of $U$), use IV methods.
- **Reporting:** Always report the reliability ratio if known, and conduct sensitivity analysis. Show how conclusions change for plausible error magnitudes.

## References

- Fuller, W. A. (1987). *Measurement Error Models*
- Carroll, R. J., et al. (2006). *Measurement Error in Nonlinear Models* (2nd ed.)
- Cook, J. R. & Stefanski, L. A. (1994). "Simulation-extrapolation estimation in parametric measurement error models"
- Rosner, B., Spiegelman, D., & Willett, W. C. (1990). "Correction of logistic regression relative risk estimates and confidence intervals for measurement error"
