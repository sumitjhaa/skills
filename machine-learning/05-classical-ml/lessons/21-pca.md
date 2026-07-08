# Lesson 05.21: PCA (Kernel, Sparse, Robust)

## Learning Objectives
- Derive PCA from maximum variance and minimum reconstruction error
- Implement PCA via SVD for numerical stability
- Understand kernel PCA for non-linear dimensionality reduction
- Apply sparse and robust PCA variants

## PCA via SVD
Given centered data $\tilde{X} = X - \bar{x}$ with $\tilde{X} \in \mathbb{R}^{n \times d}$, compute SVD:

$$\tilde{X} = U \Sigma V^\top$$

Principal components (scores): $T = \tilde{X} V = U \Sigma$

### Explained Variance
$$\text{Var}(\text{PC}_j) = \frac{\sigma_j^2}{\sum_{k=1}^r \sigma_k^2}$$

where $\sigma_j$ are singular values (diagonal of $\Sigma$). Cumulative explained variance guides dimension choice — often 95% threshold.

### PCA via Covariance (for $d < n$)
$$\Sigma_X = \frac{1}{n-1} \tilde{X}^\top \tilde{X} = V \Lambda V^\top$$

Eigenvectors $V$ = principal directions, eigenvalues $\lambda_j = \sigma_j^2/(n-1)$.

### PCA via Gram Matrix (for $n < d$)
$$G = \tilde{X} \tilde{X}^\top = U \Sigma^2 U^\top$$

Eigenvectors $U$ scaled by singular values give PC scores.

## Kernel PCA
Map data to feature space $\phi(x)$, perform PCA implicitly via kernel trick:

1. Compute kernel matrix $K_{ij} = \langle \phi(x_i), \phi(x_j) \rangle = K(x_i, x_j)$
2. Center $K$: $\tilde{K} = K - \frac{1}{n}\mathbf{1}K - \frac{1}{n}K\mathbf{1} + \frac{1}{n^2}\mathbf{1}K\mathbf{1}$
3. Eigendecompose $\tilde{K} = U \Lambda U^\top$
4. Project new point $x$ onto $k$th component: $\langle \phi(x), v_k \rangle = \sum_{i=1}^n \alpha_{ki} K(x, x_i)$ where $\alpha_{ki} = U_{ik} / \sqrt{\lambda_k}$

Unlike linear PCA, kernel PCA can capture non-linear manifolds.

## Sparse PCA (SPCA)
Modify PCA to produce sparse loadings (few non-zero entries per component):

$$\min_{A, B} \sum_{i=1}^n \|x_i - AB^\top x_i\|_2^2 + \lambda \sum_{j=1}^k \|B_j\|_1$$

s.t. $A^\top A = I$

- $B$: sparse loadings (L1 penalty)
- $A$: orthonormal basis
- Solved via alternating optimization (elastic net regression + Procrustes rotation)

Useful when interpretability matters (e.g., genetics, finance).

## Robust PCA (RPCA)
Decompose $X = L + S$ into low-rank $L$ and sparse $S$:

$$\min_{L, S} \|L\|_* + \lambda \|S\|_1 \quad \text{s.t.} \quad X = L + S$$

- $\|L\|_* = \sum \sigma_j$: nuclear norm (convex surrogate for rank)
- $\|S\|_1 = \sum |S_{ij}|$: entrywise L1 norm (captures outliers)
- $\lambda = 1/\sqrt{\max(n,d)}$ theoretically motivated

Solved via Augmented Lagrange Multiplier (ALM) or alternating direction method (ADMM).

## Code: PCA via SVD

```python
import numpy as np

class PCA:
    def __init__(self, n_components=None, whiten=False):
        self.n_components = n_components
        self.whiten = whiten

    def fit(self, X):
        n = X.shape[0]
        self.mean_ = X.mean(axis=0)
        X_centered = X - self.mean_
        # SVD (more numerically stable than eigendecomposition of covariance)
        U, S, Vt = np.linalg.svd(X_centered, full_matrices=False)
        self.components_ = Vt  # principal directions
        self.explained_variance_ = S**2 / (n - 1)
        self.explained_variance_ratio_ = self.explained_variance_ / self.explained_variance_.sum()
        self.singular_values_ = S
        if self.n_components:
            self.components_ = self.components_[:self.n_components]
        return self

    def transform(self, X):
        X_centered = X - self.mean_
        return X_centered @ self.components_.T

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)

    def inverse_transform(self, X_pca):
        return X_pca @ self.components_ + self.mean_
```

## Practical Considerations
- **Preprocessing**: Always center (subtract mean). Scale to unit variance if features have different units
- **Outliers**: PCA is highly sensitive to outliers — consider RPCA for contaminated data
- **Missing data**: Use probabilistic PCA (PPCA) with EM for MLE with missing values
- **Choosing $k$**: Scree plot, Kaiser rule ($\lambda > 1$), cumulative variance > 90%, cross-validation
- **Interpretability**: PC loadings are dense (all features contribute) — use SPCA for sparsity
- **Large $n$**: Randomized SVD (Halko et al., 2011) for $O(nd \log k)$ approximation

## Comparison of PCA Variants

| Variant | Non-linear | Sparse | Robust | Complexity |
|---------|-----------|--------|--------|------------|
| PCA | No | No | No | $O(\min(nd^2, dn^2))$ |
| Kernel PCA | Yes | No | No | $O(n^3)$ |
| Sparse PCA | No | Yes | No | $O(knd)$ per iteration |
| Robust PCA | No | No | Yes | $O(n^3)$ per iteration |
| Probabilistic PCA | No | No | No | $O(nd^2)$ per EM step |

## References
- Pearson, "On Lines and Planes of Closest Fit to Points in Space" (1901)
- Hotelling, "Analysis of a Complex of Statistical Variables into Principal Components" (J. Educ. Psych., 1933)
- Schölkopf, Smola, Müller, "Nonlinear Component Analysis as a Kernel Eigenvalue Problem" (Neural Computation, 1998)
- Candès et al., "Robust Principal Component Analysis?" (JACM, 2011)
- Zou, Hastie, Tibshirani, "Sparse Principal Component Analysis" (JCGS, 2006)
