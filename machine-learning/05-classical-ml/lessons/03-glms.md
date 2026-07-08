# Lesson 05.03: Generalized Linear Models (GLMs)

## Learning Objectives
- Understand the three components of GLMs (random, systematic, link)
- Derive IRLS for GLM parameter estimation
- Implement GLMs for Poisson, Gamma, and Binomial families
- Analyze deviance for model comparison

## Mathematical Foundation

### Three Components
1. **Random component**: $y \sim \text{ExponentialFamily}(\eta)$
2. **Systematic component**: $\eta = X\beta$
3. **Link function**: $g(\mu) = \eta$ where $\mu = \mathbb{E}[y|X]$

### Exponential Family Form
$$p(y|\theta, \phi) = \exp\left(\frac{y\theta - b(\theta)}{a(\phi)} + c(y, \phi)\right)$$

Key identities:
- $\mu = \mathbb{E}[y] = b'(\theta)$
- $\text{Var}(y) = b''(\theta) a(\phi)$
- $b''(\theta)$ is the variance function $V(\mu)$

### Canonical Link
When $g = (b')^{-1}$, the link is canonical and $\theta = \eta$. This simplifies the gradient and ensures certain optimality properties.

### Common GLM Families
| Distribution | Canonical Link | Variance $V(\mu)$ | Dispersion | Usage |
|-------------|---------------|---------------------|------------|-------|
| Normal | Identity ($\mu$) | 1 | $\sigma^2$ | Continuous response |
| Binomial | Logit ($\log\frac{\mu}{1-\mu}$) | $\mu(1-\mu)$ | 1 | Binary/proportion |
| Poisson | Log ($\log\mu$) | $\mu$ | 1 | Count data |
| Gamma | Inverse ($1/\mu$) | $\mu^2$ | $\nu^{-1}$ | Positive skewed |
| Inverse Gaussian | $1/\mu^2$ | $\mu^3$ | $\lambda^{-1}$ | Positive continuous |

## IRLS (Iteratively Reweighted Least Squares)
The estimation algorithm works for any GLM:

$$\beta_{t+1} = (X^\top W_t X)^{-1} X^\top W_t z_t$$

Where:
- $W_{ii} = \frac{1}{g'(\mu_i)^2 V(\mu_i)}$ — weights from variance function and link derivative
- $z_i = \eta_i + (y_i - \mu_i) g'(\mu_i)$ — working response (linearized)
- At convergence, this is equivalent to Fisher scoring

### Derivation
Starting from log-likelihood:

$$\ell(\beta) = \sum_i \frac{y_i\theta_i - b(\theta_i)}{a(\phi)} + c(y_i, \phi)$$

Score function: $s(\beta) = \frac{\partial \ell}{\partial \beta} = \frac{1}{a(\phi)} \sum_i \frac{(y_i - \mu_i)}{V(\mu_i)} \frac{\partial \mu_i}{\partial \eta_i} x_i$

Fisher information: $I(\beta) = \mathbb{E}[-\frac{\partial^2 \ell}{\partial \beta \partial \beta^\top}] = \frac{1}{a(\phi)} X^\top W X$

## Deviance
Generalization of residual sum of squares:

$$D = 2\phi \left[ \ell(y; y) - \ell(\hat{\mu}; y) \right]$$

The saturated model (one parameter per observation) gives the maximum achievable likelihood. Deviance is $2\phi$ times the log-likelihood ratio.

For Normal: $D = \sum_i (y_i - \hat{\mu}_i)^2$ (RSS)
For Binomial: $D = 2\sum_i [y_i \log(y_i/\hat{\mu}_i) + (1-y_i)\log((1-y_i)/(1-\hat{\mu}_i))]$
For Poisson: $D = 2\sum_i [y_i \log(y_i/\hat{\mu}_i) - (y_i - \hat{\mu}_i)]$

### Model Comparison
- Nested models: $D_{\text{reduced}} - D_{\text{full}} \sim \chi^2_{df_{\text{diff}}}$
- AIC: $\text{AIC} = -2\ell(\hat{\beta}) + 2p$ ($p$ = parameters)
- Smaller deviance indicates better fit (but penalize complexity)

## Residuals for GLMs
- **Pearson**: $r_{Pi} = (y_i - \hat{\mu}_i) / \sqrt{V(\hat{\mu}_i)}$
- **Deviance**: $r_{Di} = \text{sign}(y_i - \hat{\mu}_i) \sqrt{d_i}$
- **Working**: $r_{Wi} = (z_i - \hat{\eta}_i) / \sqrt{W_{ii}}$
- **Anscombe**: normalizing transform for approximate normality

## Code: Poisson GLM from Scratch

```python
import numpy as np
from scipy.special import gammaln

def poisson_glm(X, y, max_iter=100, tol=1e-8):
    """Poisson regression via IRLS with log link"""
    n, d = X.shape
    beta = np.zeros(d)
    for iteration in range(max_iter):
        eta = X @ beta
        mu = np.exp(eta)  # inverse link
        W = np.diag(mu)   # variance = mu, derivative = mu
        z = eta + (y - mu) / mu
        beta_new = np.linalg.solve(X.T @ W @ X, X.T @ W @ z)
        if np.linalg.norm(beta_new - beta) < tol:
            break
        beta = beta_new
    return beta
```

## Practical Considerations
- **Overdispersion**: If residual deviance > residual df, consider Quasi-Poisson or Negative Binomial
- **Zero inflation**: Use zero-inflated variants when excess zeros present
- **Convergence**: GLMs may oscillate; use step-halving if likelihood decreases
- **Link misspecification**: Use AIC to compare link functions
- **Sparse data**: Firth's bias-reduced logistic regression for rare events
- **Diagnostics**: Plot deviance residuals vs fitted values to detect patterns

## Key Points
- Unifies linear, logistic, Poisson, and many other models
- IRLS handles all GLMs uniformly
- Deviance generalizes RSS for model comparison
- Canonical links give simpler updates
- $O(nd^2)$ per IRLS iteration (same as OLS)

## References
- McCullagh & Nelder, "Generalized Linear Models", 2nd ed.
- Nelder & Wedderburn, "Generalized Linear Models" (JRSS-A, 1972)
- Dobson & Barnett, "An Introduction to Generalized Linear Models"
