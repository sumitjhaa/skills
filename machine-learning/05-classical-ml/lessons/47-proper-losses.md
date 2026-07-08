# Lesson 05.47: Proper Loss Functions

## Learning Objectives
- Define proper scoring rules and their properties
- Distinguish proper, strictly proper, and classification-calibrated losses
- Analyze composite losses and link functions
- Apply loss function choice to gradient boosting

## Definition
A loss $L(p, y)$ is **proper** if the true probability $p^*$ minimizes expected loss:

$$p^* = \arg\min_{q \in [0,1]} \mathbb{E}_{y \sim p^*}[L(q, y)]$$

**Strictly proper** if the minimizer is unique (only $q = p^*$ minimizes).

## Examples of Proper Losses

| Loss | Formula $L(p, y)$ | Proper? | Strict? | Bounded? |
|------|-----------|---------|---------|----------|
| 0-1 | $\mathbf{1}[y \neq \hat{y}]$ | No | No | Yes |
| Log-loss | $-y\log p - (1-y)\log(1-p)$ | Yes | Yes | No |
| Brier | $(p - y)^2$ | Yes | Yes | Yes |
| Hinge | $\max(0, 1 - (2y-1)f)$ | No | No | Yes |
| Exponential | $\exp(-(2y-1)f)$ | No | No | No |
| Savage | $1/(1 + e^f)^2$ | Yes | Yes | Yes |
| Boosting (logistic) | $\log(1 + e^{-2yf})$ | Yes | Yes | No |
| MAE | $|p - y|$ | Yes | No | Yes |

## Non-Property of 0-1 Loss
The expected 0-1 loss is minimized by Bayes decision rule (predict majority class), but 0-1 loss is NOT proper — it doesn't estimate probabilities, only the mode.

## Composite Losses
$$L(y, f) = \phi(y, f) \text{ where } p = \psi^{-1}(f)$$

- $\psi$: link function (e.g., logit: $\psi(p) = \log(p/(1-p))$)
- $L$ is **composite proper** if $\phi(y, f) = L_{\text{proper}}(y, \psi^{-1}(f))$

**Example**: Log-loss + logit link gives logistic loss: $\phi(y, f) = \log(1 + e^{-yf})$

## Classification Calibration
A loss $L$ is **classification-calibrated** if minimizing it yields Bayes-optimal classifier:

$$f^* = \arg\min_f \mathbb{E}[L(y, f(x))] \implies \text{sign}(f^*(x)) = \text{sign}(p^*(x) - 0.5)$$

- All proper losses are classification-calibrated
- Hinge loss is NOT proper but IS classification-calibrated — explains SVM's good classification performance despite poor probabilities
- Exponential loss is classification-calibrated but not proper

## Tail Properties (Robustness)

### Heavy-tailed losses (robust to label noise):
- **Savage loss**: $L(p, y) = 1/(1 + s)^2$ where $s = (2y-1)f$ — resists outliers
- **Huberized logistic**: Blend of L2 and logistic for robustness
- **MAE**: Robust to label noise but not proper

### Light-tailed losses (efficient for well-separated data):
- **Exponential loss**: Very sensitive to label noise
- **Boosting losses**: Exponential and logistic

## Code: Proper Loss Visualization

```python
import numpy as np

def log_loss(p, y):
    return -(y * np.log(p + 1e-15) + (1 - y) * np.log(1 - p + 1e-15))

def brier_loss(p, y):
    return (p - y)**2

def savage_loss(f, y):
    s = (2 * y - 1) * f
    return 1 / (1 + np.exp(s))**2

def hinge_loss(f, y):
    return np.maximum(0, 1 - (2 * y - 1) * f)

def logistic_loss(f, y):
    return np.log(1 + np.exp(-(2 * y - 1) * f))
```

## Key Insights
1. **Properness matters for calibration**: Proper losses yield calibrated probabilities asymptotically
2. **Classification ≠ probability estimation**: Use proper loss when probabilities are needed
3. **Log-loss vs Brier**: Log-loss is asymmetric (infinite penalty for $p=0$ when $y=1$), Brier is symmetric
4. **Loss choice affects gradient magnitude**: Important for gradient boosting convergence
5. **Robustness vs efficiency tradeoff**: Heavy-tailed losses resist outliers but may be less efficient under clean data

## Practical Guidelines
- **For calibrated probabilities**: Use log-loss (or another strictly proper loss)
- **For classification accuracy only**: Hinge or logistic loss (Boosted SVMs)
- **For label noise**: Savage or Huberized losses
- **For gradient boosting**: Logistic loss (binary), L2 (regression), Poisson (counts)
- **For neural networks**: Cross-entropy (log-loss) with softmax is standard

## References
- Brier, "Verification of Forecasts Expressed in Terms of Probability" (Monthly Weather Review, 1950)
- Savage, "Elicitation of Personal Probabilities and Expectations" (JASA, 1971)
- Hastie, Tibshirani, Friedman, "ESL", Ch. 10 (Loss functions for boosting)
- Reid & Williamson, "Information, Divergence and Risk for Binary Experiments" (JMLR, 2011)
- Bartlett et al., "Convexity, Classification, and Risk Bounds" (JASA, 2006)
