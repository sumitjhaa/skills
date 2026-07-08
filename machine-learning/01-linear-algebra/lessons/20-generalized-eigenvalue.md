# Lesson 20: Generalized Eigenvalue Problems

## Learning Objectives
- Understand the generalized eigenvalue problem $Ax = \lambda B x$
- Solve via Cholesky or QZ decomposition
- Apply to Fisher discriminant analysis and canonical correlation
- Analyze quadratic pencils and Rayleigh-Ritz for symmetric pairs

## Generalized Eigenvalue Problem

$$A x = \lambda B x$$

- $A, B$: $n \times n$ matrices (typically symmetric, $B \succ 0$)
- $\lambda$: generalized eigenvalue
- $x$: generalized eigenvector
- Reduces to standard when $B = I$

## Reduction to Standard Form

If $B \succ 0$, Cholesky $B = LL^\top$:

$$(L^{-1} A L^{-\top}) (L^\top x) = \lambda (L^\top x)$$

Solve $\tilde{A} y = \lambda y$ where $\tilde{A} = L^{-1} A L^{-\top}$, $y = L^\top x$.

**Caution**: $L^{-1} A L^{-\top}$ may be dense even if $A,B$ are sparse. Use QZ for numerical stability.

## Properties

### When $A$ symmetric, $B \succ 0$:
- Generalized eigenvalues $\lambda_i$ are real
- Generalized eigenvectors are $B$-orthogonal: $x_i^\top B x_j = 0$ for $i \neq j$
- Rayleigh quotient: $\frac{x^\top A x}{x^\top B x} \in [\lambda_{\min}, \lambda_{\max}]$

### Definite Pairs
$(A, B)$ is a **definite pair** if $\min_i |\lambda_i| > 0$. Ensures well-conditioned problem.

## The $Ax = \lambda Bx$ Problem Types

| Type | Matrix properties | Solver |
|------|------------------|--------|
| Symmetric definite | $A = A^\top, B \succ 0$ | Cholesky + symmetric QR |
| Symmetric indefinite | $A = A^\top, B$ symmetric | QZ (LAPACK: xGGEV) |
| Nonsymmetric | No symmetry | QZ algorithm |
| Polynomial | $(\lambda^2 A_2 + \lambda A_1 + A_0)x = 0$ | Linearization (companion form) |

## QZ Algorithm

1. Reduce $A$ to Hessenberg, $B$ to triangular via orthogonal transformations
2. Iteratively apply implicit shifts to converge
3. Compute eigenvalues as ratios: $\lambda_i = \alpha_i / \beta_i$

**Backward stable**: Computes $\tilde{A}, \tilde{B}$ near $A, B$ with exact generalized eigen-decomposition.

## Algorithm: Solving via Cholesky

```python
import numpy as np
from scipy import linalg

def generalized_eigenvalues_symmetric(A, B):
    """Solve Ax = lambda Bx for symmetric A, B >> 0"""
    L = np.linalg.cholesky(B)
    L_inv = np.linalg.inv(L)
    A_tilde = L_inv @ A @ L_inv.T
    eigvals, eigvecs_tilde = np.linalg.eigh(A_tilde)
    eigvecs = L_inv.T @ eigvecs_tilde
    return eigvals, eigvecs

# Using scipy (more stable)
eigvals, eigvecs = linalg.eigh(A, B)  # for symmetric A, B
eigvals, eigvecs = linalg.eig(A, B)   # for general A, B
```

## Applications

### Fisher Discriminant Analysis (FDA)
Find projection maximizing between-class / within-class scatter ratio:

$$S_B w = \lambda S_W w$$

- $S_B$: between-class scatter matrix
- $S_W$: within-class scatter matrix
- Solution: generalized eigenvectors corresponding to largest $\lambda$
- At most $c-1$ non-zero eigenvalues ($c$ = number of classes)

### Canonical Correlation Analysis (CCA)
Find correlations between two sets of variables $X \in \mathbb{R}^{n \times p}$, $Y \in \mathbb{R}^{n \times q}$:

$$\begin{pmatrix} 0 & \Sigma_{XY} \\ \Sigma_{YX} & 0 \end{pmatrix} \begin{pmatrix} a \\ b \end{pmatrix} = \lambda \begin{pmatrix} \Sigma_{XX} & 0 \\ 0 & \Sigma_{YY} \end{pmatrix} \begin{pmatrix} a \\ b \end{pmatrix}$$

- $\Sigma_{XX}, \Sigma_{YY}$: auto-covariance matrices
- $\Sigma_{XY}$: cross-covariance matrix
- Canonical correlations: $\rho_i = \lambda_i$

### Generalized Rayleigh Quotient

$$R(x) = \frac{x^\top A x}{x^\top B x}$$

**Stationarity**: At eigenvectors of $(A, B)$.
**Min-max theorem**: $\lambda_{\min} \leq R(x) \leq \lambda_{\max}$.

### Quadratic Pencil
$Q(\lambda) = \lambda^2 A + \lambda B + C$ arises in:
- Vibration analysis ($M\ddot{x} + C\dot{x} + Kx = 0$)
- Linearized by companion form:
  $$\begin{pmatrix} -B & -C \\ I & 0 \end{pmatrix} \begin{pmatrix} \lambda x \\ x \end{pmatrix} = \lambda \begin{pmatrix} A & 0 \\ 0 & I \end{pmatrix} \begin{pmatrix} \lambda x \\ x \end{pmatrix}$$

## Sensitivity and Conditioning

**Condition number of simple eigenvalue**:

$$\kappa(\lambda) = \frac{\sqrt{|y^* A x|^2 + |y^* B x|^2}}{|y^* B x|} \cdot \frac{\|y\| \|x\|}{|y^* x|}$$

- For symmetric $(A, B)$ with $B \succ 0$: $\kappa(\lambda) = 1$ (perfectly conditioned)
- For non-symmetric: can be arbitrarily ill-conditioned

## Code: Quadcopter Normal Modes (Example)

```python
import numpy as np

# Mass and stiffness matrices for 2-DOF system
M = np.array([[2, 0], [0, 1]])    # Mass matrix (B)
K = np.array([[3, -1], [-1, 1]])  # Stiffness matrix (A)

# Solve Kx = omega^2 Mx
omega_sq, modes = generalized_eigenvalues_symmetric(K, M)
frequencies = np.sqrt(omega_sq)  # Natural frequencies
print(f"Natural frequencies: {frequencies}")
print(f"Mode shapes:\n{modes}")
```

## Practical Considerations
- **Definiteness**: Verify $B \succ 0$ before using Cholesky reduction
- **Scale**: If $B$ is ill-conditioned, use QZ instead
- **Null space**: If $B$ is singular, infinite eigenvalues ($\beta_i = 0$)
- **Complexity**: $O(n^3)$ for dense, iterative methods for sparse
- **Sparse GEP**: Use shift-invert Arnoldi (e.g., scipy.sparse.linalg.eigsh with sigma)

## References
- Golub & Van Loan, "Matrix Computations", Ch. 7
- Parlett, "The Symmetric Eigenvalue Problem", Ch. 15
- Stewart & Sun, "Matrix Perturbation Theory"
- Bai, Demmel, Dongarra, Ruhe, van der Vorst, "Templates for the Solutions of Algebraic Eigenvalue Problems"
- Saad, "Numerical Methods for Large Eigenvalue Problems", Ch. 8
