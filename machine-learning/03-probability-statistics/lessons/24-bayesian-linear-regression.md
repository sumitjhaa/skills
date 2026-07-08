# Lesson 24: Bayesian Linear Regression

## Learning Objectives

After completing this lesson, you will be able to:
- Specify conjugate priors for linear regression parameters
- Derive the posterior distribution for $\beta$ and $\sigma^2$
- Compute posterior predictive distributions
- Compare models using marginal likelihood and Bayes factors
- Understand the connection between Bayesian and regularized regression

## Model Specification

### Likelihood

$$Y = X\beta + \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, \sigma^2 I)$$

The likelihood function:
$$f(Y \mid \beta, \sigma^2) = (2\pi\sigma^2)^{-n/2} \exp\left\{-\frac{1}{2\sigma^2}(Y - X\beta)^\top (Y - X\beta)\right\}$$

## Conjugate Prior

### Normal-Inverse-Chi-Squared Prior

The conjugate prior for $(\beta, \sigma^2)$ is:
$$\beta \mid \sigma^2 \sim \mathcal{N}(\beta_0, \sigma^2 \Lambda_0^{-1})$$
$$\sigma^2 \sim \text{Inv-}\chi^2(\nu_0, \sigma_0^2)$$

where:
- $\beta_0$: prior mean for coefficients
- $\Lambda_0^{-1}$: prior precision matrix (scaled by $\sigma^2$)
- $\nu_0$: prior degrees of freedom
- $\sigma_0^2$: prior scale for variance

### Posterior

The posterior is also Normal-Inverse-Chi-Squared:
$$\beta \mid \sigma^2, Y \sim \mathcal{N}(\beta_n, \sigma^2 \Lambda_n^{-1})$$
$$\sigma^2 \mid Y \sim \text{Inv-}\chi^2(\nu_n, \sigma_n^2)$$

where:
$$\Lambda_n = \Lambda_0 + X^\top X$$
$$\beta_n = \Lambda_n^{-1}(\Lambda_0\beta_0 + X^\top Y)$$
$$\nu_n = \nu_0 + n$$
$$\nu_n\sigma_n^2 = \nu_0\sigma_0^2 + (Y - X\beta_n)^\top Y + (\beta_n - \beta_0)^\top \Lambda_0 (\beta_n - \beta_0)$$

### Marginal Posterior of $\beta$

Integrating out $\sigma^2$:
$$\beta \mid Y \sim t_{\nu_n}(\beta_n, \sigma_n^2 \Lambda_n^{-1})$$

A multivariate $t$-distribution with $\nu_n$ degrees of freedom.

## Special Cases

### Zellner's g-prior

$$\beta \mid \sigma^2 \sim \mathcal{N}\left(0, g\sigma^2 (X^\top X)^{-1}\right)$$

- $\Lambda_0 = \frac{1}{g} X^\top X$ (proportional to Fisher information)
- Single hyperparameter $g$ controls shrinkage
- Posterior: $\beta_n = \frac{g}{g+1} \hat{\beta}_{\text{OLS}}$
- As $g \to \infty$, posterior $\to$ OLS; as $g \to 0$, posterior $\to$ prior

### Ridge Regression as Bayesian

Ridge regression is MAP under a Normal prior $\beta \sim \mathcal{N}(0, \lambda^{-1} I)$:
$$\hat{\beta}_{\text{ridge}} = (X^\top X + \lambda I)^{-1} X^\top Y = \beta_n$$

## Posterior Predictive Distribution

For new inputs $\tilde{X}$:
$$\tilde{Y} \mid Y \sim t_{\nu_n}\left(\tilde{X}\beta_n, \sigma_n^2 (I + \tilde{X}\Lambda_n^{-1}\tilde{X}^\top)\right)$$

The predictive variance has two components:
1. **Aleatoric uncertainty:** $\sigma_n^2 I$ (irreducible noise)
2. **Epistemic uncertainty:** $\sigma_n^2 \tilde{X}\Lambda_n^{-1}\tilde{X}^\top$ (parameter uncertainty)

## Model Comparison

### Marginal Likelihood

$$m(Y) = \int f(Y \mid \beta, \sigma^2) \pi(\beta, \sigma^2) \, d\beta \, d\sigma^2$$

Available in closed form for conjugate priors:
$$m(Y) = \frac{1}{\pi^{n/2}} \frac{|\Lambda_0|^{1/2}}{|\Lambda_n|^{1/2}} \frac{\Gamma(\nu_n/2)}{\Gamma(\nu_0/2)} \frac{(\nu_0\sigma_0^2/2)^{\nu_0/2}}{(\nu_n\sigma_n^2/2)^{\nu_n/2}}$$

### Bayes Factor

$$\text{BF}_{12} = \frac{m_1(Y)}{m_2(Y)}$$

