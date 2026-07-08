# Lesson 34: Missing Data

## Learning Objectives

After completing this lesson, you will be able to:
- Classify missing data mechanisms (MCAR, MAR, MNAR)
- Understand the consequences of each mechanism
- Apply appropriate imputation methods
- Implement multiple imputation with Rubin's rules
- Use EM algorithm for missing data

## Missing Data Mechanisms

Rubin (1976) classified missing data into three mechanisms based on the relationship between missingness and the data.

### Notation

- $Y_{\text{obs}}$: observed values
- $Y_{\text{mis}}$: missing values
- $R$: indicator matrix ($R_{ij} = 1$ if $Y_{ij}$ is observed)

### MCAR (Missing Completely At Random)

$$P(R \mid Y_{\text{obs}}, Y_{\text{mis}}) = P(R)$$

Missingness is independent of both observed and missing data.

**Example:** Survey respondents accidentally skip a question due to a printing error.

**Consequences:** Complete-case analysis is unbiased but inefficient (reduced sample size).

### MAR (Missing At Random)

$$P(R \mid Y_{\text{obs}}, Y_{\text{mis}}) = P(R \mid Y_{\text{obs}})$$

Missingness depends only on observed data.

**Example:** Women are less likely to report income, but this depends only on gender (observed).

**Consequences:** Likelihood-based and Bayesian methods give valid inference if the missingness model is correctly specified (ignorability).

### MNAR (Missing Not At Random)

$$P(R \mid Y_{\text{obs}}, Y_{\text{mis}}) = P(R \mid Y_{\text{obs}}, Y_{\text{mis}})$$

Missingness depends on unobserved data.

**Example:** High earners are less likely to report income.

**Consequences:** Requires explicit modeling of the joint distribution of $(Y, R)$.

## Complete-Case Analysis

### When It's Valid

- MCAR: unbiased, but loses power
- MAR: biased if missingness depends on $Y$ even after conditioning on $X$
- MNAR: always biased

### Efficiency

If 30% of cases have any missing data, complete-case analysis discards 30% of the sample. With $m$ variables each missing independently with probability $p$, the proportion of complete cases is $(1-p)^m$ — this decreases exponentially with $m$.

## Single Imputation

### Mean Imputation

Replace missing values with the column mean.

**Problem:** Reduces variance, distorts correlations, creates artificial spikes in distribution.

### Regression Imputation

Predict missing values from observed variables:
$$\hat{y}_i = X_i \hat{\beta}$$

