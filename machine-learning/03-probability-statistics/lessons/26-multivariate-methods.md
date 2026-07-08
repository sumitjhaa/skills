# Lesson 26: Multivariate Methods

## Learning Objectives

After completing this lesson, you will be able to:
- Understand Canonical Correlation Analysis (CCA) for multi-view data
- Apply Factor Analysis (FA) for latent variable modeling
- Implement Independent Component Analysis (ICA) for blind source separation
- Distinguish between PCA, CCA, FA, and ICA
- Select the appropriate method for different data types

## Canonical Correlation Analysis (CCA)

### Objective

CCA finds linear combinations $u = a^\top X$ and $v = b^\top Y$ that maximize the correlation between them:
$$\rho = \max_{a, b} \text{Corr}(a^\top X, b^\top Y) = \frac{a^\top \Sigma_{XY} b}{\sqrt{a^\top \Sigma_{XX} a} \sqrt{b^\top \Sigma_{YY} b}}$$

### Solution

The problem reduces to a generalized eigenvalue problem:
$$\Sigma_{XY} \Sigma_{YY}^{-1} \Sigma_{YX} a = \lambda \Sigma_{XX} a$$
$$\Sigma_{YX} \Sigma_{XX}^{-1} \Sigma_{XY} b = \lambda \Sigma_{YY} b$$

The canonical correlations $\rho_i = \sqrt{\lambda_i}$ are the square roots of the eigenvalues.

### Multiple Canonical Variates

After the first pair $(u_1, v_1)$, subsequent pairs $(u_i, v_i)$ maximize correlation subject to $u_i \perp u_j$ and $v_i \perp v_j$ for $j < i$.

### Applications

- **Multi-view learning:** Correlate image and text representations
- **Neuroimaging:** Relate brain activity patterns to behavioral measures
- **Genomics:** Link genetic markers to gene expression
- **Cross-modal retrieval:** Find matching items across modalities

## Factor Analysis (FA)

### Model

$$X = Lf + \varepsilon$$

where:
- $X \in \mathbb{R}^p$: observed variables
- $L \in \mathbb{R}^{p \times k}$: loading matrix ($k < p$)
- $f \in \mathbb{R}^k$: latent factors, $f \sim \mathcal{N}(0, I)$
- $\varepsilon \in \mathbb{R}^p$: unique factors, $\varepsilon \sim \mathcal{N}(0, \Psi)$, $\Psi$ diagonal

### Covariance Structure

$$\Sigma = \text{Cov}(X) = LL^\top + \Psi$$

- **Communality:** $h_i^2 = \sum_{j=1}^k L_{ij}^2$ — variance of $X_i$ explained by common factors
- **Uniqueness:** $\psi_i$ — variance specific to $X_i$ (not shared with other variables)

### Estimation

1. **Principal factor method:** Estimate $\Psi$ using $\hat{\psi}_i = 1 - \hat{h}_i^2$, then factor $\hat{\Sigma} - \hat{\Psi}$
2. **Maximum likelihood:** Under normality, maximize log-likelihood:
   $$\ell(L, \Psi) = -\frac{n}{2} \left[\log|\Sigma| + \text{tr}(\hat{\Sigma}\Sigma^{-1})\right]$$
3. **EM algorithm:** Treat factors as missing data, iterate E-step (expected factors) and M-step (update $L, \Psi$)

### Factor Rotation

- **Varimax:** Orthogonal rotation maximizing variance of squared loadings (simple structure)
- **Promax:** Oblique rotation (factors can correlate)
- **Oblimin:** General oblique rotation

### Applications

- **Psychometrics:** Intelligence testing (g-factor, multiple abilities)
- **Survey analysis:** Reducing many questions to underlying attitudes
- **Finance:** Identifying latent risk factors

## Independent Component Analysis (ICA)

### Model

$$X = AS$$

where:
- $X \in \mathbb{R}^{m}$: observed mixture signals
- $A \in \mathbb{R}^{m \times n}$: mixing matrix
- $S \in \mathbb{R}^{n}$: latent source signals

### Assumptions

1. **Independence:** Source signals $s_i$ are statistically independent
2. **Non-Gaussianity:** At most one source can be Gaussian
3. **No noise** (or can be pre-whitened)

### Estimation

ICA maximizes **non-Gaussianity** (contrast function):

| Method | Contrast | Approach |
|--------|----------|----------|
| FastICA | $\max E[G(w^\top X)]$ | Fixed-point iteration |
| Infomax | Maximize output entropy | Gradient descent |
| JADE | Diagonalize cumulant tensor | Algebraic |

**FastICA algorithm:**
1. Whiten data: $Z = \Lambda^{-1/2} U^\top X$ (PCA whitening)
2. Find direction $w$ maximizing $E[G(w^\top Z)]$ where $G$ is a non-quadratic function
3. Orthogonalize: $w_{i+1} = w_{i+1} - \sum_{j=1}^i w_{i+1}^\top w_j w_j$

### Applications

- **Blind source separation:** Cocktail party problem (separate audio sources)
- **EEG/fMRI:** Remove artifacts, identify brain sources
- **Financial modeling:** Identify independent market factors

