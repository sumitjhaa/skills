# 04.08 Information Geometry and Statistical Manifolds

## Motivation
Information geometry studies statistical models as Riemannian manifolds. By equipping the parameter space with the Fisher information metric, we obtain geometric tools — geodesics, curvatures, natural gradients — that yield efficient, parameterisation-invariant learning algorithms. This perspective unifies natural gradient descent, mirror descent, expectation propagation, and variational inference under a common geometric framework.

## Learning Objectives
- Understand statistical models as differentiable manifolds with the Fisher information metric.
- Derive the natural gradient and explain its invariance to reparameterisation.
- Contrast $e$-geodesics and $m$-geodesics in exponential families.
- Apply information geometry to natural gradient descent, variational inference, and continual learning.

## Math Foundation

### Statistical Manifolds
A statistical manifold is a family of probability distributions $\{p_\theta : \theta \in \Theta \subseteq \mathbb{R}^d\}$ that forms a $d$-dimensional differentiable manifold. The parameter $\theta$ serves as a coordinate system. The same distribution family can be parameterised in multiple ways (e.g., natural vs. expectation parameters for exponential families), and different choices correspond to different coordinate charts.

### Fisher Information Metric
The Fisher information matrix defines a Riemannian metric $g$ on the statistical manifold:

$$g_{ij}(\theta) = \mathbb{E}_{p_\theta} \left[ \frac{\partial \log p_\theta}{\partial \theta^i} \frac{\partial \log p_\theta}{\partial \theta^j} \right]$$

The squared length of an infinitesimal displacement $d\theta$ is:

$$ds^2 = \sum_{i,j} g_{ij}(\theta) d\theta^i d\theta^j = D_{\text{KL}}(p_\theta \| p_{\theta+d\theta})$$

Thus the Fisher metric is the local approximation of KL divergence: the distance between two nearby distributions equals (twice) their KL divergence.

### Exponential Families as Dually Flat Spaces
An exponential family has the form:

$$p_\theta(x) = \exp\left( \sum_{i=1}^d \theta^i T_i(x) - \psi(\theta) \right) h(x)$$

where $\theta$ are natural parameters, $T_i(x)$ are sufficient statistics, and $\psi$ is the log-partition function.

The expectation parameters $\eta_i = \mathbb{E}_\theta[T_i(X)] = \nabla_i \psi(\theta)$ form a dual coordinate system. The exponential family is **$e$-flat** in the $\theta$ coordinates (geodesics are linear in $\theta$) and **$m$-flat** in the $\eta$ coordinates. This duality is the foundation of $e$-projection and $m$-projection algorithms.

### Dual Connections
In standard Riemannian geometry, the Levi-Civita connection is the unique torsion-free connection compatible with the metric. Information geometry introduces two additional connections — the $e$-connection (exponential) and $m$-connection (mixture) — which are dual to each other:

$$\nabla^e g = \nabla^m g = 0 \quad \text{(metric compatibility)}$$

For an exponential family:
- $e$-geodesics: $\theta(t) = (1-t)\theta_0 + t\theta_1$ (linear in natural parameters)
- $m$-geodesics: $\eta(t) = (1-t)\eta_0 + t\eta_1$ (linear in expectation parameters)

The $e$- and $m$-curvatures are zero for exponential families, making them **dually flat spaces**.

## Natural Gradient Descent

### Motivation
Standard gradient descent $\theta_{t+1} = \theta_t - \eta \nabla L(\theta_t)$ depends on the parameterisation: reparameterising the model changes the descent direction. The natural gradient corrects this by accounting for the geometry of the parameter space:

$$\tilde{\nabla} L(\theta) = \mathcal{I}(\theta)^{-1} \nabla L(\theta)$$

The natural gradient is the steepest descent direction in the KL-divergence geometry: at each step, it minimises $L(\theta)$ subject to a small KL constraint $D_{\text{KL}}(p_{\theta_t} \| p_{\theta}) \le \epsilon$.

### Natural Gradient Update

$$\theta_{t+1} = \theta_t - \eta_t \mathcal{I}(\theta)^{-1} \nabla L(\theta_t)$$

### Invariance
If $\phi = \phi(\theta)$ is a diffeomorphic reparameterisation, the natural gradient transforms as:

$$\tilde{\nabla}_\phi L = (J^\top)^{-1} \tilde{\nabla}_\theta L$$

where $J = \partial \phi / \partial \theta$, ensuring the update direction is independent of the parameterisation. Standard gradient descent does not satisfy this property.

### Properties
- Second-order-like convergence without computing the Hessian.
- Effective near saddle points where gradients are small in some directions but not others.
- $\mathcal{I}(\theta)^{-1} \nabla L$ approximates the Newton direction $-(\nabla^2 L)^{-1} \nabla L$ for exponential families (since $\mathcal{I}(\theta) = -\mathbb{E}[\nabla^2 \log p]$, and the loss is typically $\log p$).

## Python Implementation

