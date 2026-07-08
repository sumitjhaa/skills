# 04. Systems: Gaussian Elimination, LU Decomposition

## Introduction

Solving linear systems A**x** = **b** is fundamental. Gaussian elimination converts A into upper-triangular form through elementary row operations, then back-substitutes to find **x**.

## Gaussian Elimination

Three row operations:
1. Swap two rows
2. Multiply a row by a nonzero scalar
3. Add a multiple of one row to another

```python
import numpy as np

def gauss_elimination(A, b):
    n = len(A)
    M = A.astype(float).copy()
    rhs = b.astype(float).copy()
    for col in range(n):
        # Partial pivoting: find max row
        max_row = np.argmax(np.abs(M[col:, col])) + col
        if max_row != col:
            M[[col, max_row]] = M[[max_row, col]]
            rhs[[col, max_row]] = rhs[[max_row, col]]
        for row in range(col+1, n):
            factor = M[row, col] / M[col, col]
            M[row, col:] -= factor * M[col, col:]
            rhs[row] -= factor * rhs[col]
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (rhs[i] - M[i, i+1:] @ x[i+1:]) / M[i, i]
    return x
```

## LU Decomposition

Factor A = P L U where P is a permutation, L is unit lower-triangular, and U is upper-triangular.

```python
from scipy.linalg import lu
P, L, U = lu(A)
print(f"L:\n{L}\nU:\n{U}")
```

Once decomposed, solve A**x** = **b** by solving L**y** = P**b** then U**x** = **y**.

```python
y = np.linalg.solve(L, P @ b)
x = np.linalg.solve(U, y)
```

## Pivoting Strategies

- **No pivoting**: Unstable; can fail on well-conditioned systems
- **Partial pivoting**: Swap rows so the pivot has the largest magnitude in its column (standard)
- **Complete pivoting**: Swap both rows and columns for the largest element in the submatrix (more stable, more expensive)

```python
# Complete pivoting example
def lu_complete_pivoting(A):
    n = A.shape[0]
    M = A.copy().astype(float)
    row_perm = np.arange(n)
    col_perm = np.arange(n)
    for k in range(n):
        sub = M[k:, k:]
        i, j = np.unravel_index(np.argmax(np.abs(sub)), sub.shape)
        i += k; j += k
        if i != k:
            M[[k,i]] = M[[i,k]]
            row_perm[[k,i]] = row_perm[[i,k]]
        if j != k:
            M[:, [k,j]] = M[:, [j,k]]
            col_perm[[k,j]] = col_perm[[j,k]]
        for i in range(k+1, n):
            M[i,k] /= M[k,k]
            M[i,k+1:] -= M[i,k] * M[k,k+1:]
    return M, row_perm, col_perm
```

## Condition Number and Stability

```python
cond = np.linalg.cond(A)
print(f"Condition number: {cond}")
# If cond ~ 10^k, we lose k digits of precision
```

## What You'll Implement

- Gaussian elimination with partial pivoting from scratch
- LU decomposition with partial and complete pivoting
- Forward and back substitution
- Condition number estimation
- Stability experiments (compare pivoting strategies on near-singular matrices)
