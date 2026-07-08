# Lesson 15: Exponential Family

## Learning Objectives

After completing this lesson, you will be able to:
- Recognize distributions in the exponential family
- Derive mean and variance from the log-partition function
- Identify sufficient statistics for exponential family models
- Use natural parameters and canonical link functions
- Understand conjugacy in exponential families

## Definition

A family of distributions is in the **exponential family** if its density/PMF can be written as:
$$f(x \mid \theta) = h(x) \exp\left\{\eta(\theta)^\top T(x) - A(\theta)\right\}$$

where:
- $\eta(\theta)$: **natural parameter** (may be vector-valued)
- $T(x)$: **sufficient statistic** (same dimension as $\eta$)
- $A(\theta)$: **log-partition function** (normalization constant)
- $h(x)$: **base measure**

### Canonical Form

When using the natural parameterization $\eta$ directly:
$$f(x \mid \eta) = h(x) \exp\left\{\eta^\top T(x) - A(\eta)\right\}$$

where $A(\eta) = \log \int h(x) \exp\{\eta^\top T(x)\} dx$ ensures normalization.

## Properties

### Moments from Log-Partition

The log-partition function $A(\eta)$ is the **cumulant generating function**:

- **Mean:** $E[T(X)] = \nabla A(\eta)$
- **Covariance:** $\text{Cov}(T(X)) = \nabla^2 A(\eta)$ (Hessian matrix)
- **Higher cumulants:** Higher-order derivatives of $A(\eta)$

### Maximum Likelihood

For i.i.d. data $x_1, \dots, x_n$:
$$\ell(\eta) = \sum_{i=1}^n [\eta^\top T(x_i) - A(\eta)] + \text{const}$$

Score equation:
$$\nabla \ell(\eta) = \sum T(x_i) - n \nabla A(\eta) = 0 \implies E[T(X)] = \bar{T}(x)$$

The MLE matches the expected sufficient statistic to the empirical average — **moment matching**.

### Convexity

