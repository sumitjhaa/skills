# 05. Matrix Multiplication: Naive, Strassen, Cache-Oblivious, Tiled

## Introduction

Matrix multiplication is the workhorse of scientific computing. The naive algorithm is O(n³), but better algorithms and cache-aware implementations can dramatically improve performance.

## Naive Algorithm

```python
import numpy as np

def matmul_naive(A, B):
    m, n = A.shape
    n2, p = B.shape
    assert n == n2
    C = np.zeros((m, p))
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i, j] += A[i, k] * B[k, j]
    return C
```

This has O(m n p) complexity and poor cache behavior.

## Strassen's Algorithm

Strassen multiplies 2×2 block matrices using 7 multiplications instead of 8:

M₁ = (A₁₁ + A₂₂)(B₁₁ + B₂₂)
M₂ = (A₂₁ + A₂₂)B₁₁
M₃ = A₁₁(B₁₂ − B₂₂)
M₄ = A₂₂(B₂₁ − B₁₁)
M₅ = (A₁₁ + A₁₂)B₂₂
M₆ = (A₂₁ − A₁₁)(B₁₁ + B₁₂)
M₇ = (A₁₂ − A₂₂)(B₂₁ + B₂₂)

Result:
C₁₁ = M₁ + M₄ − M₅ + M₇
C₁₂ = M₃ + M₅
C₂₁ = M₂ + M₄
C₂₂ = M₁ − M₂ + M₃ + M₆

```python
def strassen(A, B):
    n = A.shape[0]
    if n <= 64:  # Fall back to naive
        return A @ B
    mid = n // 2
    A11, A12 = A[:mid,:mid], A[:mid,mid:]
    A21, A22 = A[mid:,:mid], A[mid:,mid:]
    B11, B12 = B[:mid,:mid], B[:mid,mid:]
    B21, B22 = B[mid:,:mid], B[mid:,mid:]
    M1 = strassen(A11 + A22, B11 + B22)
    M2 = strassen(A21 + A22, B11)
    M3 = strassen(A11, B12 - B22)
    M4 = strassen(A22, B21 - B11)
    M5 = strassen(A11 + A12, B22)
    M6 = strassen(A21 - A11, B11 + B12)
    M7 = strassen(A12 - A22, B21 + B22)
    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6
    return np.block([[C11, C12], [C21, C22]])
```

## Tiled (Blocked) Multiplication

Tile the matrices to improve cache locality. Work on sub-blocks that fit in L1 cache:

```python
def matmul_tiled(A, B, tile_size=32):
    m, n = A.shape
    n2, p = B.shape
    C = np.zeros((m, p))
    for i in range(0, m, tile_size):
        for j in range(0, p, tile_size):
            for k in range(0, n, tile_size):
                i_end = min(i + tile_size, m)
                j_end = min(j + tile_size, p)
                k_end = min(k + tile_size, n)
                C[i:i_end, j:j_end] += A[i:i_end, k:k_end] @ B[k:k_end, j:j_end]
    return C
```

## Cache-Oblivious Algorithm

Recursively split the largest dimension, achieving optimal cache behavior without knowing cache size:

```python
def matmul_cache_oblivious(A, B):
    m, n = A.shape
    n2, p = B.shape
    if m <= 32 or n <= 32 or p <= 32:
        return A @ B
    if m >= max(n, p):
        mid = m // 2
        return np.vstack([matmul_cache_oblivious(A[:mid], B),
                          matmul_cache_oblivious(A[mid:], B)])
    elif n >= max(m, p):
        mid = n // 2
        return (matmul_cache_oblivious(A[:, :mid], B[:mid]) +
                matmul_cache_oblivious(A[:, mid:], B[mid:]))
    else:
        mid = p // 2
        return np.hstack([matmul_cache_oblivious(A, B[:, :mid]),
                          matmul_cache_oblivious(A, B[:, mid:])])
```

## Cache Experiments

```python
import time
for n in [64, 128, 256, 512]:
    A = np.random.randn(n, n)
    B = np.random.randn(n, n)
    start = time.time()
    C = matmul_tiled(A, B)
    tiled_time = time.time() - start
    start = time.time()
    C2 = A @ B  # numpy (BLAS)
    blas_time = time.time() - start
    print(f"n={n}: tiled={tiled_time:.4f}s, BLAS={blas_time:.4f}s")
```

## What You'll Implement

- Naive O(n³) matrix multiplication
- Strassen's algorithm with crossover
- Tiled/blocked multiplication with configurable tile size
- Cache-oblivious multiplication
- Performance benchmarking and comparison
- Cache miss analysis visualization
