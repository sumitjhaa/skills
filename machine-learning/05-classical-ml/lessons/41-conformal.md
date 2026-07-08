# Lesson 05.41: Conformal Prediction

## Learning Objectives
- Understand distribution-free prediction with coverage guarantees
- Implement split (inductive) conformal prediction
- Define nonconformity measures for classification and regression
- Apply CP to model uncertainty quantification

## Framework
Conformal prediction produces **prediction sets** (not point predictions) with finite-sample coverage guarantee:

$$P(Y_{\text{new}} \in \Gamma^\varepsilon(X_{\text{new}})) \geq 1 - \varepsilon$$

**Key property**: Distribution-free — no assumptions about data distribution. Only requires exchangeability.

## Nonconformity Measures
Score function $A$ measuring how "unusual" an example is:

### Classification
- $1 - \hat{p}_y$: 1 minus predicted probability of true class
- $-\log \hat{p}_y$: negative log-probability
- $1 - \text{margin}$: distance to decision boundary
- $1 - \hat{p}_{y_1} + \hat{p}_{y_2}$: margin-based

### Regression
- $|y - \hat{y}| / \sigma$: normalized absolute residual
- $|y - \hat{y}| / \text{max}(|\hat{y}|, 1)$: scaled residual
- Quantile regression error: $(y - \hat{q}_\alpha) / |\hat{q}_\alpha - \hat{q}_{1-\alpha}|$

## Inductive (Split) Conformal Prediction
1. Split data into proper training set ($n_{\text{train}}$) and calibration set ($n_{\text{cal}}$)
2. Train model on proper training set
3. Compute nonconformity scores $\alpha_i = A(x_i, y_i)$ for calibration set
4. For new test point $x_{\text{new}}$:
   - For each possible label $y$, compute $\alpha_{\text{new}}^y = A(x_{\text{new}}, y)$
   - Compute $p$-value: $\frac{|\{i : \alpha_i \geq \alpha_{\text{new}}^y\}| + 1}{n_{\text{cal}} + 1}$
   - Include $y$ in prediction set if $p > \varepsilon$

**Advantages**: Only one model training, fast prediction
**Disadvantages**: Split reduces data available for training

## Transductive (Full) Conformal
For each test point:
1. Try every possible label $y$
2. Train model on all data including $(x_{\text{new}}, y)$
3. Compute nonconformity for all $n+1$ points
4. $p$-value: fraction where $\alpha_i \geq \alpha_{\text{new}}$
5. Include $y$ if $p > \varepsilon$

**Advantages**: Uses all training data
**Disadvantages**: Retrain for each test point — $O(n)$ models per new point

## Jackknife+ (Cross-Conformal)
Leave-one-out without full retraining:
1. Train $n$ models (each leaving one point out)
2. For test point, compute $p$-value using LOO predictions
3. Coverage guarantee: $P(Y_{\text{new}} \in \Gamma) \geq 1 - 2\varepsilon$

Balance between inductive (fast) and transductive (data-efficient).

## CP for Regression
Nonconformity: $\alpha_i = |y_i - \hat{\mu}(x_i)|$ (or $\alpha_i = |y_i - \hat{\mu}(x_i)| / \hat{\sigma}(x_i)$)

Prediction interval:

$$\Gamma^\varepsilon(x_{\text{new}}) = \{\hat{\mu}(x_{\text{new}}) \pm q_{1-\varepsilon}\}$$

where $q_{1-\varepsilon}$ is the $(1-\varepsilon)(1+1/n)$ quantile of calibration nonconformity scores.

**Adaptive intervals**: Use quantile regression CP for prediction width that varies with $x$.

## Code: Split Conformal Classification

```python
import numpy as np

class SplitConformal:
    def __init__(self, model, alpha=0.1):
        self.model = model
        self.alpha = alpha

    def fit(self, X_train, y_train, X_cal, y_cal):
        self.model.fit(X_train, y_train)
        probs = self.model.predict_proba(X_cal)
        self.nonconformity = 1 - probs[np.arange(len(y_cal)), y_cal]

    def predict_set(self, X, return_pvalues=False):
        probs = self.model.predict_proba(X)
        n_classes = probs.shape[1]
        prediction_sets = []
        p_values_list = []
        for row_probs in probs:
            p_values = np.zeros(n_classes)
            for c in range(n_classes):
                nc_new = 1 - row_probs[c]
                p_values[c] = np.mean(self.nonconformity >= nc_new)
            prediction_sets.append(np.where(p_values > self.alpha)[0])
            p_values_list.append(p_values)
        if return_pvalues:
            return prediction_sets, np.array(p_values_list)
        return prediction_sets
```

## Properties
- **Valid coverage**: Guaranteed in finite samples (not asymptotic)
- **Adaptive**: Prediction sets adapt to instance difficulty (harder → larger sets)
- **Distribution-free**: No Gaussian or other distributional assumptions
- **Exchangeability required**: i.i.d. or random permutation (not adversarial)

## Extensions
- **Mondrian CP**: Class-conditional coverage (guarantee per class, not just overall)
- **Weighted CP**: Non-exchangeable data (covariate shift, time series)
- **Conformalized quantile regression**: Combines CP with quantile regression for adaptive intervals
- **Conformal risk control**: Generalize beyond miscoverage to other risk functions

## Practical Considerations
- **Efficiency**: Prediction set size depends on model quality (better model → smaller sets)
- **$\varepsilon$ selection**: Choose based on application requirements (medical: $\varepsilon = 0.01$, recommender: $\varepsilon = 0.1$)
- **Empty sets**: Can happen when $\varepsilon$ is too small — use class-conditional CP to avoid
- **Large label sets**: CP becomes expensive — use Monte Carlo sampling of labels

## References
- Vovk, Gammerman, Shafer, "Algorithmic Learning in a Random World" (Springer, 2005)
- Shafer & Vovk, "A Tutorial on Conformal Prediction" (JMLR, 2008)
- Angelopoulos & Bates, "A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification" (2021)
- Barber, Candès, Ramdas, Tibshirani, "Predictive Inference with the Jackknife+" (Ann. Statistics, 2021)
- Romano, Patterson, Candès, "Conformalized Quantile Regression" (NeurIPS 2019)