$A(\eta)$ is **convex** (since it's the log of a sum of exponentials). This ensures the likelihood is concave and MLE has a unique global optimum.

## Examples

| Distribution | $\eta$ | $T(x)$ | $A(\eta)$ | $h(x)$ |
|-------------|--------|--------|-----------|--------|
| Bernoulli($p$) | $\log(p/(1-p))$ | $x$ | $\log(1+e^\eta)$ | $1$ |
| Binomial($n,p$) | $\log(p/(1-p))$ | $x$ | $n\log(1+e^\eta)$ | $\binom{n}{x}$ |
| Poisson($\lambda$) | $\log\lambda$ | $x$ | $e^\eta$ | $1/x!$ |
| Normal($\mu, 1$) | $\mu$ | $x$ | $\eta^2/2$ | $\frac{1}{\sqrt{2\pi}}e^{-x^2/2}$ |
| Normal($\mu, \sigma^2$) | $(\mu/\sigma^2, -1/(2\sigma^2))$ | $(x, x^2)$ | $-\eta_1^2/(4\eta_2) - \frac{1}{2}\log(-2\eta_2)$ | $\frac{1}{\sqrt{2\pi}}$ |
| Exponential($\lambda$) | $-\lambda$ | $x$ | $-\log(-\eta)$ | $1$ |
| Gamma($\alpha, \beta$) | $(-\beta, \alpha-1)$ | $(x, \log x)$ | $\log\Gamma(\eta_2+1) - (\eta_2+1)\log(-\eta_1)$ | $1/x$ |

### Key Patterns

- **Bernoulli/Poisson:** Single-parameter, $T(x) = x$, $A(\eta)$ gives variance
- **Normal (known variance):** Natural parameter = mean, variance determined by $A''(\eta) = 1$
- **Normal (unknown variance):** Two-parameter, $T(x) = (x, x^2)$ captures both moments
- **Gamma:** $T(x) = (x, \log x)$ captures both the mean and the shape

## Sufficiency

The **sufficient statistic** $T(X)$ captures all information about $\theta$ in the data. By the Neyman-Fisher factorization theorem, $T(X)$ is sufficient iff the likelihood factors as:
$$f(x \mid \theta) = g(T(x), \theta) \cdot h(x)$$

In the exponential family, $T(x)$ is **minimally sufficient** (under mild conditions) — no further reduction is possible without losing information.

## Conjugate Priors

When the likelihood is in the exponential family, the **natural conjugate prior** has the form:
$$\pi(\eta \mid \tau, \nu) \propto \exp\{\tau^\top \eta - \nu A(\eta)\}$$

### Posterior

$$\pi(\eta \mid x) \propto \exp\{(\tau + T(x))^\top \eta - (\nu + 1) A(\eta)\}$$

The prior parameters $(\tau, \nu)$ act as **pseudo-data**: $\tau$ is the sum of sufficient statistics from prior data, and $\nu$ is the prior sample size.

### Examples

| Likelihood | Conjugate Prior | Posterior Parameters |
|-----------|----------------|---------------------|
| Bernoulli | Beta$(\alpha, \beta)$ | $(\alpha + x, \beta + n - x)$ |
| Poisson | Gamma$(\alpha, \beta)$ | $(\alpha + \sum x, \beta + n)$ |
| Normal (known $\sigma^2$) | Normal$(\mu_0, \tau^2)$ | $(\frac{\mu_0/\tau^2 + n\bar{x}/\sigma^2}{1/\tau^2 + n/\sigma^2}, \frac{1}{1/\tau^2 + n/\sigma^2})$ |
| Multinomial | Dirichlet$(\alpha_1, \dots, \alpha_k)$ | $(\alpha_i + n_i)$ |

## Generalized Linear Models (GLMs)

GLMs extend linear regression to exponential family distributions with:

1. **Random component:** $Y \sim \text{ExpFamily}(\mu)$
2. **Systematic component:** $\eta = X\beta$
3. **Link function:** $g(\mu) = \eta$, where $g$ connects the mean to the linear predictor

The **canonical link** $g(\mu) = \eta$ (where $\eta$ is the natural parameter) gives $g(\mu) = \theta$ and simplifies MLE.

| Distribution | Canonical Link | Mean Function |
|-------------|----------------|---------------|
| Normal | Identity: $\mu = \eta$ | $\mu = \eta$ |
| Bernoulli | Logit: $\log\frac{\mu}{1-\mu} = \eta$ | $\mu = \sigma(\eta)$ |
| Poisson | Log: $\log\mu = \eta$ | $\mu = e^\eta$ |
| Gamma | Inverse: $1/\mu = \eta$ | $\mu = 1/\eta$ |

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

class ExponentialFamily:
    """Base class for exponential family distributions."""

    def log_partition(self, eta):
        """Log-partition function A(eta)."""
        raise NotImplementedError

    def sufficient_statistic(self, x):
        """Sufficient statistic T(x)."""
        raise NotImplementedError

    def mean(self, eta):
        """E[T(X)] = grad A(eta)."""
        raise NotImplementedError

    def fisher_info(self, eta):
        """Cov[T(X)] = Hessian A(eta)."""
        raise NotImplementedError

class BernoulliFamily(ExponentialFamily):
    def log_partition(self, eta):
        return np.log(1 + np.exp(eta))

    def sufficient_statistic(self, x):
        return x

    def mean(self, eta):
        return 1 / (1 + np.exp(-eta))  # sigmoid

    def fisher_info(self, eta):
        mu = self.mean(eta)
        return mu * (1 - mu)

# Verify moment properties
family = BernoulliFamily()
etas = np.linspace(-5, 5, 100)
mu = family.mean(etas)
var = family.fisher_info(etas)

# Check: dA/deta = mu
dA = np.gradient([family.log_partition(e) for e in etas], etas)
plt.figure(figsize=(10, 4))
plt.plot(etas, mu, label='σ(η) = E[T]')
plt.plot(etas, dA, '--', label='dA/dη')
plt.legend()
plt.title("Exponential Family Identity: E[T(X)] = ∇A(η)")
plt.show()

# MLE via moment matching
data = np.random.binomial(1, 0.3, size=1000)
T_bar = np.mean(data)

def objective(eta):
    return (family.mean(eta) - T_bar)**2

from scipy.optimize import minimize_scalar
result = minimize_scalar(objective, bounds=(-10, 10))
eta_hat = result.x
p_hat = family.mean(eta_hat)
print(f"MLE: p = {p_hat:.4f} (empirical mean = {T_bar:.4f})")

# Natural parameters
logit_p = np.log(p_hat / (1 - p_hat))
print(f"Natural parameter η = {eta_hat:.4f} = logit(p) = {logit_p:.4f}")
```

## Visualization

Plot the log-partition function $A(\eta)$ and its first and second derivatives for the Bernoulli family. $A(\eta)$ is convex. The first derivative gives the mean $\mu = \sigma(\eta)$. The second derivative gives the variance $\mu(1-\mu)$. Show the "sigmoid" shape: as $\eta \to -\infty$, $A \to 0$ and $\mu \to 0$; as $\eta \to \infty$, $A \to \infty$ linearly and $\mu \to 1$.

## Practical Considerations

- **Undefined for some parameters:** Not all $\eta$ values correspond to valid distributions. The **natural parameter space** $\{\eta: A(\eta) < \infty\}$ must be respected.
- **Overparameterization:** In the two-parameter Normal family, the natural parameters $(\mu/\sigma^2, -1/(2\sigma^2))$ must satisfy $\eta_2 < 0$ (since $\sigma^2 > 0$).
- **Curved exponential families:** When $\dim(\eta) > \dim(\theta)$, the distribution is a curved exponential family (e.g., Normal with $\mu = \sigma^2$).
- **Computational advantages:** Exponential families have convex likelihoods, simple MLE via moment matching, and tractable posteriors with conjugate priors.

## References

- Barndorff-Nielsen, O. (1978). *Information and Exponential Families in Statistical Theory*
- McCullagh, P. & Nelder, J. A. (1989). *Generalized Linear Models*
- Efron, B. (1978). "The geometry of exponential families"
