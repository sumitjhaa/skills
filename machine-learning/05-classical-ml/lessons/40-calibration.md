# Lesson 05.40: Probability Calibration

## Learning Objectives
- Understand calibration concepts and reliability diagrams
- Implement Platt scaling and isotonic regression
- Evaluate calibration with ECE, MCE, and Brier score
- Apply calibration to SVM, RF, and gradient boosting

## Calibration Definition
A model is **perfectly calibrated** if:

$$P(Y = 1 | \hat{p} = p) = p$$

For any confidence level $p$, the actual fraction of positive examples equals $p$.

**Well-calibrated**: logistic regression, optimally trained.
**Poorly calibrated**: SVM (Platt scaling needed), modern neural networks (temperature scaling needed).

## Reliability Diagram
1. Bin predictions by confidence intervals (e.g., 10 bins: [0,0.1], [0.1,0.2], ...)
2. For each bin: compute average predicted probability vs observed frequency
3. Plot: observed frequency vs predicted probability

Perfect calibration = diagonal line.

**Common patterns**:
- Sigmoid shape: model is overconfident (high predictions too high, low predictions too low)
- Flat: model is underconfident (predictions too close to 0.5)
- Random scatter: model has some calibration but noisy

## Calibration Metrics

### Expected Calibration Error (ECE)
$$\text{ECE} = \sum_{m=1}^M \frac{n_m}{n} |\text{acc}_m - \bar{p}_m|$$

- $n_m$: number of samples in bin $m$
- $\text{acc}_m$: fraction of positives in bin $m$
- $\bar{p}_m$: average predicted probability in bin $m$

**Weighted** average of absolute calibration error across bins.

### Maximum Calibration Error (MCE)
$$\text{MCE} = \max_{m=1,\dots,M} |\text{acc}_m - \bar{p}_m|$$

Useful when worst-case calibration matters (safety-critical applications).

### Brier Score
$$\text{Brier} = \frac{1}{n} \sum_{i=1}^n (\hat{p}_i - y_i)^2$$

- Range: $[0, 1]$ (lower is better)
- Decomposes into refinement + calibration + uncertainty
- Proper scoring rule (minimized by true probabilities)

## Platt Scaling
Logistic regression on classifier scores:

$$P(y=1|f(x)) = \frac{1}{1 + \exp(A f(x) + B)}$$

- $A, B$: learned parameters (on held-out validation data)
- $f(x)$: uncalibrated score (SVM decision function, tree ensemble log-odds)
- Originally proposed for SVMs by Platt (1999)

**When to use**: Model outputs unbounded scores (SVM, boosting before sigmoid).

## Isotonic Regression
Non-parametric calibration: learn a monotone increasing function $g$:

$$\min_g \sum_i (g(s_i) - y_i)^2 \quad \text{s.t.} \quad g \text{ non-decreasing}$$

- **PAV (Pool Adjacent Violators)**: $O(n)$ algorithm for isotonic regression
- More flexible than Platt scaling
- Requires more data (prone to overfitting with small validation sets)

## Beta Calibration
Parametric calibration for models outputting $[0, 1]$ scores:

$$g(s) = \frac{1}{1 + e^{-a - b \log s + c \log(1-s)}}$$

- Better for models already bounded to $[0, 1]$ (Naive Bayes, Random Forest probabilities)
- Three parameters: $a, b, c$
- Captures non-sigmoid distortion

## Code: Platt Scaling

```python
import numpy as np
from scipy.optimize import minimize

def platt_scale(scores, y):
    """Learn Platt scaling parameters A, B"""
    def neg_log_likelihood(params):
        A, B = params
        p = 1.0 / (1.0 + np.exp(A * scores + B))
        p = np.clip(p, 1e-15, 1 - 1e-15)
        return -np.sum(y * np.log(p) + (1 - y) * np.log(1 - p))
    res = minimize(neg_log_likelihood, [1.0, 0.0], method='L-BFGS-B')
    return res.x

def platt_predict(scores, A, B):
    return 1.0 / (1.0 + np.exp(A * scores + B))
```

## Practical Considerations
- **Validation set**: Always calibrate on held-out data (not training)
- **When to calibrate**: Use when probability estimates matter (cost-sensitive decisions, filtering, ranking)
- **Model-specific**:
  - Logistic regression: naturally calibrated
  - SVM: needs Platt scaling
  - Random Forest: needs Beta calibration or isotonic
  - Gradient Boosting: needs Platt scaling (uncalibrated log-odds)
  - Neural networks: temperature scaling (single parameter $T > 0$: $p = \text{softmax}(z/T)$)
- **Multiclass**: Use temperature scaling (shared $T$), vector scaling, or matrix scaling
- **Overfitting**: Isotonic regression needs $> 1000$ validation points; Platt needs $> 100$

## Key Points
- Calibration is distinct from accuracy — can be accurate but poorly calibrated
- ECE/MCE measure calibration quality quantitatively
- Platt scaling assumes sigmoid calibration curve
- Isotonic regression is more flexible but needs more data
- Always calibrate on held-out data
- Modern neural nets (especially deep) are often poorly calibrated

## References
- DeGroot & Fienberg, "The Comparison and Evaluation of Forecasters" (JRSS-D, 1983)
- Platt, "Probabilistic Outputs for Support Vector Machines and Comparisons to Regularized Likelihood Methods" (1999)
- Niculescu-Mizil & Caruana, "Predicting Good Probabilities with Supervised Learning" (ICML 2005)
- Guo et al., "On Calibration of Modern Neural Networks" (ICML 2017)
- Kull, Silva, Shawe-Taylor, "Beta Calibration" (ECML 2012)
