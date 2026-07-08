# Lesson 05.24: ICA (FastICA, Infomax)

## Learning Objectives
- Understand the cocktail party problem and blind source separation
- Derive ICA from non-Gaussianity maximization
- Implement FastICA fixed-point algorithm
- Apply to EEG, audio, and financial data

## Model
$X = AS$, where:
- $X \in \mathbb{R}^{n \times d}$: observed mixed signals
- $S \in \mathbb{R}^{n \times k}$: independent non-Gaussian sources
- $A \in \mathbb{R}^{d \times k}$: unknown mixing matrix

Goal: find unmixing matrix $W \in \mathbb{R}^{k \times d}$ such that $Y = WX \approx S$ recovers independent sources.

## Identifiability Conditions
- At most one source can be Gaussian (Gaussian mixtures remain Gaussian)
- Sources are statistically independent
- $k \leq d$ (as many sources as mixtures, or fewer)
- $A$ has full column rank

**Ambiguities**: ICA cannot determine variance (scale) or order of sources.

## Non-Gaussianity
Central Limit Theorem: mixtures are more Gaussian than individual sources. Maximizing non-Gaussianity recovers sources.

### Kurtosis
Fourth-order cumulant: $\text{kurt}(y) = \mathbb{E}[y^4] - 3(\mathbb{E}[y^2])^2$

For unit-variance $y$: $\text{kurt}(y) = \mathbb{E}[y^4] - 3$

- Gaussian: $\text{kurt} = 0$
- Super-Gaussian (sparse, e.g., Laplacian): $\text{kurt} > 0$
- Sub-Gaussian (uniform): $\text{kurt} < 0$

Maximize $|\text{kurt}(Wx)|$ — simple but sensitive to outliers.

### Negentropy
Differential entropy relative to Gaussian:

$$J(y) = H(y_{\text{gauss}}) - H(y)$$

$J(y) \geq 0$, equals 0 only for Gaussian. Approximated via:

$$J(y) \approx \sum_{i=1}^p k_i [\mathbb{E}[G_i(y)] - \mathbb{E}[G_i(\nu)]]^2$$

where $G_i$ are non-quadratic contrast functions and $\nu \sim \mathcal{N}(0, 1)$.

Common contrast: $G(u) = \frac{1}{a} \log \cosh(a u)$ (tanh) or $G(u) = -\exp(-u^2/2)$ (Gaussian).

## FastICA
Fixed-point algorithm for ICA. For each component:

1. Initialize $w$ (unit norm)
2. $w^+ = \mathbb{E}[x g(w^\top x)] - \mathbb{E}[g'(w^\top x)] w$
3. $w = w^+ / \|w^+\|$
4. If not converged, go to 2

**Deflationary approach**: Extract components one by one, decorrelate with Gram-Schmidt.

**Symmetric approach**: Update all $W$ simultaneously, symmetrically orthogonalize via $W = (W W^\top)^{-1/2} W$.

## Preprocessing
- **Centering**: $X \leftarrow X - \mathbb{E}[X]$ (zero mean)
- **Whitening**: $Z = \Lambda^{-1/2} U^\top X$ where $\Lambda, U$ from PCA of $X$

Whitening simplifies ICA to finding an orthogonal $W$ (i.e., $W W^\top = I$), reducing the parameter space.

## Code: FastICA

```python
import numpy as np

def fast_ica(X, n_components=None, max_iter=200, tol=1e-6):
    n, d = X.shape
    if n_components is None:
        n_components = d
    # Center and whiten
    X = X - X.mean(axis=0)
    U, S, Vt = np.linalg.svd(X, full_matrices=False)
    Z = U[:, :n_components] * S[:n_components]
    # Initialize W
    W = np.random.randn(n_components, n_components)
    W, _ = np.linalg.qr(W)
    for _ in range(max_iter):
        W_old = W.copy()
        # Symmetric update
        WZX = W @ Z.T  # n_components x n
        g = np.tanh(WZX)  # contrast function
        gp = 1 - g**2      # derivative
        W = g @ Z + gp.sum(axis=1)[:, None] * W
        W = np.linalg.svd(W, full_matrices=False)[0] @ np.linalg.svd(W, full_matrices=False)[2]
        if np.min(np.abs(np.abs(np.diag(W @ W_old.T)) - 1)) < tol:
            break
    return Z @ W.T, W  # sources, unmixing matrix
```

## Practical Considerations
- **Gaussian sources**: Cannot separate more than one Gaussian component
- **Whitening**: Essential for numerical stability; can lose dimensions if $k \neq d$
- **Random initialization**: Different seeds may give different orders (and sign flips)
- **$n < d$**: Use PCA first to reduce dimensionality before ICA
- **Overcomplete ICA** ($k > d$): Harder problem, requires different methods
- **Stability**: FastICA is $O(nd)$ per iteration — very efficient
- **Ordering**: Sources are unordered — use stability or consistency to sort

## Applications
- **Blind source separation**: Audio (cocktail party), EEG/MEG artifact removal
- **Feature extraction**: ICA components for classification (face recognition)
- **Financial modeling**: Independent components of asset returns
- **Functional MRI**: Separating neural signals from noise

## Key Points
- $O(nd)$ per iteration for FastICA
- Requires non-Gaussianity (cannot separate Gaussian sources)
- Sign and permutation ambiguity inherent
- Whitening reduces problem to finding orthogonal $W$
- Super-Gaussian sources (Laplacian, t-distributed) are easiest to separate

## References
- Hyvärinen & Oja, "Independent Component Analysis: Algorithms and Applications" (Neural Networks, 2000)
- Hyvärinen, Karhunen, Oja, "Independent Component Analysis" (Wiley, 2001)
- Bell & Sejnowski, "An Information-Maximization Approach to Blind Separation and Blind Deconvolution" (Neural Computation, 1995)
- Comon, "Independent Component Analysis, a New Concept?" (Signal Processing, 1994)
