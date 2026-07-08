# 06. QR Decomposition: Gram–Schmidt, Householder, Givens

## Introduction

QR decomposition factors a matrix A into A = QR where Q has orthonormal columns and R is upper triangular. It is a workhorse for solving least-squares problems and eigenvalue algorithms.

## Gram–Schmidt QR

Classical Gram–Schmidt (CGS) and Modified Gram–Schmidt (MGS) produce the QR factor:

```python
import numpy as np

def cgs_qr(A):
    m, n = A.shape
    Q = np.zeros((m, n))
    R = np.zeros((n, n))
    for i in range(n):
        v = A[:, i].copy()
        for j in range(i):
            R[j, i] = np.dot(Q[:, j], A[:, i])
            v -= R[j, i] * Q[:, j]
        R[i, i] = np.linalg.norm(v)
        Q[:, i] = v / R[i, i]
    return Q, R
```

MGS is numerically more stable:

```python
def mgs_qr(A):
    m, n = A.shape
    Q = A.copy().astype(float)
    R = np.zeros((n, n))
    for i in range(n):
        R[i, i] = np.linalg.norm(Q[:, i])
        Q[:, i] /= R[i, i]
        for j in range(i+1, n):
            R[i, j] = np.dot(Q[:, i], Q[:, j])
            Q[:, j] -= R[i, j] * Q[:, i]
    return Q, R
```

## Householder QR

Householder reflectors zero out below-diagonal entries using reflection matrices H = I − 2**vv**ᵀ / (**v**ᵀ**v**).

```python
def householder_qr(A):
    m, n = A.shape
    R = A.copy().astype(float)
    Q = np.eye(m)
    for k in range(n):
        x = R[k:, k]
        norm_x = np.linalg.norm(x)
        v = x.copy()
        v[0] += np.sign(x[0]) * norm_x
        v = v / np.linalg.norm(v)
        R[k:, k:] -= 2 * np.outer(v, v @ R[k:, k:])
        Q[k:, :] -= 2 * np.outer(v, v @ Q[k:, :])
    return Q.T, np.triu(R[:n, :n])
```

Householder is the most numerically stable QR implementation and is used in LAPACK.

## Givens QR

Givens rotations zero individual entries. Each rotation matrix G(i,j,θ) modifies rows i and j:

```python
def givens_qr(A):
    m, n = A.shape
    R = A.copy().astype(float)
    Q = np.eye(m)
    for j in range(n):
        for i in range(m-1, j, -1):
            a, b = R[j, j], R[i, j]
            if abs(b) < 1e-14:
                continue
            r = np.hypot(a, b)
            c, s = a/r, -b/r
            R[[j, i], j:] = np.array([[c, -s], [s, c]]) @ R[[j, i], j:]
            Q[[j, i], :] = np.array([[c, -s], [s, c]]) @ Q[[j, i], :]
    return Q.T, np.triu(R[:n, :n])
```

## Least Squares via QR

Solve A**x** ≈ **b** for overdetermined systems: **x** = R⁻¹Qᵀ**b**.

```python
x = np.linalg.solve(R, Q.T @ b)
```

## Stability Comparison

Householder QR is typically the most accurate, followed by MGS, then CGS. Givens is useful when sparsity must be preserved.

## What You'll Implement

- Classical and Modified Gram–Schmidt QR
- Householder QR with reflectors
- Givens rotation QR
- Stability comparison on ill-conditioned matrices
- Least-squares solver using QR
