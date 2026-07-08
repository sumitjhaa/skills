# 04.04 Fisher Information and the Cramér–Rao Bound

## Motivation
Fisher information quantifies the amount of information a random variable carries about an unknown parameter. It defines a Riemannian metric on statistical manifolds and gives a fundamental lower bound on estimator variance. In machine learning, Fisher information appears in natural gradient descent, the Laplace approximation for Bayesian neural networks, and continual learning methods like Elastic Weight Consolidation.

## Learning Objectives
- Define the score function and Fisher information matrix.
- State, prove, and interpret the Cramér–Rao lower bound.
- Derive the natural gradient update and understand its invariance properties.
- Apply Fisher information to active learning, Bayesian inference, and optimisation.

## Math Foundation

### Score Function
For a parametric model $p(x|\theta)$, the score function is the gradient of the log-likelihood:

$$s(\theta) = \nabla_\theta \log p(x|\theta)$$

Under regularity conditions (differentiability under the integral, interchange of integration and differentiation), the score has zero mean:

$$\mathbb{E}_{p(x|\theta)}[s(\theta)] = \int \frac{\nabla_\theta p(x|\theta)}{p(x|\theta)} p(x|\theta) dx = \nabla_\theta \int p(x|\theta) dx = \nabla_\theta 1 = 0$$

### Fisher Information Matrix
The Fisher information matrix (FIM) is the covariance of the score:

$$\mathcal{I}(\theta) = \mathbb{E}_{p(x|\theta)}[s(\theta) s(\theta)^\top] = \mathbb{E}_{p(x|\theta)}[(\nabla_\theta \log p)(\nabla_\theta \log p)^\top]$$

Equivalently, under further regularity, the FIM equals the negative expected Hessian of the log-likelihood:

$$\mathcal{I}(\theta) = -\mathbb{E}_{p(x|\theta)}[\nabla^2_\theta \log p(x|\theta)]$$

### Properties
1. **Additivity**: For independent samples $x_1,\dots,x_n$, $\mathcal{I}_n(\theta) = n \mathcal{I}_1(\theta)$.
2. **Reparameterisation**: If $\phi = g(\theta)$, then $\mathcal{I}(\phi) = (J^{-1})^\top \mathcal{I}(\theta) J^{-1}$ where $J = \partial g/\partial \theta$.
3. **Tightness of CRB**: For exponential families, the MLE achieves the Cramér–Rao bound asymptotically.

## Cramér–Rao Lower Bound

### Statement
For any unbiased estimator $\hat{\theta}$ of $\theta$:

$$\text{Var}(\hat{\theta}) \ge \mathcal{I}(\theta)^{-1}$$

where the inequality is in the Loewner order (i.e., $\text{Var}(\hat{\theta}) - \mathcal{I}(\theta)^{-1}$ is positive semidefinite). For scalar $\theta$:

$$\text{Var}(\hat{\theta}) \ge \frac{1}{\mathcal{I}(\theta)}$$

### Proof Sketch
By the Cauchy-Schwarz inequality applied to the score $s(\theta)$ and the estimator $\hat{\theta}$:

$$\text{Cov}(\hat{\theta}, s(\theta))^2 \le \text{Var}(\hat{\theta}) \cdot \text{Var}(s(\theta))$$

Since $\mathbb{E}[s(\theta)] = 0$, and under unbiasedness $\mathbb{E}[\hat{\theta} s(\theta)] = \nabla_\theta \mathbb{E}[\hat{\theta}] = 1$, we get $\text{Cov}(\hat{\theta}, s(\theta)) = 1$, so $1 \le \text{Var}(\hat{\theta}) \cdot \mathcal{I}(\theta)$.

### Efficient Estimators
An estimator is called *efficient* if it achieves the Cramér–Rao bound. For exponential families, the MLE is efficient as $n \to \infty$ (asymptotically efficient). For finite samples, the bound may not be achievable.

## Observed vs Expected Fisher Information

The **observed Fisher information** is the negative Hessian evaluated at the MLE:

$$\mathcal{J}(\hat{\theta}) = -\nabla^2_\theta \log p(D|\theta)\big|_{\theta=\hat{\theta}}$$

The **expected Fisher information** is $n \mathcal{I}_1(\theta)$ evaluated at $\hat{\theta}$. Both are consistent estimators of $n \mathcal{I}_1(\theta^*)$, but the observed version is more robust to model misspecification. In the Laplace approximation, the observed Fisher information is used to approximate the posterior covariance.

## Python Implementation