Interpretation (Jeffreys' scale):
- $\text{BF} > 100$: Decisive evidence for model 1
- $10 < \text{BF} < 100$: Strong evidence
- $3 < \text{BF} < 10$: Substantial evidence
- $1 < \text{BF} < 3$: Anecdotal evidence

### BIC Approximation

$$\text{BIC} = -2\log L(\hat{\beta}, \hat{\sigma}^2) + p\log n$$
$$\log m(Y) \approx -\frac{1}{2}\text{BIC}$$

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

class BayesianLinearRegression:
    """Bayesian linear regression with conjugate Normal-Inv-Chi2 prior."""

    def __init__(self, beta_0=None, Lambda_0=None, nu_0=1, sigma2_0=1):
        self.beta_0 = beta_0
        self.Lambda_0 = Lambda_0
        self.nu_0 = nu_0
        self.sigma2_0 = sigma2_0

    def fit(self, X, y):
        n, p = X.shape
        if self.beta_0 is None:
            self.beta_0 = np.zeros(p)
        if self.Lambda_0 is None:
            self.Lambda_0 = np.eye(p) * 0.01  # weak prior

        # Posterior parameters
        self.Lambda_n = self.Lambda_0 + X.T @ X
        beta_ols = np.linalg.inv(X.T @ X) @ X.T @ y
        self.beta_n = np.linalg.solve(self.Lambda_n,
                                       self.Lambda_0 @ self.beta_0 + X.T @ y)
        self.nu_n = self.nu_0 + n
        self.sigma2_n = (self.nu_0 * self.sigma2_0 +
                         (y - X @ beta_ols).T @ (y - X @ beta_ols) +
                         (beta_ols - self.beta_0).T @ self.Lambda_0 @
                         np.linalg.solve(self.Lambda_n, X.T @ X) @
                         (beta_ols - self.beta_0)) / self.nu_n
        return self

    def predict(self, X_new):
        """Return predictive mean and variance for each point."""
        y_pred = X_new @ self.beta_n
        var_pred = self.sigma2_n * (1 + np.diag(X_new @ np.linalg.solve(
            self.Lambda_n, X_new.T)))
        return y_pred, np.sqrt(var_pred)

    def marginal_likelihood(self, X, y):
        n, p = X.shape
        log_m = (0.5 * np.linalg.slogdet(self.Lambda_0)[1] -
                 0.5 * np.linalg.slogdet(self.Lambda_n)[1] +
                 self.nu_0/2 * np.log(self.nu_0 * self.sigma2_0 / 2) -
                 self.nu_n/2 * np.log(self.nu_n * self.sigma2_n / 2) +
                 np.log(np.math.gamma(self.nu_n/2)) -
                 np.log(np.math.gamma(self.nu_0/2)) -
                 n/2 * np.log(np.pi))
        return np.exp(log_m)

# Example
np.random.seed(42)
n, p = 50, 2
X = np.random.randn(n, p)
X = np.column_stack([np.ones(n), X])
true_beta = np.array([1.0, 0.5, -0.3])
y = X @ true_beta + np.random.normal(0, 0.5, n)

# Fit Bayesian model
blr = BayesianLinearRegression(beta_0=np.zeros(3),
                                Lambda_0=0.01 * np.eye(3))
blr.fit(X, y)
print(f"Posterior mean β: {blr.beta_n}")
print(f"Posterior σ²: {blr.sigma2_n:.4f}")

# Predictions with uncertainty
X_test = np.column_stack([np.ones(20),
                          np.linspace(-2, 2, 20),
                          np.linspace(-2, 2, 20)])
y_pred, y_se = blr.predict(X_test)

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(X[:, 1], y, alpha=0.5, label='Data')
plt.plot(np.linspace(-2, 2, 20), y_pred, 'r-', lw=2, label='Predictive mean')
plt.fill_between(np.linspace(-2, 2, 20),
                  y_pred - 2*y_se, y_pred + 2*y_se,
                  color='r', alpha=0.2, label='95% interval')
plt.xlabel('X1')
plt.ylabel('y')
plt.legend()
plt.title('Bayesian Linear Regression with Uncertainty')
plt.show()

# Model comparison via marginal likelihood
print(f"\nMarginal likelihood: {blr.marginal_likelihood(X, y):.4e}")
```

## Visualization

Create a four-panel figure: (1) Prior and posterior distributions for $\beta$; (2) Predictive mean with uncertainty bands; (3) Prior predictive distribution (sampling from prior); (4) Posterior predictive check: histogram of replicated datasets with observed data overlaid.

## Practical Considerations

- **Prior sensitivity:** Check how sensitive conclusions are to prior hyperparameters. Use sensitivity analysis with multiple priors.
- **Posterior interval vs credible interval:** Both are available — use HPD interval for multi-modal posteriors.
- **Non-informative priors:** Jeffreys prior for regression: $\pi(\beta, \sigma^2) \propto 1/\sigma^2$. This gives a proper posterior when $n > p$.
- **Computational alternatives:** For non-conjugate priors (e.g., Laplace prior for Bayesian Lasso), use Stan, PyMC, or variational inference.
- **Scaling:** Standardize predictors for more interpretable priors and better MCMC mixing.

## References

- Lindley, D. V. & Smith, A. F. M. (1972). "Bayes estimates for the linear model"
- Zellner, A. (1986). "On assessing prior distributions and Bayesian regression analysis with g-prior distributions"
- Gelman, A., et al. (2013). *Bayesian Data Analysis*
- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*
