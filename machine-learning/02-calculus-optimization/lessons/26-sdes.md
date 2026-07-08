# 26. Stochastic Differential Equations

## Introduction

Stochastic differential equations model systems driven by random noise. They are central to diffusion models, stochastic gradient descent analysis, and financial modeling.

## Definition

An SDE has the form:

```
dX_t = μ(X_t, t) dt + σ(X_t, t) dW_t
```

where `dW_t` is a Wiener process (Brownian motion) increment with `E[dW_t] = 0`, `Var[dW_t] = dt`.

## Euler-Maruyama Method

The simplest numerical scheme for SDEs:

```
X_{t+Δt} = X_t + μ(X_t, t)Δt + σ(X_t, t) · √(Δt) · Z
```

where `Z ∼ N(0, 1)`.

```python
import numpy as np
import matplotlib.pyplot as plt

def euler_maruyama(drift, diffusion, x0, T=1.0, dt=0.001):
    """Euler-Maruyama integration of SDE."""
    n_steps = int(T / dt)
    t = np.linspace(0, T, n_steps + 1)
    X = np.zeros(n_steps + 1)
    X[0] = x0

    for i in range(n_steps):
        dW = np.sqrt(dt) * np.random.randn()
        X[i + 1] = X[i] + drift(X[i], t[i]) * dt + diffusion(X[i], t[i]) * dW

    return t, X

# Geometric Brownian Motion: dS = μS dt + σS dW
drift = lambda S, t: 0.05 * S
diffusion = lambda S, t: 0.2 * S

np.random.seed(42)
t, S = euler_maruyama(drift, diffusion, 100.0)
print(f"Final price: ${S[-1]:.2f} (starting at $100)")
```

## Ornstein-Uhlenbeck Process

```
dX_t = θ(μ - X_t) dt + σ dW_t
```

Mean-reverting process, used in neural networks as a noise model.

```python
def ou_process(theta=1.0, mu=0.0, sigma=0.5, x0=2.0, T=5.0, dt=0.01):
    drift = lambda x, t: theta * (mu - x)
    diff = lambda x, t: sigma
    return euler_maruyama(drift, diff, x0, T, dt)
```

## Langevin Dynamics

Langevin dynamics samples from a distribution using gradient information:

```
dX_t = -∇U(X_t) dt + √(2/β) dW_t
```

The stationary distribution is proportional to `exp(-βU(x))`.

```python
def langevin_sampling(grad_U, x0, beta=1.0, T=10.0, dt=0.01):
    """Langevin dynamics for sampling from exp(-βU)."""
    drift = lambda x, t: -grad_U(x)
    diff = lambda x, t: np.sqrt(2 / beta)
    return euler_maruyama(drift, diff, x0, T, dt)
```

## Relation to Gradient Descent

SGD can be modeled as an SDE:

```
dw = -∇L(w) dt + Σ(w) dW_t
```

This connects optimization to stochastic processes, explaining generalization through the noise structure.

## Applications in ML

- **Diffusion models**: Score-based generative models reverse an SDE
- **Stochastic optimizers**: SGD as discretized SDE
- **Bayesian deep learning**: Stochastic gradient Langevin dynamics
- **Reinforcement learning**: Exploration via stochastic dynamics
