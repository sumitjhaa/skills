# Lesson 32: Copulas

## Learning Objectives

After completing this lesson, you will be able to:
- Understand Sklar's theorem and the copula representation of joint distributions
- Identify common copula families and their tail dependence properties
- Measure dependence using Kendall's tau and tail dependence coefficients
- Estimate copula parameters using two-stage inference
- Apply copulas in finance, risk management, and multi-view learning

## Sklar's Theorem

### Statement

For any joint CDF $F$ with marginal CDFs $F_1, \dots, F_d$, there exists a **copula** $C$ such that:
$$F(x_1, \dots, x_d) = C(F_1(x_1), \dots, F_d(x_d))$$

If all marginals are continuous, $C$ is unique. Conversely, for any copula $C$ and marginal CDFs $F_1, \dots, F_d$, the function $C(F_1(x_1), \dots, F_d(x_d))$ is a valid joint CDF.

### Key Insight

Copulas **separate marginal behavior from dependence structure**. This is the fundamental advantage of copula modeling — we can model the marginals and dependence separately.

## Properties of Copulas

A copula $C: [0,1]^d \to [0,1]$ satisfies:

1. **Uniform marginals:** $C(1, \dots, 1, u_i, 1, \dots, 1) = u_i$ for all $i$
2. **Grounded:** $C(u_1, \dots, u_d) = 0$ if any $u_i = 0$
3. **$d$-increasing:** For any rectangle $[a_1, b_1] \times \cdots \times [a_d, b_d]$, the $C$-volume is non-negative

### Fréchet-Hoeffding Bounds

For any copula $C$:
$$W(u_1, \dots, u_d) \leq C(u_1, \dots, u_d) \leq M(u_1, \dots, u_d)$$

- **Lower bound (countermonotonic):** $W(u_1, u_2) = \max(u_1 + u_2 - 1, 0)$
- **Upper bound (comonotonic):** $M(u_1, \dots, u_d) = \min(u_1, \dots, u_d)$
- **Independence copula:** $\Pi(u_1, \dots, u_d) = \prod u_i$

## Common Copula Families

### Elliptical Copulas

**Gaussian copula:**
$$C_R(u) = \Phi_R(\Phi^{-1}(u_1), \dots, \Phi^{-1}(u_d))$$

- Parameter: correlation matrix $R$
- Symmetric in tails
- No tail dependence (unless $|\rho| = 1$)
- Tail dependence: $\lambda_L = \lambda_U = 0$ for $|\rho| < 1$

**t-copula:**
$$C_{R, \nu}(u) = t_{R, \nu}(t_\nu^{-1}(u_1), \dots, t_\nu^{-1}(u_d))$$

- Parameters: correlation matrix $R$, degrees of freedom $\nu$
- Symmetric, has symmetric tail dependence
- As $\nu \to \infty$, converges to Gaussian copula
- Tail dependence: $\lambda_L = \lambda_U = 2t_{\nu+1}(-\sqrt{(\nu+1)(1-\rho)/(1+\rho)})$

### Archimedean Copulas

**Clayton:**
$$C_\theta(u) = \left(\sum_{i=1}^d u_i^{-\theta} - d + 1\right)^{-1/\theta}, \quad \theta > 0$$

- Asymmetric: strong lower tail dependence, weak upper tail dependence
- Tail dependence: $\lambda_L = 2^{-1/\theta}$, $\lambda_U = 0$

**Gumbel:**
$$C_\theta(u) = \exp\left(-\left(\sum_{i=1}^d (-\log u_i)^\theta\right)^{1/\theta}\right), \quad \theta \geq 1$$

- Asymmetric: strong upper tail dependence, weak lower tail dependence
- Tail dependence: $\lambda_U = 2 - 2^{1/\theta}$, $\lambda_L = 0$

**Frank:**
$$C_\theta(u) = -\frac{1}{\theta} \log\left(1 + \frac{\prod_{i=1}^d (e^{-\theta u_i} - 1)}{(e^{-\theta} - 1)^{d-1}}\right)$$

- Symmetric, no tail dependence ($\lambda_L = \lambda_U = 0$)
- Allows both positive and negative dependence ($\theta \in \mathbb{R} \setminus \{0\}$)

## Dependence Measures

### Kendall's Tau

$$\tau = 4 \int_{[0,1]^2} C(u, v) \, dC(u, v) - 1$$

Relationships for bivariate copulas:
- Gaussian: $\tau = \frac{2}{\pi} \arcsin(\rho)$
- Clayton: $\tau = \frac{\theta}{\theta + 2}$
- Gumbel: $\tau = 1 - \frac{1}{\theta}$
- Frank: $\tau = 1 - \frac{4}{\theta} \left(1 - \frac{1}{\theta} \int_0^\theta \frac{t}{e^t - 1} dt\right)$

### Tail Dependence

**Lower tail dependence:**
$$\lambda_L = \lim_{u \to 0^+} \frac{C(u, u)}{u}$$

**Upper tail dependence:**
$$\lambda_U = \lim_{u \to 1^-} \frac{1 - 2u + C(u, u)}{1-u}$$

$\lambda \in [0, 1]$ — the probability that one variable is extreme given the other is extreme.

