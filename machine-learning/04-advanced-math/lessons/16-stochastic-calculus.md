# 04.16 Stochastic Calculus and Itô Calculus

## Motivation
Stochastic calculus generalises ordinary calculus to processes with random noise. It is the mathematical language for diffusion processes, stochastic differential equations (SDEs), and the continuous-time limit of score-based generative models. Understanding Itô calculus is essential for working with diffusion models, stochastic gradient Langevin dynamics, and continuous normalising flows.

## Learning Objectives
- Define the Itô integral and contrast it with the Riemann–Stieltjes integral.
- State and apply Itô's lemma for scalar and multivariate processes.
- Derive the Fokker–Planck equation from an SDE.
- Apply stochastic calculus to diffusion models and SGLD.

## Math Foundation

### Itô Integral
For a stochastic process $X_t$ adapted to the filtration of a Brownian motion $W_t$, the Itô integral is defined as:

$$\int_0^T X_t dW_t = \lim_{n \to \infty} \sum_{i=0}^{n-1} X_{t_i} (W_{t_{i+1}} - W_{t_i})$$

The integrand is evaluated at the left endpoint of each subinterval (Itô convention). If the midpoint is used instead, we get the Stratonovich integral. The Itô integral is a martingale: $\mathbb{E}[\int_0^T X_t dW_t] = 0$.

### Itô Isometry
A key property for computing variances:

$$\mathbb{E}\left[ \left( \int_0^T X_t dW_t \right)^2 \right] = \mathbb{E}\left[ \int_0^T X_t^2 dt \right]$$

This is the foundation for $L^2$ convergence of the Itô integral.

### Itô's Lemma
For a twice-differentiable function $f(t, x)$ and a process $dX_t = \mu_t dt + \sigma_t dW_t$:

$$df(t, X_t) = \left( \frac{\partial f}{\partial t} + \mu_t \frac{\partial f}{\partial x} + \frac12 \sigma_t^2 \frac{\partial^2 f}{\partial x^2} \right) dt + \sigma_t \frac{\partial f}{\partial x} dW_t$$

The crucial difference from ordinary calculus is the $\frac12 \sigma_t^2 \partial^2 f / \partial x^2$ term — the "Itô correction" arising from the quadratic variation of Brownian motion $(dW_t)^2 = dt$.

### Multivariate Itô's Lemma
For $d\mathbf{X}_t = \boldsymbol{\mu}_t dt + \Sigma_t d\mathbf{W}_t$ (where $\Sigma_t \Sigma_t^\top$ is the diffusion matrix):

$$df(t, \mathbf{X}_t) = \left( \partial_t f + \boldsymbol{\mu}_t^\top \nabla f + \frac12 \text{tr}\left( \Sigma_t \Sigma_t^\top \nabla^2 f \right) \right) dt + (\nabla f)^\top \Sigma_t d\mathbf{W}_t$$

### Stochastic Differential Equations
An SDE for $X_t$ driven by Brownian motion:

$$dX_t = \mu(X_t, t) dt + \sigma(X_t, t) dW_t$$

$\mu$ is the drift coefficient, $\sigma$ is the diffusion coefficient. Under Lipschitz and linear growth conditions on $\mu$ and $\sigma$, a unique strong solution exists.

### Fokker–Planck Equation
The probability density $p(x,t)$ of $X_t$ evolves according to:

$$\frac{\partial p}{\partial t} = -\frac{\partial}{\partial x}(\mu p) + \frac12 \frac{\partial^2}{\partial x^2}(\sigma^2 p)$$

This is the Kolmogorov forward equation. The adjoint equation (Kolmogorov backward) describes the evolution of expectations.

## Key Results

### Girsanov's Theorem
If $dX_t = \mu_t dt + dW_t$ under measure $P$, and $\theta_t = -\mu_t$ satisfies Novikov's condition $\mathbb{E}[\exp(\frac12 \int_0^T \theta_t^2 dt)] < \infty$, then under the measure $Q$ defined by:

$$\frac{dQ}{dP} = \exp\left( \int_0^T \theta_t dW_t - \frac12 \int_0^T \theta_t^2 dt \right)$$

the process $X_t$ is a Brownian motion (driftless). This is the foundation of risk-neutral pricing in finance and importance sampling for SDEs.

### Itô vs Stratonovich
For smooth test functions:

$$\int_0^T X_t \circ dW_t = \int_0^T X_t dW_t + \frac12 \langle X, W \rangle_T$$

(Itô) (Stratonovich)

Stratonovich calculus follows the ordinary chain rule (no Itô correction) and is the natural choice for stochastic Hamiltonian systems and SDEs arising from physical limits. Itô calculus is preferred for martingale theory and filtering.

## Python Implementation

