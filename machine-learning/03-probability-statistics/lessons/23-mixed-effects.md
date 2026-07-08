# Lesson 23: Mixed Effects Models

## Learning Objectives

After completing this lesson, you will be able to:
- Specify linear mixed models with random intercepts and slopes
- Distinguish fixed from random effects
- Estimate parameters via ML and REML
- Compute and interpret the intraclass correlation coefficient (ICC)
- Extend to generalized linear mixed models (GLMMs)

## Linear Mixed Model

### Model Specification

$$Y = X\beta + Z\gamma + \varepsilon$$

where:
- $Y \in \mathbb{R}^n$: response vector
- $X \in \mathbb{R}^{n \times p}$: fixed effects design matrix
- $\beta \in \mathbb{R}^p$: fixed effects coefficients (population-level)
- $Z \in \mathbb{R}^{n \times q}$: random effects design matrix
- $\gamma \in \mathbb{R}^q$: random effects, $\gamma \sim \mathcal{N}(0, G)$
- $\varepsilon \in \mathbb{R}^n$: residual error, $\varepsilon \sim \mathcal{N}(0, R)$
- $\gamma \perp \varepsilon$ (independent)

### Marginal Model

Integrating out the random effects:
$$Y \sim \mathcal{N}(X\beta, ZGZ^\top + R)$$

The marginal covariance $\Sigma = ZGZ^\top + R$ has a structured form that captures within-group correlation.

## Common Random Effect Structures

### Random Intercept

$$Y_{ij} = \beta_0 + \beta_1 x_{ij} + b_{0i} + \varepsilon_{ij}$$

- $b_{0i} \sim \mathcal{N}(0, \sigma_b^2)$: subject-specific intercept deviation
- $\varepsilon_{ij} \sim \mathcal{N}(0, \sigma_e^2)$
- Within-group correlation: $\text{Corr}(Y_{ij}, Y_{ik}) = \frac{\sigma_b^2}{\sigma_b^2 + \sigma_e^2} = \rho$ (constant)

### Random Intercept and Slope

$$Y_{ij} = \beta_0 + \beta_1 x_{ij} + b_{0i} + b_{1i} x_{ij} + \varepsilon_{ij}$$

- $(b_{0i}, b_{1i})^\top \sim \mathcal{N}(0, \Sigma)$ with $\Sigma = \begin{bmatrix} \sigma_0^2 & \sigma_{01} \\ \sigma_{01} & \sigma_1^2 \end{bmatrix}$
- Allows each subject to have their own intercept and slope
- Correlation between random effects is estimated

### Nested Random Effects

For students within classrooms within schools:
$$Y_{ijkl} = \beta_0 + b_{\text{school}, i} + b_{\text{class}, j(i)} + \varepsilon_{ijkl}$$

## Intraclass Correlation Coefficient (ICC)

### Definition

$$\rho = \frac{\text{Var}(\text{random intercept})}{\text{Var}(\text{random intercept}) + \text{Var}(\text{residual})}$$

- Proportion of total variance due to between-group differences
- Ranges from 0 (no group structure) to 1 (all variance between groups)
- Large ICC ($>0.1$) indicates that ignoring clustering would yield incorrect standard errors

## Estimation

### Maximum Likelihood (ML)

Maximize the log-likelihood of the marginal model:
$$\ell(\beta, \theta) = -\frac{1}{2} \log|\Sigma| - \frac{1}{2} (Y - X\beta)^\top \Sigma^{-1} (Y - X\beta) - \frac{n}{2} \log(2\pi)$$

where $\theta$ contains the variance components (parameters of $G$ and $R$).

### Restricted ML (REML)

REML estimates variance components after projecting out fixed effects. The REML log-likelihood:
$$\ell_{\text{REML}}(\theta) = \ell(\beta(\theta), \theta) - \frac{1}{2} \log|X^\top \Sigma^{-1} X|$$

- REML produces **less biased** variance component estimates (especially for small $n$)
- Use REML for variance parameters, ML for comparing fixed effects structures

## Hypothesis Testing

### Fixed Effects

- **Wald tests:** $\hat{\beta}_j / \text{SE}(\hat{\beta}_j) \sim t_{df}$ with Satterthwaite or Kenward-Roger df approximation
- **F-tests:** For multi-parameter hypotheses

### Random Effects

- **LRT:** $-2\log \Lambda \sim 0.5\chi^2_0 + 0.5\chi^2_1$ (mixture) for testing a single variance component
- **Profile likelihood:** Confidence intervals for variance components

### Model Selection

- **AIC:** $-2\ell + 2k$ (lower is better)
- **BIC:** $-2\ell + k\log n$ (penalizes complexity more)
- **LRT:** For nested models only

## Generalized Linear Mixed Models (GLMMs)

### Structure

$$g(E[Y \mid \gamma]) = X\beta + Z\gamma$$

- Extends GLMs with random effects
- Random effects $\gamma \sim \mathcal{N}(0, G)$
- Response $Y$ can be binary, count, etc.

