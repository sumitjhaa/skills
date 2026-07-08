# 27. Hamiltonian Monte Carlo

## Introduction

Hamiltonian Monte Carlo (HMC) uses Hamiltonian dynamics to propose distant states in Markov chain Monte Carlo, achieving much higher efficiency than random-walk Metropolis-Hastings.

## Hamiltonian Dynamics

HMC augments the target variable `q` (position) with a momentum variable `p`:

```
H(q, p) = U(q) + K(p)
```

where `U(q) = -log p(q)` is the potential energy and `K(p) = (1/2)pᵀM⁻¹p` is the kinetic energy.

Hamilton's equations:

```
dq/dt = ∂H/∂p = M⁻¹p
dp/dt = -∂H/∂q = -∇U(q)
```

```python
import numpy as np

def leapfrog(grad_U, q, p, dt, L):
    """Leapfrog integrator for Hamiltonian dynamics."""
    q = q.copy()
    p = p.copy()

    # Half step for momentum
    p = p - (dt / 2) * grad_U(q)

    # L full steps for position
    for i in range(L - 1):
        q = q + dt * p
        p = p - dt * grad_U(q)

    # Final half step for momentum, full step for position
    q = q + dt * p
    p = p - (dt / 2) * grad_U(q)

    return q, p
```

## HMC Algorithm

```
For each iteration:
  1. Sample momentum p ∼ N(0, M)
  2. Simulate Hamiltonian dynamics for L steps (leapfrog)
  3. Accept/reject with Metropolis: min(1, exp(H(q,p) - H(q',p')))
```

```python
def hmc(grad_U, q0, dt=0.1, L=10, n_iter=1000):
    """Hamiltonian Monte Carlo sampling."""
    n = len(q0)
    q = q0.copy()
    samples = [q.copy()]

    for i in range(n_iter):
        p = np.random.randn(n)
        H_current = 0.5 * np.dot(p, p) + U(q)

        q_prop, p_prop = leapfrog(grad_U, q, p, dt, L)
        H_proposed = 0.5 * np.dot(p_prop, p_prop) + U(q_prop)

        log_accept = H_current - H_proposed
        if np.log(np.random.rand()) < log_accept:
            q = q_prop
        samples.append(q.copy())

    return np.array(samples)
```

## Tuning HMC

- `dt`: Step size (too large → low acceptance, too small → slow exploration)
- `L`: Number of leapfrog steps (trajectory length)
- `M`: Mass matrix (often identity or estimated from covariance)

## No-U-Turn Sampler (NUTS)

NUTS automatically tunes the trajectory length by stopping when the path starts doubling back (a "U-turn"), eliminating manual tuning of L.

## Applications

- **Bayesian neural networks**: Sampling from posterior over weights
- **Probabilistic programming**: Stan, PyMC, TensorFlow Probability
- **Latent variable models**: Complex posterior inference

HMC scales to high dimensions where random-walk MCMC fails, making it the gold standard for Bayesian computation.
