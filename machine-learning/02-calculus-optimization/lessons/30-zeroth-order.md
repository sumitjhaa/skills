# 30. Zeroth-Order Optimization

## Introduction

Zeroth-order (derivative-free) optimization uses only function values, not gradients. This is essential when gradients are unavailable, too expensive, or unreliable.

## Finite Difference Approximations

### Forward Difference

```
∇f(x) · v ≈ (f(x + σv) - f(x)) / σ
```

### Central Difference

```
∇f(x) · v ≈ (f(x + σv) - f(x - σv)) / (2σ)
```

### Coordinate-Wise Gradient

```
(∇f(x))ᵢ ≈ (f(x + σeᵢ) - f(x - σeᵢ)) / (2σ)
```

```python
import numpy as np

def zeroth_order_gradient(f, x, sigma=1e-6):
    """Coordinate-wise finite difference gradient."""
    grad = np.zeros_like(x)
    for i in range(len(x)):
        e = np.zeros_like(x)
        e[i] = 1
        grad[i] = (f(x + sigma * e) - f(x - sigma * e)) / (2 * sigma)
    return grad
```

## Simultaneous Perturbation Stochastic Approximation (SPSA)

SPSA estimates the gradient using only 2 function evaluations regardless of dimension:

```
g = (f(x + σΔ) - f(x - σΔ)) / (2σ) · Δ⁻¹
```

where `Δ` is a random perturbation vector (e.g., Rademacher).

```python
def spsa(f, x, sigma=1e-3):
    """SPSA gradient estimate."""
    delta = np.random.choice([-1, 1], size=len(x))
    f_plus = f(x + sigma * delta)
    f_minus = f(x - sigma * delta)
    return (f_plus - f_minus) / (2 * sigma) * delta
```

SPSA is O(1) per gradient estimate regardless of dimension, versus O(d) for coordinate-wise.

## Evolution Strategies

ES optimize by sampling perturbations around the current solution:

```
x_{t+1} = x_t + η · (1/N) Σᵢ (f(x_t + σzᵢ) - μ) · zᵢ / σ
```

```python
def evolution_strategies(f, x0, sigma=0.1, lr=0.01, n_samples=50, n_iter=100):
    """Simple evolution strategies optimization."""
    x = x0.copy()
    for t in range(n_iter):
        noise = sigma * np.random.randn(n_samples, len(x))
        rewards = np.array([f(x + n) for n in noise])

        # Standardize rewards
        rewards = (rewards - rewards.mean()) / (rewards.std() + 1e-8)

        # Gradient estimate
        grad = (noise.T @ rewards) / (n_samples * sigma)
        x = x + lr * grad

    return x
```

## Comparison with Gradient-Based Methods

| Aspect | Zeroth-Order | First-Order |
|--------|-------------|-------------|
| Gradient access | No | Yes |
| Per-iteration cost | O(d) or O(1) | O(d) |
| Convergence rate | O(1/√t) | O(1/t) |
| Applicability | Black-box models | Differentiable models |

## Applications

- **Adversarial attacks**: Black-box attacks where model gradients are unavailable
- **Hyperparameter tuning**: When gradient through the validation pipeline is unavailable
- **Reinforcement learning**: ES for policy search (e.g., OpenAI ES)
- **Bandit optimization**: Derivative-free bandit algorithms
