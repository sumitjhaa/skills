# 18. Krylov Methods: Arnoldi, Lanczos, GMRES, CG, MINRES, BiCGSTAB

## Introduction

Krylov subspace methods are the most important class of iterative solvers for large sparse linear systems. The Krylov subspace is:

Kₖ(A, **b**) = span{**b**, A**b**, A²**b**, ..., A^{k−1}**b**}

## Arnoldi Iteration

For general (non-symmetric) matrices, Arnoldi builds an orthonormal basis of the Krylov subspace and produces an upper Hessenberg matrix Hₖ:

```python
def arnoldi(A, k):
    n = A.shape[0]
    v = b / np.linalg.norm(b)
    V = np.zeros((n, k+1))
    V[:, 0] = v
    H = np.zeros((k+1, k))
    for j in range(k):
        w = A @ V[:, j]
        for i in range(j+1):
            H[i, j] = np.dot(V[:, i], w)
            w -= H[i, j] * V[:, i]
        H[j+1, j] = np.linalg.norm(w)
        if H[j+1, j] > 1e-14:
            V[:, j+1] = w / H[j+1, j]
        else:
            break
    return V, H
```

## GMRES

GMRES minimizes ||A**x** − **b**||₂ over the Krylov subspace using Arnoldi.

## Lanczos Iteration

For symmetric matrices, Arnoldi simplifies to a three-term recurrence (Lanczos), producing a tridiagonal matrix.

## Conjugate Gradient (CG)

For SPD matrices, CG minimizes the A-norm of the error with short recurrences:

```python
def conjugate_gradient(A, b, max_iter=1000, tol=1e-10):
    x = np.zeros(len(b))
    r = b - A @ x
    p = r.copy()
    rsq = r @ r
    for i in range(max_iter):
        Ap = A @ p
        alpha = rsq / (p @ Ap)
        x += alpha * p
        r -= alpha * Ap
        rsq_new = r @ r
        if np.sqrt(rsq_new) < tol:
            break
        p = r + (rsq_new / rsq) * p
        rsq = rsq_new
    return x, i+1
```

## Preconditioners

- **Jacobi**: M = diag(A)
- **ILU**: M = L U (incomplete LU)
- **Multigrid**: Hierarchy of coarser grids

## What You'll Implement

- Arnoldi iteration
- GMRES solver
- Lanczos tridiagonalization
- Conjugate Gradient solver
- Preconditioners (Jacobi, ILU, multigrid)
- Convergence comparison (CG vs GMRES vs BiCGSTAB)
