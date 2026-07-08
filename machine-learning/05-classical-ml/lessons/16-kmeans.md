# Lesson 05.16: k-Means Clustering

## Learning Objectives
- Understand the k-means optimization objective
- Implement Lloyd's algorithm and k-means++
- Evaluate clustering quality (elbow, silhouette, gap statistic)
- Analyze limitations and extensions

## Optimization Objective
Partition $n$ points into $k$ clusters $S = \{S_1, \dots, S_k\}$ minimizing within-cluster sum of squares:

$$\min_S \sum_{j=1}^k \sum_{i \in S_j} \|x_i - c_j\|_2^2$$

where $c_j = \frac{1}{|S_j|} \sum_{i \in S_j} x_i$ is the centroid of cluster $j$.

**Equivalently**: maximize between-cluster variance (total variance - within-cluster variance).

## Algorithms

### Lloyd's Algorithm
1. Initialize $k$ centroids $c_1, \dots, c_k$
2. **Assignment step**: Assign each $x_i$ to nearest centroid: $S_j^{(t)} = \{x_i : \|x_i - c_j^{(t)}\|_2^2 \leq \|x_i - c_l^{(t)}\|_2^2 \forall l\}$
3. **Update step**: Recompute centroids: $c_j^{(t+1)} = \frac{1}{|S_j^{(t)}|} \sum_{i \in S_j^{(t)}} x_i$
4. Repeat steps 2-3 until convergence (centroids stabilize or assignment unchanged)

**Convergence**: Objective decreases monotonically (guaranteed). Converges to local optimum (not global). $O(n \cdot k \cdot d \cdot i)$ where $i$ = iterations.

### k-Means++ Initialization
Probabilistic initialization for better convergence:
1. Choose first centroid $c_1$ uniformly from data
2. For each point $x$, compute $D(x) = \min_j \|x - c_j\|_2^2$
3. Choose next centroid with probability proportional to $D(x)^2$
4. Repeat until $k$ centroids chosen

$O(\log k)$ approximation guarantee for the k-means objective.

### Mini-Batch k-Means
Use random mini-batches for large datasets:
1. Sample batch of size $b$
2. Assign batch points to nearest centroid
3. Per-point moving average update: $c_j = c_j + \eta \cdot (x - c_j)$

Faster convergence, slightly worse objective.

## Evaluating $k$

### Elbow Method
Plot inertia (within-cluster sum of squares) vs $k$. Look for "elbow" where improvement slows.

### Silhouette Score
For each point: $s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$
- $a(i)$: mean distance to points in same cluster
- $b(i)$: mean distance to points in nearest other cluster
- Range: $[-1, 1]$ (higher = better)

Average over all points. Choose $k$ maximizing average silhouette.

### Gap Statistic
Compare log(inertia) to expectation under null reference distribution:

$$\text{Gap}(k) = \mathbb{E}^*[\log W_k] - \log W_k$$

Choose smallest $k$ where $\text{Gap}(k) \geq \text{Gap}(k+1) - s_{k+1}$.

## Code: k-Means with k-Means++

```python
import numpy as np

class KMeans:
    def __init__(self, k=3, max_iter=300, tol=1e-4):
        self.k = k
        self.max_iter = max_iter
        self.tol = tol

    def _init_centroids(self, X):
        n, d = X.shape
        centroids = [X[np.random.randint(n)]]
        for _ in range(1, self.k):
            D2 = np.min([np.sum((X - c)**2, axis=1) for c in centroids], axis=0)
            probs = D2 / D2.sum()
            centroids.append(X[np.random.choice(n, p=probs)])
        return np.array(centroids)

    def fit(self, X):
        self.centroids = self._init_centroids(X)
        for _ in range(self.max_iter):
            # Assignment
            dists = np.array([np.sum((X - c)**2, axis=1) for c in self.centroids])
            self.labels_ = np.argmin(dists, axis=0)
            # Update
            new_centroids = np.array([X[self.labels_ == j].mean(axis=0) for j in range(self.k)])
            if np.all(np.abs(new_centroids - self.centroids) < self.tol):
                break
            self.centroids = new_centroids
        self.inertia_ = np.sum([np.sum((X[self.labels_ == j] - self.centroids[j])**2) for j in range(self.k)])
        return self
```

## Limitations
- Assumes spherical clusters (Euclidean distance implied spherical Voronoi cells)
- Sensitive to initialization (k-means++ helps)
- Requires specifying $k$ (elbow/silhouette/gap help)
- Sensitive to outliers (can pull centroids significantly)
- Assumes balanced cluster sizes (tends to split large clusters)
- All points assigned to exactly one cluster (hard clustering)
- Fails for non-convex shaped clusters (use DBSCAN or spectral clustering instead)

## Extensions
- **k-Medoids (PAM)**: Use actual data points as centroids; robust to outliers
- **k-Medians**: Use L1 distance; robust
- **Fuzzy c-Means**: Soft assignments (probability of membership)
- **Kernel k-Means**: Clustering in feature space for non-spherical clusters
- **Spectral Clustering**: k-Means on spectral embedding of data

## Practical Considerations
- **Feature scaling**: Essential — centroids sensitive to feature magnitudes
- **Categorical features**: Use k-modes (mode instead of mean) or Gower distance
- **Large $n$**: Use Mini-Batch k-Means or reduce data dimensionality first
- **Outliers**: Winsorize or use robust scaling
- **Multiple runs**: Run 10-50 times with different seeds, pick best inertia
- **Determinism**: k-Means++ + fixed seed ensures reproducibility

## References
- Lloyd, "Least Squares Quantization in PCM" (IEEE Trans. Info. Theory, 1982)
- Arthur & Vassilvitskii, "k-Means++: The Advantages of Careful Seeding" (SODA 2007)
- Tibshirani, Walther, Hastie, "Estimating the Number of Clusters via the Gap Statistic" (JRSS-B, 2001)
- Hastie et al., "ESL", Ch. 14
