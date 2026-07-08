# 02. Vector Spaces: Span, Basis, Dimension, Independence

## Introduction

A vector space V over a field F (typically ℝ) is a set of vectors closed under addition and scalar multiplication. The key properties are:

1. **Closure**: **u** + **v** ∈ V, c**v** ∈ V
2. **Associativity**: (**u** + **v**) + **w** = **u** + (**v** + **w**)
3. **Commutativity**: **u** + **v** = **v** + **u**
4. **Identity**: **0** ∈ V such that **v** + **0** = **v**
5. **Inverse**: **v** + (−**v**) = **0**
6. **Distributivity**: c(**u** + **v**) = c**u** + c**v**

## Span and Linear Independence

A set of vectors {**v₁**, ..., **vₖ**} **spans** V if every vector in V can be written as a linear combination of these vectors.

They are **linearly independent** if:

c₁**v₁** + ... + cₖ**vₖ** = 0 ⇒ c₁ = ... = cₖ = 0

```python
import numpy as np

v1 = np.array([1, 0])
v2 = np.array([0, 1])
# Check independence: matrix rank tells us
A = np.column_stack([v1, v2])
rank = np.linalg.matrix_rank(A)
print(f"Rank: {rank}")  # 2 → independent
```

## Basis and Dimension

A **basis** is a set of linearly independent vectors that span the space. The number of vectors in a basis is the **dimension**.

Standard basis for ℝ³: **e₁** = (1,0,0), **e₂** = (0,1,0), **e₃** = (0,0,1)

## Gram–Schmidt Process

Given a set of independent vectors, Gram–Schmidt produces an orthonormal basis:

1. **u₁** = **v₁**
2. **e₁** = **u₁** / ||**u₁**||
3. **uₖ** = **vₖ** − Σⱼ<ₖ proj_𝐞ⱼ **vₖ**
4. **eₖ** = **uₖ** / ||**uₖ**||

```python
def gram_schmidt(V):
    m, n = V.shape
    Q = np.zeros((m, n))
    for i in range(n):
        v = V[:, i].copy()
        for j in range(i):
            v -= np.dot(Q[:, j], V[:, i]) * Q[:, j]
        Q[:, i] = v / np.linalg.norm(v)
    return Q
```

## Change of Basis

If matrix P contains the new basis vectors as columns, and **x** is expressed in the standard basis, then **x'** = P⁻¹**x** gives the coordinates in the new basis.

```python
P = np.column_stack([v1, v2])  # new basis
x = np.array([3, 4])
x_prime = np.linalg.solve(P, x)  # P^{-1} x
```

## What You'll Implement

- Check linear independence via rank
- Gram–Schmidt orthonormalization from scratch
- Change-of-basis coordinate transforms
- Visualize basis vectors in 2D