**Problem:** Overestimates precision (doesn't account for prediction uncertainty).

### Stochastic Regression Imputation

$$\hat{y}_i = X_i \hat{\beta} + \varepsilon_i, \quad \varepsilon_i \sim \mathcal{N}(0, \hat{\sigma}^2)$$

Preserves variance better but still treats imputed values as known.

### LOCF (Last Observation Carried Forward)

For longitudinal data, carry the last observed value forward.

**Problem:** Creates artificial flat lines, underestimates change over time.

## Multiple Imputation (MI)

### Rubin's Framework

1. **Imputation:** Create $M$ complete datasets by drawing from the predictive distribution of missing data given observed data
2. **Analysis:** Fit the model of interest to each dataset, obtaining $\hat{\theta}_m$ and $U_m$ (variance estimates)
3. **Combination:**

**Point estimate:** $\bar{\theta} = \frac{1}{M} \sum_{m=1}^M \hat{\theta}_m$

**Total variance:** $T = \bar{U} + \left(1 + \frac{1}{M}\right) B$

where:
- $\bar{U} = \frac{1}{M} \sum U_m$: within-imputation variance
- $B = \frac{1}{M-1} \sum (\hat{\theta}_m - \bar{\theta})^2$: between-imputation variance

### Number of Imputations

- $M = 5-20$ is often sufficient (older rule of thumb)
- For $\alpha = 0.05$ and desired power, use $M \geq 100$ for high precision
- With modern computing, use $M = 100$ or more

### MICE (Multivariate Imputation by Chained Equations)

Impute each variable iteratively using its own conditional model:
1. Initialize missing values with simple imputation
2. For each variable $Y_j$ with missing data:
   a. Regress $Y_j$ on all other variables (using observed $Y_j$)
   b. Impute missing $Y_j$ from the predictive distribution
3. Repeat for several cycles (convergence typically within 5-10 iterations)

## EM Algorithm

### Expectation-Maximization for Missing Data

Treat missing data as latent variables.

**E-step:** Compute expected sufficient statistics given observed data and current $\theta^{(t)}$:
$$Q(\theta \mid \theta^{(t)}) = E\left[\log f(Y_{\text{obs}}, Y_{\text{mis}} \mid \theta) \mid Y_{\text{obs}}, \theta^{(t)}\right]$$

**M-step:** Maximize $Q$:
$$\theta^{(t+1)} = \arg\max_\theta Q(\theta \mid \theta^{(t)})$$

## MNAR Models

### Selection Models

$$f(Y, R \mid X, \theta, \psi) = f(Y \mid X, \theta) \cdot f(R \mid Y, X, \psi)$$

The missingness model $f(R \mid Y, X, \psi)$ depends on the possibly missing $Y$.

### Pattern-Mixture Models

$$f(Y, R \mid X) = f(Y \mid R, X) \cdot f(R \mid X)$$

Different distributions for different missing data patterns.

### Sensitivity Analysis

Assess how conclusions change under departures from MAR using a sensitivity parameter $\delta$:
$$\text{logit}(P(R=1 \mid Y, X)) = \text{logit}(P(R=1 \mid X)) + \delta Y$$

## Python Implementation

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, SimpleImputer
from sklearn.linear_model import BayesianRidge

# Generate data with missing values (MAR)
np.random.seed(42)
n = 500
X1 = np.random.normal(0, 1, n)
X2 = 0.5 * X1 + np.random.normal(0, 0.5, n)
Y = 2 + 0.8 * X1 - 0.3 * X2 + np.random.normal(0, 0.3, n)

df = pd.DataFrame({'X1': X1, 'X2': X2, 'Y': Y})

# Create MAR missingness in X2: depends on Y
missing_prob = 1 / (1 + np.exp(-(Y - np.mean(Y)) / np.std(Y)))
# Scale so ~30% missing overall
missing_prob = missing_prob * 0.6
missing_x2 = np.random.binomial(1, missing_prob).astype(bool)
df.loc[missing_x2, 'X2'] = np.nan

print(f"Missing rate in X2: {missing_x2.mean():.1%}")

# Complete case analysis
cc = df.dropna()
cc_model = np.linalg.lstsq(
    np.column_stack([np.ones(len(cc)), cc.X1, cc.X2]),
    cc.Y, rcond=None)[0]
print(f"\nComplete case: {cc_model}")

# Mean imputation
df_mean = df.fillna(df.mean())
mean_model = np.linalg.lstsq(
    np.column_stack([np.ones(n), df_mean.X1, df_mean.X2]),
    df_mean.Y, rcond=None)[0]
print(f"Mean imputation: {mean_model}")

# Multiple imputation via MICE (using IterativeImputer)
imputer = IterativeImputer(estimator=BayesianRidge(), max_iter=10,
                            random_state=42, sample_posterior=True)
M = 20
imputed_coefs = []
for m in range(M):
    imputer.set_params(random_state=42+m)
    df_imp = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
    coef = np.linalg.lstsq(
        np.column_stack([np.ones(n), df_imp.X1, df_imp.X2]),
        df_imp.Y, rcond=None)[0]
    imputed_coefs.append(coef)

imputed_coefs = np.array(imputed_coefs)
theta_bar = imputed_coefs.mean(axis=0)
U_bar = np.var(imputed_coefs, axis=0, ddof=0)  # within
B = np.var(imputed_coefs, axis=0, ddof=1)  # between
total_var = U_bar + (1 + 1/M) * B
print(f"MI (M={M}): {theta_bar}")
print(f"MI SE: {np.sqrt(total_var)}")

# True coefficients
true_coef = [2.0, 0.8, -0.3]
print(f"True: {true_coef}")

# Compare methods
methods = ['Complete case', 'Mean imputation', f'MI (M={M})']
estimates = [cc_model, mean_model, theta_bar]
fig, axes = plt.subplots(1, 3, figsize=(12, 3))
for j, (name, est) in enumerate(zip(methods, estimates)):
    for i in range(3):
        axes[j].bar(i, est[i] - true_coef[i], alpha=0.7)
        axes[j].axhline(y=0, color='k', linestyle='-', lw=0.5)
    axes[j].set_xticks(range(3))
    axes[j].set_xticklabels(['Intercept', 'X1', 'X2'])
    axes[j].set_title(name)
    axes[j].set_ylabel('Bias')
plt.tight_layout()
plt.show()
```

## Visualization

Create a diagnostic plot showing missing data patterns: a binary matrix where rows are observations and columns are variables, with gray for observed and white for missing (using `missingno` package). Add a second panel showing the distribution of observed vs missing values for each variable to assess MAR vs MNAR.

## Practical Considerations

- **MAR assumption is untestable:** You can't verify MAR from the data because the missing values are, by definition, unobserved. Sensitivity analysis is always recommended.
- **Auxiliary variables:** Include variables that predict missingness in the imputation model to make MAR more plausible.
- **Proper imputation:** Include the outcome variable $Y$ in the imputation model. Excluding $Y$ biases associations toward zero.
- **Interactions and non-linearity:** Imputation models should include the same complexity as the analysis model (interactions, polynomial terms).
- **Convergence:** Check MICE convergence with trace plots of imputed values. Ensure enough iterations for stationarity.

## References

- Rubin, D. B. (1976). "Inference and missing data"
- Rubin, D. B. (1987). *Multiple Imputation for Nonresponse in Surveys*
- Little, R. J. A. & Rubin, D. B. (2019). *Statistical Analysis with Missing Data* (3rd ed.)
- Van Buuren, S. (2018). *Flexible Imputation of Missing Data*
- White, I. R., Royston, P., & Wood, A. M. (2011). "Multiple imputation using chained equations"
