# Lesson 05.48: Model Selection (AIC / BIC)

## Learning Objectives
- Understand information criteria for model comparison
- Derive AIC from KL divergence and BIC from marginal likelihood
- Apply MDL principle for model complexity control
- Compare with cross-validation for model selection

## AIC (Akaike Information Criterion)
$$\text{AIC} = -2 \log \hat{L} + 2k$$

- $\hat{L}$: maximized likelihood under model
- $k$: number of parameters
- Lower AIC is better
- Derived from KL divergence: minimizing AIC ≈ minimizing expected KL between true and fitted distribution

### Derivation
Akaike (1973) showed that:

$$\mathbb{E}[-2 \log L(\hat{\theta}_{\text{MLE}} | \text{new data})] \approx -2 \log \hat{L} + 2k + \text{const}$$

The $2k$ term corrects the optimism bias of in-sample log-likelihood.

**Asymptotic equivalence**: AIC ≈ leave-one-out cross-validation for large $n$.

## BIC (Bayesian Information Criterion)
$$\text{BIC} = -2 \log \hat{L} + k \log n$$

- $n$: sample size
- Penalty is stronger than AIC ($\log n > 2$ for $n > 8$)
- **Consistent**: As $n \to \infty$, BIC selects the true model with probability 1 (if true model is in the candidate set)

### Derivation (Laplace approximation)
From marginal likelihood:

$$P(D|M) = \int P(D|\theta, M) P(\theta|M) d\theta$$

Laplace approximation: $\log P(D|M) \approx \log P(D|\hat{\theta}_{\text{MLE}}) - \frac{k}{2} \log n + O(1)$

BIC ≈ $-2 \log P(D|M)$, so minimizing BIC ≈ maximizing approximate marginal likelihood.

## MDL (Minimum Description Length)
$$L(D) = L(D|M) + L(M)$$

- Total description length = data given model + model complexity
- **Two-part MDL**: First describe model (complexity), then data using model
- **Refined MDL**: Normalized maximum likelihood coding (no separate model description)

**Connection to BIC**: Both penalize complexity, but MDL derives from coding theory perspective.

## Cross-Validation

### Types
- **LOO-CV**: $O(n)$, high variance, asymptotically equivalent to AIC
- **$k$-fold CV**: $O(k)$, $k=5$ or $10$ standard
- **Repeated CV**: Multiple $k$-fold passes, reduces variance
- **Nested CV**: Outer loop for evaluation, inner for model selection

### 1-SE Rule
From Breiman et al. (1984): pick the simplest model whose CV error is within 1 standard error of the best model.

**Rationale**: The best and second-best are often statistically indistinguishable; choose simpler.

## Comparison

| Criterion | Penalty | Consistency | Target | Uses likelihood? |
|-----------|---------|-------------|--------|-----------------|
| AIC | $2k$ | No (over-selects) | Prediction error | Yes |
| BIC | $k \log n$ | Yes | True model | Yes |
| MDL | Variable | Yes | Data compression | No (coding) |
| $k$-fold CV | Data-driven | Yes | Prediction error | No |
| LOO-CV | $O(n)$ | Yes | Prediction error | No |

## Code: Model Selection with AIC/BIC

```python
import numpy as np
from scipy.stats import norm

def compute_aic_bic(model, X, y):
    """Compute AIC and BIC for a linear model"""
    n, k = X.shape
    residuals = y - model.predict(X)
    mse = np.sum(residuals**2) / n
    log_likelihood = -n/2 * np.log(2 * np.pi * mse) - n/2
    aic = -2 * log_likelihood + 2 * (k + 1)
    bic = -2 * log_likelihood + (k + 1) * np.log(n)
    return aic, bic
```

## Practical Guidelines
1. **AIC for prediction**: Minimizes expected prediction error (selects model that predicts best)
2. **BIC for identification**: Selects true model asymptotically (more conservative)
3. **CV when likelihood unavailable**: Tree-based models, ensemble methods
4. **Large $n$**: AIC and BIC converge (BIC selects simpler, both select the same when $n$ is very small)
5. **Overfitting prevention**: Use BIC when overfitting cost is high

### Common Pitfalls
- Don't compare AIC/BIC across non-nested models with different likelihood types
- Don't use model selection criteria to compare models on same data used for selection — need nested CV
- L1 regularization (Lasso) changes effective degrees of freedom — use effective df instead of $k$

## Effective Degrees of Freedom
For regularized models, use trace of the hat matrix:

$$df(\lambda) = \text{tr}(X(X^\top X + \lambda I)^{-1} X^\top) = \sum_{j=1}^d \frac{\sigma_j^2}{\sigma_j^2 + \lambda}$$

For Lasso: $df(\hat{\beta}) = |\{j : \hat{\beta}_j \neq 0\}|$ (number of non-zero coefficients).

## References
- Akaike, "A New Look at the Statistical Model Identification" (IEEE Trans. Auto. Control, 1974)
- Schwarz, "Estimating the Dimension of a Model" (Ann. Statistics, 1978)
- Rissanen, "Modeling by Shortest Data Description" (Automatica, 1978)
- Burnham & Anderson, "Model Selection and Multimodel Inference" (Springer, 2002)
- Hastie, Tibshirani, Friedman, "ESL", Ch. 7
