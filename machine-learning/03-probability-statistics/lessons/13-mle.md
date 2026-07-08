# Lesson 13: Maximum Likelihood Estimation (MLE)

## Learning Objectives

After completing this lesson, you will be able to:
- Define and compute the likelihood and log-likelihood functions
- Derive MLEs for standard distributions
- Understand asymptotic properties (consistency, normality, efficiency)
- Compute Fisher information and the Cramér-Rao Lower Bound
- Implement MLE numerically using optimization

## Likelihood Function

### Definition

Given i.i.d. observations $x_1, \dots, x_n$ from a distribution with PDF/PMF $f(x \mid \theta)$, the **likelihood function** is:
$$L(\theta) = \prod_{i=1}^n f(x_i \mid \theta)$$

The **log-likelihood** is:
$$\ell(\theta) = \log L(\theta) = \sum_{i=1}^n \log f(x_i \mid \theta)$$

### Likelihood Principle

All evidence about $\theta$ contained in the data is captured by the likelihood function. Two experiments with proportional likelihoods yield identical inferences about $\theta$.

## Maximum Likelihood Estimator

$$\hat{\theta}_{\text{MLE}} = \arg\max_{\theta \in \Theta} L(\theta) = \arg\max_{\theta \in \Theta} \ell(\theta)$$

### Score Function

The **score function** is the gradient of the log-likelihood:
$$S(\theta) = \frac{\partial \ell(\theta)}{\partial \theta} = \sum_{i=1}^n \frac{\partial}{\partial \theta} \log f(x_i \mid \theta)$$

MLE solves: $S(\hat{\theta}) = 0$ (the score equation).

### Second Derivative / Hessian

$$H(\theta) = \frac{\partial^2 \ell(\theta)}{\partial \theta \partial \theta^\top}$$

The negative Hessian at the MLE gives the **observed Fisher information**.

## Examples

### Bernoulli

$X_i \sim \text{Bernoulli}(p)$, $\ell(p) = \sum x_i \log p + (n - \sum x_i) \log(1-p)$
$$\frac{d\ell}{dp} = \frac{\sum x_i}{p} - \frac{n - \sum x_i}{1-p} = 0 \implies \hat{p} = \bar{X}$$

### Normal (Gaussian)

$X_i \sim \mathcal{N}(\mu, \sigma^2)$:
$$\ell(\mu, \sigma^2) = -\frac{n}{2} \log(2\pi\sigma^2) - \frac{1}{2\sigma^2} \sum (x_i - \mu)^2$$
$$\hat{\mu} = \bar{X}, \quad \hat{\sigma}^2 = \frac{1}{n} \sum (x_i - \bar{X})^2$$

Note: The MLE for $\sigma^2$ is biased (divides by $n$, not $n-1$). The unbiased estimator uses $n-1$.

### Poisson

$X_i \sim \text{Poisson}(\lambda)$:
$$\ell(\lambda) = \sum (x_i \log \lambda - \lambda - \log x_i!)$$
$$\frac{d\ell}{d\lambda} = \frac{\sum x_i}{\lambda} - n = 0 \implies \hat{\lambda} = \bar{X}$$

### Exponential

$X_i \sim \text{Exponential}(\lambda)$:
$$\ell(\lambda) = n \log \lambda - \lambda \sum x_i$$
$$\frac{d\ell}{d\lambda} = \frac{n}{\lambda} - \sum x_i = 0 \implies \hat{\lambda} = \frac{1}{\bar{X}}$$

## Properties of MLE

### Consistency

Under regularity conditions: $\hat{\theta}_n \xrightarrow{p} \theta_0$ (the true parameter).

**Conditions:** Identifiability, compact parameter space, continuity of $\ell(\theta)$, uniform convergence.

### Asymptotic Normality

$$\sqrt{n}(\hat{\theta}_n - \theta_0) \xrightarrow{d} \mathcal{N}(0, I(\theta_0)^{-1})$$

where $I(\theta_0)$ is the **Fisher information**.

### Asymptotic Efficiency

The MLE attains the Cramér-Rao Lower Bound asymptotically — no consistent estimator has lower asymptotic variance.

### Invariance

If $\hat{\theta}$ is the MLE of $\theta$, then for any function $g$, $g(\hat{\theta})$ is the MLE of $g(\theta)$.

## Fisher Information

### Observed Fisher Information

$$J(\theta) = -\frac{\partial^2 \ell(\theta)}{\partial \theta \partial \theta^\top}$$

### Expected Fisher Information

$$I(\theta) = -E\left[\frac{\partial^2}{\partial \theta^2} \log f(X \mid \theta)\right] = E[S(\theta)^2]$$

### Information Matrix Identity

Under regularity conditions:
$$E\left[\frac{\partial}{\partial \theta} \log f(X \mid \theta)\right] = 0$$
$$\text{Var}\left(\frac{\partial}{\partial \theta} \log f(X \mid \theta)\right) = I(\theta)$$

### Examples

