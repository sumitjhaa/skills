# Lesson 05.19: Hierarchical Clustering

## Learning Objectives
- Understand agglomerative and divisive clustering strategies
- Implement linkage criteria (single, complete, average, Ward)
- Interpret dendrograms for cluster analysis
- Analyze complexity and scalability

## Types

### Agglomerative (Bottom-Up)
1. Start with $n$ clusters (each point is its own cluster)
2. Find two closest clusters and merge them
3. Repeat step 2 until $k$ clusters remain (or one cluster)
4. Result: binary tree (dendrogram) of merges

### Divisive (Top-Down)
1. Start with one cluster containing all points
2. Split cluster into two (using, e.g., k-means with $k=2$)
3. Recursively split until $k$ clusters remain
4. Computationally more expensive than agglomerative

## Linkage Criteria

| Linkage | Distance $d(A, B)$ | Properties |
|---------|-------------------|------------|
| Single | $\min_{a \in A, b \in B} d(a,b)$ | Chaining, finds elongated clusters |
| Complete | $\max_{a \in A, b \in B} d(a,b)$ | Compact clusters, sensitive to outliers |
| Average (UPGMA) | $\frac{1}{|A||B|} \sum_{a,b} d(a,b)$ | Compromise, balanced |
| Centroid | $\|\bar{a} - \bar{b}\|_2$ | May invert (non-monotonic) |
| Median | $\|\tilde{a} - \tilde{b}\|_2$ | Non-monotonic possible |
| Ward | $\frac{|A||B|}{|A|+|B|} \|\bar{a} - \bar{b}\|_2^2$ | Minimizes within-cluster variance |

### Single Linkage Chaining
Single linkage tends to produce long, chain-like clusters because a single pair of close points can merge clusters, even if the clusters are far apart otherwise. This is useful for elongated shapes but bad for compact clusters.

### Ward's Method
At each step, merge the two clusters that minimize the increase in total within-cluster variance:

$$\Delta(A, B) = \frac{|A||B|}{|A|+|B|} \|\bar{a} - \bar{b}\|_2^2$$

This is equivalent to minimizing the sum of squared errors (k-means objective) hierarchically. Tends to produce compact, spherical clusters.

## Lance-Williams Formula
Efficiently update distance between new cluster $C = A \cup B$ and existing cluster $D$:

$$d(C, D) = \alpha_A d(A,D) + \alpha_B d(B,D) + \beta d(A,B) + \gamma |d(A,D) - d(B,D)|$$

| Linkage | $\alpha_A$ | $\alpha_B$ | $\beta$ | $\gamma$ |
|---------|-----------|-----------|---------|----------|
| Single | 1/2 | 1/2 | 0 | -1/2 |
| Complete | 1/2 | 1/2 | 0 | +1/2 |
| Average | $n_A/(n_C)$ | $n_B/(n_C)$ | 0 | 0 |
| Ward | $(n_A+n_D)/(n_C+n_D)$ | $(n_B+n_D)/(n_C+n_D)$ | $-n_D/(n_C+n_D)$ | 0 |

## Dendrogram Interpretation
- Vertical axis: merge distance (or dissimilarity)
- Horizontal axis: data points
- Cut at height $h$ → $k$ clusters (number of horizontal lines intersected)
- Long vertical lines indicate well-separated clusters
- Short vertical lines indicate close clusters (may be merged)

### Cophenetic Correlation
Measures how faithfully dendrogram preserves pairwise distances:
- Compute cophenetic distance (height at which two points first merged)
- Correlation with original distance matrix
- Higher = better representation

## Complexity
- Naive agglomerative: $O(n^3)$ time, $O(n^2)$ memory
- SLINK (single linkage): $O(n^2)$ time, $O(n)$ memory
- CLINK (complete linkage): $O(n^2)$ time, $O(n^2)$ memory
- Nearest-neighbor chain algorithm: $O(n^2)$ for many linkages
- Not feasible for $n > 50,000$ due to $O(n^2)$ memory

## Code: Agglomerative Clustering

```python
import numpy as np
from scipy.spatial.distance import pdist, squareform

class AgglomerativeClustering:
    def __init__(self, n_clusters=2, linkage='ward'):
        self.n_clusters = n_clusters
        self.linkage = linkage

    def fit(self, X):
        n = X.shape[0]
        # Distance matrix (condensed)
        D = squareform(pdist(X))
        np.fill_diagonal(D, np.inf)
        clusters = {i: [i] for i in range(n)}
        cluster_dist = {(i, j): D[i, j] for i in range(n) for j in range(i+1, n)}
        while len(clusters) > self.n_clusters:
            # Find closest pair
            i, j = min(cluster_dist, key=cluster_dist.get)
            # Merge j into i
            clusters[i] = clusters[i] + clusters[j]
            del clusters[j]
            # Update distances
            new_dist = {}
            for k in clusters:
                if k == i or k == j: continue
                if self.linkage == 'single':
                    d = min(cluster_dist.get((min(i,k), max(i,k)), np.inf),
                            cluster_dist.get((min(j,k), max(j,k)), np.inf))
                elif self.linkage == 'complete':
                    d = max(cluster_dist.get((min(i,k), max(i,k)), np.inf),
                            cluster_dist.get((min(j,k), max(j,k)), np.inf))
                elif self.linkage == 'average':
                    d = (len(clusters[i]) * cluster_dist.get((min(i,k), max(i,k)), 0) +
                         len(clusters[j]) * cluster_dist.get((min(j,k), max(j,k)), 0)) / len(clusters[i] + clusters[j])
                new_dist[(min(i,k), max(i,k))] = d
            cluster_dist = new_dist
        self.labels_ = np.zeros(n, dtype=int)
        for label, (cid, members) in enumerate(clusters.items()):
            for m in members:
                self.labels_[m] = label
        return self
```

## Practical Considerations
- **Distance matrix**: $O(n^2)$ memory — use SLINK for large $n$ or subsample
- **Feature scaling**: Critical — use standardization
- **Mixed data**: Use Gower distance (Hennig & Liao, 2013)
- **Large $n$**: Consider k-means first (to $n' \ll n$), then hierarchical on centroids
- **Dendrogram visualization**: Use `scipy.cluster.hierarchy.dendrogram`
- **Scalability**: For $n > 10^5$, use approximate methods (BIRCH, CURE)

## Key Points
- Produces full hierarchy (no need to specify $k$ for exploration)
- Deterministic (unlike k-means)
- Heatmap + dendrogram for exploratory analysis
- $O(n^2)$ memory limits scalability to ~50k points
- Ward's method tends to produce balanced clusters

## References
- Ward, "Hierarchical Grouping to Optimize an Objective Function" (JASA, 1963)
- Sneath & Sokal, "Numerical Taxonomy" (1973)
- Murtagh & Contreras, "Algorithms for Hierarchical Clustering" (WIREs Data Mining, 2012)
- Hastie et al., "ESL", Ch. 14
