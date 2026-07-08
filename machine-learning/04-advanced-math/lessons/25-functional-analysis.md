# 04.25 Functional Analysis: Banach and Hilbert Spaces

## Motivation
Functional analysis studies infinite-dimensional vector spaces (function spaces) and the operators on them. It is the mathematical bedrock of kernel methods, neural network approximation theory, and the theory of PDEs underlying physics-informed ML. Understanding Banach and Hilbert spaces is essential for developing rigorous results about the capacity, convergence, and generalisation of learning algorithms.

## Learning Objectives
- Define normed spaces, Banach spaces, and Hilbert spaces with key examples.
- State and apply the Riesz representation theorem and the spectral theorem.
- Understand the role of $L^2$ and RKHS in ML.
- Analyse neural network approximation rates in Sobolev spaces.

## Math Foundation

### Normed Spaces
A normed space $(X, \|\cdot\|)$ is a vector space with a norm satisfying:
1. $\|x\| \ge 0$, equality iff $x = 0$.
2. $\|\alpha x\| = |\alpha| \|x\|$.
3. $\|x + y\| \le \|x\| + \|y\|$ (triangle inequality).

### Banach Spaces
A Banach space is a complete normed space — every Cauchy sequence converges. Examples:
- $\ell^p$: sequences with $\sum |x_n|^p < \infty$.
- $L^p(\Omega)$: functions with $\int_\Omega |f|^p d\mu < \infty$.
- $C([0,1])$: continuous functions with $\|f\|_\infty = \max_{x \in [0,1]} |f(x)|$.
- $W^{k,p}(\Omega)$: Sobolev spaces of functions with $k$ weak derivatives in $L^p$.

### Hilbert Spaces
A Hilbert space is a Banach space equipped with an inner product $\langle \cdot, \cdot \rangle$ inducing the norm $\|x\| = \sqrt{\langle x, x \rangle}$. The inner product satisfies the Cauchy–Schwarz inequality:

$$|\langle x, y \rangle| \le \|x\| \|y\|$$

**Examples**:
- $\ell^2$: square-summable sequences, $\langle x, y \rangle = \sum x_n \bar{y}_n$.
- $L^2(\Omega)$: square-integrable functions, $\langle f, g \rangle = \int f \bar{g}$.
- $H^k(\Omega)$: Sobolev space with $\langle f, g \rangle = \sum_{|\alpha| \le k} \langle D^\alpha f, D^\alpha g \rangle_{L^2}$.

### Riesz Representation Theorem
For a Hilbert space $\mathcal{H}$, every bounded linear functional $f \in \mathcal{H}^*$ can be uniquely represented as:

$$f(x) = \langle x, y_f \rangle$$

for some $y_f \in \mathcal{H}$, with $\|f\| = \|y_f\|$. This identifies $\mathcal{H}^* \cong \mathcal{H}$.

### Spectral Theorem
Every self-adjoint compact operator $T: \mathcal{H} \to \mathcal{H}$ has a spectral decomposition:

$$T = \sum_{i=1}^\infty \lambda_i \langle \cdot, e_i \rangle e_i$$

where $\{e_i\}$ is an orthonormal basis of eigenvectors and $\lambda_i \to 0$. This generalises the eigendecomposition of symmetric matrices.

### Orthogonal Projections and Best Approximation
The orthogonal projection onto a closed subspace $M \subseteq \mathcal{H}$ satisfies:

$$\|x - P_M x\| = \min_{y \in M} \|x - y\|$$

This is the foundation of least squares regression: the optimal predictor is the orthogonal projection of the target function onto the subspace spanned by the features.

## Python Implementation

```python
import numpy as np
from scipy.linalg import eigh

def orthogonal_projection(x, basis):
    """Project x onto span of basis vectors via least squares."""
    # x in R^n, basis is (n x k) matrix
    coefficients = np.linalg.lstsq(basis, x, rcond=None)[0]
    return basis @ coefficients

def function_approx_l2(f, basis_fns, a=-1, b=1, n_quad=1000):
    """Approximate f in L^2([a,b]) using a set of basis functions.
    
    Computes the orthogonal projection using numerical quadrature.
    """
    x = np.linspace(a, b, n_quad)
    dx = (b - a) / (n_quad - 1)
    
    fx = f(x)
    B = np.column_stack([phi(x) for phi in basis_fns])
    
    # Gram matrix G_{ij} = <phi_i, phi_j>_{L^2}
    G = (B * B).sum(axis=0)  # approximate: assumes orthogonal basis
    # Actually: G_ij = int phi_i(x) phi_j(x) dx
    G = B.T @ B * dx
    
    # RHS: b_i = <f, phi_i>  
    rhs = B.T @ fx * dx
    
    coeffs = np.linalg.solve(G, rhs)
    return coeffs, B @ coeffs

# Example: approximate f(x) = |x| in L^2([-1,1]) using Legendre polynomials
def legendre_poly(n):
    """Return n-th Legendre polynomial as a function."""
    if n == 0:
        return lambda x: np.ones_like(x)
    elif n == 1:
        return lambda x: x
    # Use recurrence: (n+1)P_{n+1} = (2n+1)xP_n - nP_{n-1}
    p0 = lambda x: np.ones_like(x)
    p1 = lambda x: x
    for i in range(2, n+1):
        p2 = lambda x, p0=p0, p1=p1, i=i: ((2*i-1)*x*p1(x) - (i-1)*p0(x)) / i
        p0, p1 = p1, p2
    return p1

f = lambda x: np.abs(x)
basis = [legendre_poly(i) for i in range(6)]
coeffs, approx = function_approx_l2(f, basis)
print(f"L^2 approximation error: {np.sqrt(np.mean((f(np.linspace(-1,1,1000)) - approx)**2)):.4f}")
```

