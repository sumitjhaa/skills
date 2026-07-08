# Lesson 22: Generalized Linear Models (GLMs)

## Learning Objectives

After completing this lesson, you will be able to:
- Identify the three components of a GLM (random, systematic, link)
- Understand the canonical link function and its properties
- Implement logistic regression, Poisson regression, and other GLMs
- Diagnose and address overdispersion
- Estimate GLM parameters via IRLS/Fisher scoring

## GLM Components

### Three-Part Structure

1. **Random component:** The response $Y$ follows a distribution from the exponential family:
   $$f(y \mid \theta, \phi) = \exp\left\{\frac{y\theta - b(\theta)}{a(\phi)} + c(y, \phi)\right\}$$

2. **Systematic component:** A linear predictor $\eta = X\beta$

3. **Link function:** A monotone differentiable function connecting the mean $\mu = E[Y \mid X]$ to the linear predictor:
   $$g(\mu) = \eta = X\beta$$

### Mean and Variance

For exponential family distributions:
$$E[Y] = \mu = b'(\theta)$$
$$\text{Var}(Y) = \phi \cdot b''(\theta) = \phi \cdot V(\mu)$$

where $V(\mu)$ is the **variance function**.

## Canonical Link

When the link function is chosen so that $\eta = \theta$ (the natural parameter), it is the **canonical link**:

| Distribution | Support | Canonical Link $g(\mu)$ | Variance Function $V(\mu)$ |
|-------------|---------|------------------------|---------------------------|
| Normal | $\mathbb{R}$ | Identity: $\mu$ | 1 |
| Bernoulli | $\{0,1\}$ | Logit: $\log(\mu/(1-\mu))$ | $\mu(1-\mu)$ |
| Poisson | $\{0,1,\dots\}$ | Log: $\log(\mu)$ | $\mu$ |
| Gamma | $(0, \infty)$ | Inverse: $1/\mu$ | $\mu^2$ |
| Inverse Gaussian | $(0, \infty)$ | $1/\mu^2$ | $\mu^3$ |

The canonical link simplifies MLE because the sufficient statistics appear naturally in the score equations.

## Logistic Regression

### Model

For binary $Y \in \{0, 1\}$:
$$P(Y = 1 \mid X) = \pi(X) = \frac{1}{1 + e^{-X\beta}}$$
$$\text{logit}(\pi) = \log\frac{\pi}{1-\pi} = X\beta$$

### Log-Likelihood

$$\ell(\beta) = \sum_{i=1}^n [y_i \log \pi_i + (1-y_i) \log(1-\pi_i)]$$

### Odds Ratio

The exponentiated coefficient $e^{\beta_j}$ is the **odds ratio**: a one-unit increase in $X_j$ multiplies the odds of $Y=1$ by $e^{\beta_j}$, holding other predictors constant.

### Deviance

$$D = -2 \sum [y_i \log \hat{\pi}_i + (1-y_i) \log(1-\hat{\pi}_i)]$$
Null deviance: deviance of intercept-only model. Residual deviance: deviance of fitted model. $D_{\text{null}} - D_{\text{res}} \sim \chi^2_{p-1}$ under $H_0$.

## Poisson Regression

### Model

For count data:
$$\log(E[Y \mid X]) = X\beta$$
$$P(Y = y \mid X) = \frac{e^{-\mu} \mu^y}{y!}, \quad \mu = e^{X\beta}$$

### Rate Models with Offset

When modeling rates (e.g., events per time), include an **offset**:
$$\log(E[Y \mid X]) = X\beta + \log(\text{exposure})$$

The offset has coefficient fixed at 1.

## Overdispersion

### Detection

In Poisson regression, the residual deviance should be approximately $\chi^2_{n-p}$. If $D/(n-p) \gg 1$, there is overdispersion.

### Solutions

1. **Quasi-likelihood:** Scale standard errors by $\sqrt{\hat{\phi}}$ where $\hat{\phi} = D/(n-p)$
2. **Negative binomial:** Add a dispersion parameter $r$ so that $\text{Var}(Y) = \mu + \mu^2/r$
3. **Robust sandwich estimator:** Heteroscedasticity-consistent standard errors

## Deviance and Model Comparison

### Deviance as Goodness-of-Fit

$$D = 2[\ell(y; y) - \ell(\hat{\beta}; y)]$$

- Measures discrepancy between saturated model (perfect fit) and fitted model
- Generalizes RSS from linear regression
- For Normal: $D = \text{RSS}/\sigma^2$

### Nested Model Comparison

$$D_{\text{reduced}} - D_{\text{full}} \sim \chi^2_{df_{\text{full}} - df_{\text{reduced}}}$$

