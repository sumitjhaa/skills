# Phase 01 — Linear Algebra

## 1. Phase Overview

| Field | Value |
|---|---|
| **Phase** | 01 — Linear Algebra |
| **Lessons** | 30 |
| **Core topics** | Vectors, vector spaces, linear transformations, matrix decompositions (QR, Cholesky, SVD), eigenvalues, matrix norms, low-rank approximations, perturbation theory, positive-definite matrices, NMF, tensor decompositions, random matrix theory, sparse matrices, Krylov methods, matrix functions, generalized eigenvalue problems, graph Laplacians, spectral graph theory, matrix completion, tensor methods, INDSCAL/PARAFAC2, constrained CP, tensor networks, sensitivity/stability, PCA-SVD pipeline, tensor recommendation |

## 2. Prerequisites

- **Prior phases:** None (foundational)
- **Python frameworks:** [`../../python-frameworks/numpy-pandas/`](../../python-frameworks/numpy-pandas/) (array operations)

## 3. Lesson Table

| # | Title | What You'll Learn | Lesson | Code | Cross-References |
|---|---|---|---|---|---|
| 01 | Vectors | Dot, cross, outer products, projections | [lesson](lessons/01-vectors.md) | [code](code/01-vectors.py) | Used in: Phase 02 (gradients), Phase 05 (PCA), Phase 06 (backprop) |
| 02 | Vector Spaces | Span, basis, dimension, linear independence | [lesson](lessons/02-vector-spaces.md) | [code](code/02-vector-spaces.py) | Used in: Phase 03 (random vars), Phase 04 (RKHS) |
| 03 | Linear Transformations | Matrix as linear map, kernel, image, rank-nullity | [lesson](lessons/03-linear-transformations.md) | [code](code/03-linear-transformations.py) | Used in: Phase 06 (layer as transform), Phase 07 (neural ODEs) |
| 04 | Gaussian Elimination | LU decomposition, pivoting, computational complexity | [lesson](lessons/04-gaussian-elimination.md) | [code](code/04-gaussian-elimination.py) | Used in: Phase 02 (Newton methods), Phase 05 (solvers) |
| 05 | Matrix Multiplication | Strassen, distributed, block algorithms | [lesson](lessons/05-matrix-multiplication.md) | [code](code/05-matrix-multiplication.py) | Used in: Phase 06 (batched matmul), Phase 08 (convolutions) |
| 06 | QR Decomposition | Gram–Schmidt, Householder, Givens, least squares | [lesson](lessons/06-qr-decomposition.md) | [code](code/06-qr-decomposition.py) | Used in: Phase 05 (linear regression), Phase 10 (least-squares DP) |
| 07 | Cholesky Decomposition | LDL, pivoted, semidefinite | [lesson](lessons/07-cholesky.md) | [code](code/07-cholesky.py) | Used in: Phase 03 (GP regression), Phase 02 (Newton) |
| 08 | Eigenvalues | Power iteration, QR algorithm, eigendecomposition | [lesson](lessons/08-eigenvalues.md) | [code](code/08-eigenvalues.py) | Used in: Phase 05 (PCA), Phase 06 (spectral norms) |
| 09 | SVD | Full, thin, randomized, applications | [lesson](lessons/09-svd.md) | [code](code/09-svd.py) | Used in: Phase 05 (PCA), Phase 08 (image compression), Phase 09 (word embeddings) |
| 10 | Matrix Norms | Spectral, Frobenius, nuclear, induced norms | [lesson](lessons/10-matrix-norms.md) | [code](code/10-matrix-norms.py) | Used in: Phase 06 (weight decay), Phase 02 (Lipschitz) |
| 11 | Low-Rank Approximations | Eckart–Young, randomized SVD, CUR | [lesson](lessons/11-low-rank-approximations.md) | [code](code/11-low-rank-approximations.py) | Used in: Phase 05 (collaborative filtering), Phase 09 (embeddings) |
| 12 | Perturbation Theory | Condition number, backward stability, Bauer–Fike | [lesson](lessons/12-perturbation-theory.md) | [code](code/12-perturbation-theory.py) | Used in: Phase 06 (numerical stability) |
| 13 | Positive Definite Matrices | Definiteness, quadratic forms, Cholesky | [lesson](lessons/13-positive-definite.md) | [code](code/13-positive-definite.py) | Used in: Phase 02 (convexity), Phase 03 (covariance) |
| 14 | NMF | Alternating least squares, multiplicative updates | [lesson](lessons/14-nmf.md) | [code](code/14-nmf.py) | Used in: Phase 05 (topic modeling), Phase 09 (NLP) |
| 15 | Tensor Decompositions | CP, Tucker, tensor trains | [lesson](lessons/15-tensor-decompositions.md) | [code](code/15-tensor-decompositions.py) | Used in: Phase 06 (multi-dim data) |
| 16 | Random Matrix Theory | Wigner semicircle, Marchenko–Pastur, spectral | [lesson](lessons/16-random-matrix-theory.md) | [code](code/16-random-matrix-theory.py) | Used in: Phase 03 (covariance estimation), Phase 06 (initialization) |
| 17 | Sparse Matrices | CSR/CSC, reordering, sparse solvers | [lesson](lessons/17-sparse-matrices.md) | [code](code/17-sparse-matrices.py) | Used in: Phase 05 (large-scale ML), Phase 09 (sparse attention) |
| 18 | Krylov Methods | CG, GMRES, Lanczos, Arnoldi | [lesson](lessons/18-krylov-methods.md) | [code](code/18-krylov-methods.py) | Used in: Phase 02 (CG optimization) |
| 19 | Matrix Functions | Exp, log, sqrt of matrices, Fréchet derivative | [lesson](lessons/19-matrix-functions.md) | [code](code/19-matrix-functions.py) | Used in: Phase 06 (normalization layers), Phase 07 (neural ODEs) |
| 20 | Generalized Eigenvalue | Rayleigh quotient, generalized SVD | [lesson](lessons/20-generalized-eigenvalue.md) | [code](code/20-generalized-eigenvalue.py) | Used in: Phase 05 (LDA), Phase 08 (vision) |
| 21 | Graph Laplacians | Adjacency, degree, Laplacian, normalized Laplacian | [lesson](lessons/21-graph-laplacians.md) | [code](code/21-graph-laplacians.py) | Used in: Phase 05 (spectral clustering), Phase 04 (graph theory) |
| 22 | Spectral Graph Theory | Eigenvalues of Laplacian, Cheeger, expanders | [lesson](lessons/22-spectral-graph-theory.md) | [code](code/22-spectral-graph-theory.py) | Used in: Phase 05 (manifold learning) |
| 23 | Matrix Completion | Nuclear norm minimization, alternating minimization | [lesson](lessons/23-matrix-completion.md) | [code](code/23-matrix-completion.py) | Used in: Phase 09 (recommender systems) |
| 24 | Tensor Methods | Tensor trains, tensor SVD, tensor regression | [lesson](lessons/24-tensor-methods.md) | [code](code/24-tensor-methods.py) | Used in: Phase 06 (multi-modal) |
| 25 | INDSCAL / PARAFAC2 | Individual differences, three-way data | [lesson](lessons/25-indscal-parafac2.md) | [code](code/25-indscal-parafac2.py) | Used in: Phase 03 (longitudinal data) |
| 26 | Constrained CP | Non-negativity, sparsity, smoothness constraints | [lesson](lessons/26-constrained-cp.md) | [code](code/26-constrained-cp.py) | Used in: Phase 05 (interpretable models) |
| 27 | Tensor Networks | PEPS, MERA, tensor renormalization | [lesson](lessons/27-tensor-networks.md) | [code](code/27-tensor-networks.py) | Used in: Phase 07 (quantum ML) |
| 28 | Sensitivity & Stability | Condition numbers for tensors, perturbation bounds | [lesson](lessons/28-sensitivity-stability.md) | [code](code/28-sensitivity-stability.py) | Used in: Phase 06 (robust training) |
| 29 | PCA-SVD Pipeline | Randomized PCA, whitening, scree plots | [lesson](lessons/29-pca-svd-pipeline.md) | [code](code/29-pca-svd-pipeline.py) | Used in: Phase 05 (PCA), Phase 08 (feature reduction) |
| 30 | Tensor Recommendation | Tensor-based recommender systems, CP/WOPT | [lesson](lessons/30-tensor-recommendation.md) | [code](code/30-tensor-recommendation.py) | Used in: Phase 09 (recommender systems) |

## 4. Builds Toward

- **ALL subsequent phases** — Linear algebra is the core mathematical language of ML
- **Phase 02** (gradients, Jacobians, Hessians as linear operators)
- **Phase 05** (PCA, SVD, linear models, kernel methods)
- **Phase 06** (matrix multiply in neural nets, backprop as Jacobian products)
- **Phase 08** (image transformations, convolutions as linear ops)
- **Phase 09** (embeddings, attention as inner products)

## 5. Quick Start

```bash
python3 code/01-vectors.py
```
