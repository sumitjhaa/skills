# 04.09 Reproducing Kernel Hilbert Spaces

## Motivation
RKHS theory lifts data into infinite-dimensional feature spaces where linear methods solve nonlinear problems. It is the mathematical foundation of kernel methods (SVMs, kernel PCA), Gaussian processes, kernel mean embeddings, and the neural tangent kernel that explains the generalisation behaviour of wide neural networks.

## Learning Objectives
- Define a reproducing kernel Hilbert space and the reproducing property.
- State and apply the Moore–Aronszajn and representer theorems.
- Derive the kernel trick and apply it to SVM, GP regression, and MMD.
- Understand the neural tangent kernel as the infinite-width limit of a neural network.

## Math Foundation

### Reproducing Kernel Hilbert Space
A Hilbert space $\mathcal{H}$ of functions $f: \mathcal{X} \to \mathbb{R}$ is an RKHS if the evaluation functional $\delta_x: f \mapsto f(x)$ is continuous (equivalently, bounded) for every $x \in \mathcal{X}$. By the Riesz representation theorem, for each $x$ there exists a function $k_x \in \mathcal{H}$ such that:

$$f(x) = \langle f, k_x \rangle_{\mathcal{H}} \quad \forall f \in \mathcal{H}$$

The **reproducing kernel** is $k(x,y) = k_x(y) = \langle k_x, k_y \rangle_{\mathcal{H}}$.

### Moore–Aronszajn Theorem
A symmetric function $k: \mathcal{X} \times \mathcal{X} \to \mathbb{R}$ is a positive-definite kernel if for any $n$, any $\{x_i\}_{i=1}^n \subseteq \mathcal{X}$, and any $\{c_i\}_{i=1}^n \subseteq \mathbb{R}$:

$$\sum_{i=1}^n \sum_{j=1}^n c_i c_j k(x_i, x_j) \ge 0$$

The Moore–Aronszajn theorem states that for every positive-definite kernel $k$ there exists a unique RKHS $\mathcal{H}_k$ with $k$ as its reproducing kernel. Conversely, every RKHS has a unique reproducing kernel that is positive-definite.

### Mercer's Theorem
For a compact $\mathcal{X}$ and continuous kernel $k$, there exists an orthonormal basis $\{e_i\}_{i=1}^\infty$ of $L^2(\mathcal{X})$ and non-negative eigenvalues $\{\lambda_i\}_{i=1}^\infty$ such that:

$$k(x,y) = \sum_{i=1}^\infty \lambda_i e_i(x) e_i(y)$$

The RKHS then consists of functions $f(x) = \sum_i a_i \sqrt{\lambda_i} e_i(x)$ with $\|f\|_{\mathcal{H}}^2 = \sum_i a_i^2 < \infty$.

### Common Kernels
| Kernel | Formula | Key Property |
|--------|---------|-------------|
| Linear | $k(x,y) = x^\top y$ | Reproduces inner product |
| Polynomial | $k(x,y) = (x^\top y + c)^d$ | Finite-dimensional feature space |
| RBF/Gaussian | $k(x,y) = \exp(-\|x-y\|^2 / 2\sigma^2)$ | Universal approximator |
| Matérn | $k(r) = \frac{2^{1-\nu}}{\Gamma(\nu)} \left(\frac{\sqrt{2\nu}r}{\rho}\right)^\nu K_\nu\left(\frac{\sqrt{2\nu}r}{\rho}\right)$ | Controls smoothness |
| Laplace | $k(x,y) = \exp(-\|x-y\|/\sigma)$ | Less smooth than RBF |

### Representer Theorem
For any loss function $\ell$ that is increasing in $\|f\|$ and depends on $f$ only through its evaluations at the training points $\{x_i\}$, the minimiser of:

$$\frac{1}{n} \sum_{i=1}^n \ell(y_i, f(x_i)) + \lambda \|f\|_{\mathcal{H}}^2$$

has the form $f(x) = \sum_{i=1}^n \alpha_i k(x_i, x)$ for some coefficients $\alpha_i \in \mathbb{R}^n$. This reduces an infinite-dimensional optimisation to a finite-dimensional one.

## Python Implementation

```python
import numpy as np
from scipy.linalg import cholesky, solve_triangular

def rbf_kernel(X, Y=None, sigma=1.0):
    """RBF (Gaussian) kernel matrix between X and Y."""
    if Y is None:
        Y = X
    sq_dists = np.sum(X**2, axis=1)[:, None] + np.sum(Y**2, axis=1)[None, :] - 2 * X @ Y.T
    return np.exp(-sq_dists / (2 * sigma**2))

def kernel_ridge_regression(X_train, y_train, X_test, kernel_fn, lam=1.0):
    """Kernel ridge regression (dual form)."""
    K = kernel_fn(X_train)
    n = len(X_train)
    alpha = np.linalg.solve(K + lam * n * np.eye(n), y_train)
    K_s = kernel_fn(X_test, X_train)
    return K_s @ alpha

def kernel_pca(X, kernel_fn, n_components=2):
    """Kernel PCA via eigendecomposition of the kernel matrix."""
    K = kernel_fn(X)
    n = len(K)
    # centre in feature space
    one_n = np.ones((n, n)) / n
    K_centered = K - one_n @ K - K @ one_n + one_n @ K @ one_n
    eigvals, eigvecs = np.linalg.eigh(K_centered)
    idx = np.argsort(eigvals)[::-1]
    eigvecs = eigvecs[:, idx] * np.sqrt(np.maximum(eigvals[idx], 0))
    return eigvecs[:, :n_components]

# Example: 1D regression with RBF kernel
np.random.seed(42)
X_train = np.random.uniform(-3, 3, 20)[:, None]
y_train = np.sin(X_train[:, 0]) + 0.1 * np.random.randn(20)
X_test = np.linspace(-3, 3, 100)[:, None]

y_pred = kernel_ridge_regression(X_train, y_train, X_test, 
                                  lambda X, Y=None: rbf_kernel(X, Y, sigma=1.0), lam=0.01)
print(f"Predictions at x=0: {y_pred[49]:.3f} (true: {np.sin(0):.3f})")
```

