# Lesson 07.17: Normalizing Flows

## Learning Objectives
- Understand change of variables for density estimation
- Implement affine coupling layers (Real NVP)
- Apply flows for variational inference and generation
- Compare flow architectures: Real NVP, GLOW, MAF, IAF, FFJORD

## Theory
Normalizing flows transform a simple base distribution $p_Z(z)$ into a complex target distribution $p_X(x)$ through an invertible mapping $f$:

$$x = f(z), \quad z = f^{-1}(x)$$

### Change of Variables
$$p_X(x) = p_Z(z) \left|\det\left(\frac{\partial f}{\partial z}\right)\right|^{-1} = p_Z(f^{-1}(x)) \left|\det\left(\frac{\partial f^{-1}}{\partial x}\right)\right|$$

### Log-Likelihood
$$\log p_X(x) = \log p_Z(f^{-1}(x)) + \log \left|\det \frac{\partial f^{-1}}{\partial x}\right|$$

## Key Requirements
- **Invertible**: $f$ must be bijective
- **Tractable Jacobian determinant**: Efficient $O(D)$ or $O(D \log D)$ computation
- **Expressive**: Chain of transformations $f = f_K \circ \dots \circ f_1$

## Flow Architectures

### Planar Flows
$$f(z) = z + u \cdot h(w^\top z + b)$$

- Simple, low capacity
- $|\det(I + u \cdot h'(w^\top z + b) w^\top)| = |1 + u^\top h' w|$ (matrix determinant lemma)

### Real NVP (Affine Coupling Layers)

**Forward** ($x = f(z)$):
$$z_{1:d}' = z_{1:d}$$
$$z_{d+1:D}' = z_{d+1:D} \odot \exp(s(z_{1:d})) + t(z_{1:d})$$

**Inverse** ($z = f^{-1}(x)$):
$$z_{1:d} = x_{1:d}$$
$$z_{d+1:D} = (x_{d+1:D} - t(x_{1:d})) \odot \exp(-s(x_{1:d}))$$

- $s$: scale network, $t$: translate network (any NN, no invertibility needed)
- Jacobian is lower-triangular: $\prod_i \exp(s_i) = \exp(\sum_i s_i)$

### GLOW
$$x = f_{\text{actnorm}} \circ f_{\text{1x1conv}} \circ f_{\text{coupling}}$$

- **Actnorm**: Data-dependent initialization (scale + shift)
- **1x1 Conv**: Learned permutation of channels (replace fixed permutation)
- **Multi-scale**: Split off half channels at each level

### MAF (Masked Autoregressive Flow)
$$x_i = z_i \cdot \exp(\alpha_i(x_{<i})) + \mu_i(x_{<i})$$

- Forward: slow (sequential) — $O(D)$
- Inverse: fast (parallel using masks) — $O(1)$
- Good for density estimation

### IAF (Inverse Autoregressive Flow)
$$z_i = (x_i - \mu_i(z_{<i})) \cdot \exp(-\alpha_i(z_{<i}))$$

- Forward: fast (parallel) — $O(1)$
- Inverse: slow (sequential) — $O(D)$
- Good for variational inference (encoding)

## Code: Real NVP Coupling Block

```python
import torch
import torch.nn as nn

class AffineCoupling(nn.Module):
    def __init__(self, d, hidden_dim=64):
        super().__init__()
        self.d = d
        self.net = nn.Sequential(
            nn.Linear(d, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 2 * (d - d//2)),  # scale + shift
        )

    def forward(self, x):
        # Split
        x_a, x_b = x[:, :self.d//2], x[:, self.d//2:]
        params = self.net(x_a)
        s, t = params[:, :params.shape[1]//2], params[:, params.shape[1]//2:]
        s = torch.tanh(s)  # Bound log_scale
        # Affine transform
        y_b = x_b * torch.exp(s) + t
        y = torch.cat([x_a, y_b], dim=1)
        log_det = s.sum(dim=-1)
        return y, log_det

    def inverse(self, y):
        y_a, y_b = y[:, :self.d//2], y[:, self.d//2:]
        params = self.net(y_a)
        s, t = params[:, :params.shape[1]//2], params[:, params.shape[1]//2:]
        s = torch.tanh(s)
        x_b = (y_b - t) * torch.exp(-s)
        x = torch.cat([y_a, x_b], dim=1)
        return x, -s.sum(dim=-1)
```

## Comparison

| Flow | Jacobian | Forward | Inverse | Best for |
|------|----------|---------|---------|----------|
| Planar | $O(D)$ | $O(D)$ | $O(D)$ | Toy data |
| Real NVP | $O(D)$ | $O(D)$ | $O(D)$ | Images (fast both ways) |
| GLOW | $O(D)$ | $O(D)$ | $O(D)$ | Images (high quality) |
| MAF | $O(D)$ | $O(D)$ (seq) | $O(D)$ (par) | Density estimation |
| IAF | $O(D)$ | $O(D)$ (par) | $O(D)$ (seq) | Variational inference |
| FFJORD | $O(D)$ trace | $O(D \log D)$ | $O(D \log D)$ | Continuous data |

## Practical Considerations
- **Coupling layers**: Need alternating splitting patterns (different channels/dimensions)
- **Batch normalization**: Use actnorm or moving average BN between coupling layers
- **Multi-scale architecture**: Split dimensions to reduce computation in deeper layers
- **Base distribution**: Standard Gaussian is typical; mixture of Gaussians for multimodal data
- **Numerical stability**: Clamp log scale parameters (e.g., $\tanh(s)$)

## Limitations
- **Invertibility constraint**: Architecture design is constrained by invertibility requirement
- **Dimensionality**: Input and output dimensions must match (cannot learn manifold structure)
- **Expressiveness**: Coupling layers have limited expressiveness per layer; need many layers
- **Training stability**: Deep flows can be numerically unstable

## References
- Rezende & Mohamed, "Variational Inference with Normalizing Flows", ICML 2015
- Dinh, Krueger, Bengio, "Density Estimation using Real NVP", ICLR 2017
- Kingma & Dhariwal, "Glow: Generative Flow with Invertible 1x1 Convolutions", NeurIPS 2018
- Papamakarios, Pavlakou, Murray, "Masked Autoregressive Flow for Density Estimation", NeurIPS 2017
- Grathwohl, Chen, Bettencourt, Sutskever, Duvenaud, "FFJORD: Free-form Continuous Dynamics for Scalable Reversible Generative Models", ICLR 2019
