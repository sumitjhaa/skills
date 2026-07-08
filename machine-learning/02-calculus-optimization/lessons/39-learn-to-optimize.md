# 39. Learning to Optimize

## Introduction

Learning to optimize (L2O) replaces hand-designed optimizers with learned ones. An optimizer is parameterized as a neural network and trained to minimize a distribution of loss functions.

## Formulation

Instead of manually designing update rules, we learn:

```
x_{t+1} = x_t - g_θ(∇f(x_t), h_t)
```

where `g_θ` is a learned update function (often an RNN or small MLP) and `h_t` is hidden state.

## RNN-Based Optimizer

```python
import numpy as np

def rnn_optimizer_step(x, grad, h, W):
    """Single step of a learned RNN optimizer."""
    # Input: gradient and previous state
    # Output: update direction
    input_features = np.hstack([grad, x])

    # Simple RNN cell
    h_next = np.tanh(W['ih'] @ input_features + W['hh'] @ h)
    update = W['ho'] @ h_next

    return x - update, h_next
```

## Learned Gradient Descent

For a quadratic loss, the optimal update can be learned:

```python
def learned_gd_step(x, grad, alpha, beta):
    """Learned step sizes (coordinate-wise)."""
    # alpha and beta are learned per-parameter
    return x - (alpha * grad + beta * x)
```

## Training the Optimizer

The optimizer is trained by minimizing the cumulative loss across a trajectory:

```
L(θ) = E_{f ∼ D} [Σ_t w_t f(x_t(θ))]
```

where `D` is a distribution of problems and `w_t` are time weights (often `w_t = 1` for all t).

```python
def train_optimizer(optimizer_net, problem_dist, n_steps=50, lr=0.001):
    """Train a learned optimizer via backpropagation through time."""
    for iteration in range(1000):
        total_loss = 0
        f, x0 = problem_dist.sample()

        x = x0.copy()
        h = np.zeros(hidden_size)

        for t in range(n_steps):
            grad = f.gradient(x)
            x, h = optimizer_net(x, grad, h)
            total_loss += f(x)

        # Backpropagate through time
        # Update optimizer_net parameters
        # optimizer_net.update(total_loss)
    return optimizer_net
```

## Learned Optimizers in Practice

### Meta-Learning (MAML)

```
θ' = θ - α ∇_θ L(θ)   ← inner gradient
θ = θ - β ∇_θ L_val(θ')  ← outer (meta) gradient
```

The outer loop learns optimization across tasks.

### L2O for Scientific Computing

```python
# Learned iterative solver for PDEs
def learned_pde_solver(u0, f, net, n_iter=20):
    """Learn a solver for Poisson equation -Δu = f."""
    u = u0.copy()
    residual_history = []

    for i in range(n_iter):
        r = f + laplacian(u)  # residual
        correction = net(r, u)  # learned correction
        u = u + correction
        residual_history.append(np.linalg.norm(r))

    return u, residual_history
```

## Challenges

- **Generalization**: Learned optimizers often overfit to the training task distribution
- **Stability**: Optimization trajectories can diverge outside the training distribution
- **Computational cost**: BPTT is expensive for long trajectories
- **Theoretical guarantees**: Lacks convergence proofs of classical methods

## Promising Directions

- **Warm-starting** classical optimizers with learned initializations
- **Hybrid approaches** that switch between learned and classical based on performance
- **Metalearning optimizers** that adapt to new tasks in a few gradient steps
- **Transformers as optimizers** (e.g., OptFormer) for hyperparameter tuning

L2O represents a paradigm shift from hand-crafted to data-driven optimization, with the potential to discover algorithms superior to any human-designed optimizer.
