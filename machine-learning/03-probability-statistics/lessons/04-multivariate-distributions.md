# Lesson 04: Multivariate Distributions

## Learning Objectives

After completing this lesson, you will be able to:
- Define and work with joint CDFs, PMFs, and PDFs
- Understand the Multinomial and Multivariate Normal distributions
- Compute marginal and conditional distributions analytically
- Recognize properties of the Wishart distribution
- Apply the MVN in ML contexts (Mahalanobis distance, Gaussian processes)

## Joint Distribution Functions

### Joint CDF

For random variables $X$ and $Y$, the joint CDF is:
$$F_{X,Y}(x, y) = P(X \leq x, Y \leq y)$$

**Properties:**
1. **Non-decreasing** in each argument: $x_1 \leq x_2 \implies F(x_1, y) \leq F(x_2, y)$
2. **Right-continuous** in each argument
3. **Rectangle inequality:** For $a \leq b, c \leq d$:
   $$P(a < X \leq b, c < Y \leq d) = F(b,d) - F(a,d) - F(b,c) + F(a,c) \geq 0$$
4. **Limits:** $F(-\infty, y) = F(x, -\infty) = 0$, $F(\infty, \infty) = 1$

### Joint PMF (Discrete)

$$p_{X,Y}(x, y) = P(X = x, Y = y)$$

Properties: $p(x,y) \geq 0$, $\sum_x \sum_y p(x,y) = 1$

### Joint PDF (Continuous)

$$f_{X,Y}(x, y) \geq 0, \quad \int_{-\infty}^{\infty} \int_{-\infty}^{\infty} f_{X,Y}(x, y) \, dx \, dy = 1$$

Relationship to CDF: $F_{X,Y}(x, y) = \int_{-\infty}^{x} \int_{-\infty}^{y} f_{X,Y}(u, v) \, du \, dv$

If the joint PDF exists almost everywhere:
$$f_{X,Y}(x, y) = \frac{\partial^2}{\partial x \partial y} F_{X,Y}(x, y)$$

## Multinomial Distribution

The Multinomial distribution models $n$ independent trials each falling into one of $k$ categories with probabilities $p_1, \dots, p_k$.

$$P(X_1 = n_1, \dots, X_k = n_k) = \frac{n!}{n_1! \cdots n_k!} p_1^{n_1} \cdots p_k^{n_k}$$

where $\sum_{i=1}^k n_i = n$ and $\sum_{i=1}^k p_i = 1$.

**Moments:**
- $E[X_i] = np_i$
- $\text{Var}(X_i) = np_i(1-p_i)$
- $\text{Cov}(X_i, X_j) = -np_i p_j$ for $i \neq j$

**ML Connection:** Multi-class classification, Naive Bayes, topic models (LDA).

## Multivariate Normal Distribution

The MVN is the most important multivariate distribution in statistics and ML.

### Definition

$X \in \mathbb{R}^d$ follows a multivariate normal distribution $\mathcal{N}(\mu, \Sigma)$ with density:
$$f(x) = \frac{1}{(2\pi)^{d/2} |\Sigma|^{1/2}} \exp\left(-\frac{1}{2}(x - \mu)^\top \Sigma^{-1} (x - \mu)\right)$$

where $\mu \in \mathbb{R}^d$ is the mean vector and $\Sigma \in \mathbb{R}^{d \times d}$ is the positive definite covariance matrix.

### Key Properties

1. **Linear transformations preserve normality:**
   If $X \sim \mathcal{N}(\mu, \Sigma)$ and $A \in \mathbb{R}^{m \times d}$, $b \in \mathbb{R}^m$:
   $$AX + b \sim \mathcal{N}(A\mu + b, A\Sigma A^\top)$$

2. **Marginal distributions are normal:**
   Partition $X = (X_1, X_2)^\top$ with $X_1 \in \mathbb{R}^{d_1}$, $X_2 \in \mathbb{R}^{d_2}$:
   $$X_1 \sim \mathcal{N}(\mu_1, \Sigma_{11})$$
   $$X_2 \sim \mathcal{N}(\mu_2, \Sigma_{22})$$

3. **Conditional distributions are normal:**
   $$X_1 \mid X_2 = x_2 \sim \mathcal{N}(\mu_{1|2}, \Sigma_{1|2})$$
   $$\mu_{1|2} = \mu_1 + \Sigma_{12}\Sigma_{22}^{-1}(x_2 - \mu_2)$$
   $$\Sigma_{1|2} = \Sigma_{11} - \Sigma_{12}\Sigma_{22}^{-1}\Sigma_{21}$$

4. **Zero covariance implies independence:**
   If $\Sigma_{12} = 0$, then $X_1$ and $X_2$ are independent. This is unique to the MVN.