## Method Comparison

| Method | Goal | Assumptions | Output |
|--------|------|-------------|--------|
| PCA | Maximize variance | Orthogonal components | Principal components |
| CCA | Maximize cross-correlation | Two variable sets | Canonical variates |
| FA | Explain shared variance | Latent factors + unique variance | Factor loadings |
| ICA | Recover independent sources | Non-Gaussian, independent | Source signals |

### When to Use Which

- **PCA:** When you want to reduce dimensionality without labeled data
- **CCA:** When you have two views of the same phenomenon
- **FA:** When you hypothesize latent constructs underlying observed measurements
- **ICA:** When you believe observations are linear mixtures of independent sources

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_decomposition import CCA
from sklearn.decomposition import FactorAnalysis, PCA, FastICA

# Generate multi-view data
np.random.seed(42)
n = 200
latent = np.random.randn(n, 2)
# View 1
X = latent @ np.array([[0.8, 0.3], [0.2, 0.7]]) + np.random.randn(n, 2) * 0.2
# View 2
Y = latent @ np.array([[0.7, 0.4], [0.3, 0.6]]) + np.random.randn(n, 2) * 0.2

# CCA
cca = CCA(n_components=2)
X_c, Y_c = cca.fit_transform(X, Y)
print(f"CCA correlations: {np.corrcoef(X_c.T, Y_c.T)[0, 1]:.4f}, {np.corrcoef(X_c.T, Y_c.T)[1, 0]:.4f}")

# Factor Analysis
fa = FactorAnalysis(n_components=2, random_state=42)
X_fa = fa.fit_transform(X)
print(f"\nFA loadings shape: {fa.components_.shape}")
print(f"Noise variance: {fa.noise_variance_}")

# ICA
ica = FastICA(n_components=2, random_state=42)
S_ = ica.fit_transform(X)  # Estimated sources
A_ = ica.mixing_  # Estimated mixing matrix
print(f"\nICA recovered mixing matrix:\n{A_}")
print(f"Correlation with true latent: {np.abs(np.corrcoef(S_.T, latent.T)[:2, 2:]).max():.3f}")

# Visualization
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

axes[0, 0].scatter(X[:, 0], Y[:, 0], alpha=0.6)
axes[0, 0].set_xlabel('X1')
axes[0, 0].set_ylabel('Y1')
axes[0, 0].set_title('Cross-view correlation')

axes[0, 1].scatter(X_c[:, 0], Y_c[:, 0], alpha=0.6, c='red')
axes[0, 1].set_xlabel('Canonical variate U1')
axes[0, 1].set_ylabel('Canonical variate V1')
axes[0, 1].set_title(f'CCA: ρ = {np.corrcoef(X_c[:,0], Y_c[:,0])[0,1]:.3f}')

axes[0, 2].scatter(X_fa[:, 0], X_fa[:, 1], alpha=0.6)
axes[0, 2].set_xlabel('Factor 1')
axes[0, 2].set_ylabel('Factor 2')
axes[0, 2].set_title('Factor Analysis')

# ICA sources
axes[1, 0].plot(S_[:100, 0], 'b-', label='Source 1')
axes[1, 0].plot(S_[:100, 1], 'r-', label='Source 2')
axes[1, 0].legend()
axes[1, 0].set_title('ICA Recovered Sources')

axes[1, 1].plot(S_[:100, 0] + S_[:100, 1], 'g-', lw=2)
axes[1, 1].set_title('Mixture (observed would be noisy)')

axes[1, 2].scatter(S_[:, 0], S_[:, 1], alpha=0.5)
axes[1, 2].set_xlabel('IC 1')
axes[1, 2].set_ylabel('IC 2')
axes[1, 2].set_title(f'Sources (independence: r={np.corrcoef(S_[:,0], S_[:,1])[0,1]:.3f})')

plt.tight_layout()
plt.show()
```

## Visualization

Create a correlation heatmap for PCA (diagonal covariance), CCA (canonical correlations), FA (loading matrix), and ICA (mixing matrix). For ICA, show the original sources and mixed signals in the time domain to illustrate the blind source separation problem.

## Practical Considerations

- **Number of components:** Use scree plot (PCA), eigenvalue > 1 (Kaiser), parallel analysis, or cross-validated likelihood (FA/ICA).
- **Identifiability:** Factor analysis has rotational indeterminacy — any rotation $LR$ with $RR^\top = I$ gives the same covariance. Use varimax for interpretable loadings.
- **ICA estimation:** FastICA may converge to different solutions depending on initialization. Run multiple times with different seeds.
- **Pre-whitening:** ICA typically requires data whitening (PCA) as a preprocessing step to remove second-order dependencies.

## References

- Hotelling, H. (1936). "Relations between two sets of variates"
- Spearman, C. (1904). "General intelligence, objectively determined and measured"
- Hyvärinen, A., Karhunen, J., & Oja, E. (2001). *Independent Component Analysis*
- Jolliffe, I. T. (2002). *Principal Component Analysis*
