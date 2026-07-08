# Lesson 05.15: k-Nearest Neighbors

## Learning Objectives
- Understand instance-based (lazy) learning
- Implement k-NN classification and regression from scratch
- Compare search structures (brute force, KD-tree, ball tree)
- Analyze curse of dimensionality effects

## Basic Algorithm
For query point $x$:
1. Compute distances to all training points
2. Select $k$ closest points
3. **Classification**: majority vote among neighbors
4. **Regression**: mean (or median) of neighbor values

The decision boundary is a Voronoi diagram in the feature space.

## Distance Metrics

| Metric | Formula | Use case |
|--------|---------|----------|
| Euclidean | $\|x-z\|_2 = \sqrt{\sum_j (x_j - z_j)^2}$ | Default, isotropic |
| Manhattan | $\sum_j |x_j - z_j|$ | High dimensions, robust |
| Minkowski | $(\sum_j |x_j - z_j|^p)^{1/p}$ | Generalized (p=1: Manhattan, p=2: Euclidean) |
| Chebyshev | $\max_j |x_j - z_j|$ | Chessboard distance |
| Cosine | $1 - \frac{x^\top z}{\|x\|\|z\|}$ | Text, sparse data |
| Mahalanobis | $\sqrt{(x-z)^\top \Sigma^{-1} (x-z)}$ | Correlated features |

### Distance Weighting
Simple majority vote fails when neighbors are at very different distances:

- Inverse: $w_i = 1 / d(x, x_i)$
- Inverse square: $w_i = 1 / d(x, x_i)^2$
- Exponential: $w_i = \exp(-d(x, x_i)^2 / \sigma^2)$

Then predict: $\hat{y} = \frac{\sum_i w_i y_i}{\sum_i w_i}$

## Search Structures

### Brute Force
- $O(nd)$ per query — only feasible for small $n$
- Simple to implement and parallelize
- Works well for $n < 1000$

### KD-Tree
Recursive axis-aligned partitioning:
1. Split data at median along chosen axis
2. Recurse on left and right subsets
3. At query: prune branches that cannot contain neighbors

- $O(d \log n)$ average query, $O(dn)$ worst-case
- Degrades in high dimensions ($d > 20$)
- Only suitable for low to moderate dimensions

### Ball Tree
Hierarchical hypersphere partitioning:
1. Partition data into overlapping balls
2. Build tree of balls with centroids and radii
3. At query: prune balls that cannot contain closer neighbors

- $O(d \log n)$ average query
- More robust in high dimensions than KD-tree
- Often preferred for $d > 20$

## Curse of Dimensionality
As $d$ increases:
- All points become approximately equidistant
- Ratio of nearest to farthest distance approaches 1
- Requires exponential data to maintain density

**Critical dimension**: For $k$-NN, effective when $d \ll \log n$. Beyond that, consider dimensionality reduction (PCA, t-SNE) first.

## Code: k-NN Classifier

```python
import numpy as np
from collections import Counter

class KNN:
    def __init__(self, k=5, metric='euclidean', weights='uniform'):
        self.k = k
        self.metric = metric
        self.weights = weights

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def _distance(self, x1, x2):
        if self.metric == 'euclidean':
            return np.sqrt(np.sum((x1 - x2)**2))
        elif self.metric == 'manhattan':
            return np.sum(np.abs(x1 - x2))
        elif self.metric == 'cosine':
            return 1 - (x1 @ x2) / (np.linalg.norm(x1) * np.linalg.norm(x2) + 1e-10)

    def _predict_one(self, x):
        dists = [self._distance(x, x_train) for x_train in self.X_train]
        idx = np.argsort(dists)[:self.k]
        k_dists = np.array([dists[i] for i in idx])
        k_labels = self.y_train[idx]
        if self.weights == 'uniform':
            return Counter(k_labels).most_common(1)[0][0]
        else:
            weights = 1.0 / (k_dists + 1e-10)
            weighted_votes = {}
            for label, w in zip(k_labels, weights):
                weighted_votes[label] = weighted_votes.get(label, 0) + w
            return max(weighted_votes, key=weighted_votes.get)

    def predict(self, X):
        return np.array([self._predict_one(x) for x in X])
```

## Hyperparameter Tuning

### Choosing $k$
- Small $k$ ($k=1$): low bias, high variance (overfitting)
- Large $k$: high bias, low variance (smoothing)
- Typical values: $\sqrt{n}$ or tuned via cross-validation
- Rule of thumb: $k \approx \sqrt{n/2}$ for balanced classes

### Choosing Distance Metric
- Cross-validate over Euclidean, Manhattan, Cosine
- For high-dimensional data, use Cosine or adaptive metrics
- For correlated features, use Mahalanobis

## Practical Considerations
- **Feature scaling**: Absolutely essential — use standardization or min-max scaling
- **Large $n$**: Use approximate nearest neighbor (ANN) libraries (Faiss, Annoy, HNSW)
- **Imbalanced data**: Weight decision by class frequency or use distance weighting
- **Categorical features**: Convert to binary encoding or use Hamming distance
- **$k$-NN for large $d$**: Always reduce dimensionality first or use metric learning
- **Memory**: Store training data — can be prohibitive for large $n$

## Properties
- Non-parametric, instance-based (lazy: no training)
- Decision boundary adapts to local data density
- Sensitive to irrelevant features (distance dominated by noise)
- Curse of dimensionality: all distances become uniform in high-D
- $k$ controls the bias-variance tradeoff
- Asymptotic error rate at most twice Bayes optimal

## References
- Cover & Hart, "Nearest Neighbor Pattern Classification" (IEEE Trans. Info. Theory, 1967)
- Hastie, Tibshirani, Friedman, "ESL", Ch. 13
- Shakhnarovich, Darrell, Indyk, "Nearest-Neighbor Methods in Learning and Vision" (2005)