## IRLS Algorithm (Fisher Scoring)

GLM parameters are estimated via **Iteratively Reweighted Least Squares**:

1. Initialize $\hat{\beta}^{(0)}$
2. For iteration $t$:
   a. Compute linear predictor: $\eta^{(t)} = X\hat{\beta}^{(t)}$
   b. Compute fitted means: $\mu^{(t)} = g^{-1}(\eta^{(t)})$
   c. Compute working weights: $W^{(t)} = \text{diag}\left(\frac{(g'(\mu^{(t)}))^2}{V(\mu^{(t)})}\right)$
   d. Compute working response: $z^{(t)} = \eta^{(t)} + g'(\mu^{(t)})(y - \mu^{(t)})$
   e. Update: $\hat{\beta}^{(t+1)} = (X^\top W^{(t)} X)^{-1} X^\top W^{(t)} z^{(t)}$
3. Repeat until convergence

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression, PoissonRegressor
from sklearn.preprocessing import StandardScaler

# Logistic Regression
np.random.seed(42)
n = 200
X = np.random.randn(n, 2)
beta_true = np.array([1.0, -0.5])
logit = X @ beta_true
y = 1 / (1 + np.exp(-logit)) > np.random.uniform(0, 1, n)

# Using statsmodels
X_with_intercept = sm.add_constant(X)
logit_model = sm.Logit(y, X_with_intercept).fit()
print(logit_model.summary())
print(f"Odds ratios: {np.exp(logit_model.params)}")

# Using sklearn
clf = LogisticRegression(C=1e10, solver='lbfgs').fit(X, y)
print(f"Sklearn coefficients: {clf.intercept_[0]:.3f}, {clf.coef_[0]}")

# ROC curve
from sklearn.metrics import roc_curve, roc_auc_score
y_pred = clf.predict_proba(X)[:, 1]
fpr, tpr, _ = roc_curve(y, y_pred)
auc = roc_auc_score(y, y_pred)

plt.figure(figsize=(12, 4))
plt.subplot(121)
plt.plot(fpr, tpr, lw=2, label=f'AUC = {auc:.3f}')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.title('ROC Curve')

# Poisson regression
n_pois = 200
X_pois = np.random.randn(n_pois, 2)
mu_pois = np.exp(1.0 + X_pois[:, 0] * 0.5 - X_pois[:, 1] * 0.3)
y_pois = np.random.poisson(mu_pois)

pois_model = sm.GLM(y_pois, sm.add_constant(X_pois),
                     family=sm.families.Poisson()).fit()
print(f"\nPoisson regression deviance: {pois_model.deviance:.1f}")
print(f"Deviance / df: {pois_model.deviance / pois_model.df_resid:.3f}")

# Check for overdispersion
if pois_model.deviance / pois_model.df_resid > 1.5:
    print("Overdispersion detected — using Negative Binomial")
    nb_model = sm.GLM(y_pois, sm.add_constant(X_pois),
                      family=sm.families.NegativeBinomial()).fit()
    print(nb_model.summary())

# Model predictions
plt.subplot(122)
plt.scatter(mu_pois, pois_model.fittedvalues, alpha=0.5)
plt.plot([0, mu_pois.max()], [0, mu_pois.max()], 'r--')
plt.xlabel('True mean')
plt.ylabel('Fitted mean')
plt.title('Poisson Regression: Fitted vs True')
plt.tight_layout()
plt.show()
```

## Visualization

Create a three-panel figure: (1) Logistic regression: data and decision boundary with $\pi = 0.5$ contour; (2) Poisson regression: observed vs fitted counts; (3) Deviance residuals vs linear predictor to check model fit and overdispersion.

## Practical Considerations

- **Separation in logistic regression:** When classes are perfectly separable, MLE does not exist (coefficients diverge). Use Firth's penalized likelihood or Bayesian logistic regression.
- **Rare events:** Logistic regression underestimates $P(Y=1)$ for rare events. Use case-control sampling with offset correction or complementary log-log link.
- **Zero inflation:** For count data with excess zeros, use zero-inflated Poisson (ZIP) or hurdle models.
- **Multiple comparisons:** When testing many predictors, adjust p-values for multiple testing.

## References

- McCullagh, P. & Nelder, J. A. (1989). *Generalized Linear Models* (2nd ed.)
- Dobson, A. J. & Barnett, A. G. (2008). *An Introduction to Generalized Linear Models*
- Agresti, A. (2015). *Foundations of Linear and Generalized Linear Models*
- Nelder, J. A. & Wedderburn, R. W. M. (1972). "Generalized linear models"
