# 04.03 Maximum Entropy Principle

## Motivation
Given partial knowledge about a distribution (e.g., its mean and variance), there are infinitely many distributions consistent with those constraints. The maximum entropy principle selects the distribution that is maximally uncertain — i.e., makes the fewest unwarranted assumptions — subject to the known constraints. This principle unifies statistical mechanics, Bayesian inference, and several key machine learning models.

## Learning Objectives
- State and prove the maximum entropy distribution for given moment constraints.
- Derive the exponential family form from the maximum entropy principle.
- Apply max entropy to classification (MaxEnt classifiers), spectral estimation, and feature learning.
- Understand the duality between maximum entropy and maximum likelihood in exponential families.

## Math Foundation

### Entropy as a Measure of Uncertainty
For a discrete distribution $p$ over $\mathcal{X}$, the Shannon entropy is:

$$H(p) = -\sum_{x \in \mathcal{X}} p(x) \log p(x)$$

The maximum entropy principle seeks $p^*$ that maximizes $H(p)$ subject to moment constraints $\mathbb{E}_p[f_i(X)] = \mu_i$ for $i=1,\dots,m$.

### Constrained Optimization via Lagrange Multipliers
The Lagrangian is:

$$\mathcal{L}(p, \lambda, \lambda_0) = -\sum_x p(x) \log p(x) + \sum_{i=1}^m \lambda_i \left( \mathbb{E}_p[f_i(X)] - \mu_i \right) + \lambda_0 \left( \sum_x p(x) - 1 \right)$$

Taking the derivative w.r.t. $p(x)$ and setting to zero:

$$-\log p(x) - 1 + \sum_i \lambda_i f_i(x) + \lambda_0 = 0$$

Solving for $p(x)$ gives:

$$p^*(x) = \frac{1}{Z(\lambda)} \exp\left( \sum_{i=1}^m \lambda_i f_i(x) \right)$$

where $Z(\lambda) = \sum_x \exp(\sum_i \lambda_i f_i(x))$ is the partition function.

This is the **exponential family** form. The Lagrange multipliers $\lambda_i$ must satisfy $\mathbb{E}_{p^*}[f_i] = \mu_i$.

## Classical Maximum Entropy Distributions

### Uniform Distribution (No Constraints)
With only the normalization constraint, the solution is:

$$p^*(x) = \frac{1}{|\mathcal{X}|}$$

This is the principle of indifference — without any information, assign equal probability to all outcomes.

### Exponential Distribution (Non-negative Support, Fixed Mean)
For $X \in [0, \infty)$ with $\mathbb{E}[X] = \mu$, the maximum entropy distribution is the exponential:

$$p^*(x) = \frac{1}{\mu} e^{-x/\mu}$$

This is the memoryless distribution, reflecting that knowing the mean alone tells us nothing about higher moments.

### Gaussian Distribution (Real Line, Fixed Mean and Variance)
For $X \in \mathbb{R}$ with $\mathbb{E}[X] = \mu$ and $\text{Var}(X) = \sigma^2$, the maximum entropy distribution is Gaussian:

