# Lesson 07.06: Implicit Neural Representations (NeRF, SIREN)

## Learning Objectives
- Understand coordinate-based MLPs for continuous signal representation
- Implement NeRF with volume rendering
- Apply positional encoding and SIREN activations
- Compare hash encoding (Instant NGP) with Fourier features

## Theory
Implicit neural representations (INRs) map coordinates directly to field values:

$$f_\theta: \mathbb{R}^d \to \mathbb{R}^k$$

- $d$: input dimension (e.g., 3D position, 2D pixel, time)
- $k$: output field (e.g., RGB, density, occupancy, distance)

**Key property**: Continuous and differentiable — query at any resolution.

## Positional Encoding

### Fourier Features
Map coordinates to high-frequency basis:

$$\gamma(v) = [\sin(2\pi B v), \cos(2\pi B v)]$$

- $B \in \mathbb{R}^{m \times d}$: frequency matrix
- $m$: number of frequency bands (typically 10-16)
- Critical for capturing high-frequency detail — without it, MLPs learn only low frequencies

### Multi-Resolution Hash Encoding (Instant NGP)
Replace Fourier features with learned hash tables:

- Multi-resolution grid: $L$ levels with $T$ hash entries each
- Each corner indexed by spatial hash
- Feature vector per corner, trilinearly interpolated
- **Speed**: 1000x faster than Fourier + MLP

## NeRF: Neural Radiance Fields

### Input-Output
$$F_\Theta: (x, y, z, \theta, \phi) \to (r, g, b, \sigma)$$

- $(x,y,z)$: 3D position
- $(\theta,\phi)$: viewing direction
- $(r,g,b)$: emitted color
- $\sigma$: volume density (opacity)

### Volume Rendering
$$C(r) = \int_{t_n}^{t_f} T(t) \sigma(r(t)) c(r(t), d) \, dt$$

$$T(t) = \exp\left(-\int_{t_n}^t \sigma(r(s)) \, ds\right)$$

- $r(t)$: ray from camera through pixel
- $T(t)$: accumulated transmittance
- **Discretized**: Stratified sampling + hierarchical sampling (coarse + fine networks)

### Two-Phase Sampling
1. **Coarse**: Uniform samples along ray
2. **Fine**: Importance sampling based on coarse density — allocate more samples where density is high

### Loss
MSE between rendered and ground-truth pixel colors:

$$\mathcal{L} = \sum_{r \in \mathcal{R}} \|C_{\text{pred}}(r) - C_{\text{gt}}(r)\|_2^2$$

## SIREN (Sinusoidal Representation Networks)

$$y(x) = W_n (\phi_{n-1} \circ \phi_{n-2} \circ \dots \circ \phi_0)(x) + b_n$$
$$\phi_i(x) = \sin(\omega_0 W_i x + b_i)$$

**First layer**: $\phi_0(x) = \sin(\omega_0 W_0 x + b_0)$

**Benefits**:
- Derivative of sine is cosine (still a sine wave) — derivatives are well-defined
- Can represent signals and their derivatives simultaneously
- Solves Poisson/image interpolation equations naturally

## Architecture Comparison

| Feature | MLP + ReLU | MLP + Fourier | SIREN | Instant NGP |
|---------|-----------|---------------|-------|-------------|
| High freq detail | Poor | Good | Excellent | Excellent |
| Derivative quality | Poor | Moderate | Excellent | Poor |
| Training speed | Fast | Moderate | Fast | Very fast |
| Memory | Low | Low | Low | Moderate (hash) |
| Parameter count | Moderate | Moderate | Moderate | Variable |

## Code: SIREN Block

```python
import torch
import torch.nn as nn

class SIRENLayer(nn.Module):
    def __init__(self, in_dim, out_dim, w0=30.0, is_first=False):
        super().__init__()
        self.w0 = w0
        self.is_first = is_first
        self.linear = nn.Linear(in_dim, out_dim)
        self.init_weights()

    def init_weights(self):
        with torch.no_grad():
            if self.is_first:
                nn.init.uniform_(self.linear.weight, -1/self.linear.in_features,
                                  1/self.linear.in_features)
            else:
                nn.init.uniform_(self.linear.weight, -np.sqrt(6/self.linear.in_features)/self.w0,
                                  np.sqrt(6/self.linear.in_features)/self.w0)

    def forward(self, x):
        return torch.sin(self.w0 * self.linear(x))
```

## Applications Beyond NeRF

| Application | Input | Output |
|------------|-------|--------|
| Image compression | $(x,y)$ | RGB |
| 3D shape (SDF) | $(x,y,z)$ | Signed distance |
| Video | $(x,y,t)$ | RGB |
| Audio | $t$ | Amplitude |
| MRI reconstruction | $(x,y,z)$ | Tissue intensity |
| CT reconstruction | Ray parameters | Attenuation |

## Practical Considerations
- **Sampling strategy**: Coarse-to-fine sampling critical for NeRF training efficiency
- **View dependence**: Separate color MLP (conditioned on direction) from density MLP (position only)
- **Hash collisions**: Instant NGP uses hash tables — collisions resolved by gradient averaging
- **Background**: Use separate background model or inverse sphere parametrization for unbounded scenes
- **Multi-GPU**: Parallelize ray batches across GPUs

## Limitations
- **Slow rendering**: Each ray requires hundreds of MLP evaluations
- **Static scenes**: Standard NeRF assumes static scene with fixed lighting
- **Unbounded scenes**: Requires specialized parameterization (NeRF++, Mip-NeRF)
- **Generalization**: Each scene requires separate training — no zero-shot generalization

## References
- Mildenhall et al., "NeRF: Representing Scenes as Neural Radiance Fields", ECCV 2020
- Sitzmann et al., "Implicit Neural Representations with Periodic Activations (SIREN)", NeurIPS 2020
- Müller et al., "Instant Neural Graphics Primitives with a Multiresolution Hash Encoding", SIGGRAPH 2022
- Tancik et al., "Fourier Features Let Networks Learn High Frequency Functions in Low Dimensional Domains", NeurIPS 2020
- Barron et al., "Mip-NeRF: A Multiscale Representation for Anti-Aliasing Neural Radiance Fields", ICCV 2021
