# Lesson 08: Transformations of Random Variables

## Learning Objectives

After completing this lesson, you will be able to:
- Derive the PDF of a transformed univariate random variable using the Jacobian method
- Apply the multivariate change-of-variables formula
- Use the probability integral transform for sampling
- Implement Box-Muller and other transformation-based sampling methods

## Univariate Transformations

### Monotone Transformation

If $X$ has density $f_X$ and $Y = g(X)$ where $g$ is strictly monotone (and hence invertible) and differentiable:

$$f_Y(y) = f_X(g^{-1}(y)) \cdot \left|\frac{d}{dy} g^{-1}(y)\right|$$

**Derivation:** $F_Y(y) = P(Y \leq y) = P(g(X) \leq y) = P(X \leq g^{-1}(y))$ for increasing $g$. Differentiate using chain rule and absolute value.

### Example: Linear Transformation

If $Y = aX + b$ with $a \neq 0$:
$$f_Y(y) = f_X\left(\frac{y - b}{a}\right) \cdot \frac{1}{|a|}$$

### Example: Exponential Transformation

If $X \sim \text{Uniform}(0,1)$ and $Y = -\frac{1}{\lambda} \log X$:
- $g(x) = -\frac{1}{\lambda} \log x$, $g^{-1}(y) = e^{-\lambda y}$
- Jacobian: $|d/dy \, g^{-1}(y)| = \lambda e^{-\lambda y}$
- $f_Y(y) = 1 \cdot \lambda e^{-\lambda y} = \lambda e^{-\lambda y}$ for $y \geq 0$
- Therefore $Y \sim \text{Exponential}(\lambda)$ — inverse transform sampling!

### General Univariate Case

