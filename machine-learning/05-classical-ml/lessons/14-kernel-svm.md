# Lesson 05.14: Kernel SVM

## Learning Objectives
- Understand the kernel trick for non-linear SVMs
- Implement common kernels (RBF, polynomial, sigmoid)
- Apply the representer theorem
- Tune kernel hyperparameters via cross-validation

## Kernel Trick
For non-linear decision boundaries, map data to a higher-dimensional feature space via $\phi(x)$:

$$f(x) = w^\top \phi(x) + b$$

The dual formulation only requires inner products $\phi(x_i)^\top \phi(x_j)$, which can be replaced by a kernel function:

$$K(x_i, x_j) = \langle \phi(x_i), \phi(x_j) \rangle$$

The dual becomes:

$$\max_\alpha \sum_i \alpha_i - \frac12 \sum_{i,j} \alpha_i \alpha_j y_i y_j K(x_i, x_j)$$

Decision function: $f(x) = \sum_i \alpha_i y_i K(x_i, x) + b$

**The kernel trick**: Never need to compute $\phi(x)$ explicitly — only need to evaluate $K(x, z)$.

## Common Kernels

| Kernel | $K(x, z)$ | Parameters | Feature Space |
|--------|-----------|------------|---------------|
| Linear | $x^\top z$ | — | Original |
| Polynomial | $(\gamma x^\top z + r)^d$ | $\gamma, r, d$ | Degree-$d$ monomials |
| RBF (Gaussian) | $\exp(-\gamma \|x-z\|^2)$ | $\gamma$ | Infinite-dimensional |
| Sigmoid | $\tanh(\gamma x^\top z + r)$ | $\gamma, r$ | Varies |
| Laplacian | $\exp(-\gamma \|x-z\|_1)$ | $\gamma$ | Infinite |
| Chi-squared | $\exp(-\gamma \sum_j \frac{(x_j-z_j)^2}{x_j+z_j})$ | $\gamma$ | Histogram |

### RBF Kernel Properties
- $K(x, x) = 1$ (bounded, normalized)
- Universal approximator (can learn any continuous function given enough data)
- $\gamma$ controls radius of influence: large $\gamma$ = narrow kernel (complex boundary), small $\gamma$ = wide kernel (smooth boundary)
- Infinitely differentiable (smooth decision boundary)

## Representer Theorem
The optimal $w$ in kernelized SVM lies in the span of training data:

$$w = \sum_{i=1}^n \alpha_i y_i \phi(x_i)$$

This is why SVMs are sparse: most $\alpha_i = 0$, only support vectors define the solution. The theorem applies to any regularized empirical risk minimizer with a convex loss and RKHS norm penalty.

## Mercer's Theorem
A function $K(x, z)$ is a valid kernel (positive definite) if for any set of points $\{x_i\}$, the Gram matrix $K_{ij} = K(x_i, x_j)$ is positive semidefinite.

Valid kernels can be combined:
- Sum: $K_1 + K_2$ is a kernel
- Product: $K_1 \cdot K_2$ is a kernel
- Scaling: $c \cdot K$ is a kernel for $c > 0$
- Composition with polynomial: $p(K)$ is a kernel if $p$ has positive coefficients

## Kernel Selection and Tuning

### RBF Parameter Grid
Log-scale search: $\gamma \in \{2^{-15}, 2^{-13}, \dots, 2^3\}$, $C \in \{2^{-5}, 2^{-3}, \dots, 2^{15}\}$

Rule of thumb: start with $\gamma = 1/d$ (inverse of feature dimension).

### Practical Guidelines
| Dataset | Suggested Kernel |
|---------|-----------------|
| High-dimensional, sparse ($d \gg n$, text) | Linear |
| Low-dimensional, dense | RBF |
| Images (raw pixels) | RBF |
| Structured with known similarity | Custom kernel |
| Histogram features | Chi-squared |
| Time series | DTW kernel |

## Code: Kernel Functions

```python
import numpy as np
from scipy.spatial.distance import cdist, pdist, squareform

def rbf_kernel(X1, X2, gamma=1.0):
    """RBF kernel matrix between two sets of points"""
    dists = cdist(X1, X2, 'sqeuclidean')
    return np.exp(-gamma * dists)

def poly_kernel(X1, X2, degree=3, gamma=1.0, coef0=1.0):
    """Polynomial kernel"""
    return (gamma * X1 @ X2.T + coef0) ** degree

def sigmoid_kernel(X1, X2, gamma=1.0, coef0=0.0):
    """Sigmoid kernel"""
    return np.tanh(gamma * X1 @ X2.T + coef0)

def laplacian_kernel(X1, X2, gamma=1.0):
    """Laplacian kernel (L1 distance)"""
    dists = cdist(X1, X2, 'cityblock')
    return np.exp(-gamma * dists)
```

## Practical Considerations
- **Feature scaling**: Absolutely essential for RBF kernel — all features must have equal influence
- **Memory**: Kernel matrix is $n \times n$ — $O(n^2)$ storage limits to $n < 10^5$
- **Training time**: $O(n^2)$ to $O(n^3)$ with SMO — consider approximations for large data
- **Overfitting**: Large $\gamma$ (narrow kernel) causes overfitting; cross-validate carefully
- **Multiple kernel learning**: Combine kernels using learned weights for heterogeneous data
- **Nyström approximation**: Sample $m \ll n$ points to approximate kernel matrix in $O(m^3)$

## Limitations
- No interpretability of the decision function in feature space
- Kernel matrix computation is $O(n^2 d)$ memory and time
- Selecting kernel hyperparameters requires expensive grid search
- Cannot handle very large datasets without approximations

## References
- Boser, Guyon, Vapnik, "A Training Algorithm for Optimal Margin Classifiers" (COLT 1992)
- Schölkopf & Smola, "Learning with Kernels" (2002)
- Shawe-Taylor & Cristianini, "Kernel Methods for Pattern Analysis" (2004)
- Hsu, Chang, Lin, "A Practical Guide to Support Vector Classification" (2003)
