# 17. Sparse Matrices: CSR, CSC, COO, ELL, HYB

## Introduction

Sparse matrices have most entries equal to zero. Storing them as dense arrays wastes memory and computation. Specialized formats exploit sparsity.

## COO (Coordinate) Format

Store (row, col, value) triples:

```python
rows = [0, 1, 2, 0]
cols = [0, 2, 1, 3]
vals = [1.0, 2.0, 3.0, 4.0]
```

## CSR (Compressed Sparse Row)

Three arrays: values, column indices, row pointers (length n+1, start index of each row).

```python
class CSRMatrix:
    def __init__(self, values, col_indices, row_ptr, shape):
        self.values = values
        self.col_indices = col_indices
        self.row_ptr = row_ptr
        self.shape = shape

    def matvec(self, x):
        n, m = self.shape
        y = np.zeros(n)
        for i in range(n):
            for j in range(self.row_ptr[i], self.row_ptr[i+1]):
                y[i] += self.values[j] * x[self.col_indices[j]]
        return y
```

## CSC (Compressed Sparse Column)

Similar to CSR but column-major. Better for column access patterns.

## ELL (ELLPACK)

Store a fixed number of non-zeros per row in a dense matrix. Good for GPU and vectorization.

## HYB (Hybrid)

Combine ELL (for rows with typical non-zeros) and COO (for rows with excessive non-zeros).

## Sparse Solvers

```python
from scipy.sparse.linalg import spsolve, cg, gmres
x = spsolve(A_sparse, b)
x_cg, info = cg(A_sparse, b, tol=1e-6)
```

## Custom Matvec Performance

```python
def benchmark_matvec(A_dense, A_sparse, x):
    import time
    t0 = time.time()
    y1 = A_dense @ x
    t_dense = time.time() - t0
    t0 = time.time()
    y2 = A_sparse @ x
    t_sparse = time.time() - t0
    return t_dense, t_sparse
```

## What You'll Implement

- COO, CSR, CSC matrix formats from scratch
- Custom matvec for each format
- ELL and HYB formats
- Performance benchmarks vs dense
- Sparse solver via CG
- Compare formats for different sparsity patterns
