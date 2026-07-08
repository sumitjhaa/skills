# Lesson 13: Positive Definite Matrices

## Learning Objectives
- Understand positive definiteness and its geometric meaning
- Recognize equivalent characterizations of positive (semi)definite matrices
- Apply Cholesky decomposition and test positive definiteness
- Analyze covariance matrices and quadratic forms

## Positive Definite Matrices
A symmetric matrix $A \in \mathbb{S}^n$ is **positive definite** ($A \succ 0$) if:

$$x^\top A x > 0 \quad \forall x \neq 0$$

**Positive semidefinite** ($A \succeq 0$): $x^\top A x \geq 0 \quad \forall x$.

## Equivalent Characterizations

| Condition | Positive Definite | Positive Semidefinite |
|-----------|-------------------|-----------------------|
| Quadratic form | $x^\top A x > 0$, $x \neq 0$ | $x^\top A x \geq 0$ |
| Eigenvalues | $\lambda_i > 0$ | $\lambda_i \geq 0$ |
| Leading principal minors | All $> 0$ | All $\geq 0$ |
| Cholesky decomposition | Exists $L$ lower triangular, invertible | Exists $L$ with zeros on diag |
| Square root | Unique $A^{1/2} \succ 0$ | Exists $A^{1/2} \succeq 0$ |
| Decomposition | $A = B^\top B$, $B$ invertible | $A = B^\top B$ |

### Leading Principal Minors (Sylvester's Criterion)
$A$ is positive definite iff all leading principal minors are positive:

$$\det(A_{1:k,1:k}) > 0 \quad \forall k \in \{1, \dots, n\}$$

For positive semidefinite: all principal minors (not just leading) must be non-negative.

## Example: $2 \times 2$ Case

$$A = \begin{pmatrix} a & b \\ b & c \end{pmatrix}$$

$A \succ 0 \iff a > 0$ and $ac - b^2 > 0$. This means the ellipse $x^\top A x = 1$ is finite and non-degenerate.

## Geometry of Quadratic Forms

Level sets of $x^\top A x = c$ are ellipsoids when $A \succ 0$:

- Axes aligned with eigenvectors of $A$
- Axis lengths proportional to $1/\sqrt{\lambda_i}$
- Volume proportional to $\det(A)^{-1/2}$

**Generalized ellipsoid**: $\{x : (x-\mu)^\top \Sigma^{-1} (x-\mu) \leq 1\}$ defines a confidence region for Gaussian $N(\mu, \Sigma)$.

## Covariance Matrices

Any valid covariance matrix $\Sigma$ is positive semidefinite:

- $\Sigma = \mathbb{E}[(X-\mu)(X-\mu)^\top]$
- For any $v$: $v^\top \Sigma v = \text{Var}(v^\top X) \geq 0$
- Eigenvalues represent variance along principal components

**Sample covariance**: $\hat{\Sigma} = \frac{1}{n-1} \sum_i (x_i - \bar{x})(x_i - \bar{x})^\top$

## Cholesky Decomposition

If $A \succ 0$, there exists a unique lower triangular $L$ such that $A = LL^\top$ with $L_{ii} > 0$.

**Algorithm** ($O(n^3/3)$):

$$L_{jj} = \sqrt{A_{jj} - \sum_{k=1}^{j-1} L_{jk}^2}$$

$$L_{ij} = \frac{1}{L_{jj}}\left(A_{ij} - \sum_{k=1}^{j-1} L_{ik}L_{jk}\right), \quad i > j$$

**Example**:

$$A = \begin{pmatrix} 4 & 2 \\ 2 & 5 \end{pmatrix} \Rightarrow L = \begin{pmatrix} 2 & 0 \\ 1 & 2 \end{pmatrix}$$

Check: $LL^\top = \begin{pmatrix} 4 & 2 \\ 2 & 1+4 \end{pmatrix} = A$.

### Modified Cholesky
If $A$ is nearly singular, add a small $\tau > 0$ to diagonal: $A + \tau I$. Used in optimization (quasi-Newton).

## Positive Definiteness Tests

0. Symmetry check first (PD requires symmetric by definition)
1. Cholesky decomposition: if it succeeds, $A \succ 0$
2. Check all eigenvalues $> 0$ ($O(n^3)$)
3. Sylvester's criterion (not recommended for large $n$ due to stability)
4. Check diagonal $A_{ii} > 0$ (necessary but not sufficient)

## Code: Cholesky and PD Testing

```python
import numpy as np

def is_positive_definite(A, tol=1e-10):
    """Test via Cholesky decomposition"""
    A = (A + A.T) / 2
    try:
        L = np.linalg.cholesky(A)
        return True
    except np.linalg.LinAlgError:
        return False

def modified_cholesky(A, tau=1e-6):
    """Modified Cholesky for near-PD matrices"""
    A = (A + A.T) / 2
    n = A.shape[0]
    A_mod = A.copy()
    for k in range(n):
        if A_mod[k, k] <= tau:
            A_mod[k, k] = tau + np.abs(A_mod[k, k])
        for i in range(k+1, n):
            A_mod[i, k] = A_mod[k, i] / A_mod[k, k]
            A_mod[i, i] -= A_mod[i, k] ** 2 * A_mod[k, k]
            A_mod[k, i] = 0
    return np.linalg.cholesky(A_mod)
```

## Applications

| Application | Why PD matters |
|-------------|---------------|
| Linear systems $Ax = b$ | PD $\Rightarrow$ unique solution, efficient solvers |
| Newton's method | Hessian $\nabla^2 f(x) \succ 0$ for convexity |
| Covariance estimation | $\Sigma \succeq 0$ always |
| Ridge regression | $X^\top X + \lambda I \succ 0$ for any $\lambda > 0$ |
| Kernel methods | Kernel matrix $K \succeq 0$ (Mercer's theorem) |
| Trust region methods | Quadratic model must be PD for unique minimizer |

## Common Mistakes
- **Non-symmetric**: PD requires symmetric (Hermitian). For $A$ not symmetric, $x^\top A x$ can be rewritten using $(A + A^\top)/2$.
- **Near-singular**: Floating-point errors can make a PD matrix appear indefinite. Use tolerance-based tests.
- **Leading vs all minors**: For PSD, all principal minors must be non-negative (Sylvester's criterion for PSD is more restrictive).

## References
- Strang, "Linear Algebra and Learning from Data", Ch. VII
- Boyd & Vandenberghe, "Convex Optimization", Ch. 9
- Golub & Van Loan, "Matrix Computations", Ch. 4 (Cholesky)
- Higham, "Accuracy and Stability of Numerical Algorithms", Ch. 10
- Horn & Johnson, "Matrix Analysis", Ch. 7