```python
import numpy as np
from scipy.optimize import approx_fprime

def natural_gradient_step(theta, loss_grad_fn, fisher_fn, lr=0.1):
    """Single natural gradient descent step."""
    grad = loss_grad_fn(theta)
    F = fisher_fn(theta)
    natural_grad = np.linalg.solve(F, grad)
    return theta - lr * natural_grad

def fisher_logistic(theta, X):
    """Fisher information for logistic regression."""
    p = 1.0 / (1.0 + np.exp(-X @ theta))
    W = np.diag(p * (1 - p))
    return X.T @ W @ X  # (d, d)

def logistic_loss_grad(theta, X, y):
    """Gradient of logistic loss."""
    p = 1.0 / (1.0 + np.exp(-X @ theta))
    return X.T @ (p - y)  # for binary cross-entropy

# Example: logistic regression on synthetic data
np.random.seed(42)
n, d = 1000, 5
X = np.random.randn(n, d)
theta_true = np.random.randn(d)
y = 1.0 / (1.0 + np.exp(-X @ theta_true)) > 0.5

theta_sgd = np.zeros(d)
theta_ng = np.zeros(d)
lr = 0.5

for t in range(50):
    grad_sgd = logistic_loss_grad(theta_sgd, X, y)
    theta_sgd -= lr * grad_sgd
    
    grad_ng = logistic_loss_grad(theta_ng, X, y)
    F = fisher_logistic(theta_ng, X)
    theta_ng -= lr * np.linalg.solve(F + 1e-4 * np.eye(d), grad_ng)

print(f"SGD final loss: {np.sum(np.log(1+np.exp(-y * (X @ theta_sgd)))):.2f}")
print(f"Natural GD final loss: {np.sum(np.log(1+np.exp(-y * (X @ theta_ng)))):.2f}")
```

## Visualization
Plot the optimisation trajectories of SGD vs natural gradient on a 2D logistic regression loss landscape (contour plot). The natural gradient path is straighter (fewer oscillations) and reaches the optimum faster. A second panel shows the Riemannian distance $D_{\text{KL}}$ along the natural gradient path vs. Euclidean distance along SGD — the natural gradient moves a constant KL divergence per step.

## Applications

### Variational Inference
In variational inference, we minimise $D_{\text{KL}}(q_\phi \| p)$ over an approximating family $q_\phi$. The natural gradient of the ELBO w.r.t. $\phi$ is:

$$\tilde{\nabla}_\phi \text{ELBO} = \mathcal{I}(\phi)^{-1} \nabla_\phi \text{ELBO}$$

For mean-field Gaussians (diagonal covariance), the Fisher information is block-diagonal, making the natural gradient update particularly simple. The natural gradient for the mean is just the gradient w.r.t. the mean, and for the covariance it rescales by the inverse covariance. This leads to faster convergence than standard gradient VI.

### Expectation Propagation
Expectation propagation (EP) $m$-projects the posterior onto a tractable approximating family. In information geometric terms, EP iteratively matches moments (expectation parameters) of the approximation with the tilted distribution. Each EP update is an $m$-projection onto the approximating family.

### Continual Learning
Elastic Weight Consolidation (EWC) uses the Fisher information diagonal as a measure of parameter importance:

$$\mathcal{L}(\theta) = \mathcal{L}_{\text{new}}(\theta) + \sum_i \frac{\lambda}{2} \mathcal{I}_i (\theta_i - \theta^*_i)^2$$

This is justified information-geometrically: the Fisher diagonal locally approximates the KL divergence between the old and new posterior. Moving far in parameters with high Fisher information incurs a large KL penalty, protecting previously learned knowledge.

### Mirror Descent
Mirror descent generalises gradient descent by choosing a Bregman divergence $B_\psi$ instead of the Euclidean distance:

$$\theta_{t+1} = \arg\min_\theta \langle \nabla L(\theta_t), \theta - \theta_t \rangle + \frac{1}{\eta} B_\psi(\theta, \theta_t)$$

For $\psi(\theta) = \log Z(\theta)$ (the log-partition function of an exponential family), $B_\psi$ is the KL divergence, and mirror descent is equivalent to natural gradient descent. Other choices of $\psi$ (e.g., negative entropy) yield algorithms like exponentiated gradient.

## Practical Considerations

### Computational Cost
- Computing the full $d \times d$ Fisher matrix is $O(d^2)$ storage and $O(d^3)$ inversion.
- **K-FAC (Kronecker-Factored Approximate Curvature)**: approximates $\mathcal{F}$ as a block-diagonal matrix where each block is a Kronecker product of two smaller matrices, reducing cost to $O(d^{1.5})$.
- **Diagonal approximation**: $\mathcal{I}(\theta) \approx \text{diag}(\mathbb{E}[(\partial_i \log p)^2])$ — cheap but loses off-diagonal information about parameter interactions.

### When to Use Natural Gradient
- **Well-conditioned**: natural gradient excels when the loss has highly elliptical contours (common in deep networks).
- **Small data**: with few samples, the Fisher can be ill-conditioned; damping (adding $\lambda I$) is necessary.
- **Large neural networks**: full natural gradient is infeasible, but K-FAC and Shampoo (which tracks a preconditioner) are practical approximations.

### Relationship to Adam
Adam can be viewed as a diagonal approximation to natural gradient with an EMA of squared gradients replacing the Fisher diagonal. RMSProp and Adam are not invariant to reparameterisation but work well in practice due to their adaptive per-parameter learning rates.

## References
- Amari, *Information Geometry and Its Applications*, Springer 2016
- Amari, "Natural Gradient Works Efficiently in Learning," *Neural Computation*, 1998
- Martens, "New Insights and Perspectives on the Natural Gradient Method," *arXiv:1412.1193*, 2014
- Hoffman et al., "Stochastic Variational Inference," *JMLR*, 2013
- Kirkpatrick et al., "Overcoming catastrophic forgetting in neural networks," *PNAS*, 2017
