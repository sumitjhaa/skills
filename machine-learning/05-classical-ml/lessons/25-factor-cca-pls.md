# Lesson 05.25: Factor Analysis / CCA / PLS

## Learning Objectives
- Understand latent variable models and factor analysis
- Derive CCA as a generalized eigenvalue problem
- Implement PLS regression (NIPALS algorithm)
- Distinguish between PCA, FA, CCA, and PLS

## Factor Analysis
$X = \mu + LF + \epsilon$, where:
- $X \in \mathbb{R}^d$: observed variables
- $F \in \mathbb{R}^k$: latent factors ($k \ll d$)
- $L \in \mathbb{R}^{d \times k}$: factor loadings
- $\epsilon \sim \mathcal{N}(0, \Psi)$: unique variances ($\Psi$ diagonal)
- $F \sim \mathcal{N}(0, I)$: factors

### Marginal Distribution
$$X \sim \mathcal{N}(\mu, \Sigma), \quad \Sigma = LL^\top + \Psi$$

### Estimation via EM
**E-step**: Compute expected sufficient statistics given current parameters:

$$\mathbb{E}[F_i|X_i] = (L^\top \Psi^{-1} L + I)^{-1} L^\top \Psi^{-1} (X_i - \mu)$$

$$\text{Cov}[F_i|X_i] = (L^\top \Psi^{-1} L + I)^{-1}$$

**M-step**: Update parameters:

$$L^{\text{new}} = \left( \sum_i (X_i - \mu) \mathbb{E}[F_i]^\top \right) \left( \sum_i (\mathbb{E}[F_i]\mathbb{E}[F_i]^\top + \text{Cov}[F_i]) \right)^{-1}$$

$$\Psi^{\text{new}} = \frac{1}{n} \sum_i \text{diag}\left( (X_i - \mu)(X_i - \mu)^\top - L^{\text{new}} \mathbb{E}[F_i] (X_i - \mu)^\top \right)$$

### Factor Rotation
Loadings $L$ are only identifiable up to orthogonal rotation: $L^* = LR$ for any orthogonal $R$. Varimax rotation maximizes variance of squared loadings for interpretability.

## CCA (Canonical Correlation Analysis)
Find projections $a \in \mathbb{R}^{d_x}, b \in \mathbb{R}^{d_y}$ maximizing correlation between two views:

$$\max_{a,b} \frac{a^\top \Sigma_{XY} b}{\sqrt{a^\top \Sigma_{XX} a} \sqrt{b^\top \Sigma_{YY} b}}$$

### Generalized Eigenvalue Solution
Solve:

$$\Sigma_{XY} \Sigma_{YY}^{-1} \Sigma_{YX} a = \lambda \Sigma_{XX} a$$

$$\Sigma_{YX} \Sigma_{XX}^{-1} \Sigma_{XY} b = \lambda \Sigma_{YY} b$$

Canonical correlations: $\rho_j = \sqrt{\lambda_j}$ (ordered decreasing).

### Regularized CCA (RCCA)
Add ridge penalties: $(\Sigma_{XX} + \lambda_x I)^{-1}$ and $(\Sigma_{YY} + \lambda_y I)^{-1}$, essential when $d > n$.

## PLS (Partial Least Squares)
Decomposes $X$ and $Y$ simultaneously:

$$X = TP^\top + E, \quad Y = TQ^\top + F$$

$T \in \mathbb{R}^{n \times k}$: shared latent scores (common components).

### NIPALS Algorithm
1. Start with some $y$ (or first column of $Y$)
2. Iterate until convergence:
   - $w = X^\top y / \|X^\top y\|$ (X weights)
   - $t = X w$ (X scores)
   - $c = Y^\top t / (t^\top t)$ (Y weights)
   - $y = Y c / (c^\top c)$ (update Y scores)
3. Deflate: $p = X^\top t / (t^\top t)$; $X \leftarrow X - t p^\top$; $Y \leftarrow Y - t c^\top$
4. Repeat for next component

### PLS vs PCR
PLS uses both $X$ and $Y$ for component extraction (supervised), while Principal Component Regression (PCR) uses only $X$ (unsupervised). PLS typically requires fewer components.

## Comparison

| Method | Type | Goal | Uses $y$? | Components |
|--------|------|------|-----------|------------|
| PCA | Unsupervised | Maximize variance | No | Principal components |
| FA | Unsupervised | Model covariance | No | Latent factors |
| CCA | View-pair | Maximize correlation | Yes (paired) | Canonical variates |
| PLS | Regression | Maximize covariance | Yes | Latent scores |

## Code: CCA

```python
import numpy as np
from scipy.linalg import eigh

def cca(X, Y, n_components=2, reg_x=0.0, reg_y=0.0):
    n, dx = X.shape
    dy = Y.shape[1]
    X = X - X.mean(axis=0)
    Y = Y - Y.mean(axis=0)
    C_xx = X.T @ X / (n - 1) + reg_x * np.eye(dx)
    C_yy = Y.T @ Y / (n - 1) + reg_y * np.eye(dy)
    C_xy = X.T @ Y / (n - 1)
    # Solve generalized eigenvalue problem
    C_xx_inv = np.linalg.inv(C_xx)
    C_yy_inv = np.linalg.inv(C_yy)
    A = C_xx_inv @ C_xy @ C_yy_inv @ C_xy.T
    eigvals, eigvecs = eigh(A, subset_by_index=[dx-n_components, dx-1])
    idx = np.argsort(eigvals)[::-1]
    return eigvecs[:, idx[:n_components]].T  # canonical directions
```

## Practical Considerations
- **FA with $d \gg n$**: Use regularized EM (add small ridge to $\Psi$)
- **CCA with $d > n$**: RCCA essential; or use PCA preprocessing
- **PLS for $n \ll d$**: Works well; widely used in chemometrics (NIR spectroscopy)
- **Scalability**: PLS $O(ndk)$ per component; FA $O(ndk)$ per EM step
- **Overfitting**: Cross-validate number of components for all methods

## References
- Spearman, "General Intelligence, Objectively Determined and Measured" (1904)
- Hotelling, "Relations Between Two Sets of Variates" (Biometrika, 1936)
- Wold, "Soft Modelling by Latent Variables: The Nonlinear Iterative Partial Least Squares Approach" (1975)
- Tipping & Bishop, "Probabilistic Principal Component Analysis" (JRSS-B, 1999)
