# 04.15 Stochastic Processes: Gaussian Processes, Brownian Motion, Martingales

## Motivation
Stochastic processes model randomness evolving over time or space. They are essential for time-series modelling, Bayesian nonparametrics, finance, and diffusion-based generative models. Gaussian processes provide a flexible framework for regression and optimisation, Brownian motion is the fundamental building block of stochastic calculus, and martingales underpin the theory of fair games and sequential decision-making.

## Learning Objectives
- Define and distinguish Gaussian processes, Brownian motion, and martingales.
- Perform GP regression with closed-form posterior inference.
- Understand the path properties of Brownian motion (non-differentiability, quadratic variation).
- Apply martingale theory to convergence of stochastic algorithms.

## Math Foundation

### Gaussian Processes
A Gaussian process (GP) is a collection of random variables such that any finite subset is jointly Gaussian. It is fully specified by a mean function $m(x)$ and covariance (kernel) function $k(x,x')$:

$$f(x) \sim \mathcal{GP}(m(x), k(x,x'))$$

where $\mathbb{E}[f(x)] = m(x)$ and $\text{Cov}(f(x), f(x')) = k(x,x')$.

### GP Regression
Given noisy observations $y_i = f(x_i) + \epsilon_i$ with $\epsilon_i \sim \mathcal{N}(0, \sigma^2)$, the joint distribution of training outputs $y$ and test outputs $f_*$ is:

$$\begin{bmatrix} y \\ f_* \end{bmatrix} \sim \mathcal{N}\left( \begin{bmatrix} m(X) \\ m(X_*) \end{bmatrix}, \begin{bmatrix} K(X,X) + \sigma^2 I & K(X,X_*) \\ K(X_*,X) & K(X_*,X_*) \end{bmatrix} \right)$$

The predictive posterior is:

$$f_* | X, y, X_* \sim \mathcal{N}(\bar{f}_*, \text{Cov}(f_*))$$

$$\bar{f}_* = m(X_*) + K(X_*, X) [K(X,X) + \sigma^2 I]^{-1} (y - m(X))$$

$$\text{Cov}(f_*) = K(X_*, X_*) - K(X_*, X) [K(X,X) + \sigma^2 I]^{-1} K(X, X_*)$$

### Brownian Motion (Wiener Process)
A Brownian motion $\{W_t\}_{t \ge 0}$ satisfies:
1. $W_0 = 0$ almost surely.
2. Independent increments: $W_t - W_s$ independent of $\mathcal{F}_s$ for $t > s$.
3. Gaussian increments: $W_t - W_s \sim \mathcal{N}(0, t-s)$.
4. Continuous paths: $t \mapsto W_t$ is continuous almost surely.

**Key properties**:
- Quadratic variation: $\langle W \rangle_t = t$.
- Paths are nowhere differentiable almost surely.
- Scaling: $W_{ct} \stackrel{d}{=} \sqrt{c} W_t$.
- Time inversion: $t W_{1/t} \stackrel{d}{=} W_t$.

### Martingales
A stochastic process $\{M_t\}$ adapted to filtration $\{\mathcal{F}_t\}$ is a martingale if:
1. $\mathbb{E}[|M_t|] < \infty$ for all $t$.
2. $\mathbb{E}[M_{t+s} | \mathcal{F}_t] = M_t$ for all $s \ge 0$.

**Examples**:
- Brownian motion $W_t$ is a martingale.
- $W_t^2 - t$ is a martingale.
- $\exp(\theta W_t - \theta^2 t/2)$ is an exponential martingale.

## Python Implementation

```python
import numpy as np
from scipy.linalg import cholesky, solve_triangular

def gp_regression(X_train, y_train, X_test, kernel_fn, sigma_noise=0.1):
    """Gaussian process regression with exact inference."""
    K = kernel_fn(X_train, X_train)
    K += sigma_noise**2 * np.eye(len(X_train))
    L = cholesky(K, lower=True)
    
    # solve K alpha = y
    alpha = solve_triangular(L.T, solve_triangular(L, y_train, lower=True))
    
    K_s = kernel_fn(X_test, X_train)
    mu = K_s @ alpha
    
    v = solve_triangular(L, K_s.T, lower=True)
    cov = kernel_fn(X_test, X_test) - v.T @ v
    
    return mu, np.sqrt(np.diag(cov))

def brownian_motion_path(n_steps=1000, T=1.0):
    """Simulate a Brownian motion path."""
    dt = T / n_steps
    dW = np.random.randn(n_steps) * np.sqrt(dt)
    W = np.zeros(n_steps + 1)
    W[1:] = np.cumsum(dW)
    return W

def quadratic_variation(path):
    """Compute quadratic variation of a path."""
    return np.sum(np.diff(path)**2)

# Example: 1D GP regression
np.random.seed(42)
X_train = np.random.uniform(-5, 5, 15)[:, None]
y_train = np.sin(X_train[:, 0]) + 0.1 * np.random.randn(15)
X_test = np.linspace(-6, 6, 200)[:, None]

def rbf_kernel(X, Y=None, sigma=1.0):
    if Y is None:
        Y = X
    sq_dists = np.sum(X**2, axis=1)[:, None] + np.sum(Y**2, axis=1)[None, :] - 2 * X @ Y.T
    return np.exp(-sq_dists / (2 * sigma**2))

mu, std = gp_regression(X_train, y_train, X_test, rbf_kernel, sigma_noise=0.15)
print(f"Prediction at x=0: {mu[100]:.3f} ± {std[100]:.3f} (true: {np.sin(0):.3f})")

# Brownian motion example
W = brownian_motion_path()
print(f"Quadratic variation: {quadratic_variation(W):.4f} (expected approx 1.0)")
```

## Visualization
Plot the GP regression: training points, mean prediction, and 95% credible interval (shaded). The uncertainty increases away from training data. A second panel shows Brownian motion paths with their quadratic variation converging to $t$ as discretisation refines. A third panel shows a martingale convergence plot — the sample mean of an increasing number of draws from a martingale difference sequence approaches zero.

## Connections to Machine Learning

### Bayesian Optimisation
GP surrogates guide the optimisation of expensive black-box functions. The acquisition function (expected improvement, GP-UCB, Thompson sampling) balances exploration (high uncertainty) and exploitation (low predicted value). GP regression provides both the point prediction and the uncertainty — essential for the exploration-exploitation trade-off.

### Diffusion Models
Score-based diffusion models reverse an Ornstein-Uhlenbeck process:

$$dX_t = -\frac12 \beta_t X_t dt + \sqrt{\beta_t} dW_t$$

The forward process adds noise, and the reverse process (learned by a neural network) removes noise. The reverse SDE is:

$$dX_t = \left( -\frac12 \beta_t X_t - \beta_t \nabla_{X_t} \log p_t(X_t) \right) dt + \sqrt{\beta_t} d\bar{W}_t$$

This is a stochastic process governed by Itô calculus.

### Martingale Convergence in SGD
Stochastic gradient descent with decreasing step sizes $\eta_t$ such that $\sum \eta_t = \infty$ and $\sum \eta_t^2 < \infty$ generates a sequence where the loss $L(\theta_t)$ is a martingale (or a supermartingale). The martingale convergence theorem guarantees $L(\theta_t) \to L^*$ almost surely — the theoretical basis for SGD convergence.

## Practical Considerations

### GP Scaling
- Full GP is $O(n^3)$ — infeasible for $n > 10^4$.
- **Sparse GPs**: use $m \ll n$ inducing points, reducing to $O(nm^2)$.
- **Structured kernels**: for grid data, Kronecker structure reduces to $O(d n^{1+1/d})$.
- **Deep GPs**: composition of GP layers for non-stationary functions.

### Kernel Choice for GPs
- RBF: infinitely smooth, may oversmooth discontinuities.
- Matérn: controls smoothness via $\nu$; $\nu=3/2$ (once diff.) or $\nu=5/2$ (twice diff.) are robust defaults.
- Periodic: $k(x,x') = \exp(-2\sin^2(\pi|x-x'|/p)/\ell^2)$ — for seasonal data.
- Spectral mixture: learn a mixture of RBFs in frequency domain.

## References
- Rasmussen & Williams, *Gaussian Processes for Machine Learning*, MIT Press 2006
- Øksendal, *Stochastic Differential Equations*, 6th ed., Springer 2003
- Karatzas & Shreve, *Brownian Motion and Stochastic Calculus*, 2nd ed., Springer 1991
- Williams & Rasmussen, "Gaussian Processes for Regression," *NeurIPS 1995*
- Ho et al., "Denoising Diffusion Probabilistic Models," *NeurIPS 2020*