```python
import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm

def fisher_information_gaussian(mu, sigma2, n=1):
    """Fisher information for Gaussian N(mu, sigma2) with n iid samples."""
    I_mu = n / sigma2
    I_var = n / (2 * sigma2**2)
    return I_mu, I_var

def observed_fisher_logistic(X, y, beta):
    """Observed Fisher info for logistic regression at beta."""
    p = 1.0 / (1.0 + np.exp(-X @ beta))
    W = np.diag(p * (1 - p))
    return X.T @ W @ X  # negative Hessian

def cramer_rao_bound(likelihood, theta0, data, param_idx=0):
    """Estimate CRB via numerical Hessian at MLE."""
    def neg_log_lik(theta):
        return -np.sum(likelihood(data, theta))
    
    result = minimize(neg_log_lik, theta0)
    hess = approx_hessian(result.x, neg_log_lik)
    cramer_rao = np.sqrt(np.linalg.inv(hess)[param_idx, param_idx])
    return result.x, cramer_rao

def approx_hessian(theta, f, eps=1e-5):
    """Numerical approximation of Hessian via finite differences."""
    n = len(theta)
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            theta_pp = theta.copy(); theta_pp[i] += eps; theta_pp[j] += eps
            theta_pm = theta.copy(); theta_pm[i] += eps; theta_pm[j] -= eps
            theta_mp = theta.copy(); theta_mp[i] -= eps; theta_mp[j] += eps
            theta_mm = theta.copy(); theta_mm[i] -= eps; theta_mm[j] -= eps
            H[i,j] = (f(theta_pp) - f(theta_pm) - f(theta_mp) + f(theta_mm)) / (4*eps**2)
    return H

# Example: Gaussian location parameter
np.random.seed(42)
data = np.random.randn(100) + 2.0  # true mu = 2.0
mu_mle = np.mean(data)
I_n = 100 / 1.0  # sigma^2 = 1, n = 100 -> I = 100
crb = 1.0 / I_n
print(f"MLE = {mu_mle:.3f}, CRB = {crb:.4f}, Empirical var = {(1/99):.4f}")
```

## Visualization
Plot the log-likelihood function for a Gaussian location parameter alongside its curvature (second derivative) at the MLE. A second panel shows the score function across $\theta$ for different sample sizes — its variance at the true $\theta$ equals the Fisher information. For the Cramér–Rao bound, show a Monte Carlo histogram of MLE estimates overlayed with the asymptotic Gaussian $\mathcal{N}(\theta^*, \mathcal{I}^{-1})$.

## Practical Considerations

### Fisher Information in Neural Network Optimisation
For a neural network with parameters $\theta$, the empirical Fisher information (expectation under the empirical distribution) is:

$$\mathcal{F}(\theta) = \frac{1}{n} \sum_{i=1}^n \nabla_\theta \log p(y_i|x_i,\theta) \nabla_\theta \log p(y_i|x_i,\theta)^\top$$

Computing the full $d \times d$ Fisher matrix is infeasible for large $d$. Methods like K-FAC (Kronecker-Factored Approximate Curvature) factorise $\mathcal{F}$ into Kronecker products of per-layer matrices, enabling tractable inversion.

### Natural Gradient Descent
The standard gradient $\nabla L$ points in the direction of steepest ascent in Euclidean parameter space. The natural gradient $\tilde{\nabla} L = \mathcal{I}(\theta)^{-1} \nabla L$ points in the direction of steepest ascent in the KL divergence geometry. Natural gradient descent:

$$\theta_{t+1} = \theta_t - \eta_t \mathcal{I}(\theta_t)^{-1} \nabla L(\theta_t)$$

is invariant to reparameterisation and often converges in fewer iterations than standard gradient descent, especially near saddle points.

### Elastic Weight Consolidation (EWC)
For continual learning, EWC adds a quadratic penalty based on Fisher information:

$$\mathcal{L}(\theta) = \mathcal{L}_{\text{new}}(\theta) + \sum_i \frac{\lambda}{2} \mathcal{I}_i (\theta_i - \theta^*_i)^2$$

where $\mathcal{I}_i$ are the diagonal entries of the Fisher information at the previous task's optimum. This protects important parameters from catastrophic forgetting.

### Active Learning with Fisher Information
In Bayesian experimental design, the goal is to select inputs $x$ that maximise the expected information gain about $\theta$:

$$I(\theta; y|x) = \frac12 \log \det\left( \mathcal{I}(\theta) \right)$$

For logistic regression, this corresponds to selecting points near the decision boundary where $p(1-p)$ is largest — i.e., where the model is most uncertain.

## Limitations and Caveats
1. The Cramér–Rao bound applies only to *unbiased* estimators. Biased estimators (e.g., regularised MLE, MAP) can have lower variance, potentially below the CRB.
2. The bound requires regularity conditions (support independent of $\theta$, differentiability, interchange of $\nabla$ and $\int$). Violations occur for uniform distributions $\mathcal{U}[0,\theta]$, where the MLE converges at $O(1/n^2)$ rather than $O(1/\sqrt{n})$.
3. The empirical Fisher (using labels from the model rather than the true data distribution) is not the true Fisher but a Gauss-Newton approximation.

## References
- Lehmann & Casella, *Theory of Point Estimation*, 2nd ed.
- Amari, *Information Geometry and Its Applications*
- Fisher, "On the Mathematical Foundations of Theoretical Statistics," *Philosophical Transactions of the Royal Society A*, 1922
- Martens, "New Insights and Perspectives on the Natural Gradient Method," *arXiv:1412.1193*, 2014
- Kirkpatrick et al., "Overcoming catastrophic forgetting in neural networks," *PNAS*, 2017
