# Lesson 08.17: Neural Rendering (NeRF, 3D Gaussian Splatting)

## Learning Objectives
- Understand NeRF's volume rendering formulation
- Implement 3D Gaussian Splatting for real-time rendering
- Apply Instant NGP for fast NeRF training
- Compare neural rendering methods for scene representation

## NeRF (Neural Radiance Fields)

### Representation
$$F_\Theta: (x, y, z, \theta, \phi) \to (r, g, b, \sigma)$$

- $(x,y,z)$: 3D position
- $(\theta,\phi)$: viewing direction
- $(r,g,b,\sigma)$: emitted color + volume density

### Volume Rendering
$$C(r) = \int_{t_n}^{t_f} T(t) \sigma(r(t)) c(r(t), d) \, dt$$

$$T(t) = \exp\left(-\int_{t_n}^t \sigma(r(s)) \, ds\right)$$

### Positional Encoding
$$\gamma(p) = (\sin(2^k \pi p), \cos(2^k \pi p))_{k=0}^{L-1}$$

- $L=10$ for position, $L=4$ for direction
- Enables high-frequency detail learning

### Hierarchical Sampling
1. **Coarse network**: Uniform samples along ray → coarse density
2. **Fine network**: Importance samples based on coarse density

## 3D Gaussian Splatting (3DGS)

### Representation
Scene as 3D Gaussians $\mathcal{G} = \{G_k\}_{k=1}^K$:

$$G_k(x) = \exp\left(-\frac{1}{2}(x - \mu_k)^\top \Sigma_k^{-1} (x - \mu_k)\right)$$

- $\mu_k \in \mathbb{R}^3$: position
- $\Sigma_k \in \mathbb{R}^{3 \times 3}$: covariance (learned as $R S S^\top R^\top$)
- $\sigma_k \in [0, 1]$: opacity
- $c_k \in \mathbb{R}^3$: spherical harmonics coefficients (view-dependent color)

### Differentiable Rasterization
1. Sort Gaussians by depth
2. Project to screen space (2D Gaussians)
3. Alpha-composite from front to back:
   $$C = \sum_{k=1}^K c_k \cdot \alpha_k \cdot \prod_{j=1}^{k-1} (1 - \alpha_j)$$

### Training
- Gradient-based: Optimize $\mu, \Sigma, \sigma, c$
- **Adaptive density control**: Split Gaussians with large gradients, prune with low opacity
- **Loss**: $\mathcal{L} = \lambda \mathcal{L}_1 + (1-\lambda) \mathcal{L}_{\text{D-SSIM}}$

## Instant NGP

### Multi-Resolution Hash Encoding
Replace positional encoding with learned hash tables:
- $L$ levels of resolution (coarse to fine)
- $F$ features per level
- $T$ hash table entries per level
- Trilinear interpolation + concatenation

### Speed
- NeRF: hours to days
- Instant NGP: seconds to minutes
- Method: small MLP (2-4 layers) + hash encoding

## Code: Volume Rendering

```python
import torch
import torch.nn as nn

def volume_render(rays_o, rays_d, model, n_samples=64):
    """Render rays through NeRF model"""
    B, N = rays_o.shape[0], n_samples
    
    # Sample points along ray
    z_vals = torch.linspace(2.0, 6.0, N, device=rays_o.device)
    z_vals = z_vals.unsqueeze(0).expand(B, -1)
    points = rays_o.unsqueeze(1) + rays_d.unsqueeze(1) * z_vals.unsqueeze(-1)
    
    # Predict density and color
    rgb, sigma = model(points, rays_d.unsqueeze(1).expand(-1, N, -1))
    
    # Volume rendering
    dists = z_vals[:, 1:] - z_vals[:, :-1]
    alpha = 1 - torch.exp(-sigma[:, :-1] * dists)
    T = torch.cumprod(1 - alpha + 1e-10, dim=1)
    T = torch.cat([torch.ones_like(T[:, :1]), T[:, :-1]], dim=1)
    weights = T * alpha
    
    rgb_map = (weights.unsqueeze(-1) * rgb[:, :-1]).sum(dim=1)
    depth_map = (weights * z_vals[:, :-1]).sum(dim=1)
    return rgb_map, depth_map
```

## Neural Rendering Comparison

| Method | Quality | Training Time | Rendering FPS | Memory |
|--------|---------|--------------|--------------|--------|
| NeRF (original) | High | 1-3 days | < 1 | High |
| Instant NGP | High | 1-5 min | 10-50 | Medium |
| 3D Gaussian Splatting | Very high | 10-30 min | 100+ | High |
| Plenoxels | Medium | 10 min | 10 | Low |

## Practical Considerations
- **Multi-view consistency**: NeRF assumes static scene with consistent lighting
- **Unbounded scenes**: Parameterize with contracted coordinates (Mip-NeRF 360)
- **Anti-aliasing**: Mip-NeRF uses integrated positional encoding (cone tracing)
- **Dynamic scenes**: NeRF-W (with transient objects), Nerfies (deformable)
- **Editing**: 3DGS enables direct manipulation (move, delete Gaussians)

## References
- Mildenhall, Srinivasan, Tancik, Barron, Ramamoorthi, Ng, "NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis", ECCV 2020
- Kerbl, Kopanas, Leimkühler, Drettakis, "3D Gaussian Splatting for Real-Time Radiance Field Rendering", ACM Trans. Graphics 2023
- Müller, Evans, Schied, Keller, "Instant Neural Graphics Primitives with a Multiresolution Hash Encoding", SIGGRAPH 2022
- Barron, Mildenhall, Tancik, Hedman, Martin-Brualla, Srinivasan, "Mip-NeRF: A Multiscale Representation for Anti-Aliasing Neural Radiance Fields", ICCV 2021
- Fridovich-Keil, Yu, Tancik, Chen, Recht, Kanazawa, "Plenoxels: Radiance Fields without Neural Networks", CVPR 2022
