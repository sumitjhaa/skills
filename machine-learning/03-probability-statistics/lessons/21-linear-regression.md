# Lesson 21: Linear Regression

## Learning Objectives

After completing this lesson, you will be able to:
- Derive the OLS estimator and understand its properties
- Compute and interpret fitted values, residuals, and diagnostic measures
- Perform hypothesis tests on regression coefficients
- Understand the Gauss-Markov theorem and BLUE property
- Apply regularization for high-dimensional or collinear data

## Model Specification

### Matrix Form

$$Y = X\beta + \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, \sigma^2 I)$$

- $Y \in \mathbb{R}^n$: response vector
- $X \in \mathbb{R}^{n \times p}$: design matrix (first column of 1s for intercept)
- $\beta \in \mathbb{R}^p$: coefficient vector
- $\varepsilon \in \mathbb{R}^n$: error vector, $E[\varepsilon] = 0$, $\text{Cov}(\varepsilon) = \sigma^2 I$

### Gauss-Markov Assumptions

1. **Linearity:** $E[Y \mid X] = X\beta$
2. **Full rank:** $\text{rank}(X) = p$ (no perfect multicollinearity)
3. **Exogeneity:** $E[\varepsilon \mid X] = 0$
4. **Homoscedasticity:** $\text{Var}(\varepsilon \mid X) = \sigma^2 I$ (constant variance)
5. **Independence:** $\varepsilon_i$ are independent (uncorrelated)

Normality is **not** required for Gauss-Markov (needed only for finite-sample inference).

## OLS Estimator

### Derivation

Minimize $S(\beta) = \|Y - X\beta\|_2^2 = (Y - X\beta)^\top (Y - X\beta)$:

$$\frac{\partial S}{\partial \beta} = -2X^\top Y + 2X^\top X\beta = 0$$
$$X^\top X\beta = X^\top Y \quad \text{(normal equations)}$$
$$\hat{\beta} = (X^\top X)^{-1} X^\top Y$$

### Properties

- **Unbiased:** $E[\hat{\beta}] = \beta$
- **Variance:** $\text{Var}(\hat{\beta}) = \sigma^2 (X^\top X)^{-1}$
- **Gauss-Markov:** OLS is BLUE (Best Linear Unbiased Estimator)
- **Consistent:** $\hat{\beta} \xrightarrow{p} \beta$ as $n \to \infty$

## Fitted Values and Residuals

### Hat Matrix

$$\hat{Y} = X\hat{\beta} = X(X^\top X)^{-1} X^\top Y = HY$$

$H = X(X^\top X)^{-1}X^\top$ is the **hat matrix** or **projection matrix** with properties:
- $H = H^\top$ (symmetric)
- $H = H^2$ (idempotent)
- $\text{tr}(H) = p$ (rank = number of parameters)
- $h_{ii} \in [0, 1]$ (leverage of observation $i$)

### Residuals

$$e = Y - \hat{Y} = (I - H)Y$$

Properties:
- $\sum e_i = 0$ (if intercept included)
- $e \perp \hat{Y}$ (residuals orthogonal to fitted values)
- $\text{Var}(e) = \sigma^2(I - H)$
- $\hat{\sigma}^2 = \frac{e^\top e}{n-p}$ (unbiased estimate of $\sigma^2$)

### Leverage and Influence

- **Leverage** $h_{ii}$: measures how far $x_i$ is from the center of $X$-space. High leverage $\geq 2p/n$
- **Cook's distance:** $D_i = \frac{e_i^2}{p \hat{\sigma}^2} \cdot \frac{h_{ii}}{(1-h_{ii})^2}$, measures influence of observation $i$
- **DFFITS:** $\text{DFFITS}_i = \sqrt{\frac{h_{ii}}{1-h_{ii}}} \cdot \frac{e_i}{\hat{\sigma}_{(i)} \sqrt{1-h_{ii}}}$

## Inference

### Standard Errors

$$\text{SE}(\hat{\beta}_j) = \hat{\sigma} \sqrt{((X^\top X)^{-1})_{jj}}$$

### t-tests

For $H_0: \beta_j = \beta_j^0$:
$$t_j = \frac{\hat{\beta}_j - \beta_j^0}{\text{SE}(\hat{\beta}_j)} \sim t_{n-p}$$

### F-test

For $H_0: \beta_{q+1} = \cdots = \beta_p = 0$ (reduced model):
$$F = \frac{(\text{RSS}_{\text{reduced}} - \text{RSS}_{\text{full}})/(p-q)}{\text{RSS}_{\text{full}}/(n-p)} \sim F_{p-q, n-p}$$

### Confidence and Prediction Intervals

**Confidence interval for mean response at $x_0$:**
$$\hat{y}_0 \pm t_{\alpha/2, n-p} \cdot \hat{\sigma} \sqrt{x_0^\top (X^\top X)^{-1} x_0}$$

**Prediction interval for new response at $x_0$:**
$$\hat{y}_0 \pm t_{\alpha/2, n-p} \cdot \hat{\sigma} \sqrt{1 + x_0^\top (X^\top X)^{-1} x_0}$$

## Model Fit

### R-squared

$$R^2 = 1 - \frac{\text{RSS}}{\text{TSS}} = \frac{\text{SS}_{\text{reg}}}{\text{TSS}}$$

Proportion of variance in $Y$ explained by $X$.

### Adjusted R-squared

$$\bar{R}^2 = 1 - (1-R^2)\frac{n-1}{n-p}$$

Penalizes adding uninformative predictors. Used for model selection with nested models.