- **Bernoulli:** $I(p) = \frac{1}{p(1-p)}$
- **Normal (known $\sigma^2$):** $I(\mu) = \frac{1}{\sigma^2}$
- **Poisson:** $I(\lambda) = \frac{1}{\lambda}$
- **Exponential:** $I(\lambda) = \frac{1}{\lambda^2}$

## Cramér-Rao Lower Bound (CRLB)

### Statement

For any unbiased estimator $\delta(X)$ of $\theta$:
$$\text{Var}(\delta(X)) \geq \frac{1}{I(\theta)}$$

For vector-valued $\theta$:
$$\text{Cov}(\delta(X)) \succeq I(\theta)^{-1}$$

(where $\succeq$ means the matrix difference is positive semidefinite)

### Efficiency

An estimator achieving the CRLB is called **efficient**. The MLE is asymptotically efficient.

## Numerical MLE via Optimization

When no closed-form MLE exists (e.g., logistic regression, GLMs with non-canonical links), use numerical optimization:

1. **Newton-Raphson:** $\theta^{(t+1)} = \theta^{(t)} - H(\theta^{(t)})^{-1} S(\theta^{(t)})$
2. **Fisher scoring:** $\theta^{(t+1)} = \theta^{(t)} + I(\theta^{(t)})^{-1} S(\theta^{(t)})$
3. **BFGS / L-BFGS:** Quasi-Newton methods using approximate Hessian
4. **Gradient descent:** $\theta^{(t+1)} = \theta^{(t)} + \eta S(\theta^{(t)})$

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import minimize

# MLE for Gamma distribution (no closed form)
np.random.seed(42)
true_alpha, true_beta = 2.0, 0.5
data = np.random.gamma(true_alpha, 1/true_beta, size=500)

def neg_log_likelihood(params):
    alpha, beta = params
    if alpha <= 0 or beta <= 0:
        return np.inf
    n = len(data)
    return -n * (alpha * np.log(beta) - np.log(stats.gamma(alpha).pdf(1))) \
           - (alpha - 1) * np.sum(np.log(data)) + beta * np.sum(data)

result = minimize(neg_log_likelihood, x0=[1.0, 1.0], method='L-BFGS-B',
                  bounds=[(0.01, 10), (0.01, 10)])
alpha_hat, beta_hat = result.x
print(f"MLE: alpha={alpha_hat:.3f} (true={true_alpha}), beta={beta_hat:.3f} (true={true_beta})")

# Fisher information and standard errors
# For Gamma, observed Fisher info from Hessian
hessian = result.hess  # approximation
se = np.sqrt(np.diag(np.linalg.inv(hessian)))
print(f"SE(alpha) = {se[0]:.4f}, SE(beta) = {se[1]:.4f}")

# Profile likelihood
def profile_likelihood(alpha_val):
    # MLE of beta given alpha
    beta_mle = alpha_val / np.mean(data)
    return -neg_log_likelihood([alpha_val, beta_mle])

alphas = np.linspace(1.5, 2.5, 100)
profile = [profile_likelihood(a) for a in alphas]

plt.figure(figsize=(10, 4))
plt.plot(alphas, profile, 'b-', lw=2)
plt.axvline(x=true_alpha, color='r', linestyle='--', label=f'True α={true_alpha}')
plt.axvline(x=alpha_hat, color='g', linestyle='--', label=f'MLE α={alpha_hat:.3f}')
plt.axhline(y=profile_likelihood(alpha_hat) - 1.92, color='gray', linestyle=':', label='95% LR CI')
plt.xlabel('α')
plt.ylabel('Profile log-likelihood')
plt.legend()
plt.title('Profile Likelihood for Gamma Shape Parameter')
plt.show()
```

## Visualization

Plot the log-likelihood surface for a two-parameter model (e.g., Normal $(\mu, \sigma^2)$) as a contour plot. Mark the MLE at the peak. Show the Fisher information geometrically as the curvature at the MLE — sharper curvature (higher Fisher information) means lower variance. Add the profile likelihood for one parameter, showing the 95% confidence interval where the log-likelihood drops by $\chi^2_{1,0.05}/2 \approx 1.92$.

## Practical Considerations

- **Multiple local maxima:** For multimodal likelihoods, use multiple starting points or global optimization.
- **Boundary issues:** MLEs may lie on the boundary of the parameter space (e.g., $\hat{\sigma}^2 = 0$). This breaks asymptotic theory.
- **Singular Fisher information:** When parameters are not identifiable, $I(\theta)$ is singular. Use constraints or reparameterization.
- **Small-sample bias:** MLEs are generally biased (e.g., $\hat{\sigma}^2$ for Normal). Use bias corrections or bootstrap for small samples.
- **Computational cost:** For large $n$ and many parameters, evaluate log-likelihood on mini-batches (stochastic optimization).

## References

- Fisher, R. A. (1922). "On the mathematical foundations of theoretical statistics"
- Cramér, H. (1946). *Mathematical Methods of Statistics*
- Rao, C. R. (1945). "Information and the accuracy attainable in the estimation of statistical parameters"
- Pawitan, Y. (2001). *In All Likelihood: Statistical Modelling and Inference Using Likelihood*