## Inference for Margins (IFM)

### Two-Stage Estimation

1. **Marginal parameters:** Estimate $\hat{\theta}_j$ for each margin $F_j$ (e.g., via MLE)
2. **Copula parameters:** Maximize:
   $$\hat{\psi} = \arg\max_\psi \sum_{i=1}^n \log c(F_1(x_{i1}; \hat{\theta}_1), \dots, F_d(x_{id}; \hat{\theta}_d); \psi)$$

where $c$ is the copula density.

### Semi-Parametric Estimation

Use empirical CDFs for marginals (pseudo-observations):
$$\hat{u}_{ij} = \frac{\text{rank}(x_{ij})}{n+1}$$

Then estimate copula parameters from pseudo-observations.

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import minimize

# Generate data with Clayton copula
np.random.seed(42)
n = 1000
theta = 2.0  # Clayton parameter

# Generate from Clayton copula using conditional method
u = np.random.uniform(0, 1, n)
v = np.random.uniform(0, 1, n)
# Inverse conditional for Clayton
w = u * (v**(-theta/(theta+1)) - 1) + 1
clayton_v = w**(-1/theta)
clayton_u = u

# Transform to have Gamma and Beta marginals
x = stats.gamma.ppf(clayton_u, a=2, scale=2)
y = stats.beta.ppf(clayton_v, a=2, b=5)

plt.figure(figsize=(12, 4))
plt.subplot(131)
plt.scatter(x, y, alpha=0.3, s=5)
plt.xlabel('X ~ Gamma(2,2)')
plt.ylabel('Y ~ Beta(2,5)')
plt.title(f'Clayton copula (θ={theta})')
plt.xlim(0, 20)

# Estimate Kendall's tau
tau_emp = stats.kendalltau(x, y).statistic
theta_est = 2 * tau_emp / (1 - tau_emp)
print(f"Empirical Kendall's τ = {tau_emp:.3f}")
print(f"Estimated θ = {theta_est:.3f} (true = {theta})")

# Fit Gaussian copula
# Transform to uniform
u_x = stats.gamma.cdf(x, a=2, scale=2)
u_y = stats.beta.cdf(y, a=2, b=5)

# Estimate correlation
rho_est = np.corrcoef(stats.norm.ppf(u_x), stats.norm.ppf(u_y))[0, 1]
print(f"Gaussian copula ρ = {rho_est:.3f}")

# Compare tail behaviors
plt.subplot(132)
threshold = 0.1
lower_x = x < stats.gamma.ppf(threshold, a=2, scale=2)
lower_y = y < stats.beta.ppf(threshold, a=2, b=5)
joint_lower = np.mean(lower_x & lower_y)
indep_lower = threshold**2
print(f"\nJoint lower tail probability: {joint_lower:.3f} (independence: {indep_lower:.3f})")

plt.scatter(x[lower_x & lower_y], y[lower_x & lower_y], c='red', alpha=0.5, s=5, label='Lower tail')
plt.scatter(x[~(lower_x & lower_y)], y[~(lower_x & lower_y)], alpha=0.2, s=2, label='Other')
plt.legend()
plt.title('Lower Tail Dependence')

# Copula density visualization
plt.subplot(133)
u_grid, v_grid = np.meshgrid(np.linspace(0.01, 0.99, 50), np.linspace(0.01, 0.99, 50))
# Clayton density
density = (theta + 1) * (u_grid * v_grid)**(-theta - 1) * \
          (u_grid**(-theta) + v_grid**(-theta) - 1)**(-(2 * theta + 1) / theta)
plt.contourf(u_grid, v_grid, density, levels=20, cmap='viridis')
plt.colorbar(label='Copula density')
plt.xlabel('u')
plt.ylabel('v')
plt.title('Clayton Copula Density')

plt.tight_layout()
plt.show()
```

## Visualization

Create a scatterplot of the data on the original scale (showing marginal distributions) and on the uniform scale (showing the copula). The copula density plot shows how dependence concentrates: Clayton in the lower-left corner (lower tail dependence), Gumbel in the upper-right, Gaussian symmetric with no corners. A second figure compares the empirical copula (estimated from data) with the fitted parametric copula via contour plots.

## Practical Considerations

- **Curse of dimensionality:** For $d > 10$, most copulas become restrictive (elliptical) or computationally expensive (vine copulas are the practical solution).
- **Vine copulas:** Decompose a $d$-dimensional copula into a cascade of bivariate copulas (pair-copula constructions). Flexible and scalable.
- **Time-varying copulas:** For financial data, copula parameters may change over time. Use regime-switching or DCC-type copula models.
- **Goodness-of-fit:** Use the Cramér-von Mises statistic based on the empirical copula process. Bootstrap for p-values.
- **Model selection:** Compare copulas using AIC/BIC. The "best" copula depends on the tail behavior of your data.

## References

- Sklar, A. (1959). "Fonctions de répartition à n dimensions et leurs marges"
- Joe, H. (2014). *Dependence Modeling with Copulas*
- Nelsen, R. B. (2006). *An Introduction to Copulas*
- Aas, K., et al. (2009). "Pair-copula constructions of multiple dependence"