5. **Quadratic form is Chi-squared:**
   $$(X - \mu)^\top \Sigma^{-1} (X - \mu) \sim \chi^2_d$$

### Mahalanobis Distance

The **Mahalanobis distance** between $x$ and $\mu$:
$$D_M(x) = \sqrt{(x - \mu)^\top \Sigma^{-1} (x - \mu)}$$

This accounts for correlation between dimensions. Points with $D_M(x) > \chi^2_{d, 0.95}$ are potential outliers.

## Wishart Distribution

The Wishart distribution generalizes the chi-squared distribution to multivariate settings.

If $X_1, \dots, X_n \overset{\text{i.i.d.}}{\sim} \mathcal{N}_d(0, \Sigma)$, then:
$$S = \sum_{i=1}^n X_i X_i^\top \sim \mathcal{W}_d(\Sigma, n)$$

- $E[S] = n\Sigma$
- Used as the conjugate prior for the precision matrix $\Sigma^{-1}$ in Bayesian analysis
- **Inverse Wishart:** $S^{-1} \sim \mathcal{W}_d^{-1}(\Sigma^{-1}, n)$ is the conjugate prior for $\Sigma$

## Copulas

A **copula** separates marginal distributions from dependence structure. By Sklar's theorem:
$$F(x_1, \dots, x_d) = C(F_1(x_1), \dots, F_d(x_d))$$

where $C$ is a copula (CDF on $[0,1]^d$ with uniform marginals).

Common copulas:
- **Gaussian copula:** $C(u) = \Phi_\Sigma(\Phi^{-1}(u_1), \dots, \Phi^{-1}(u_d))$
- **Clayton copula:** Lower tail dependence
- **Gumbel copula:** Upper tail dependence
- **t-copula:** Symmetric tail dependence

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

# 2D Multivariate Normal
mu = np.array([0.0, 0.0])
sigma = np.array([[1.0, 0.8], [0.8, 1.0]])

# Create grid
x, y = np.mgrid[-3:3:100j, -3:3:100j]
pos = np.dstack((x, y))
rv = multivariate_normal(mu, sigma)

# Plot contours
plt.figure(figsize=(8, 6))
plt.contourf(x, y, rv.pdf(pos), levels=20, cmap='viridis')
plt.colorbar(label='PDF')
plt.xlabel('X1')
plt.ylabel('X2')
plt.title('Bivariate Normal PDF')
plt.axis('equal')
plt.show()

# Conditional distribution
# P(X1 | X2 = 0.5)
x2_val = 0.5
mu_cond = mu[0] + sigma[0,1] * (1/sigma[1,1]) * (x2_val - mu[1])
sigma_cond = sigma[0,0] - sigma[0,1] * (1/sigma[1,1]) * sigma[1,0]
print(f"E[X1 | X2={x2_val}] = {mu_cond:.3f}")
print(f"Var[X1 | X2={x2_val}] = {sigma_cond:.3f}")

# Sampling
samples = rv.rvs(5000)
plt.figure(figsize=(8, 6))
plt.scatter(samples[:, 0], samples[:, 1], alpha=0.3, s=1)
plt.xlabel('X1')
plt.ylabel('X2')
plt.title('Samples from Bivariate Normal')
plt.axis('equal')
plt.show()
```

## Visualization

Plot a bivariate normal with contours representing equal Mahalanobis distance ($(x-\mu)^\top \Sigma^{-1}(x-\mu) = c$). These are ellipses centered at $\mu$, with axes determined by the eigenvectors of $\Sigma$ and radii proportional to the square roots of the eigenvalues. Show a secondary plot with the conditional distribution $f(x_1 \mid x_2 = c)$ overlaid — a one-dimensional normal sliced from the joint density.

## Practical Considerations

- **Curse of dimensionality:** In high dimensions ($d > 10$), the MVN density involves inverting a $d \times d$ matrix, costing $O(d^3)$. Use Cholesky decomposition for stability.
- **Numerical stability:** Use log-density ($\log f(x)$) instead of density to avoid underflow. The log-density involves $-d/2 \log(2\pi) - 1/2 \log|\Sigma| - 1/2 (x-\mu)^\top \Sigma^{-1}(x-\mu)$.
- **Singular covariance:** If $\Sigma$ is not full rank (e.g., $n < d$ in data), use the pseudoinverse or add a small diagonal $\epsilon I$.
- **Gaussian processes:** The MVN conditional formula is the foundation of GP regression, where the conditional mean gives predictions and the conditional variance gives uncertainty.

## References

- Anderson, T. W. (2003). *An Introduction to Multivariate Statistical Analysis*
- Mardia, K. V., Kent, J. T., & Bibby, J. M. (1979). *Multivariate Analysis*
- Eaton, M. L. (1983). *Multivariate Statistics: A Vector Space Approach*
