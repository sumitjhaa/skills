# Lesson 05.09: XGBoost

## Learning Objectives
- Understand Newton (second-order) boosting vs first-order gradient boosting
- Derive optimal leaf weight and split gain with regularization
- Implement the core XGBoost tree-building algorithm
- Analyze system optimizations for speed

## Objective Function
At iteration $t$:

$$\mathcal{L}^{(t)} = \sum_{i=1}^n L(y_i, \hat{y}_i^{(t-1)} + f_t(x_i)) + \Omega(f_t)$$

Regularization: $\Omega(f) = \gamma T + \frac12 \lambda \|w\|^2 + \alpha |w|$

- $T$: number of leaves
- $w$: leaf weights
- $\gamma$: per-leaf penalty (prunes)
- $\lambda$: L2 regularization on leaf weights
- $\alpha$: L1 regularization on leaf weights

## Second-Order Approximation
Using Taylor expansion to second order:

$$\mathcal{L}^{(t)} \approx \sum_{i=1}^n \left[ L(y_i, \hat{y}^{(t-1)}) + g_i f_t(x_i) + \frac12 h_i f_t^2(x_i) \right] + \Omega(f_t)$$

where $g_i = \partial_{\hat{y}^{(t-1)}} L(y_i, \hat{y}^{(t-1)})$ (gradient) and $h_i = \partial^2_{\hat{y}^{(t-1)}} L(y_i, \hat{y}^{(t-1)})$ (hessian).

Removing constant terms:

$$\tilde{\mathcal{L}}^{(t)} = \sum_{i=1}^n \left[ g_i f_t(x_i) + \frac12 h_i f_t^2(x_i) \right] + \gamma T + \frac12 \lambda \sum_{j=1}^T w_j^2$$

## Optimal Leaf Weight
For leaf $j$ with instance set $I_j = \{i : f_t(x_i) = w_j\}$:

$$w_j^* = -\frac{\sum_{i \in I_j} g_i}{\sum_{i \in I_j} h_i + \lambda}$$

The Hessian in the denominator acts as a per-instance weight, naturally handling uncertainty.

## Gain for Split Candidacy
For a candidate split dividing $I$ into $I_L$ and $I_R$:

$$\text{Gain} = \frac12 \left[ \frac{G_L^2}{H_L + \lambda} + \frac{G_R^2}{H_R + \lambda} - \frac{(G_L+G_R)^2}{H_L+H_R+\lambda} \right] - \gamma$$

where $G_L = \sum_{i \in I_L} g_i$, $H_L = \sum_{i \in I_L} h_i$.

Split only accepted if $\text{Gain} > 0$ (otherwise pruning via $\gamma$).

## System Optimizations

### Weighted Quantile Sketch
For approximate split finding on large data:
1. Propose candidate split points via quantiles of feature distribution weighted by $|h_i|$
2. Scan candidates to find best split

The sketch algorithm guarantees $\varepsilon$-approximate quantiles with $O(1/\varepsilon)$ memory.

### Column Block (Parallelization)
Pre-sort features and store in compressed column (CSC) format:
- Each feature is one block in memory
- Split statistics computed in parallel across features
- Cache-aware prefetching for optimal memory access

### Sparsity-Aware Algorithm
For missing values, learn "default direction" for each split:
- For each split, compute gain going left vs right for missing values
- Choose direction that maximizes gain
- Handles sparse data (e.g., one-hot encoded) efficiently

## Code: XGBoost-Style Tree

```python
import numpy as np

class XGBoostTree:
    def __init__(self, max_depth=6, lam=1.0, gamma=0.0, learning_rate=0.3):
        self.max_depth = max_depth
        self.lam = lam
        self.gamma = gamma
        self.lr = learning_rate

    def _gain(self, G, H, G_left, H_left, G_right, H_right):
        left = G_left**2 / (H_left + self.lam)
        right = G_right**2 / (H_right + self.lam)
        root = (G)**2 / (H + self.lam)
        return 0.5 * (left + right - root) - self.gamma

    def _build(self, X, g, h, depth=0):
        n = len(X)
        if depth >= self.max_depth or n < 2 or np.sum(np.abs(g)) < 1e-10:
            return -np.sum(g) / (np.sum(h) + self.lam)
        best_gain, best_feat, best_thresh = -float('inf'), None, None
        G_total, H_total = np.sum(g), np.sum(h)
        for f in range(X.shape[1]):
            order = np.argsort(X[:, f])
            G_left, H_left = 0.0, 0.0
            for i in range(n - 1):
                idx = order[i]
                G_left += g[idx]; H_left += h[idx]
                if X[order[i], f] == X[order[i+1], f]:
                    continue
                G_right = G_total - G_left
                H_right = H_total - H_left
                gain = self._gain(G_total, H_total, G_left, H_left, G_right, H_right)
                if gain > best_gain:
                    best_gain, best_feat, best_thresh = gain, f, X[order[i], f]
        if best_gain <= 0:
            return -np.sum(g) / (np.sum(h) + self.lam)
        left_idx = X[:, best_feat] <= best_thresh
        left_child = self._build(X[left_idx], g[left_idx], h[left_idx], depth + 1)
        right_child = self._build(X[~left_idx], g[~left_idx], h[~left_idx], depth + 1)
        return {'feature': best_feat, 'threshold': best_thresh,
                'left': left_child, 'right': right_child}
```

## Key Differences from Classic GBM

| Feature | Classic GBM | XGBoost |
|---------|------------|---------|
| Order | First-order | Second-order (Newton) |
| Regularization | None in objective | $\gamma, \lambda, \alpha$ in objective |
| Split finding | Exact greedy | Quantile sketch (approx) |
| Missing values | Impute beforehand | Native sparsity-aware |
| Parallelism | No | Column block parallel |
| Cache | None | Cache-aware access |
| Distributed | Limited | Built-in (Rabit) |

## Practical Considerations
- **$\gamma$ pruning**: Increase for more conservative trees (prevents overfitting)
- **$\lambda$ regularization**: Larger values smooth leaf weights
- **Tree depth**: Rarely need more than depth 6-8
- **Subsample + colsample**: Row + column subsampling reduce correlation
- **Early stopping**: Monitor AUC/logloss on validation set
- **GPU acceleration**: Use `gpu_hist` tree method for large datasets

## References
- Chen & Guestrin, "XGBoost: A Scalable Tree Boosting System" (KDD 2016)
- XGBoost documentation: https://xgboost.readthedocs.io
- Friedman et al., "Additive Logistic Regression" (Ann. Statistics, 2000)
