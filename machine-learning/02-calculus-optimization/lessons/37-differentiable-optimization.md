# 37. Differentiable Optimization Layers

## Introduction

Differentiable optimization layers embed optimization problems as neural network layers, enabling end-to-end learning through constraints and structured predictions.

## Motivation

Standard neural networks have fixed architectures. Optimization layers let us incorporate domain knowledge (physics, geometry, constraints) while remaining trainable via gradient descent.

## OptNet: Differentiable Quadratic Programming

OptNet solves a QP as a layer:

```
minimize    (1/2)zᵀQz + qᵀz
subject to  Az = b, Gz ≤ h
```

The gradient through the QP solution uses implicit differentiation via KKT conditions:

```python
import numpy as np

def dqp_layer(Q, q, A, b, G, h):
    """Differentiable QP layer (forward pass)."""
    # Solve QP using interior point or active set
    from scipy.optimize import minimize

    def objective(z):
        return 0.5 * z @ Q @ z + q @ z

    constraints = [{'type': 'eq', 'fun': lambda z: A @ z - b}]
    result = minimize(objective, np.zeros(Q.shape[0]),
                      constraints=constraints)
    return result.x

def qp_backward(Q, q, A, G, z_star, lambda_eq, lambda_ineq, dl_dz):
    """Backward pass through QP using implicit differentiation."""
    # KKT system at optimality:
    # [Q   Aᵀ  G_activeᵀ] [dz        ]   [0]
    # [A   0    0        ] [dλ_eq    ] = [0]
    # [G_a 0    0        ] [dλ_ineq_a]   [0]
    # ∂z/∂[Q,q,A,b,G,h] from perturbed KKT

    # Extract active constraints
    active = np.where(G @ z_star >= h - 1e-8)[0]
    G_active = G[active]

    n = len(z_star)
    KKT = np.block([
        [Q, A.T, G_active.T],
        [A, np.zeros((A.shape[0], A.shape[0] + G_active.shape[0]))],
        [G_active, np.zeros((G_active.shape[0], A.shape[0] + G_active.shape[0]))]
    ])

    # Solve for (dz, dλ_eq, dλ_ineq)
    rhs = np.hstack([-dl_dz, np.zeros(A.shape[0] + G_active.shape[0])])
    grad = np.linalg.solve(KKT, rhs)
    return grad[:n]
```

## Deep Equilibrium Models (DEQs)

DEQs find fixed points of implicit layers:

```
z* = f(z*, x, θ)
```

The gradient uses implicit differentiation:

```
dz*/dθ = (I - ∂f/∂z*)⁻¹ · ∂f/∂θ
```

```python
def deq_forward(f, x, theta, max_iter=50):
    """Forward pass via fixed-point iteration."""
    z = np.zeros(f(np.zeros_like(x), x, theta).shape)
    for i in range(max_iter):
        z_next = f(z, x, theta)
        if np.linalg.norm(z_next - z) < 1e-6:
            break
        z = z_next
    return z

def deq_backward(f, z_star, x, theta, dl_dz):
    """Backward pass using implicit differentiation."""
    def f_z(z):
        return f(z, x, theta)

    # J = ∂f/∂z at z_star (via finite differences)
    eps = 1e-6
    n = len(z_star)
    J = np.zeros((n, n))
    for i in range(n):
        e = np.zeros(n); e[i] = eps
        J[:, i] = (f_z(z_star + e) - f_z(z_star - e)) / (2 * eps)

    # dz*/dθ = -(I - J)⁻¹ · ∂f/∂θ (via linear solve)
    I_minus_J = np.eye(n) - J
    return np.linalg.solve(I_minus_J.T, dl_dz)
```

## Applications

- **Structured SVMs**: Differentiable QP for structured prediction
- **Optimal transport layers**: Differentiable Sinkhorn for alignment
- **Robust optimization layers**: Learning under uncertainty
- **Physics-constrained learning**: Differentiable simulation
- **Satellite imagery**: Differentiable sensor fusion

Differentiable optimization layers combine the expressiveness of deep learning with the rigor of constrained optimization, enabling new architectures that are both powerful and interpretable.