```python
import numpy as np
from scipy.integrate import solve_ivp

def ito_integral(X, dW, dt):
    """Approximate Itô integral sum X_i dW_i."""
    return np.sum(X[:-1] * dW)

def euler_maruyama(drift, diffusion, x0, T=1.0, n_steps=1000):
    """Euler-Maruyama discretisation of an SDE."""
    dt = T / n_steps
    x = np.zeros(n_steps + 1)
    t = np.linspace(0, T, n_steps + 1)
    x[0] = x0
    
    for i in range(n_steps):
        dW = np.random.randn() * np.sqrt(dt)
        x[i+1] = x[i] + drift(x[i], t[i]) * dt + diffusion(x[i], t[i]) * dW
    
    return t, x

def geometric_brownian_path(mu, sigma, x0=1.0, T=1.0, n_steps=1000):
    """Simulate geometric Brownian motion via exact solution."""
    dt = T / n_steps
    t = np.linspace(0, T, n_steps + 1)
    dW = np.random.randn(n_steps) * np.sqrt(dt)
    W = np.concatenate([[0], np.cumsum(dW)])
    X = x0 * np.exp((mu - 0.5 * sigma**2) * t + sigma * W)
    return t, X

def fokker_planck_numeric(mu, sigma_sq, x_range, T, nx=200, nt=1000):
    """Solve Fokker-Planck PDE via finite differences."""
    x = np.linspace(-x_range, x_range, nx)
    dx = 2 * x_range / (nx - 1)
    dt = T / nt
    p = np.zeros((nt + 1, nx))
    p[0] = np.exp(-x**2 / 2) / np.sqrt(2 * np.pi)  # initial N(0,1)
    p[0] /= p[0].sum() * dx
    
    for i in range(nt):
        # upwind scheme for drift, centred for diffusion
        p_curr = p[i]
        # drift term: -d(mu p)/dx
        flux_drift = -np.gradient(mu(x) * p_curr, dx)
        # diffusion term: 0.5 * d^2(sigma^2 p)/dx^2
        flux_diff = 0.5 * np.gradient(np.gradient(sigma_sq(x) * p_curr, dx), dx)
        p[i+1] = p_curr + dt * (flux_drift + flux_diff)
        # boundary condition: p = 0 at boundaries
        p[i+1, 0] = p[i+1, -1] = 0.0
        # normalise
        p[i+1] /= p[i+1].sum() * dx
    
    return x, p

# Example: simulate Ornstein-Uhlenbeck process dX = -theta X dt + sigma dW
theta, sigma = 1.0, 0.5
drift = lambda x, t: -theta * x
diffusion = lambda x, t: sigma
t, X = euler_maruyama(drift, diffusion, x0=2.0, T=5.0)
print(f"Final value: {X[-1]:.3f} (stationary mean: 0, var: {sigma**2/(2*theta):.3f})")

# Check Itô isometry
np.random.seed(42)
dW = np.random.randn(1000) * np.sqrt(0.001)
X_path = np.cumsum(np.random.randn(1001) * 0.001)
ito_int = ito_integral(X_path, dW, 0.001)
print(f"Itô integral: {ito_int:.4f}, Expected: 0")
```

## Visualization
Plot the exact solution of geometric Brownian motion (log-normal) with a few realisations. A second panel shows the numerical solution to the Fokker–Planck equation for the OU process, with the density evolving from a delta at $x_0$ to the stationary Gaussian. A third panel illustrates the Itô correction: compare $d(W^2)$ computed via Itô's lemma ($2W dW + dt$) vs. ordinary calculus ($2W dW$).

## Applications in Machine Learning

### Score-Based Diffusion Models
The forward SDE adds noise: $dX_t = f(X_t, t) dt + g(t) dW_t$. The reverse SDE (Anderson 1982) is:

$$dX_t = \left( f(X_t, t) - g(t)^2 \nabla_{X_t} \log p_t(X_t) \right) dt + g(t) d\bar{W}_t$$

The score $\nabla_x \log p_t(x)$ is approximated by a neural network $s_\theta(x, t)$ trained with denoising score matching. The reverse SDE is discretised (Euler-Maruyama or predictor-corrector), and the Fokker-Planck equation describes the evolution of the data distribution through the diffusion process.

### Stochastic Gradient Langevin Dynamics
SGLD combines SGD with Langevin dynamics:

$$d\theta_t = -\frac{\eta_t}{2} \nabla \tilde{L}(\theta_t) dt + \sqrt{\eta_t} dW_t$$

where $\tilde{L}$ is the minibatch loss. The Itô correction ensures the stationary distribution is the true posterior (not the SGD stationary distribution). SGLD provably converges to the posterior under decreasing step sizes.

### Neural SDEs
Neural SDEs generalise neural ODEs to stochastic dynamics:

$$dh_t = \mu_\theta(h_t, t) dt + \sigma_\theta(h_t, t) dW_t$$

The drift and diffusion are neural networks. Training uses adjoint sensitivity methods adapted for SDEs (Li et al. 2020). Applications include time-series modelling with uncertainty and generative modelling on Riemannian manifolds.

## Practical Considerations

### Discretisation Error
- **Euler-Maruyama**: strong error $O(\sqrt{dt})$, weak error $O(dt)$. Sufficient for most ML applications.
- **Milstein scheme**: adds the $\sigma \sigma'$ term: strong error $O(dt)$. Better for multiplicative noise.
- **Runge-Kutta for SDEs**: higher-order schemes exist but are complex.

### Numerical Stability
- Implicit methods (e.g., implicit Euler) are needed for stiff SDEs where the drift has large gradients.
- The tamed Euler scheme $X_{n+1} = X_n + \frac{\mu(X_n)}{1 + \sqrt{dt}|\mu(X_n)|} dt + \sigma(X_n) dW_n$ prevents blow-up for superlinearly growing coefficients.

## References
- Øksendal, *Stochastic Differential Equations*, 6th ed., Springer 2003
- Särkkä & Solin, *Applied Stochastic Differential Equations*, Cambridge 2019
- Kloeden & Platen, *Numerical Solution of Stochastic Differential Equations*, Springer 1992
- Song et al., "Score-Based Generative Modeling through Stochastic Differential Equations," *ICLR 2021*
- Welling & Teh, "Bayesian Learning via Stochastic Gradient Langevin Dynamics," *ICML 2011*