If $g$ is not monotone, enumerate the pre-images:
$$f_Y(y) = \sum_{x: g(x) = y} \frac{f_X(x)}{|g'(x)|}$$

This is the **multivalued inverse** formula.

## Multivariate Transformations (Jacobian Method)

Let $X \in \mathbb{R}^d$ have joint PDF $f_X$ and let $Y = g(X)$ where $g: \mathbb{R}^d \to \mathbb{R}^d$ is differentiable and invertible:

$$f_Y(y) = f_X(g^{-1}(y)) \cdot |\det J|$$

where $J$ is the **Jacobian matrix** of the inverse transformation:
$$J_{ij} = \frac{\partial x_i}{\partial y_j} \quad \text{where } x = g^{-1}(y)$$

### Example: Linear Transformation

If $Y = AX + b$ with $A$ invertible:
$$f_Y(y) = f_X(A^{-1}(y - b)) \cdot \frac{1}{|\det A|}$$

**Special case — affine transformation of MVN:** If $X \sim \mathcal{N}(\mu, \Sigma)$ and $Y = AX + b$:
$$Y \sim \mathcal{N}(A\mu + b, A\Sigma A^\top)$$

### Example: Sum and Difference

For $(U, V) = (X+Y, X-Y)$:
$$(X, Y) = \left(\frac{U+V}{2}, \frac{U-V}{2}\right)$$
$$J = \begin{bmatrix} 1/2 & 1/2 \\ 1/2 & -1/2 \end{bmatrix}, \quad |\det J| = \frac{1}{2}$$
$$f_{U,V}(u, v) = \frac{1}{2} f_{X,Y}\left(\frac{u+v}{2}, \frac{u-v}{2}\right)$$

### Example: Polar to Cartesian

For $(R, \Theta)$ where $X = R\cos\Theta$, $Y = R\sin\Theta$:
$$f_{R,\Theta}(r, \theta) = r \cdot f_{X,Y}(r\cos\theta, r\sin\theta)$$

## Probability Integral Transform (PIT)

### Forward PIT

If $X$ has continuous CDF $F_X$, then:
$$U = F_X(X) \sim \text{Uniform}(0, 1)$$

**Proof:** $P(U \leq u) = P(F_X(X) \leq u) = P(X \leq F_X^{-1}(u)) = F_X(F_X^{-1}(u)) = u$

### Inverse PIT (Quantile Transform)

If $U \sim \text{Uniform}(0, 1)$ and $F$ is a CDF, then:
$$X = F^{-1}(U) \sim F$$

where $F^{-1}(p) = \inf\{x: F(x) \geq p\}$ is the generalized inverse (quantile function).

### Applications

- **Sampling:** Generate samples from any distribution using uniform random numbers
- **Copulas:** Joint distributions with uniform marginals
- **Calibration:** If predictive CDFs are correct, PIT values should be uniform
- **Goodness-of-fit:** Test whether data follows a specified distribution

## Box-Muller Transform

If $U_1, U_2 \sim \text{Uniform}(0, 1)$ independently:

$$Z_1 = \sqrt{-2 \ln U_1} \cos(2\pi U_2)$$
$$Z_2 = \sqrt{-2 \ln U_1} \sin(2\pi U_2)$$

Then $Z_1, Z_2 \overset{\text{i.i.d.}}{\sim} \mathcal{N}(0, 1)$.

**Derivation:** Transform $(U_1, U_2)$ to $(Z_1, Z_2)$ via polar coordinates. Joint density of $(Z_1, Z_2)$ is:
$$f(z_1, z_2) = \frac{1}{2\pi} e^{-(z_1^2 + z_2^2)/2}$$

## Cholesky Transformation

To sample from $\mathcal{N}(\mu, \Sigma)$:
1. Compute Cholesky decomposition: $\Sigma = LL^\top$
2. Sample $Z \sim \mathcal{N}(0, I)$
3. Set $X = \mu + LZ$

Then $\text{Cov}(X) = L \cdot I \cdot L^\top = \Sigma$.

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Inverse transform sampling: Gamma(2, 1) via Gamma CDF inverse
# (using built-in but showing the principle)
def inverse_transform_sampling(n=10000):
    u = np.random.uniform(0, 1, n)
    return stats.gamma.ppf(u, a=2, scale=1)

samples = inverse_transform_sampling()
xs = np.linspace(0, 10, 1000)
plt.figure(figsize=(10, 4))
plt.hist(samples, bins=80, density=True, alpha=0.7, label='Samples')
plt.plot(xs, stats.gamma.pdf(xs, a=2, scale=1), 'r-', lw=2, label='True PDF')
plt.legend()
plt.title("Inverse Transform Sampling: Gamma(2,1)")
plt.show()

# Box-Muller transform
def box_muller(n=10000):
    u1 = np.random.uniform(0, 1, n)
    u2 = np.random.uniform(0, 1, n)
    z1 = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
    z2 = np.sqrt(-2 * np.log(u1)) * np.sin(2 * np.pi * u2)
    return z1, z2

z1, z2 = box_muller()
plt.figure(figsize=(10, 4))
plt.hist(z1, bins=80, density=True, alpha=0.7, label='Box-Muller samples')
xs = np.linspace(-4, 4, 1000)
plt.plot(xs, stats.norm.pdf(xs), 'r-', lw=2, label='N(0,1) PDF')
plt.legend()
plt.title("Box-Muller Transform: Standard Normal")
plt.show()

# Cholesky sampling from MVN
mu = np.array([1.0, 2.0])
sigma = np.array([[2.0, 1.5], [1.5, 1.0]])
L = np.linalg.cholesky(sigma)
Z = np.random.normal(0, 1, (5000, 2))
X = mu + Z @ L.T

plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], alpha=0.3, s=1)
plt.xlabel('X1')
plt.ylabel('X2')
plt.title('Cholesky Sampling from MVN')
plt.axis('equal')
plt.show()
```

## Visualization

The Box-Muller transform can be visualized as mapping the unit square $(U_1, U_2)$ through a polar coordinate transformation. Samples from the uniform square "wrap" around the origin and map to a 2D Gaussian cloud. Show a 2×2 subplot grid: (1) uniform samples in $[0,1]^2$, (2) intermediate polar coordinates, (3) resulting Gaussian samples, (4) the theoretical standard normal PDF overlaid.

## Practical Considerations

- **PIT for diagnostics:** After fitting a probabilistic model, compute PIT values. If they deviate from Uniform(0,1), the model is misspecified (too narrow, too wide, or biased).
- **Numerical stability:** Box-Muller can suffer from overflow when $U_1$ is near 0. Use the Marsaglia polar method as a more stable alternative.
- **High-dimensional transformations:** The Jacobian determinant scales poorly with dimension. Normalizing flows use carefully designed transformations with tractable Jacobians.
- **Reproducibility:** Always set random seeds for sampling-based transformations.

## References

- Box, G. E. P. & Muller, M. E. (1958). "A note on the generation of random normal deviates"
- Devroye, L. (1986). *Non-Uniform Random Variate Generation*
- Casella, G. & Berger, R. L. (2002). *Statistical Inference*
