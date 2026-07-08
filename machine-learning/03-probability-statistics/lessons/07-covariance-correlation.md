# Lesson 07: Covariance & Correlation

## Learning Objectives

After completing this lesson, you will be able to:
- Compute covariance and interpret its sign and magnitude
- Use correlation coefficient as a standardized measure of linear association
- Understand the covariance matrix and its properties (PSD, symmetry)
- Apply Spearman and Kendall rank correlation for non-linear relationships
- Interpret partial correlation for conditional independence

## Covariance

Covariance measures the **direction of linear relationship** between two random variables.

### Definition

$$\text{Cov}(X, Y) = E[(X - \mu_X)(Y - \mu_Y)] = E[XY] - E[X]E[Y]$$

### Interpretation

- **Cov(X,Y) > 0:** When $X$ is above its mean, $Y$ tends to be above its mean (positive association)
- **Cov(X,Y) < 0:** When $X$ is above its mean, $Y$ tends to be below its mean (negative association)
- **Cov(X,Y) = 0:** No linear relationship (but could have non-linear dependence)

### Properties

1. **Symmetry:** $\text{Cov}(X, Y) = \text{Cov}(Y, X)$
2. **Self-covariance:** $\text{Cov}(X, X) = \text{Var}(X)$
3. **Bilinearity:**
   - $\text{Cov}(aX + b, cY + d) = ac \cdot \text{Cov}(X, Y)$
   - $\text{Cov}(X + Y, Z) = \text{Cov}(X, Z) + \text{Cov}(Y, Z)$
4. **Variance of sum:**
   $$\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) + 2\text{Cov}(X, Y)$$
   $$\text{Var}\left(\sum_{i=1}^n a_i X_i\right) = \sum_{i=1}^n a_i^2\text{Var}(X_i) + 2\sum_{i<j} a_i a_j \text{Cov}(X_i, X_j)$$

5. **Independence implication:** If $X \perp Y$, then $\text{Cov}(X, Y) = 0$ (but converse is false)

### Limitations

- Covariance is **scale-dependent**: $\text{Cov}(aX, bY) = ab \cdot \text{Cov}(X, Y)$
- Magnitude is hard to interpret without context
- Only captures **linear** relationships

## Pearson Correlation Coefficient

### Definition

$$\rho_{XY} = \frac{\text{Cov}(X, Y)}{\sigma_X \sigma_Y}$$

The sample correlation is:
$$r_{xy} = \frac{\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^n (x_i - \bar{x})^2} \sqrt{\sum_{i=1}^n (y_i - \bar{y})^2}}$$

### Properties

1. **Bounds:** $-1 \leq \rho \leq 1$
2. **Perfect correlation:** $|\rho| = 1$ iff $Y = aX + b$ almost surely (perfect linear relationship)
3. **Zero correlation:** $\rho = 0$ does NOT imply independence — only absence of linear relationship
4. **Scale/location invariance:** $\rho(aX + b, cY + d) = \text{sign}(ac) \cdot \rho(X, Y)$
5. **Interpretation:** $\rho^2$ is the proportion of variance in $Y$ explained by linear prediction from $X$

### Anscombe's Quartet

Anscombe's quartet demonstrates why visualization is essential: four datasets with identical $\bar{x}, \bar{y}, r, \text{Var}(x), \text{Var}(y)$ but wildly different relationships (linear, quadratic, outlier-driven, vertical). Always **plot your data** before interpreting correlation.

## Covariance Matrix

For a random vector $X = (X_1, X_2, \dots, X_d)^\top$:

$$\Sigma = \text{Cov}(X) = E[(X - \mu)(X - \mu)^\top]$$

$$\Sigma_{ij} = \text{Cov}(X_i, X_j)$$

### Properties

1. **Symmetric:** $\Sigma = \Sigma^\top$
2. **Positive semidefinite (PSD):** $a^\top \Sigma a \geq 0$ for all $a \in \mathbb{R}^d$
3. **Diagonal entries:** $\Sigma_{ii} = \text{Var}(X_i)$
4. **Factorization:** $\Sigma = LL^\top$ for some matrix $L$ (Cholesky decomposition) — used for sampling
5. **Spectral decomposition:** $\Sigma = Q\Lambda Q^\top$ where $Q$ is orthogonal and $\Lambda$ is diagonal (eigenvalues)

### Correlation Matrix

$$R_{ij} = \frac{\Sigma_{ij}}{\sqrt{\Sigma_{ii}\Sigma_{jj}}}$$

Or: $R = D^{-1/2} \Sigma D^{-1/2}$ where $D = \text{diag}(\Sigma)$.

## Rank Correlation Measures

### Spearman's Rank Correlation

Pearson correlation applied to **ranks** rather than raw values:

$$\rho_S = \frac{\text{Cov}(R(X), R(Y))}{\sigma_{R(X)} \sigma_{R(Y)}}$$