## Visualization
Plot the kernel ridge regression fit with uncertainty bands (using GP formulation) — the fit smoothly interpolates noisy observations. A second panel shows the kernel PCA embedding of 2D Swiss roll data, with the first two kernel principal components unrolling the manifold.

## Connections to Machine Learning

### Support Vector Machines
The SVM dual objective depends only on kernel evaluations:

$$\max_\alpha \sum_i \alpha_i - \frac12 \sum_{i,j} \alpha_i \alpha_j y_i y_j k(x_i, x_j)$$

The decision function is $f(x) = \sum_i \alpha_i y_i k(x_i, x) + b$. The kernel trick enables nonlinear classification at the cost of a linear SVM in feature space.

### Gaussian Processes
A GP with covariance function $k$ is a distribution over functions where any finite set of evaluations is jointly Gaussian:

$$p(f|X) = \mathcal{N}(0, K_{XX})$$

GP regression predicts $f_*$ at test points $X_*$ using the conditional Gaussian:

$$\mathbb{E}[f_* | X, y, X_*] = K_{*X} (K_{XX} + \sigma^2 I)^{-1} y$$

This is equivalent to kernel ridge regression but also provides uncertainty estimates $\text{Var}[f_*] = K_{**} - K_{*X}(K_{XX} + \sigma^2 I)^{-1} K_{X*}$.

### Kernel Mean Embeddings
The mean embedding of a distribution $P$ in the RKHS is:

$$\mu_P = \mathbb{E}_{x \sim P}[k(\cdot, x)]$$

The Maximum Mean Discrepancy (MMD) between $P$ and $Q$ is:

$$\text{MMD}^2(P,Q) = \|\mu_P - \mu_Q\|_{\mathcal{H}}^2 = \mathbb{E}[k(x,x')] + \mathbb{E}[k(y,y')] - 2\mathbb{E}[k(x,y)]$$

MMD provides a two-sample test and is used in generative model evaluation and domain adaptation.

### Neural Tangent Kernel (NTK)
For an infinitely wide neural network $f(\theta, x)$ trained by gradient flow with MSE loss, the network function evolves according to the kernel gradient flow:

$$\partial_t f_t(x) = -\sum_{i=1}^n \Theta(x, x_i) (f_t(x_i) - y_i)$$

where $\Theta(x, x') = \nabla_\theta f(\theta, x)^\top \nabla_\theta f(\theta, x')$ is the NTK. In the infinite-width limit, the NTK converges to a deterministic kernel, explaining why wide networks behave like kernel methods.

## Practical Considerations

### Scaling Kernels to Large Datasets
- Standard kernel methods are $O(n^3)$ in training and $O(n)$ per test point.
- **Random Fourier features**: approximate $k(x,y) \approx \frac{1}{m} \sum_{j=1}^m \cos(w_j^\top (x-y))$ with $w_j \sim \mathcal{N}(0, \sigma^{-2} I)$, reducing to $O(nm^2 + m^3)$.
- **Nyström approximation**: sample $m \ll n$ landmark points and approximate $K \approx K_{nm} K_{mm}^{-1} K_{mn}$.
- **Inducing points** (in GPs): replace $n$ training points with $m$ pseudo-inputs, reducing cost to $O(nm^2)$.

### Choosing the Kernel
- RBF is the default for most applications — it is universal (can approximate any continuous function on a compact set).
- Matérn kernels offer controlled smoothness via $\nu$: $\nu = 1/2$ (Laplace, non-differentiable), $\nu = 3/2$ (once differentiable), $\nu = 5/2$ (twice differentiable), $\nu = \infty$ (RBF, infinitely differentiable).
- For non-stationary data, consider the arc-cosine kernel (equivalent to an infinite ReLU network) or deep kernels learned by optimising the kernel parameters.

### Negative Results
- Fixed kernels can fail when the data manifold is low-dimensional or has complex structure.
- Deep learning often outperforms kernel methods on large-scale raw data (images, audio) because learned representations are more efficient than generic kernels.
- Kernel methods are sensitive to hyperparameters (lengthscale $\sigma$, regularisation $\lambda$), which must be carefully tuned via cross-validation or marginal likelihood maximisation.

## References
- Schölkopf & Smola, *Learning with Kernels*, MIT Press 2002
- Rasmussen & Williams, *Gaussian Processes for Machine Learning*, MIT Press 2006
- Jacot, Gabriel, Hongler, "Neural Tangent Kernel: Convergence and Generalization in Neural Networks," *NeurIPS 2018*
- Rahimi & Recht, "Random Features for Large-Scale Kernel Machines," *NeurIPS 2007*
- Gretton et al., "A Kernel Two-Sample Test," *JMLR*, 2012
