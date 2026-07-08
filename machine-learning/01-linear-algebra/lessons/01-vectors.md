# 01. Vectors: Dot, Cross, Outer, Projections

## Introduction

A vector is a mathematical object that has both magnitude and direction. In machine learning, vectors represent data points, features, weights, and activations. We denote vectors in bold lowercase: **v**.

## Vector Operations

### Dot Product

The dot product of two vectors **a**, **b** ∈ ℝⁿ is:

**a** · **b** = Σᵢ aᵢ bᵢ = ||**a**|| ||**b**|| cos θ

```python
import numpy as np
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
dot = np.dot(a, b)
print(f"Dot product: {dot}")
```

The dot product measures how much **a** projects onto **b**. When it is zero, the vectors are orthogonal.

### Cross Product

The cross product **a** × **b** is defined only in ℝ³ and produces a vector perpendicular to both **a** and **b** with magnitude equal to the area of the parallelogram they span.

**a** × **b** = (a₂b₃ − a₃b₂, a₃b₁ − a₁b₃, a₁b₂ − a₂b₁)

```python
cross = np.cross(a, b)
print(f"Cross product: {cross}")
```

### Outer Product

The outer product **a** ⊗ **b** produces a matrix of rank 1:

(**a** ⊗ **b**)ᵢⱼ = aᵢ bⱼ

```python
outer = np.outer(a, b)
print(f"Outer product:\n{outer}")
```

### Projections

The projection of **a** onto **b** is:

proj_𝐛 **a** = ((**a** · **b**) / (**b** · **b**)) **b**

```python
proj = (np.dot(a, b) / np.dot(b, b)) * b
print(f"Projection of a onto b: {proj}")
```

The component of **a** orthogonal to **b** is simply **a** − proj_𝐛 **a**.

## Geometric Visualization

We can visualize vectors in ℝ² or ℝ³ using matplotlib:

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.quiver(0, 0, a[0], a[1], angles='xy', scale_units='xy', scale=1, color='r')
ax.quiver(0, 0, b[0], b[1], angles='xy', scale_units='xy', scale=1, color='b')
ax.set_xlim(0, 5); ax.set_ylim(0, 6)
plt.show()
```

## What You'll Implement

- Dot product from scratch (without numpy)
- Cross product from scratch
- Outer product from scratch
- Vector projection and rejection
- Geometric visualization in 2D and 3D