- Measures **monotonic** (not necessarily linear) association
- Invariant to any monotonic transformation
- Equivalent to Pearson on ranks

### Kendall's Tau ($\tau$)

$$\tau = \frac{2}{n(n-1)} \sum_{i<j} \text{sign}(x_i - x_j) \cdot \text{sign}(y_i - y_j)$$

- Measures **concordance probability minus discordance probability**
- More robust to outliers than Spearman
- $\tau \in [-1, 1]$, $\tau = 1$ for perfectly monotone increasing

## Partial Correlation

### Definition

The partial correlation $\rho_{XY \cdot Z}$ measures the correlation between $X$ and $Y$ after removing the effect of $Z$:

1. Regress $X$ on $Z$: $\hat{X} = \hat{\beta}_X Z$, get residuals $r_X = X - \hat{X}$
2. Regress $Y$ on $Z$: $\hat{Y} = \hat{\beta}_Y Z$, get residuals $r_Y = Y - \hat{Y}$
3. $\rho_{XY \cdot Z} = \text{corr}(r_X, r_Y)$

### Formula

$$\rho_{XY \cdot Z} = \frac{\rho_{XY} - \rho_{XZ} \rho_{YZ}}{\sqrt{(1 - \rho_{XZ}^2)(1 - \rho_{YZ}^2)}}$$

### Graphical Models

In Gaussian graphical models, partial correlations determine conditional independence: $X \perp Y \mid Z$ iff $\rho_{XY \cdot Z} = 0$. The partial correlation matrix gives the precision matrix $\Theta = \Sigma^{-1}$:
$$\rho_{XY \cdot \text{rest}} = -\frac{\Theta_{XY}}{\sqrt{\Theta_{XX} \Theta_{YY}}}$$

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# Generate correlated data
np.random.seed(42)
n = 1000
x = np.random.normal(0, 1, n)
y = 0.7 * x + np.sqrt(1 - 0.7**2) * np.random.normal(0, 1, n)

# Pearson
pearson_r, p_val = stats.pearsonr(x, y)
print(f"Pearson r = {pearson_r:.4f} (p = {p_val:.2e})")

# Spearman
spearman_r, _ = stats.spearmanr(x, y)
print(f"Spearman ρ = {spearman_r:.4f}")

# Kendall
kendall_tau, _ = stats.kendalltau(x, y)
print(f"Kendall τ = {kendall_tau:.4f}")

# Covariance matrix
data = np.column_stack([x, y, np.random.normal(0, 1, n)])
cov_matrix = np.cov(data.T)
corr_matrix = np.corrcoef(data.T)

print("\nCovariance matrix:")
print(cov_matrix)
print("\nCorrelation matrix:")
print(corr_matrix)

# Partial correlation using precision matrix
precision = np.linalg.inv(cov_matrix)
D = np.diag(np.sqrt(np.diag(precision)))
partial_corr = -D @ precision @ D
partial_corr[np.diag_indices_from(partial_corr)] = 1.0
print("\nPartial correlation matrix:")
print(partial_corr)

# Anscombe's quartet
anscombe_x = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
anscombe_y1 = [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]
anscombe_y2 = [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].scatter(anscombe_x, anscombe_y1)
axes[0].set_title(f"Set 1: r={np.corrcoef(anscombe_x, anscombe_y1)[0,1]:.3f}")
axes[1].scatter(anscombe_x, anscombe_y2)
axes[1].set_title(f"Set 2: r={np.corrcoef(anscombe_x, anscombe_y2)[0,1]:.3f}")
plt.tight_layout()
plt.show()
```

## Visualization

Create a scatterplot matrix (pairplot) showing: (1) Strong positive correlation (points clustered along diagonal), (2) Strong negative correlation (anti-diagonal cluster), (3) No correlation (circular cloud), (4) Non-linear relationship with zero correlation (e.g., parabola). Overlay the best-fit line for Pearson. Add a second figure showing how Spearman and Kendall capture monotonic relationships that Pearson misses.

## Practical Considerations

- **Correlation ≠ causation:** This cannot be overemphasized. Spurious correlation arises from confounders, selection bias, and coincidence.
- **Range restriction:** Correlation is attenuated when the range of one variable is restricted. This is a common issue in psychometrics and hiring.
- **Outliers:** A single outlier can dramatically change Pearson correlation. Always use robust measures (Spearman, Kendall) as a check.
- **Weighted correlation:** When observations have different weights, use weighted versions of covariance.
- **Numerical stability:** Computing covariance as $E[XY] - E[X]E[Y]$ can cause catastrophic cancellation. Use the two-pass or Welford algorithm.

## References

- Pearson, K. (1895). "Notes on regression and inheritance in the case of two parents"
- Spearman, C. (1904). "The proof and measurement of association between two things"
- Kendall, M. G. (1938). "A new measure of rank correlation"
- Anscombe, F. J. (1973). "Graphs in statistical analysis"