### Estimation Challenges

GLMMs require **integrating over random effects**, which is computationally intensive:
- **Laplace approximation:** Fast, first-order approximation
- **Adaptive Gauss-Hermite quadrature:** More accurate for small clusters
- **Penalized quasi-likelihood (PQL):** Fast but can be biased

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.regression.mixed_linear_model import MixedLM
import pandas as pd

# Generate hierarchical data
np.random.seed(42)
n_groups = 20
n_per_group = 10
groups = []
y = []
x = []

sigma_b = 1.5  # random intercept SD
sigma_e = 1.0  # residual SD
beta = [2.0, 0.5]  # fixed effects (intercept, slope)

for g in range(n_groups):
    b0 = np.random.normal(0, sigma_b)  # random intercept
    x_group = np.random.uniform(-2, 2, n_per_group)
    y_group = beta[0] + b0 + beta[1] * x_group + np.random.normal(0, sigma_e, n_per_group)
    groups.extend([f'G{g+1}'] * n_per_group)
    x.extend(x_group)
    y.extend(y_group)

df = pd.DataFrame({'y': y, 'x': x, 'group': groups})

# Fit LMM
model = MixedLM.from_formula('y ~ x', groups='group', data=df)
result = model.fit(reml=True)
print(result.summary())

# Extract variance components
print(f"\nVariance components:")
print(f"  Random intercept SD: {np.sqrt(result.cov_re.iloc[0, 0]):.3f}")
print(f"  Residual SD: {result.scale:.3f}")
print(f"  ICC: {result.cov_re.iloc[0, 0] / (result.cov_re.iloc[0, 0] + result.scale):.3f}")

# Compare with OLS (ignoring clustering)
ols = sm.OLS(y, sm.add_constant(np.array(x))).fit()
print(f"\nOLS SE for x coefficient: {ols.bse[1]:.4f}")
print(f"LMM SE for x coefficient: {result.bse_fe[1]:.4f}")
print("(LMM larger because it accounts for between-group variation)")

# Random slopes model
model_rs = MixedLM.from_formula('y ~ x', groups='group',
                                 re_formula='1 + x', data=df)
result_rs = model_rs.fit(reml=True)
print("\nRandom slopes model:")
print(result_rs.summary())

# Likelihood ratio test for random slope
lr_stat = 2 * (result_rs.llf - result.llf)
p_value = 0.5 * (1 - stats.chi2.cdf(lr_stat, 1)) + 0.5 * (1 - stats.chi2.cdf(lr_stat, 0))
print(f"\nLRT for random slope: LR = {lr_stat:.3f}, p = {p_value:.4f}")

# Visualize
from scipy import stats
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Individual trajectories
for g in range(min(5, n_groups)):
    mask = df['group'] == f'G{g+1}'
    axes[0].plot(df.loc[mask, 'x'], df.loc[mask, 'y'], 'o-', alpha=0.7, label=f'G{g+1}')
axes[0].set_xlabel('x')
axes[0].set_ylabel('y')
axes[0].legend()
axes[0].set_title('Individual Group Trajectories')

# Predicted random effects
ranef = result.random_effects
axes[1].hist([v[0] for v in ranef.values()], bins=15, density=True, alpha=0.7)
xs = np.linspace(-3, 3, 100)
axes[1].plot(xs, stats.norm.pdf(xs, 0, sigma_b), 'r-', lw=2)
axes[1].set_xlabel('Random intercept')
axes[1].set_ylabel('Density')
axes[1].set_title(f'Random Intercept Distribution (SD = {sigma_b})')

plt.tight_layout()
plt.show()
```

## Visualization

Create a "spaghetti plot" showing individual group trajectories (thin lines) with the population-average fixed effect line (thick line) overlaid. The random intercepts appear as vertical shifts of the group lines from the population line. A second plot shows the distribution of estimated random effects with the theoretical $\mathcal{N}(0, \sigma_b^2)$ density overlaid.

## Practical Considerations

- **Centering:** Center continuous predictors to improve convergence and interpret random effects (especially random slopes).
- **Convergence issues:** Use optimizers (Nelder-Mead, BFGS), increase iterations, or simplify random effect structure.
- **Singular fit:** When a random effect variance is estimated as 0, the model is overparameterized. Remove the zero-variance random effect.
- **Crossed random effects:** For crossed designs (e.g., students across multiple test items), specify crossed random effects rather than nested.
- **Bayesian alternatives:** For complex random effect structures or convergence issues, use Bayesian MCMC (Stan, brms).

## References

- Laird, N. M. & Ware, J. H. (1982). "Random-effects models for longitudinal data"
- Pinheiro, J. C. & Bates, D. M. (2000). *Mixed-Effects Models in S and S-PLUS*
- Gelman, A. & Hill, J. (2007). *Data Analysis Using Regression and Multilevel/Hierarchical Models*
- Bates, D., et al. (2015). "Fitting linear mixed-effects models using lme4"
