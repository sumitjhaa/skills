# 33. Bilevel Optimization

## Introduction

Bilevel optimization involves two nested optimization problems: the outer problem's objective depends on the solution of an inner problem. This arises in hyperparameter tuning, meta-learning, and adversarial learning.

## Formulation

```
minimize    F(x, y*(x))
subject to  y*(x) = argmin_y f(x, y)
```

where `x` are hyperparameters (outer variables) and `y` are model parameters (inner variables).

## Gradient-Based Methods via Implicit Differentiation

Using the implicit function theorem at optimality (`∇_y f = 0`):

```
dF/dx = ∂F/∂x + ∂F/∂y · dy*/dx
dy*/dx = -(∇²_y f)⁻¹ · ∂(∇_y f)/∂x
```

```python
import numpy as np
from scipy.optimize import minimize

def bilevel_hypergradient(F, f, grad_f_y, hess_f_yy, grad_f_yx, x, y_opt):
    """Compute hypergradient dF/dx using implicit differentiation."""
    # f is the inner objective, F is the outer objective
    # y_opt minimizes f(x, ·)

    dF_dy = np.gradient(F(x, y_opt), y_opt)  # ∂F/∂y
    dF_dx = np.gradient(F(x, y_opt), x)      # ∂F/∂x

    # dy*/dx = -H_f^{-1} @ ∂(∇_y f)/∂x
    H = hess_f_yy(x, y_opt)
    dy_dx = np.linalg.solve(H, -grad_f_yx(x, y_opt))

    return dF_dx + dF_dy @ dy_dx
```

## Unrolled Differentiation

Alternatively, unroll the inner optimization and differentiate through it:

```python
def unrolled_hypergradient(F, grad_f, x, y0, inner_steps=10, lr=0.1):
    """Hypergradient via unrolling inner GD."""
    y = y0.copy()
    ys = [y.copy()]

    # Inner loop (forward)
    for t in range(inner_steps):
        y = y - lr * grad_f(x, y)
        ys.append(y.copy())

    # Outer gradient via reverse-mode through unrolled updates
    dF_dy = np.gradient(F(x, y), y)
    dy_accum = np.zeros_like(y)

    for t in reversed(range(inner_steps)):
        y_t = ys[t]
        dgrad_dy = hess_f_yy(x, y_t)  # ∂∇f/∂y = ∇²f
        dy_accum = dF_dy + (np.eye(len(y)) - lr * dgrad_dy).T @ dy_accum

    dF_dx = np.gradient(F(x, y), x)
    dgrad_dx = grad_f_yx(x, y_t)  # ∂∇f/∂x

    return dy_accum @ dgrad_dx + dF_dx
```

## Applications

### Hyperparameter Optimization

```python
# Outer: validation loss, Inner: training loss
F = lambda lr, w: validation_loss(w)  # lr is hyperparameter
f = lambda lr, w: training_loss(w, lr)  # inner objective
```

### Meta-Learning (MAML)

```
Outer: minimize Σ L_val(θ - α ∇L_train(θ))
Inner: θ' = θ - α ∇L_train(θ)  (one or few gradient steps)
```

### Adversarial Learning

```
Outer: minimize classifier loss
Inner: maximize perturbation within ε-ball
```

Bilevel optimization provides a principled framework for problems where optimization occurs at multiple levels, from hyperparameter tuning to neural architecture search.