## Visualization
Plot the absolute value function $|x|$ and its $L^2$ approximation using truncated Legendre series (Gibbs phenomenon at the kink). A second panel shows the eigenvalue decay of a compact operator (e.g., the Hilbert–Schmidt integral operator for the RBF kernel) — exponential decay indicates the operator is well-approximated by a low-rank truncation. A third panel shows the orthogonal projection of a 2D point onto a subspace.

## Connections to Machine Learning

### RKHS and Kernel Methods
The RKHS $\mathcal{H}_k$ is a Hilbert space of functions where evaluation is a bounded linear functional. The Riesz representation theorem gives:

$$f(x) = \langle f, k(\cdot, x) \rangle_{\mathcal{H}_k}$$

The representer theorem reduces empirical risk minimisation in $\mathcal{H}_k$ to a finite-dimensional problem.

### Sobolev Spaces and Neural Network Approximation
Sobolev spaces $W^{k,p}$ contain functions whose weak derivatives up to order $k$ are in $L^p$. Key results in approximation theory:
- **Barron spaces**: functions with bounded Fourier-domain $L^1$ norm can be approximated by 2-layer ReLU networks with $O(1/\sqrt{m})$ error.
- **Spectral bias**: neural networks learn low-frequency functions first (a consequence of the eigenvalue decay of the neural tangent kernel operator in $\mathcal{H}^1$).
- **Curse of dimensionality**: approximating functions in $W^{k,\infty}$ with ReLU networks requires $O(\epsilon^{-d/k})$ parameters — deep networks can be exponentially more efficient than shallow ones for certain hierarchical function classes.

### Operator Learning
Neural operators (FNO, DeepONet) learn mappings between infinite-dimensional function spaces:

$$\mathcal{G}: U \to V, \quad u \mapsto v \quad \text{where } u, v \in L^2(\Omega)$$

The FNO parameterises the operator in Fourier space: each layer applies an integral kernel $\kappa_\theta$ as a convolution:

$$( \mathcal{K}_\theta v)(x) = \mathcal{F}^{-1}\big( \mathcal{F}(\kappa_\theta) \cdot \mathcal{F}(v) \big)(x)$$

Functional analysis ensures that the operator norm of $\mathcal{G}_\theta - \mathcal{G}^*$ can be controlled as the discretisation refines.

### Regularisation in Hilbert Spaces
Tikhonov regularisation solves:

$$\min_{f \in \mathcal{H}} \frac{1}{n} \sum_{i=1}^n \ell(y_i, f(x_i)) + \lambda \|f\|_{\mathcal{H}}^2$$

By the representer theorem, the solution is $f(x) = \sum_i \alpha_i k(x_i, x)$. In a general Hilbert space, this is equivalent to spectral filtering: the solution is obtained by applying a filter function to the eigenvalues of the sample covariance operator.

## Practical Considerations

### Finite vs Infinite Dimensions
- In ML, we work in finite-dimensional subspaces (finite samples, finite parameters) but the target function typically lives in an infinite-dimensional space.
- The discretisation error (how well a finite subspace approximates the target) decays with the number of basis functions / parameters.
- The generalisation error has two components: approximation error (bias) and estimation error (variance).

### Choosing the Right Space
- $L^2$: suitable when only mean-squared error matters (regression).
- $L^1$: robust to outliers (absolute deviation), but not a Hilbert space.
- $L^\infty$: guarantees uniform approximation but hard to estimate.
- $H^1$: includes derivative information; relevant for PDEs and physics-informed learning.
- RKHS: convenient for kernel methods via the representer theorem.

## References
- Kreyszig, *Introductory Functional Analysis with Applications*, Wiley 1989
- Reed & Simon, *Functional Analysis*, Academic Press 1980
- Cucker & Smale, "On the Mathematical Foundations of Learning," *Bull. Amer. Math. Soc.*, 2002
- Lu, Jin, Karniadakis, "DeepONet: Learning Nonlinear Operators for Identifying Differential Equations," *NeurIPS 2019*
- Li et al., "Fourier Neural Operator for Parametric Partial Differential Equations," *ICLR 2021*
- Steinwart & Christmann, *Support Vector Machines*, Springer 2008
