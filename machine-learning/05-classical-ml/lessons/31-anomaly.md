# Lesson 05.31: Anomaly Detection

## Learning Objectives
- Understand different anomaly types (point, contextual, collective)
- Implement Isolation Forest, LOF, and One-Class SVM
- Analyze contamination estimation and threshold selection
- Apply to fraud detection, intrusion detection, and quality control

## Types of Anomalies
- **Point anomalies**: Single instance deviating from normal (e.g., credit card fraud)
- **Contextual anomalies**: Anomalous in specific context (e.g., 30°C in winter vs summer)
- **Collective anomalies**: Collection of instances anomalous together (e.g., repeated failed logins)

## Isolation Forest
Key insight: anomalies are few and different → easier to isolate (shorter path in random trees).

### Algorithm
1. Build forest of isolation trees (iTrees):
   - Randomly select a feature
   - Random split between min and max
   - Recurse until isolation or max depth
2. Anomaly score:

   $$s(x, n) = 2^{-\frac{\mathbb{E}[h(x)]}{c(n)}}$$

   where $h(x)$ = path length, $c(n) = 2H(n-1) - 2(n-1)/n$ (average path length in BST), $H(i) = \log i + \gamma$ (harmonic number).

   - $s \approx 0.5$: normal
   - $s \to 1$: anomaly (short path)
   - $s \to 0$: highly normal (long path)

3. Anomaly threshold: top-$k$ highest scores or $s > 0.5$ cutoff.

### Properties
- $O(n \log n)$ training, $O(\log n)$ prediction
- Handles high-dimensional data
- No distance computation needed (axis-aligned splits)
- Works without contamination estimate

## LOF (Local Outlier Factor)
Compares local density of a point to that of its neighbors:

$$\text{LOF}_k(A) = \frac{\frac{1}{|N_k(A)|} \sum_{B \in N_k(A)} \text{lrd}(B)}{\text{lrd}(A)}$$

where:
- $\text{lrd}(A) = 1 / \left( \frac{1}{|N_k(A)|} \sum_{B \in N_k(A)} \text{reach-dist}_k(A, B) \right)$ — local reachability density
- $\text{reach-dist}_k(A, B) = \max(\text{k-distance}(B), d(A, B))$
- $N_k(A)$: $k$ nearest neighbors of $A$

**Interpretation**: LOF ≈ 1: normal (density similar to neighbors). LOF > 1: anomaly (lower density). LOF < 1: inlier (higher density).

## One-Class SVM
Finds maximum margin hyperplane separating data from origin in feature space:

$$\min_{w, \xi, \rho} \frac12 \|w\|^2 + \frac{1}{\nu n} \sum_i \xi_i - \rho$$

s.t. $w^\top \phi(x_i) \geq \rho - \xi_i$, $\xi_i \geq 0$

- $\nu \in (0, 1)$: upper bound on fraction of outliers (and lower bound on support vectors)
- Decision: $f(x) = \text{sign}(w^\top \phi(x) - \rho)$

## Elliptic Envelope
Assumes data is approximately Gaussian:

1. Estimate robust mean and covariance via MCD (Minimum Covariance Determinant)
2. Mahalanobis distance: $d_i = \sqrt{(x_i - \hat{\mu})^\top \hat{\Sigma}^{-1} (x_i - \hat{\mu})}$
3. Threshold: $\chi^2_{d, 0.975}$ (or based on desired contamination)

## Code: Isolation Forest Core

```python
import numpy as np

class IsolationTree:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth

    def fit(self, X, depth=0):
        n = X.shape[0]
        if depth >= self.max_depth or n <= 2:
            self.size = n
            return self
        self.split_feat = np.random.randint(X.shape[1])
        min_val, max_val = X[:, self.split_feat].min(), X[:, self.split_feat].max()
        if min_val == max_val:
            self.size = n
            return self
        self.split_val = np.random.uniform(min_val, max_val)
        left_idx = X[:, self.split_feat] < self.split_val
        self.left = IsolationTree(self.max_depth).fit(X[left_idx], depth + 1)
        self.right = IsolationTree(self.max_depth).fit(X[~left_idx], depth + 1)
        return self

    def path_length(self, x, depth=0):
        if not hasattr(self, 'split_feat'):
            return depth + self._c(self.size)
        if x[self.split_feat] < self.split_val:
            return self.left.path_length(x, depth + 1)
        return self.right.path_length(x, depth + 1)

    def _c(self, n):
        if n <= 1: return 0
        return 2 * (np.log(n - 1) + 0.5772156649) - 2 * (n - 1) / n

class IsolationForest:
    def __init__(self, n_trees=100, max_samples=256):
        self.n_trees = n_trees
        self.max_samples = max_samples

    def fit(self, X):
        n = X.shape[0]
        sample_size = min(self.max_samples, n)
        self.trees = []
        for _ in range(self.n_trees):
            idx = np.random.choice(n, sample_size, replace=False)
            tree = IsolationTree(max_depth=int(np.ceil(np.log2(sample_size))))
            tree.fit(X[idx])
            self.trees.append(tree)
        self.c = self.trees[0]._c(sample_size)
        return self

    def anomaly_score(self, X):
        paths = np.mean([[t.path_length(x) for t in self.trees] for x in X], axis=1)
        return 2 ** (-paths / self.c)
```

## Practical Considerations
- **Contamination**: Specify expected % of anomalies — affects threshold
- **Feature scaling**: LOF and EE need it; IF does not (axis-aligned splits)
- **Window size**: For time series, use sliding window or STL decomposition
- **Multivariate vs univariate**: Use independent detectors per dimension for simpler cases
- **Ensemble**: Combine multiple detectors (IF + LOF + OCSVM) for robustness
- **Labeled data**: Use supervised methods (XGBoost) when anomaly labels exist

## Evaluation Metrics
| Metric | Formula | Use |
|--------|---------|-----|
| Precision@k | TP@k / k | Fixed budget |
| Recall@k | TP@k / total_anomalies | Coverage |
| AUC-ROC | Area under TPR vs FPR | Ranking |
| Average Precision | Weighted mean of precision | Imbalanced |

## References
- Liu, Ting, Zhou, "Isolation Forest" (ICDM 2008)
- Breunig et al., "LOF: Identifying Density-Based Local Outliers" (SIGMOD 2000)
- Schölkopf et al., "Estimating the Support of a High-Dimensional Distribution" (Neural Computation, 2001)
- Rousseeuw & Driessen, "A Fast Algorithm for the Minimum Covariance Determinant Estimator" (Technometrics, 1999)
- Chandola, Banerjee, Kumar, "Anomaly Detection: A Survey" (ACM Computing Surveys, 2009)
