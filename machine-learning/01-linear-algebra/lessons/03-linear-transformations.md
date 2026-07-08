# 03. Linear Transformations and Matrix Representations

## Introduction

A transformation T: V → W is **linear** if:

1. T(**u** + **v**) = T(**u**) + T(**v**)
2. T(c**v**) = c T(**v**)

Every linear transformation from ℝⁿ to ℝᵐ can be represented by an m×n matrix A such that T(**x**) = A**x**.

## Matrix as Linear Transformation

The columns of A are the images of the standard basis vectors:

A = [T(**e₁**) | T(**e₂**) | ... | T(**eₙ**)]

```python
import numpy as np
# 2D rotation by 90 degrees
theta = np.pi/2
A = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta),  np.cos(theta)]])
v = np.array([1, 0])
w = A @ v  # Rotated
print(f"Original: {v}, Transformed: {w}")
```

## Common Transformations

| Transformation | Matrix | Effect |
|---|---|---|
| Rotation | [[cos θ, −sin θ], [sin θ, cos θ]] | Rotates by θ |
| Scaling | [[sₓ, 0], [0, sᵧ]] | Scales axes |
| Shear | [[1, s], [0, 1]] | Shears x-direction |
| Reflection | [[1, 0], [0, −1]] | Reflects over x-axis |

```python
def apply_transform(A, points):
    return (A @ points.T).T

points = np.array([[0,0], [1,0], [1,1], [0,1]])
scale = np.array([[2, 0], [0, 2]])
scaled = apply_transform(scale, points)
```

## Composition

Applying T₂ after T₁: T₂ ∘ T₁ corresponds to matrix multiplication A₂A₁.

```python
rotate = np.array([[0, -1], [1, 0]])  # 90° rotation
scale = np.array([[2, 0], [0, 2]])    # 2x scaling
composed = scale @ rotate  # Scale then rotate
```

Note that matrix multiplication is not commutative: A₂A₁ ≠ A₁A₂ generally.

## Visualization

Plot the unit square before and after transformation to see the geometric effect:

```python
import matplotlib.pyplot as plt
original = np.array([[0,0],[1,0],[1,1],[0,1],[0,0]])
transformed = (composed @ original.T).T
plt.plot(original[:,0], original[:,1], 'b-', label='Original')
plt.plot(transformed[:,0], transformed[:,1], 'r-', label='Transformed')
plt.axis('equal'); plt.legend(); plt.show()
```

## What You'll Implement

- Matrix representing common 2D transformations
- Composition of transformations
- Matrix-as-transformation visualizer
- Apply transformation to a set of points and plot
