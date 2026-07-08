# Lesson 05.17: DBSCAN / HDBSCAN / OPTICS

## Learning Objectives
- Understand density-based clustering and noise handling
- Implement DBSCAN core/border/noise classification
- Analyze hierarchical density clustering (HDBSCAN)
- Handle variable density with OPTICS

## DBSCAN (Density-Based Spatial Clustering of Applications with Noise)

### Definitions
- **$\varepsilon$-neighborhood**: $N_\varepsilon(p) = \{q \mid d(p,q) \leq \varepsilon\}$
- **Core point**: $|N_\varepsilon(p)| \geq \text{min\_pts}$ — dense region center
- **Border point**: in $N_\varepsilon$ of a core point, but not core itself
- **Noise point**: not core and not in any core's $\varepsilon$-neighborhood
- **Directly density-reachable**: $q \in N_\varepsilon(p)$ and $p$ is core
- **Density-reachable**: chain of directly density-reachable points (asymmetric)
- **Density-connected**: exists $o$ such that both $p$ and $q$ are density-reachable from $o$ (symmetric)

### Algorithm
```
for each unvisited point p:
    neighbors = region_query(p, eps)
    if len(neighbors) < min_pts:
        mark p as noise
    else:
        C = next_cluster
        expand_cluster(p, neighbors, C, eps, min_pts)

def expand_cluster(p, neighbors, C, eps, min_pts):
    add p to cluster C
    for each q in neighbors:
        if not visited:
            mark q visited
            q_neighbors = region_query(q, eps)
            if len(q_neighbors) >= min_pts:
                neighbors = union(neighbors, q_neighbors)
        if q not in any cluster:
            add q to cluster C
```

### Complexity
- Naive: $O(n^2)$ — compute all pairwise distances
- With spatial index (R-tree, KD-tree): $O(n \log n)$ — range queries faster
- Memory: $O(n)$ for labels (no distance matrix stored)

## HDBSCAN (Hierarchical DBSCAN)
Extension handling varying density clusters:

1. **Mutual reachability graph**: Build weighted graph where
   $$d_{\text{mreach}}(a,b) = \max\{\text{core}_k(a), \text{core}_k(b), d(a,b)\}$$
   with $\text{core}_k(a) = \text{distance to } k^{\text{th}}$ nearest neighbor of $a$

2. **Minimum spanning tree**: Compute MST of mutual reachability graph (using Prim's or Borůvka's)

3. **Cluster hierarchy**: Sort MST edges by distance descending, merge connected components
   - Start with each point as its own cluster
   - Remove edges from largest to smallest distance
   - When edge removed, clusters split → build dendrogram

4. **Stable cluster extraction**: For each cluster in hierarchy, compute stability:
   $$s_{\text{cluster}} = \sum_{p \in \text{cluster}} (\lambda_{\text{max}}(p) - \lambda_{\text{min}}(p))$$
   where $\lambda = 1/\text{distance}$. Select clusters maximizing total stability.

## OPTICS (Ordering Points To Identify Clustering Structure)
Produces augmented ordering for visualizing density structure:

- **Core-distance**: $\text{core-dist}(p) = \text{distance to min\_pts}^{\text{th}}$ nearest neighbor
- **Reachability-distance**: $\max(\text{core-dist}(p), d(p, q))$

Algorithm maintains priority queue ordered by reachability distance. Output is a reachability plot (distance vs point order) where valleys indicate clusters.

No explicit $\varepsilon$ needed — $\varepsilon$ is just a maximum radius for search (can be $\infty$).

## Comparison

| Feature | DBSCAN | HDBSCAN | OPTICS |
|---------|--------|---------|--------|
| Varying density | Poor | Good | Good |
| Parameters | $\varepsilon$, min\_pts | min\_cluster\_size, min\_samples | min\_pts, $\varepsilon$ (optional) |
| Hierarchy | No | Yes | Yes |
| Noise identification | Yes | Yes | Yes |
| Speed | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ |
| Arbitrary shapes | Yes | Yes | Yes |

## Code: DBSCAN Implementation

```python
import numpy as np
from scipy.spatial import KDTree

class DBSCAN:
    def __init__(self, eps=0.5, min_pts=5):
        self.eps = eps
        self.min_pts = min_pts

    def fit(self, X):
        n = X.shape[0]
        tree = KDTree(X)
        self.labels_ = -np.ones(n, dtype=int)
        cluster_id = 0
        for i in range(n):
            if self.labels_[i] != -1:
                continue
            neighbors = tree.query_ball_point(X[i], self.eps)
            if len(neighbors) < self.min_pts:
                self.labels_[i] = -2  # noise
                continue
            self._expand_cluster(X, tree, i, neighbors, cluster_id)
            cluster_id += 1
        return self

    def _expand_cluster(self, X, tree, point_idx, neighbors, cluster_id):
        self.labels_[point_idx] = cluster_id
        i = 0
        while i < len(neighbors):
            nb = neighbors[i]
            if self.labels_[nb] == -2:
                self.labels_[nb] = cluster_id
            elif self.labels_[nb] == -1:
                self.labels_[nb] = cluster_id
                new_neighbors = tree.query_ball_point(X[nb], self.eps)
                if len(new_neighbors) >= self.min_pts:
                    neighbors = list(set(neighbors) | set(new_neighbors))
            i += 1
```

## Practical Considerations
- **$\varepsilon$ selection**: Use k-distance plot (sort distances to $k$th NN, look for elbow)
- **min\_pts**: Typically 2$\times$dim or 5-10; too small → many noise points, too large → merging
- **Feature scaling**: Absolutely essential (distance-based algorithm)
- **High dimensions**: All distances become similar → use dimensionality reduction first
- **Varying density**: HDBSCAN is strictly better for real-world data
- **Large $n$**: Approximate nearest neighbor search (Faiss, Annoy) for scalability
- **Categorical data**: Use Hamming distance or Gower dissimilarity

## References
- Ester et al., "A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise" (KDD 1996)
- Campello et al., "Density-Based Clustering Based on Hierarchical Density Estimates" (PAKDD 2013)
- Ankerst et al., "OPTICS: Ordering Points to Identify the Clustering Structure" (SIGMOD 1999)
- Schubert et al., "DBSCAN Revisited, Revisited" (ACM Trans. Database Systems, 2017)
