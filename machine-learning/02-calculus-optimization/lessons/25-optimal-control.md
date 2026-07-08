# 25. Optimal Control

## Introduction

Optimal control selects control inputs to steer a dynamical system while minimizing a cost. It is foundational to robotics, reinforcement learning, and continuous-time trajectory optimization.

## Problem Formulation

```
minimize    J = ∫₀ᵀ L(x(t), u(t), t) dt + Φ(x(T))
subject to  ẋ = f(x(t), u(t), t)
            x(0) = x₀
```

where `x(t)` is the state, `u(t)` is the control, `L` is the running cost, and `Φ` is the terminal cost.

## Pontryagin's Maximum Principle

Define the Hamiltonian:

```
H(x, u, λ, t) = L(x, u, t) + λᵀ f(x, u, t)
```

Optimality conditions:

```
ẋ = ∂H/∂λ = f(x, u, t)
-λ̇ = ∂H/∂x = ∂L/∂x + λᵀ ∂f/∂x
0 = ∂H/∂u = ∂L/∂u + λᵀ ∂f/∂u
λ(T) = ∂Φ/∂x(T)
```

```python
import numpy as np
from scipy.integrate import solve_ivp

# Example: LQR (Linear Quadratic Regulator)
# ẋ = Ax + Bu, J = ∫(xᵀQx + uᵀRu) dt
def lqr_riccati(A, B, Q, R, T, n_steps=100):
    """Solve continuous-time LQR via backward Riccati."""
    n = A.shape[0]
    dt = T / n_steps
    P = np.zeros((n, n, n_steps + 1))
    P[:, :, -1] = np.zeros((n, n))  # terminal cost

    for k in range(n_steps - 1, -1, -1):
        P_t = P[:, :, k + 1]
        P_dot = -(A.T @ P_t + P_t @ A - P_t @ B @ np.linalg.inv(R) @ B.T @ P_t + Q)
        P[:, :, k] = P_t - dt * P_dot

    return P

# Simulate LQR controller
A = np.array([[0, 1], [0, 0]])
B = np.array([[0], [1]])
Q = np.eye(2)
R = np.array([[0.1]])

P = lqr_riccati(A, B, Q, R, 10.0)
print(f"Riccati solution P(0):\n{P[:, :, 0]}")
```

## Hamilton-Jacobi-Bellman (HJB)

The value function `V(x, t)` satisfies:

```
-∂V/∂t = min_u { L(x, u) + ∇V · f(x, u) }
```

This is the continuous-time analog of the Bellman equation in RL.

## Direct Methods

Discretize the problem and solve as a nonlinear program:

```python
from scipy.optimize import minimize

def direct_transcription(x0, N=20, dt=0.1):
    """Solve control problem via direct transcription."""
    n_states = 2
    n_controls = 1

    def objective(z):
        x = z[:N * n_states].reshape(N, n_states)
        u = z[N * n_states:].reshape(N, n_controls)
        return dt * np.sum(u**2)

    # Dynamics constraints: x_{k+1} = x_k + dt * f(x_k, u_k)
    def dynamics_constraint(z):
        x = z[:N * n_states].reshape(N, n_states)
        u = z[N * n_states:].reshape(N, n_controls)
        cons = []
        for k in range(N - 1):
            x_next = x[k] + dt * np.array([x[k, 1], u[k, 0]])
            cons.extend(x[k+1] - x_next)
        return np.array(cons)

    return minimize(objective, np.zeros(N * (n_states + n_controls)),
                    constraints={'type': 'eq', 'fun': dynamics_constraint})
```

## Model Predictive Control (MPC)

MPC solves a finite-horizon optimal control problem at each step, applies only the first control, then recedes the horizon. This provides feedback control with constraint handling.
