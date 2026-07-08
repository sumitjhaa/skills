# Lesson 07.01: KAN (Kolmogorov-Arnold Networks)

## Learning Objectives
- Understand the Kolmogorov-Arnold representation theorem
- Implement KAN layers with learnable edge activations
- Compare KANs with MLPs on approximation and interpretability
- Apply B-spline parameterization for smooth learnable functions

## Theory

### Kolmogorov-Arnold Representation Theorem
Any multivariate continuous function $f: [0,1]^n \to \mathbb{R}$ can be represented as:

$$f(x_1, \dots, x_n) = \sum_{q=0}^{2n} \Phi_q\left(\sum_{p=1}^n \psi_{qp}(x_p)\right)$$

- $\psi_{qp}: [0,1] \to \mathbb{R}$: inner functions (univariate)
- $\Phi_q: \mathbb{R} \to \mathbb{R}$: outer functions (univariate)
- Only 2 layers needed theoretically, but inner functions can be non-smooth

### KAN Network Structure
Instead of fixed activations on nodes with learnable weights on edges, KANs place **learnable activation functions on edges**:

$$\text{KAN}(x) = (\Phi_2 \circ \Phi_1)(x)$$

where $\Phi$ is a matrix of learnable univariate functions $\phi_{i,j}$.

### B-Spline Parameterization
Each edge function $\phi(x)$ is parameterized as:

$$\phi(x) = w_b \cdot \text{SiLU}(x) + w_s \cdot \text{spline}(x)$$

- **SiLU (residual)**: $\text{SiLU}(x) = x \cdot \sigma(x)$ — ensures non-zero gradient even outside spline grid
- **Spline**: Linear combination of B-spline basis functions $B_i(x)$:
  $$\text{spline}(x) = \sum_{i=1}^{G+k} c_i B_i(x)$$
  where $G$ = grid size, $k$ = spline order (typically 3)

## Architecture Comparison

| Aspect | MLP | KAN |
|--------|-----|-----|
| Weights | Fixed linear transformations | Learnable edge functions |
| Activations | Fixed (ReLU, GELU) | Learnable (B-spline) |
| Nodes | Summation + activation | Summation only (no activation) |
| Parameters per edge | 1 scalar | $G+k+1$ scalars (spline coeffs + weights) |
| Interpretability | Hard (distributed) | Easier (edge functions visualizable) |
| Accuracy scaling | $O(L)$ depth | $O(L)$ depth, but better with few params |

## Sparsification and Pruning

Apply L1 regularization on activation magnitudes:

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{task}} + \lambda \sum_{\phi \in \text{edges}} |\phi(x)|$$

After training, prune edges with near-zero magnitude, yielding interpretable computation graphs.

## Code: Simple KAN Layer

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class BSplineActivation(nn.Module):
    def __init__(self, grid_size=8, spline_order=3):
        super().__init__()
        self.grid_size = grid_size
        self.spline_order = spline_order
        n_bases = grid_size + spline_order
        self.coefficients = nn.Parameter(torch.randn(n_bases) * 0.1)
        self.grid = nn.Parameter(torch.linspace(-1, 1, grid_size), requires_grad=False)

    def forward(self, x):
        # B-spline basis evaluation (simplified)
        basis = []
        for i in range(len(self.coefficients)):
            b = self.bspline_basis(x, i)
            basis.append(b)
        basis = torch.stack(basis, dim=-1)
        return (basis * self.coefficients).sum(dim=-1)
```

## Representations KANs Excel At
- **Symbolic formulas**: Can recover exact symbolic structure (e.g., $f(x,y) = xy$ via multiplication as addition in log space)
- **Compositional functions**: Naturally represent hierarchical structure
- **Feature interactions**: Pruned KAN shows which features interact

## Practical Considerations
- **Training**: KANs are slower per iteration (spline eval), but may need fewer parameters
- **Scaling**: Grid size can be progressively increased during training (grid extension)
- **Regularization**: L1 on edge activations + entropy regularization for pruning
- **Initialization**: Initialize spline coefficients near zero so KAN starts like a shallow network

## Limitations
- **Speed**: B-spline evaluation is slower than simple matrix multiply
- **High-dim scaling**: K-A theorem says 2 layers suffice but inner functions may be non-smooth
- **Hardware**: Does not exploit GPU tensor cores as efficiently as matmul
- **Maturity**: Less tested than MLPs/Transformers across diverse tasks

## References
- Liu et al., "KAN: Kolmogorov-Arnold Networks", 2024
- Kolmogorov, "On the representation of continuous functions of several variables", 1957
- Arnold, "On functions of three variables", 1957
- De Boor, "A Practical Guide to Splines", 1978
- Pinkus, "Approximation Theory of the MLP Model", 1999
