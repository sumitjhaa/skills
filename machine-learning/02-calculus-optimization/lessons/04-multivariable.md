# 04. Multivariable Calculus

## Introduction

In machine learning, functions typically have many inputs (features, parameters). Multivariable calculus extends differentiation to functions of multiple variables.

## Partial Derivatives

For `f(x₁, ..., xₙ)`, the partial derivative with respect to `xᵢ` is:

```
∂f/∂xᵢ = lim_{h→0} (f(x₁, ..., xᵢ + h, ..., xₙ) - f(x₁, ..., xₙ)) / h
```

```python
import numpy as np

def partial_derivative(f, x, i, h=1e-7):
    """Compute partial derivative of f at x w.r.t. x[i]."""
    x_plus = x.copy()
    x_minus = x.copy()
    x_plus[i] += h
    x_minus[i] -= h
    return (f(x_plus) - f(x_minus)) / (2 * h)

f = lambda x: x[0]**2 + 3*x[1]**2 + 2*x[0]*x[1]
x = np.array([1.0, 2.0])
print(f"∂f/∂x₁ = {partial_derivative(f, x, 0):.6f}")
print(f"∂f/∂x₂ = {partial_derivative(f, x, 1):.6f}")
```

## The Gradient

The gradient ∇f is the vector of all partial derivatives:

```
∇f(x) = [∂f/∂x₁, ∂f/∂x₂, ..., ∂f/∂xₙ]ᵀ
```

The gradient points in the direction of steepest ascent. In gradient descent, we move opposite to the gradient.

```python
def gradient(f, x, h=1e-7):
    grad = np.zeros_like(x)
    for i in range(len(x)):
        grad[i] = partial_derivative(f, x, i, h)
    return grad

print(f"∇f(1,2) = {gradient(f, x)}")
```

## Directional Derivative

The derivative of `f` at `x` in direction `v` (unit vector) is:

```
D_v f(x) = ∇f(x) · v
```

## Level Sets and Gradients

The gradient is always perpendicular to level sets (contours of constant function value). This is why gradient descent moves orthogonal to contour lines.

## Chain Rule (Multivariable)

For `f(g₁(t), g₂(t), ..., gₙ(t))`:

```
df/dt = Σᵢ (∂f/∂gᵢ) · (dgᵢ/dt) = ∇f · g'(t)
```

This extends to the full Jacobian for vector-valued functions: `J_{ij} = ∂fᵢ/∂xⱼ`.
