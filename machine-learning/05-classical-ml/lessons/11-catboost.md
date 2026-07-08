# Lesson 05.11: CatBoost

## Learning Objectives
- Understand Ordered Boosting for unbiased gradient estimates
- Implement Ordered Target Statistics for categorical encoding
- Analyze symmetric (oblivious) tree structure
- Compare with XGBoost and LightGBM

## Ordered Boosting
Standard boosting leaks future information: when computing residuals for instance $x_i$, the model has already seen $x_i$ during training of previous trees. CatBoost's Ordered Boosting solves this:

1. Generate $s$ random permutations $\sigma_1, \dots, \sigma_s$ of training data
2. For each permutation, maintain $s$ supporting models $M_1, \dots, M_s$
3. For instance $x_i$ under permutation $\sigma$, use model $M_{\sigma(i)-1}$ (trained on first $\sigma(i)-1$ instances) to compute residual

This produces unbiased gradient estimates, reducing overfitting and generalization error.

### Why This Matters
Standard boosting: $\text{residual}_i^{(t)} = y_i - F_{t-1}(x_i)$ where $F_{t-1}$ was trained on $x_i$ itself → optimistic residuals → overfitting.

Ordered Boosting: $\text{residual}_i^{(t)} = y_i - F_{t-1}^{\sigma(i)-1}(x_i)$ where $F^{\sigma(i)-1}$ never saw $x_i$ → unbiased.

## Categorical Feature Encoding

### Ordered Target Statistics (TS)
Standard target encoding leaks information. CatBoost's ordered version:

$$\hat{x}_k^i = \frac{\sum_{j < p(i)} [x_{j,k} = x_{i,k}] y_j + aP}{\sum_{j < p(i)} [x_{j,k} = x_{i,k}] + a}$$

- $p(i)$: position of $i$ in permutation $p$
- $P$: prior (e.g., global mean of target)
- $a$: prior weight (controls smoothing)

For each permutation, compute TS using only preceding instances. At test time, use entire training set (or an additional permutation).

### Feature Combinations
CatBoost greedily constructs feature combinations:
1. Start with base categorical features
2. At each split, consider all current categorical features and their existing combinations
3. Pick combination that minimizes loss

Combinations capture interactions between categorical features without manual engineering.

## Symmetric (Oblivious) Trees
CatBoost uses balanced, symmetric trees where the same split condition applies at each level for all nodes:

```
Level 1: feature_a < 0.5?
Level 2: feature_b > 0.3?  (same split for both Level 1 branches)
Level 3: feature_c < 0.7?  (same split for all four Level 2 branches)
```

### Advantages
- **Regularization**: Symmetry reduces capacity → less overfitting
- **Inference speed**: $O(\text{depth} \cdot \log(\text{features}))$ — all instances follow same decision path structure
- **Feature importance**: Clear per-level importance ranking
- **Less pruning needed**: Symmetry naturally limits expressiveness

### Tradeoffs
- May underfit if true split structure is asymmetric
- Requires more trees than asymmetric methods
- Each leaf covers a different region despite same split boundaries (due to cumulative conditions)

## Code: Ordered Target Statistics

```python
import numpy as np

def ordered_target_statistic(X_cat, y, perm, prior=None, a=1.0):
    """Compute ordered target statistics for a categorical feature"""
    n = len(y)
    if prior is None:
        prior = np.mean(y)
    ts = np.zeros(n)
    sum_prior = 0
    count = 0
    for idx in perm:
        val = X_cat[idx]
        ts[idx] = (sum_prior + a * prior) / (count + a)
        # Update statistics AFTER computing TS for this point
        sum_prior += y[idx]
        count += 1
    return ts
```

## Key Parameters

| Parameter | Effect | Default |
|-----------|--------|---------|
| `iterations` | Number of trees | 1000 |
| `learning_rate` | Step size | 0.03 |
| `depth` | Tree depth (symmetric) | 6 |
| `l2_leaf_reg` | L2 regularization | 3.0 |
| `border_count` | Number of bins for numeric features | 128 |
| `one_hot_max_size` | One-hot encode categories below this | 2 |
| `rsm` | Random column subspace | 1.0 |

## Comparison

| Aspect | CatBoost | LightGBM | XGBoost |
|--------|----------|----------|---------|
| Tree type | Symmetric (oblivious) | Leaf-wise | Level-wise |
| Categorical | Ordered TS + combinations | Max-sum grouping | One-hot |
| Gradient | Ordered (unbiased) | Standard | Standard |
| Training speed | Slower | Fastest | Moderate |
| Default params | Good defaults | Needs tuning | Needs tuning |
| Overfitting | Less prone | More prone | Moderate |
| GPU support | Excellent | Good | Good |

## Practical Considerations
- **Categorical data**: CatBoost is often best-in-class for datasets with many categorical features
- **Default parameters**: Usually work well without extensive tuning
- **Training time**: Slower than LightGBM, especially with Ordered Boosting
- **Memory**: Higher than LightGBM due to storing multiple model copies
- **Text features**: CatBoost has native text feature support (transforms text columns)
- **Cross-validation**: CatBoost's CV is built-in and efficient

## References
- Prokhorenkova et al., "CatBoost: unbiased boosting with categorical features" (NIPS 2018)
- Dorogush et al., "CatBoost: gradient boosting with categorical features support" (NIPS 2018 Workshop)
- CatBoost documentation: https://catboost.ai
