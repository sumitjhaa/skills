# Lesson 07.05: DEQ (Deep Equilibrium Models)

## Learning Objectives
- Understand implicit layers and fixed-point solving
- Implement DEQ forward pass with root-finding
- Apply implicit differentiation for backpropagation
- Analyze stability and well-posedness of DEQ layers

## Theory
DEQs replace explicit stacked layers with a single implicit layer that finds a fixed point:

$$z^* = f_\theta(z^*, x)$$

- $x$: input
- $z^*$: equilibrium state (output)
- $f_\theta$: nonlinear transformation

**"Infinite depth"**: Equivalent to applying $f_\theta$ infinitely many times to convergence.

## Forward Pass: Fixed-Point Solving
Find $z^*$ such that $g(z) = f_\theta(z, x) - z = 0$:

### Broyden's Method
Quasi-Newton method for root-finding, updating Jacobian approximation:

$$z_{k+1} = z_k - \alpha B_k^{-1} g(z_k)$$

- $B_k$: approximate Jacobian of $g$ at $z_k$
- $O(n^2)$ update per iteration (vs $O(n^3)$ for Newton)

### Anderson Acceleration
Mixing past iterates to accelerate convergence:

$$z_{k+1} = (1-\beta) z_k + \beta \tilde{z}_{k+1}$$

- Maintains history of $m$ past iterates
- Solves least-squares for optimal mixing coefficients

### Forward Algorithm
```python
def deq_forward(f, z0, x, tol=1e-5, max_iter=50):
    z = z0
    for k in range(max_iter):
        z_next = f(z, x)
        if torch.norm(z_next - z) < tol:
            break
        # Anderson mixing
        z = anderson_mix(z, z_next, history=m)
    return z.detach(), z  # output, final state for backward
```

## Backward Pass: Implicit Differentiation

### Key Insight
At equilibrium $z^*$, we have $z^* = f_\theta(z^*, x)$. Differentiating:

$$\frac{\partial L}{\partial \theta} = \frac{\partial L}{\partial z^*} \left(I - \frac{\partial f_\theta}{\partial z^*}\right)^{-1} \frac{\partial f_\theta}{\partial \theta}$$

**No backprop through solver iterations!** Only need the final Jacobian at $z^*$.

### Jacobian-Free Backprop (JFB)
Approximate $\frac{\partial f_\theta}{\partial z^*} \approx 0$:

$$\frac{\partial L}{\partial \theta} \approx \frac{\partial L}{\partial z^*} \frac{\partial f_\theta}{\partial \theta}$$

- **Bias**: Consistent (gradient points in a descent direction)
- **Variance**: Higher variance but cheaper
- **Memory**: No Hessian needed

### Neumann Series
$$(I - J)^{-1} = I + J + J^2 + J^3 + \dots$$

Truncate after $k$ terms for approximate gradient — trades accuracy for compute.

## DEQ Layer Types

| Layer | $f_\theta$ | Equilibrium in |
|-------|-----------|---------------|
| Transformer DEQ | Multi-head attention + FFN | Hidden states |
| Conv DEQ | Residual conv blocks | Feature maps |
| Graph DEQ | Graph message passing | Node features |
| Monotone DEQ | $f_\theta$ is a contraction | Any |

## Code: Basic DEQ Block

```python
import torch
import torch.nn as nn

class DEQBlock(nn.Module):
    def __init__(self, hidden_dim, ffn_dim):
        super().__init__()
        self.norm1 = nn.LayerNorm(hidden_dim)
        self.linear = nn.Linear(hidden_dim, hidden_dim)
        self.norm2 = nn.LayerNorm(hidden_dim)
        self.ffn = nn.Sequential(
            nn.Linear(hidden_dim, ffn_dim),
            nn.ReLU(),
            nn.Linear(ffn_dim, hidden_dim),
        )

    def forward(self, z, x):
        # Residual connection
        z = z + self.linear(self.norm1(z))
        z = z + self.ffn(self.norm2(z))
        return z

class DEQ(nn.Module):
    def __init__(self, hidden_dim, ffn_dim):
        super().__init__()
        self.f = DEQBlock(hidden_dim, ffn_dim)
        self.fixed_point = None

    def forward(self, x, max_iter=50, tol=1e-4, method='anderson'):
        z = x  # initialize
        with torch.no_grad():
            z_star = _fixed_point_iteration(self.f, z, x, max_iter, tol, method)
        self.fixed_point = z_star
        return z_star

    def backward(self, dl_dz):
        if self.fixed_point is None:
            raise ValueError("No fixed point stored")
        z_star = self.fixed_point
        # Implicit differentiation via CG (for Monotone DEQ)
        I = torch.eye(z_star.shape[-1], device=z_star.device)
        J = torch.autograd.functional.jacobian(lambda z: self.f(z, x), z_star)
        grad = torch.linalg.solve(I - J, dl_dz)
        return grad
```

## Stability and Well-Posedness
For DEQ to be well-posed, $(I - \partial f / \partial z)$ must be invertible:

### Monotone Operator
$f$ is a $\kappa$-contraction if:
$$\|f(z_1) - f(z_2)\| \leq \kappa \|z_1 - z_2\|, \quad \kappa < 1$$

**Sufficient condition** for unique fixed point: weight normalization or spectral normalization.

### Weight-Tied Norm Constraint
$$\|W\|_2 \leq \frac{1}{\sqrt{L}}$$

where $L$ is Lipschitz constant of activation. Ensures contraction.

## Practical Considerations
- **Initialization**: Start $z_0$ at zero or input embedding; better init reduces iterations
- **Tolerance**: 1e-4 to 1e-5 for most tasks; lower tolerance = more iterations but better convergence
- **Damped Anderson**: Use $\beta < 1$ for stability
- **Gradient clipping**: Essential for stable training of implicit layers
- **Memory savings**: DEQ uses $O(L)$ less memory than $L$-layer explicit network

## Limitations
- **Convergence**: May not converge for complex $f_\theta$ or poorly conditioned problems
- **Training instability**: Oscillations during training common; requires careful tuning
- **Batch inconsistency**: Different samples may converge at different rates
- **Fixed-point drift**: Small changes in $\theta$ can cause large changes in $z^*$
- **Hardware**: Solver iterations are sequential — hard to parallelize fully

## References
- Bai, Koltun, Kolter, "Deep Equilibrium Models", NeurIPS 2019
- Bai, Koltun, Kolter, "Multiscale Deep Equilibrium Models", NeurIPS 2020
- Fung, He, Zhang, "JFB: Jacobian-Free Backpropagation for Implicit Models", 2022
- Winston, Kolter, "Monotone Operator Equilibrium Networks", NeurIPS 2020
- El Ghaoui et al., "Implicit Deep Learning", Foundations and Trends in ML, 2021
