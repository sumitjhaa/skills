# Lesson 05.06: Decision Trees (CART, ID3, C4.5)

## Learning Objectives
- Understand tree structure and recursive partitioning
- Implement splitting criteria (Gini, entropy, MSE)
- Apply pruning to prevent overfitting
- Compare ID3, C4.5, and CART algorithms

## Tree Structure
A decision tree is a hierarchical model consisting of:
- **Internal nodes**: Tests on individual features
- **Branches**: Outcomes of tests (binary or multi-way)
- **Leaves**: Class labels (classification) or mean values (regression)

Predictions follow the path from root to leaf based on feature values.

## Splitting Criteria

### Information Gain (ID3)
Based on entropy $H(D) = -\sum_{k=1}^K p_k \log_2 p_k$:

$$\text{IG}(D, f) = H(D) - \sum_{v \in \text{vals}(f)} \frac{|D_v|}{|D|} H(D_v)$$

Select feature $f$ maximizing $\text{IG}$. Biased toward features with many values.

### Gain Ratio (C4.5)
Normalizes information gain by split information:

$$\text{GR} = \frac{\text{IG}}{\text{SplitInfo}}, \quad \text{SplitInfo} = -\sum_v \frac{|D_v|}{|D|} \log \frac{|D_v|}{|D|}$$

Corrects information gain's bias toward multi-valued features.

### Gini Impurity (CART)
$$\text{Gini}(D) = 1 - \sum_{k=1}^K p_k^2$$

Impurity reduction: $\Delta = \text{Gini}(D) - \sum_v \frac{|D_v|}{|D|} \text{Gini}(D_v)$

Gini is computationally cheaper than entropy (no logarithms) and produces similar trees.

### MSE (Regression Trees)
$$\text{MSE}(D) = \frac{1}{|D|} \sum_{i \in D} (y_i - \bar{y}_D)^2$$

Split to minimize weighted MSE of children nodes.

## Pruning

### Pre-pruning (Early Stopping)
Stop growing when:
- Max depth reached
- Min samples per leaf insufficient
- Split improvement below threshold

Risk: may stop too early, missing informative splits.

### Cost-Complexity Pruning (CART)
Grow full tree $T_0$, then find subtree minimizing:

$$R_\alpha(T) = R(T) + \alpha |T|$$

where $R(T)$ is misclassification rate and $|T|$ is number of leaves. $\alpha \geq 0$ controls complexity.

Weakest-link cutting: for each internal node, compute the $\alpha$ at which pruning that node reduces cost. Prune the node with smallest $\alpha$, creating a sequence of nested subtrees. Select via cross-validation.

### Reduced Error Pruning (C4.5)
Split data into training + validation. Grow on training, prune nodes where removing the subtree does not increase validation error.

## Algorithm Comparison

| Feature | ID3 | C4.5 | CART |
|---------|-----|------|------|
| Splits | Multi-way | Multi-way | Binary |
| Criteria | Info gain | Gain ratio | Gini/MSE |
| Features | Categorical | Both | Both |
| Pruning | None | Reduced error | Cost-complexity |
| Missing values | No | Yes (surrogate splits) | Yes (surrogate splits) |
| Regression | No | No | Yes |

## Code: Decision Tree Classifier (CART-like)

```python
import numpy as np
from collections import Counter

class DecisionTree:
    def __init__(self, max_depth=10, min_samples_leaf=2):
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf

    def _gini(self, y):
        _, counts = np.unique(y, return_counts=True)
        probs = counts / len(y)
        return 1 - np.sum(probs**2)

    def _split(self, X, y, feature, threshold):
        left = X[:, feature] <= threshold
        return X[left], y[left], X[~left], y[~left]

    def _best_split(self, X, y):
        best_gain, best_feat, best_thresh = -1, None, None
        current_gini = self._gini(y)
        n = len(y)
        for f in range(X.shape[1]):
            thresholds = np.unique(X[:, f])
            for t in thresholds:
                _, y_l, _, y_r = self._split(X, y, f, t)
                if len(y_l) < self.min_samples_leaf or len(y_r) < self.min_samples_leaf:
                    continue
                gain = current_gini - (len(y_l)/n * self._gini(y_l) + len(y_r)/n * self._gini(y_r))
                if gain > best_gain:
                    best_gain, best_feat, best_thresh = gain, f, t
        return best_feat, best_thresh

    def _build_tree(self, X, y, depth=0):
        if depth >= self.max_depth or len(np.unique(y)) == 1 or len(y) < self.min_samples_leaf * 2:
            return Counter(y).most_common(1)[0][0]
        feat, thresh = self._best_split(X, y)
        if feat is None:
            return Counter(y).most_common(1)[0][0]
        X_l, y_l, X_r, y_r = self._split(X, y, feat, thresh)
        return {'feature': feat, 'threshold': thresh,
                'left': self._build_tree(X_l, y_l, depth+1),
                'right': self._build_tree(X_r, y_r, depth+1)}

    def fit(self, X, y):
        self.tree_ = self._build_tree(X, y)

    def _predict_one(self, x, node):
        if not isinstance(node, dict):
            return node
        if x[node['feature']] <= node['threshold']:
            return self._predict_one(x, node['left'])
        return self._predict_one(x, node['right'])

    def predict(self, X):
        return np.array([self._predict_one(x, self.tree_) for x in X])
```

## Practical Considerations
- **Instability**: Small data changes can produce very different trees (high variance)
- **Interpretability**: Trees are fully interpretable, rule extraction possible
- **Mixed features**: Handle numeric and categorical naturally
- **Missing values**: Surrogate splits or instance weighting
- **Imbalanced data**: Use class weights in impurity calculation
- **Feature importance**: Features used near root are more important

## Key Points
- Non-parametric, fully interpretable
- Handles mixed feature types natively
- Prone to overfitting — pruning essential
- Axis-aligned splits limit expressiveness compared to oblique splits
- Ensemble methods (RF, GBM) address high variance

## References
- Breiman et al., "Classification and Regression Trees" (1984)
- Quinlan, "C4.5: Programs for Machine Learning" (1993)
- Quinlan, "Induction of Decision Trees" (Machine Learning, 1986)
- Hastie et al., "ESL", Ch. 9
