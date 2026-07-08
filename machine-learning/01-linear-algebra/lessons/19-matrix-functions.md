# 19. Matrix Functions: expm, logm, sqrtm

## Introduction

Matrix functions extend scalar functions to matrices. If A = VΛV⁻¹ is diagonalizable, then:

f(A) = V f(Λ) V⁻¹

where f(Λ) is applied elementwise to the diagonal.

## Matrix Exponential

exp(A) = Σ_{k=0}^{∞} A^{k} / k!

```python
def expm_series(A, max_terms=50):
    n = A.shape[0]
    result = np.eye(n)
    term = np.eye(n)
    for k in range(1, max_terms):
        term = term @ A / k
        result += term
        if np.linalg.norm(term) < 1e-15:
            break
    return result
```

## Scaling and Squaring

The most common method: scale A by a power of 2 so ||A/2^s|| ≤ 1, compute the series, then square s times.

```python
def expm_scaling_squaring(A, s=6):
    A_scaled = A / (2**s)
    E = expm_series(A_scaled)
    for _ in range(s):
        E = E @ E
    return E
```

## Matrix Logarithm

The inverse of expm. Computed via the Schur–Parlett algorithm or inverse scaling and squaring.

## Matrix Square Root

A^{1/2} such that A^{1/2} A^{1/2} = A. For SPD matrices, use the eigendecomposition.

```python
def sqrtm_eig(A):
    eigvals, eigvecs = np.linalg.eigh(A)
    return eigvecs @ np.diag(np.sqrt(eigvals)) @ eigvecs.T
```

## Schur–Parlett Algorithm

For general matrix functions, reduce to triangular form (Schur), then compute the function on triangular blocks.

## What You'll Implement

- Series-based matrix exponential
- Scaling-and-squaring expm
- Matrix logarithm via inverse scaling-and-squaring
- Matrix square root (eigendecomposition and Denman–Beavers)
- Schur–Parlett for general functions
- Visualize matrix function dynamics (e.g., exp(tA))
