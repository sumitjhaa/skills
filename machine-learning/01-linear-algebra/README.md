# Phase 01: Linear Algebra

> Foundations of linear algebra for machine learning — from vectors to tensor networks.

## Overview

This phase covers the full spectrum of linear algebra used in modern machine learning: basic vector/ matrix operations, decompositions (LU, QR, SVD, Cholesky, eigenvalue), spectral graph theory, matrix completion, random matrix theory, sparse solvers, Krylov methods, and tensor decompositions. Each topic is accompanied by a standalone Python implementation and a lesson document.

## Lessons

| #  | Lesson | Code | Topic |
|----|--------|------|-------|
| 01 | [01-vectors](lessons/01-vectors.md) | [01-vectors.py](code/01-vectors.py) | Vectors: dot, cross, outer, projections |
| 02 | [02-vector-spaces](lessons/02-vector-spaces.md) | [02-vector-spaces.py](code/02-vector-spaces.py) | Vector spaces: span, basis, Gram–Schmidt |
| 03 | [03-linear-transformations](lessons/03-linear-transformations.md) | [03-linear-transformations.py](code/03-linear-transformations.py) | Linear transformations, matrix representations |
| 04 | [04-gaussian-elimination](lessons/04-gaussian-elimination.md) | [04-gaussian-elimination.py](code/04-gaussian-elimination.py) | Gaussian elimination, LU, pivoting |
| 05 | [05-matrix-multiplication](lessons/05-matrix-multiplication.md) | [05-matrix-multiplication.py](code/05-matrix-multiplication.py) | Matrix multiply: naive, Strassen, tiled |
| 06 | [06-qr-decomposition](lessons/06-qr-decomposition.md) | [06-qr-decomposition.py](code/06-qr-decomposition.py) | QR: Gram–Schmidt, Householder, Givens |
| 07 | [07-cholesky](lessons/07-cholesky.md) | [07-cholesky.py](code/07-cholesky.py) | Cholesky, LDL^T decomposition |
| 08 | [08-eigenvalues](lessons/08-eigenvalues.md) | [08-eigenvalues.py](code/08-eigenvalues.py) | Eigenvalues: power iteration, QR algorithm |
| 09 | [09-svd](lessons/09-svd.md) | [09-svd.py](code/09-svd.py) | SVD: full, truncated, randomized |
| 10 | [10-matrix-norms](lessons/10-matrix-norms.md) | [10-matrix-norms.py](code/10-matrix-norms.py) | Matrix norms: Frobenius, spectral, nuclear |
| 11 | [11-low-rank-approximations](lessons/11-low-rank-approximations.md) | [11-low-rank-approximations.py](code/11-low-rank-approximations.py) | Low-rank approximations, Eckart–Young |
| 12 | [12-perturbation-theory](lessons/12-perturbation-theory.md) | [12-perturbation-theory.py](code/12-perturbation-theory.py) | Perturbation theory, condition numbers |
| 13 | [13-positive-definite](lessons/13-positive-definite.md) | [13-positive-definite.py](code/13-positive-definite.py) | Positive definite matrices, quadratic forms |
| 14 | [14-nmf](lessons/14-nmf.md) | [14-nmf.py](code/14-nmf.py) | Non-negative Matrix Factorization |
| 15 | [15-tensor-decompositions](lessons/15-tensor-decompositions.md) | [15-tensor-decompositions.py](code/15-tensor-decompositions.py) | Tensor decompositions: CP, Tucker, TT |
| 16 | [16-random-matrix-theory](lessons/16-random-matrix-theory.md) | [16-random-matrix-theory.py](code/16-random-matrix-theory.py) | Random matrix theory, phase transitions |
| 17 | [17-sparse-matrices](lessons/17-sparse-matrices.md) | [17-sparse-matrices.py](code/17-sparse-matrices.py) | Sparse matrices: CSR, CSC, COO |
| 18 | [18-krylov-methods](lessons/18-krylov-methods.md) | [18-krylov-methods.py](code/18-krylov-methods.py) | Krylov methods: Arnoldi, GMRES, CG |
| 19 | [19-matrix-functions](lessons/19-matrix-functions.md) | [19-matrix-functions.py](code/19-matrix-functions.py) | Matrix functions: expm, logm, sqrtm |
| 20 | [20-generalized-eigenvalue](lessons/20-generalized-eigenvalue.md) | [20-generalized-eigenvalue.py](code/20-generalized-eigenvalue.py) | Generalized eigenvalue, GSVD |
| 21 | [21-graph-laplacians](lessons/21-graph-laplacians.md) | [21-graph-laplacians.py](code/21-graph-laplacians.py) | Graph Laplacians, spectral clustering |
| 22 | [22-spectral-graph-theory](lessons/22-spectral-graph-theory.md) | [22-spectral-graph-theory.py](code/22-spectral-graph-theory.py) | Spectral graph theory, graph Fourier |
| 23 | [23-matrix-completion](lessons/23-matrix-completion.md) | [23-matrix-completion.py](code/23-matrix-completion.py) | Matrix completion, SVT algorithm |
| 24 | [24-tensor-methods](lessons/24-tensor-methods.md) | [24-tensor-methods.py](code/24-tensor-methods.py) | Tensor methods for ML |
| 25 | [25-indscal-parafac2](lessons/25-indscal-parafac2.md) | [25-indscal-parafac2.py](code/25-indscal-parafac2.py) | INDSCAL, PARAFAC2, nonnegative CP |
| 26 | [26-constrained-cp](lessons/26-constrained-cp.md) | [26-constrained-cp.py](code/26-constrained-cp.py) | Canonical Polyadic with constraints |
| 27 | [27-tensor-networks](lessons/27-tensor-networks.md) | [27-tensor-networks.py](code/27-tensor-networks.py) | Tensor networks: MPS, TT, PEPS |
| 28 | [28-sensitivity-stability](lessons/28-sensitivity-stability.md) | [28-sensitivity-stability.py](code/28-sensitivity-stability.py) | Sensitivity and stability in ML |
| 29 | [29-pca-svd-pipeline](lessons/29-pca-svd-pipeline.md) | [29-pca-svd-pipeline.py](code/29-pca-svd-pipeline.py) | PCA/SVD pipeline: eigenfaces, compression |
| 30 | [30-tensor-recommendation](lessons/30-tensor-recommendation.md) | [30-tensor-recommendation.py](code/30-tensor-recommendation.py) | Tensor methods for recommendation |

## Prerequisites

- Python 3.10+
- `numpy`, `scipy`, `matplotlib`
- Optional: `tensorly` (for tensor operations in lessons 15, 24–27, 30)

## How to use

```bash
# Run any lesson's code
python code/01-vectors.py

# Read a lesson
cat lessons/01-vectors.md
```
