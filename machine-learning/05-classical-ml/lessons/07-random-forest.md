# Lesson 05.07: Random Forest

## Learning Objectives
- Understand bagging and random subspace methods
- Implement random forest training from scratch
- Interpret OOB error, feature importance, and proximity measures
- Analyze bias-variance decomposition of ensemble

## Algorithm

### Bagging (Bootstrap Aggregating)
1. For $b = 1$ to $B$:
   - Draw bootstrap sample $Z_b$ of size $n$ with replacement
   - Grow tree $T_b$ on $Z_b$ (deep, unpruned)
2. Output ensemble: $\hat{f}(x) = \frac{1}{B} \sum_{b=1}^B T_b(x)$ (regression) or majority vote (classification)

### Random Feature Selection
At each node, only consider $m \ll d$ randomly selected features for splitting:
- Classification: $m = \sqrt{d}$ (or $\lfloor \sqrt{d} \rfloor$)
- Regression: $m = d/3$ (or $\lfloor d/3 \rfloor$)

This decorrelates trees: even if a feature is very strong, most trees won't consider it at a given split, allowing weaker features to contribute.

### Why Random Forests Work
Variance reduction via averaging: if $B$ i.i.d. trees each have variance $\sigma^2$ and correlation $\rho$:

$$\text{Var}(\bar{T}) = \rho \sigma^2 + \frac{1-\rho}{B} \sigma^2$$

As $B \to \infty$, variance is $\rho \sigma^2$. Reducing $\rho$ (via random features) is more impactful than increasing $B$.

## Out-of-Bag (OOB) Error
Each bootstrap sample omits ~37% of data (probability $1 - 1/e$). These OOB instances serve as built-in validation:

$$\text{OOB Error} = \frac{1}{n} \sum_{i=1}^n L(y_i, \hat{f}_{\text{OOB}}(x_i))$$

where $\hat{f}_{\text{OOB}}(x_i)$ uses only trees where $x_i$ was OOB. OOB error is an unbiased estimate of test error, often equivalent to $k$-fold CV.

## Feature Importance

### Mean Decrease in Impurity (MDI)
Sum impurity reductions over all splits using feature $j$, weighted by the fraction of samples reaching each node, averaged across trees:

$$\text{Importance}(j) = \frac{1}{B} \sum_{b=1}^B \sum_{\text{node } n \text{ splits on } j} \frac{N_n}{N} \Delta I(n)$$

### Permutation Importance
For each feature $j$:
1. Permute feature $j$ in OOB data
2. Compute increase in OOB error
3. Average across trees

Permutation importance measures how much the model relies on each feature, unaffected by feature scale.

## Proximity Matrix
Count how often two instances end up in the same leaf across all trees: $P_{ij} = \frac{1}{B} \sum_b [\text{leaf}_b(x_i) = \text{leaf}_b(x_j)]$. Useful for clustering, outlier detection, and missing value imputation.

## Code: Random Forest from Scratch

```python
import numpy as np
from collections import Counter

class RandomForest:
    def __init__(self, n_trees=100, max_features='sqrt', max_depth=None, min_samples_leaf=1):
        self.n_trees = n_trees
        self.max_features = max_features
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.trees = []

    def _bootstrap_sample(self, X, y):
        n = X.shape[0]
        idx = np.random.choice(n, n, replace=True)
        return X[idx], y[idx]

    def fit(self, X, y):
        self.trees = []
        n_features = X.shape[1]
        if self.max_features == 'sqrt':
            m = int(np.sqrt(n_features))
        elif self.max_features == 'log2':
            m = int(np.log2(n_features)) + 1
        else:
            m = n_features
        for _ in range(self.n_trees):
            X_boot, y_boot = self._bootstrap_sample(X, y)
            tree = DecisionTree(max_features=m, max_depth=self.max_depth,
                                min_samples_leaf=self.min_samples_leaf)
            tree.fit(X_boot, y_boot)
            self.trees.append(tree)

    def predict(self, X):
        preds = np.array([t.predict(X) for t in self.trees])
        if self.trees[0].is_classifier:
            return np.array([Counter(preds[:, i]).most_common(1)[0][0] for i in range(X.shape[0])])
        return preds.mean(axis=0)
```

## Hyperparameter Tuning

| Parameter | Effect | Typical Range |
|-----------|--------|---------------|
| $n\_estimators$ | Higher = better (diminishing returns) | 100-2000 |
| $m\_features$ | Correlation vs strength tradeoff | $\sqrt{d}$, $d/3$, $\log_2 d$ |
| $max\_depth$ | Control overfitting | None or 10-50 |
| $min\_samples\_leaf$ | Smooth predictions | 1-20 |
| $max\_samples$ | Bootstrap size | 0.5-1.0 |

## Properties and Extensions

### Advantages
- No pruning needed (trees grown deep)
- Parallelizable across trees
- Handles high-dimensional data
- Built-in OOB evaluation
- Robust to outliers (via tree averaging)

### Limitations
- Cannot extrapolate beyond training range
- Biased toward categorical features with many levels
- Large model size ($B$ trees stored)
- Less interpretable than single tree

### Extensions
- **ExtraTrees** (Extremely Randomized Trees): random thresholds for splits, no bootstrap — lower variance
- **Quantile Regression Forests**: store all $y$ in each leaf for full conditional distribution
- **Isolation Forest**: uses RF for anomaly detection (short paths = anomalies)
- **Rotation Forest**: PCA on random feature subsets before tree building

## Practical Considerations
- **Large $n$**: Use subsampling ($max\_samples$) for faster training
- **High $d$**: Increase $m$ if few features are informative
- **Class imbalance**: Use balanced bootstrap (stratified sampling) or class weights
- **Memory**: Trees can be large; limit with $max\_depth$ or $max\_leaf\_nodes$
- **Reproducibility**: Set random state for consistent results

## References
- Breiman, "Random Forests" (Machine Learning, 2001)
- Breiman, "Bagging Predictors" (Machine Learning, 1996)
- Hastie et al., "ESL", Ch. 15
- Louppe, "Understanding Random Forests" (PhD thesis, 2014)
