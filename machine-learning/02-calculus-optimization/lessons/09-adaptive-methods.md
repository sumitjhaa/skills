# 09. Adaptive Optimization Methods (AdaGrad, RMSprop, Adam)

## Introduction

Adaptive methods adjust the learning rate per-parameter based on historical gradient information. They handle sparse gradients and varying parameter scales automatically.

## AdaGrad

AdaGrad adapts the learning rate by dividing by the square root of accumulated squared gradients:

```
G_{t+1} = G_t + (∇f(x_t))²
x_{t+1} = x_t - η · ∇f(x_t) / (√(G_{t+1}) + ε)
```

```python
import numpy as np

def adagrad(grad_f, x0, lr=1.0, epsilon=1e-8, n_iter=100):
    x = x0.copy()
    G = np.zeros_like(x)
    for t in range(1, n_iter + 1):
        g = grad_f(x)
        G += g**2
        x = x - lr * g / (np.sqrt(G) + epsilon)
    return x
```

AdaGrad works well for sparse features but the accumulation of squared gradients causes the learning rate to shrink too aggressively.

## RMSprop

RMSprop uses an exponentially decaying average of squared gradients:

```
E[g²]_{t+1} = β·E[g²]_t + (1-β)·(∇f(x_t))²
x_{t+1} = x_t - η · ∇f(x_t) / (√(E[g²]_{t+1}) + ε)
```

```python
def rmsprop(grad_f, x0, lr=0.001, beta=0.9, epsilon=1e-8, n_iter=100):
    x = x0.copy()
    s = np.zeros_like(x)
    for t in range(1, n_iter + 1):
        g = grad_f(x)
        s = beta * s + (1 - beta) * g**2
        x = x - lr * g / (np.sqrt(s) + epsilon)
    return x
```

## Adam (Adaptive Moment Estimation)

Adam combines momentum with RMSprop's per-parameter scaling:

```
m_{t+1} = β₁·m_t + (1-β₁)·∇f(x_t)
v_{t+1} = β₂·v_t + (1-β₂)·(∇f(x_t))²
m̂ = m_{t+1} / (1 - β₁ᵗ)
v̂ = v_{t+1} / (1 - β₂ᵗ)
x_{t+1} = x_t - η · m̂ / (√v̂ + ε)
```

```python
def adam(grad_f, x0, lr=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8, n_iter=100):
    x = x0.copy()
    m = np.zeros_like(x)
    v = np.zeros_like(x)
    for t in range(1, n_iter + 1):
        g = grad_f(x)
        m = beta1 * m + (1 - beta1) * g
        v = beta2 * v + (1 - beta2) * g**2
        m_hat = m / (1 - beta1**t)
        v_hat = v / (1 - beta2**t)
        x = x - lr * m_hat / (np.sqrt(v_hat) + epsilon)
    return x
```

## Variants

- **AdaMax**: Uses infinity norm instead of L2 for v
- **Nadam**: Adam with Nesterov momentum
- **AMSGrad**: Fixes convergence issues with a maximum v