$$p^*(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left( -\frac{(x-\mu)^2}{2\sigma^2} \right)**

The Gaussian is the most uncertain distribution with known first and second moments. This provides a fundamental justification for the central role of the Gaussian in statistics and signal processing.

### Other Examples
- **Poisson**: integer support, fixed mean; max entropy among distributions with fixed $\mathbb{E}[X]$.
- **Boltzmann/Gibbs**: finite state space, fixed expected energy; foundational for statistical mechanics.
- **Von Mises**: circle, fixed first circular moment; max entropy on the circle.

## Dual Relationship with Maximum Likelihood

Given observed data $\{x_1,\dots,x_n\}$, the maximum likelihood estimate of the exponential family parameters $\lambda$ maximizes:

$$\ell(\lambda) = \frac{1}{n} \sum_{j=1}^n \log p_\lambda(x_j) = \frac{1}{n} \sum_{j=1}^n \left( \sum_i \lambda_i f_i(x_j) \right) - \log Z(\lambda)$$

The gradient of $\ell$ w.r.t. $\lambda_i$ is $\mu_i^{\text{empirical}} - \mathbb{E}_{p_\lambda}[f_i]$. At the optimum, the model moments match the empirical moments — exactly the max entropy condition. Therefore **maximum likelihood in an exponential family is dual to maximum entropy**: the ML estimate is the distribution in the family whose moments match the data.

## Python Implementation

```python
import numpy as np
from scipy.optimize import minimize
from scipy.special import softmax

def max_entropy_discrete(features, target_moments, support):
    """Find max entropy distribution over discrete support.
    
    Args:
        features: array of shape (n_support, m) — each row is f_i(x)
        target_moments: array of shape (m,) — target expected values
        support: array of shape (n_support,) — the support values
        
    Returns:
        p: max entropy distribution over support
    """
    m = features.shape[1]
    
    def neg_dual(lamb):
        """Negative of the dual objective: log Z - lambda^T mu"""
        logits = features @ lamb
        Z = np.sum(np.exp(logits))
        log_Z = np.log(Z)
        return -(log_Z - np.dot(lamb, target_moments))
    
    def grad_dual(lamb):
        logits = features @ lamb
        p = softmax(logits)
        moments = features.T @ p
        return -(moments - target_moments)
    
    result = minimize(neg_dual, np.zeros(m), jac=grad_dual, method='BFGS')
    lamb_opt = result.x
    p_opt = softmax(features @ lamb_opt)
    return p_opt, lamb_opt

# Example: find distribution with mean = 1.5 and second moment = 3.0
# over support {0, 1, 2, 3, 4, 5}
support = np.arange(6)
features = np.column_stack([support, support**2])  # f1(x)=x, f2(x)=x^2
targets = np.array([1.5, 3.0])
p_opt, _ = max_entropy_discrete(features, targets, support)
print("Max entropy distribution:")
for x, prob in zip(support, p_opt):
    print(f"  p({x}) = {prob:.4f}")
print(f"  Mean = {np.sum(support * p_opt):.3f} (target: 1.5)")
print(f"  E[X^2] = {np.sum(support**2 * p_opt):.3f} (target: 3.0)")
```

## Visualization
Plot the maximum entropy distribution from the example as a bar chart overlaid with the data moments (vertical lines). On a second panel, trace the convergence of the dual objective $\log Z - \lambda^T \mu$ across BFGS iterations. For the Gaussian case, show a family of distributions with the same mean but different second moments — the Gaussian is the flattest (highest entropy).

## Practical Considerations

### Max Entropy Models in ML
- **MaxEnt classifiers**: $p(y|x) \propto \exp(\sum_i \lambda_i f_i(x,y))$ — a multinomial logistic regression model explicitly derived from the max entropy principle. Training maximizes log-likelihood, which is dual to min entropy.
- **Conditional Random Fields (CRFs)**: sequence-level max entropy models where the features $f_i(x, y_t, y_{t-1})$ depend on neighboring labels.
- **Spectral density estimation**: given autocorrelation coefficients, the max entropy spectrum (Burg's method) produces the flattest spectrum consistent with the data, avoiding spurious peaks.

### Numerical Issues
- The partition function $Z(\lambda)$ may overflow for large $|\lambda|$. Use the log-sum-exp trick: $\log Z = \max_j s_j + \log \sum_j \exp(s_j - \max_k s_k)$ where $s_j = \sum_i \lambda_i f_i(x_j)$.
- For continuous spaces, the optimization over $p$ is infinite-dimensional. Practical algorithms (e.g., the information bottleneck method) discretize or use parametric forms.
- Moment matching can be ill-posed if the target moments are infeasible (e.g., a variance target that violates the Cramér-Rao bound for the given support).

### When Not to Use Max Entropy
The max entropy principle gives the most uncertain distribution consistent with constraints. If prior knowledge beyond moments is available (e.g., sparsity, smoothness, a Bayesian prior), the prior should be incorporated through relative entropy minimization (the principle of minimum discrimination information, a.k.a. the Bayes-Laplace rule).

## Connections to ML

### Maximum Entropy and Regularization
The max entropy solution $p \propto \exp(\lambda^T f(x))$ can be unstable when the number of features exceeds the sample size. Adding an $\ell_2$ penalty on $\lambda$ is equivalent to performing maximum a posteriori (MAP) estimation under a Gaussian prior; this is also the maximum entropy under an additional constraint on $\|\lambda\|^2$.

### Information Bottleneck
The information bottleneck method finds a representation $Z$ of $X$ that preserves information about $Y$:

$$\min_{p(z|x)} I(X;Z) - \beta I(Z;Y)$$

This can be viewed as a constrained maximum entropy problem: maximize $H(Z)$ subject to constraints on $I(X;Z)$ and $I(Z;Y)$. The self-consistent equations yield the Blahut-Arimoto algorithm.

### Energy-Based Models
Energy-based models $p(x) = \exp(-E(x))/Z$ are maximum entropy distributions when the constraints are feature expectations $\mathbb{E}[f_i(X)]$. The energy function $E(x) = -\sum \lambda_i f_i(x)$ is learned by contrastive divergence or score matching.

## References
- Jaynes, "Information Theory and Statistical Mechanics," *Physical Review*, 1957
- Berger, "The Maximum Entropy Principle," *Encyclopedia of Statistical Sciences*, 1986
- Cover & Thomas, *Elements of Information Theory*, 2nd ed.
- Dudík, Schapire, "Maximum Entropy Distribution and Maximum Likelihood in Exponential Families," *Encyclopedia of Machine Learning*, 2010
