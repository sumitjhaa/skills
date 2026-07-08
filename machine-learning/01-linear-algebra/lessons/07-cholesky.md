# 07. Cholesky and LDL^T Decomposition

## Introduction

For a symmetric positive definite (SPD) matrix A, the Cholesky decomposition A = LLᵀ is the most efficient decomposition, requiring half the work of LU and being numerically stable without pivoting.

## Positive Definiteness

A symmetric matrix A is positive definite if **x**ᵀA**x** > 0 for all nonzero **x**. Equivalently, all eigenvalues are positive and all leading principal minors have positive determinants.

```python
def is_positive_definite(A):
    try:
        np.linalg.cholesky(A)
        return True
    except np.linalg.LinAlgError:
        return False
```

## Cholesky Decomposition

A = LLᵀ where L is lower triangular with positive diagonal entries.

```python
def cholesky(A):
    n = A.shape[0]
    L = np.zeros((n, n))
    for j in range(n):
        s = A[j, j]
        for k in range(j):
            s -= L[j, k] ** 2
        L[j, j] = np.sqrt(s)
        for i in range(j + 1, n):
            s = A[i, j]
            for k in range(j):
                s -= L[i, k] * L[j, k]
            L[i, j] = s / L[j, j]
    return L
```

The cost is n³/3 flops — half the n³/3 of LU since symmetry is exploited.

## LDL^T Decomposition

For symmetric matrices that may not be positive definite, the LDLᵀ decomposition avoids square roots:

A = LDLᵀ where D is diagonal (possibly with negative entries).

```python
def ldl_decomposition(A):
    n = A.shape[0]
    L = np.eye(n)
    D = np.zeros(n)
    v = np.zeros(n)
    for j in range(n):
        for i in range(j):
            v[i] = L[j, i] * D[i]
        s = A[j, j] - L[j, :j] @ v[:j]
        D[j] = s
        for i in range(j + 1, n):
            s = A[i, j] - L[j, :j] @ (L[i, :j] * D[:j])
            L[i, j] = s / D[j]
    return L, np.diag(D)
```

## Applications

- Solving linear systems: forward/back substitution with L
- Computing determinants: det(A) = Πᵢ L[i,i]²
- Generating correlated random variables
- Geometric interpretation: LLᵀ maps standard basis to ellipsoid

## What You'll Implement

- Positive definiteness checking via Cholesky attempt and eigenvalues
- Cholesky decomposition from scratch
- LDL^T decomposition from scratch
- Solve Ax = b using Cholesky
- Compare stability on well-conditioned vs near-singular matrices
