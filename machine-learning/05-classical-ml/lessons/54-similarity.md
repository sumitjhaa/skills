# Lesson 05.54: Similarity / Distance Measures

## Learning Objectives
- Understand metric properties and distance axioms
- Implement vector, sequence, and set distances
- Apply Mahalanobis distance for correlated features
- Use DTW for time series alignment

## Metric Axioms
A distance function $d$ is a metric if:
1. Non-negativity: $d(x, y) \geq 0$
2. Identity: $d(x, y) = 0 \iff x = y$
3. Symmetry: $d(x, y) = d(y, x)$
4. Triangle inequality: $d(x, z) \leq d(x, y) + d(y, z)$

Many useful "distances" violate some axioms (e.g., cosine distance is not a metric — violates triangle inequality for some definitions).

## Vector Distances

| Metric | Formula | Invariant | When to use |
|--------|---------|-----------|-------------|
| Euclidean | $\|x-y\|_2 = \sqrt{\sum_j (x_j - y_j)^2}$ | Rotation, translation | Isotropic data |
| Manhattan | $\sum_j \|x_j - y_j\|$ | Translation | High-D, robust |
| Chebyshev | $\max_j \|x_j - y_j\|$ | Translation | Uniform norm |
| Cosine | $1 - \frac{x^\top y}{\|x\|\|y\|}$ | Scale, rotation | Text, angle matters |
| Mahalanobis | $\sqrt{(x-y)^\top \Sigma^{-1} (x-y)}$ | Affine transformations | Correlated features |

### Euclidean Distance
Most common. Sensitive to feature scale — always standardize features before computing.

### Cosine Similarity/Distance
$$\text{cosine}(x, y) = \frac{x^\top y}{\|x\| \|y\|}$$

Distance: $d_{\text{cos}}(x, y) = 1 - \text{cosine}(x, y)$

**Scale invariant**: Only measures direction. Default for text data (documents as TF-IDF vectors).

### Mahalanobis Distance
$$D_M(x, y) = \sqrt{(x-y)^\top \Sigma^{-1} (x-y)}$$

- $\Sigma$: covariance matrix of the data
- Equivalent to Euclidean in whitened space: $z = \Sigma^{-1/2} x$
- Accounts for feature correlations and different scales
- $O(d^2)$ to compute $\Sigma^{-1}$ — use Cholesky decomposition

## Dynamic Time Warping (DTW)
Align two sequences of potentially different lengths:

$$D(i,j) = d(x_i, y_j) + \min(D(i-1,j), D(i,j-1), D(i-1,j-1))$$

- Base: $D(0,0) = 0$, $D(i,0) = D(0,j) = \infty$
- Result: $D(n, m)$

**Complexity**: $O(nm)$ time and space.

**Window constraint**: Sakoe-Chiba band limits warping to width $w$, reducing to $O(w \cdot \max(n,m))$.

## Edit Distances

### Levenshtein Distance
Minimum insertions, deletions, substitutions:

$$D(i,j) = \begin{cases}
\max(i,j) & \min(i,j) = 0 \\
\min \begin{cases}
D(i-1,j)+1 & \text{(insert)}\\
D(i,j-1)+1 & \text{(delete)}\\
D(i-1,j-1) + [a_i \neq b_j] & \text{(substitute)}
\end{cases} & \text{otherwise}
\end{cases}$$

### Other Edit Distances
- **Damerau-Levenshtein**: Adds transposition operation (adjacent swap)
- **Hamming**: Equal length only, counts substitutions
- **Jaro-Winkler**: Character overlap + transpositions, optimized for name matching
- **Needleman-Wunsch**: Global sequence alignment with variable gap penalty
- **Smith-Waterman**: Local sequence alignment

## Kernel Alignment
Measure similarity between two kernel matrices:

$$A(K_1, K_2) = \frac{\langle K_1, K_2 \rangle_F}{\sqrt{\langle K_1, K_1 \rangle_F \langle K_2, K_2 \rangle_F}}$$

- $\langle A, B \rangle_F = \sum_{i,j} A_{ij} B_{ij}$: Frobenius inner product
- Used for kernel selection and multiple kernel learning (MKL)

## Code: Distance Functions

```python
import numpy as np
from scipy.spatial.distance import cdist

def mahalanobis_distance(X, Y, cov=None):
    if cov is None:
        cov = np.cov(X.T)
    inv_cov = np.linalg.inv(cov + 1e-6 * np.eye(cov.shape[0]))
    return cdist(X, Y, metric='mahalanobis', VI=inv_cov)

def dtw(x, y, window=None):
    n, m = len(x), len(y)
    D = np.full((n+1, m+1), np.inf)
    D[0, 0] = 0
    for i in range(1, n+1):
        for j in range(max(1, i-window) if window else 1, m+1):
            cost = abs(x[i-1] - y[j-1])
            D[i, j] = cost + min(D[i-1, j], D[i, j-1], D[i-1, j-1])
    return D[n, m]
```

## Practical Considerations
- **Scaling**: Always standardize features before computing vector distances
- **Curse of dimensionality**: Euclidean distance becomes uniform in high-D — all points equally far
- **Null values**: Handle missing values via imputation or distance ignoring missing dims
- **Mixed types**: Use Gower distance (range-standardized numeric + category matching)
- **Weighted distances**: Weight features by importance (learned from data)

## References
- Minkowski, "Geometric der Zahlen" (1896)
- Mahalanobis, "On the Generalised Distance in Statistics" (Proc. Nat. Inst. Sci., 1936)
- Sakoe & Chiba, "Dynamic Programming Algorithm Optimization for Spoken Word Recognition" (IEEE ASSP, 1978)
- Levenshtein, "Binary Codes Capable of Correcting Deletions, Insertions and Reversals" (Soviet Physics Doklady, 1966)
- Gower, "A General Coefficient of Similarity and Some of Its Properties" (Biometrics, 1971)
- Cha, "Comprehensive Survey on Distance/Similarity Measures" (Int. J. Math. Models, 2007)