## Regularized Regression

### Ridge Regression (L2)

$$\hat{\beta}_{\text{ridge}} = \arg\min \|Y-X\beta\|_2^2 + \lambda \|\beta\|_2^2$$
$$\hat{\beta}_{\text{ridge}} = (X^\top X + \lambda I)^{-1} X^\top Y$$

- Shrinks coefficients toward 0
- Closed form exists
- Does not perform variable selection

### Lasso (L1)

$$\hat{\beta}_{\text{lasso}} = \arg\min \|Y-X\beta\|_2^2 + \lambda \|\beta\|_1$$

- Performs variable selection (sparse solutions)
- No closed form (coordinate descent, LARS)
- Can select at most $n$ variables

### Elastic Net

$$\hat{\beta}_{\text{EN}} = \arg\min \|Y-X\beta\|_2^2 + \lambda_1 \|\beta\|_1 + \lambda_2 \|\beta\|_2^2$$

- Combines L1 and L2 penalties
- Handles groups of correlated predictors
- Good for $p \gg n$ problems

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm

# Generate data
np.random.seed(42)
n, p = 100, 5
X = np.random.randn(n, p)
true_beta = np.array([2.0, -1.0, 0.5, 0.0, 0.0])
y = X @ true_beta + np.random.normal(0, 0.5, n)

# OLS
X_with_intercept = sm.add_constant(X)
model = sm.OLS(y, X_with_intercept).fit()
print(model.summary())

# scikit-learn
ols = LinearRegression(fit_intercept=True).fit(X, y)
print(f"\nOLS coefficients: {ols.intercept_:.3f}, {ols.coef_}")

# Diagnostics
residuals = model.resid
fitted = model.fittedvalues

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
# Residuals vs fitted
axes[0, 0].scatter(fitted, residuals, alpha=0.6)
axes[0, 0].axhline(y=0, color='r', linestyle='--')
axes[0, 0].set_xlabel('Fitted')
axes[0, 0].set_ylabel('Residuals')
axes[0, 0].set_title('Residuals vs Fitted')

# Q-Q plot
sm.qqplot(residuals, line='s', ax=axes[0, 1])
axes[0, 1].set_title('Q-Q Plot')

# Scale-location
std_residuals = np.sqrt(np.abs(residuals / np.std(residuals)))
axes[1, 0].scatter(fitted, std_residuals, alpha=0.6)
axes[1, 0].set_xlabel('Fitted')
axes[1, 0].set_ylabel('√|Standardized residuals|')
axes[1, 0].set_title('Scale-Location')

# Cook's distance
influence = model.get_influence()
cooks = influence.cooks_distance[0]
axes[1, 1].stem(range(len(cooks)), cooks)
axes[1, 1].set_xlabel('Observation')
axes[1, 1].set_ylabel("Cook's distance")
axes[1, 1].set_title("Cook's Distance")

plt.tight_layout()
plt.show()

# Regularization comparison
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

alphas = np.logspace(-3, 2, 50)
ridge_coefs = []
lasso_coefs = []

for alpha in alphas:
    ridge = Ridge(alpha=alpha).fit(X_scaled, y)
    lasso = Lasso(alpha=alpha, max_iter=10000).fit(X_scaled, y)
    ridge_coefs.append(ridge.coef_)
    lasso_coefs.append(lasso.coef_)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for i in range(p):
    axes[0].semilogx(alphas, [c[i] for c in ridge_coefs], label=f'β{i+1}')
    axes[1].semilogx(alphas, [c[i] for c in lasso_coefs], label=f'β{i+1}')
axes[0].set_xlabel('λ')
axes[0].set_ylabel('Coefficient')
axes[0].set_title('Ridge Paths')
axes[0].legend()
axes[1].set_xlabel('λ')
axes[1].set_ylabel('Coefficient')
axes[1].set_title('Lasso Paths')
axes[1].legend()
plt.tight_layout()
plt.show()
```

## Visualization

Create a four-panel diagnostic plot: (1) Residuals vs fitted (check for non-linearity, heteroscedasticity); (2) Q-Q plot of residuals (check normality); (3) Scale-location plot (check homoscedasticity); (4) Residuals vs leverage with Cook's distance contours (identify influential points). A second figure shows coefficient paths for Ridge (smooth shrinkage) and Lasso (stepwise sparsity) as $\lambda$ varies.

## Practical Considerations

- **Multicollinearity:** High correlation among predictors inflates standard errors. Detect via VIF (Variance Inflation Factor): $\text{VIF}_j = 1/(1-R_j^2)$ where $R_j^2$ is from regressing $X_j$ on other predictors.
- **Heteroscedasticity:** Use robust standard errors (HC0, HC1, HC2, HC3) or weighted least squares.
- **Transformation:** If relationships are non-linear, try polynomial terms, splines, or GAMs.
- **Interaction terms:** Include $X_i X_j$ to model non-additive effects. Always include main effects when including interactions.
- **Categorical predictors:** Use one-hot encoding (treatment coding) with $k-1$ dummies for $k$ categories.

## References

- Gauss, C. F. (1809). *Theoria Motus Corporum Coelestium*
- Fisher, R. A. (1925). *Statistical Methods for Research Workers*
- Hoerl, A. E. & Kennard, R. W. (1970). "Ridge regression: Biased estimation for nonorthogonal problems"
- Tibshirani, R. (1996). "Regression shrinkage and selection via the lasso"
- Seber, G. A. F. & Lee, A. J. (2003). *Linear Regression Analysis*
