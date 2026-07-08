# Lesson 07.25: Differentiable Programming

## Learning Objectives
- Understand forward-mode and reverse-mode automatic differentiation
- Implement differentiable control flows with straight-through estimators
- Apply differentiable physics engines for robotics
- Design differentiable rendering pipelines for inverse graphics

## Theory
Differentiable programming extends deep learning beyond neural networks by making entire programs differentiable, enabling gradient-based optimization of parameters.

### Automatic Differentiation
- **Forward-mode (tangent)**: Compute $\partial f / \partial x$ in one forward pass — good for $f: \mathbb{R}^n \to \mathbb{R}^m$ with $m \gg n$
- **Reverse-mode (adjoint)**: Compute $\partial f / \partial x$ in two passes (forward + backward) — good for $f: \mathbb{R}^n \to \mathbb{R}^m$ with $n \gg m$

## Differentiable Control Flow

### Straight-Through Estimator (STE)
For discrete operations (e.g., threshold, argmax):

$$\frac{\partial \text{round}(x)}{\partial x} \approx 1$$

- Forward pass: use discrete operation (e.g., $\text{sign}(x)$)
- Backward pass: pass gradient through as if identity

### Gumbel-Softmax
Continuous relaxation of discrete sampling:

$$y_i = \frac{\exp((\log \pi_i + g_i) / \tau)}{\sum_j \exp((\log \pi_j + g_j) / \tau)}$$

- $g_i \sim \text{Gumbel}(0, 1)$
- $\tau \to 0$: approaches one-hot (hard)
- $\tau \to \infty$: approaches uniform

### Concrete Relaxation
Relax discrete operations (sort, top-k) to continuous approximations:
- **Neural sort**: Soft sorting via optimal transport
- **Differentiable sorting networks**: Continuous relaxation of comparators

## Differentiable Physics

### Key Idea
Physics simulators are programs with known physical equations — make them differentiable:

$$\frac{\partial \text{loss}}{\partial \theta} = \frac{\partial \text{loss}}{\partial x_T} \cdot \frac{\partial x_T}{\partial \theta}$$

- $x_T$: final state after simulation
- $\theta$: simulation parameters (mass, friction, stiffness)

### Applications
- **Robotics**: Learn controller parameters by differentiating through simulation
- **Material design**: Discover materials by optimizing simulation parameters
- **Fluid control**: Optimize initial conditions for desired flow patterns

### Libraries
| Library | Focus | Differentiation |
|---------|-------|---------------|
| Taichi | Graphics, physics simulation | Source-to-source AD |
| DiffTaichi | Physical simulation | Reverse-mode AD |
| Brax | Robotics simulation | JAX-based (vmap) |
| MuJoCo (MJX) | Robotics simulation | JAX-based |
| Theseus | Differentiable optimization layers | PyTorch-based |

## Differentiable Rendering

### Rendering Equation
$$L_o(x, \omega_o) = L_e(x, \omega_o) + \int_\Omega f_r(x, \omega_i, \omega_o) L_i(x, \omega_i) (\omega_i \cdot n) d\omega_i$$

- $L_o$: outgoing radiance
- $f_r$: BRDF
- Differentiate through the entire rendering pipeline

### Key Challenges
- **Visibility**: Hard shadows and occlusions are discontinuous
- **Sampling**: Monte Carlo integration introduces noise
- **Solution**: Approximate gradients via surrogate or reparameterization

### Libraries for Differentiable Rendering
| Library | Type | Gradients |
|---------|------|-----------|
| PyTorch3D | Rasterization-based | Approximate |
| Mitsuba 3 | Ray tracing (path) | Reprojected |
| redner | Differentiable rasterization | Approximate |
| Kaolin | 3D deep learning | Various |

## Code: Differentiable Physics with Taichi

```python
import taichi as ti
import taichi.math as tm

ti.init(arch=ti.gpu)

@ti.kernel
def simulate(dt: float, mass: ti.template(), pos: ti.template(),
             vel: ti.template(), gravity: tm.vec2):
    # Forward Euler integration (differentiable)
    for i in pos:
        acc = gravity / mass[i]
        vel[i] += acc * dt
        pos[i] += vel[i] * dt

# Tape-based AD for gradient computation
with ti.ad.Tape(loss=total_loss):
    simulate(dt, mass, pos, vel, gravity)
    # Compute loss
    total_loss[None] = compute_loss(pos, target_pos)
    # Gradients available in .grad fields
    grad_mass = mass.grad
```

## Differentiable Optimization Layers

### OptNet (Amos & Kolter, 2017)
Embed QP solver as a differentiable layer:

$$z^* = \arg\min_z \frac{1}{2} z^\top Q(x) z + c(x)^\top z$$
$$\text{s.t. } A(x) z = b(x), \, G(x) z \leq h(x)$$

- Forward: Solve QP via interior point method
- Backward: Differentiate through KKT conditions

## Practical Considerations
- **Memory**: Unrolling simulation loops stores all intermediate states
- **Checkpointing**: Rematerialize states during backward to save memory
- **Numerical stability**: Physics simulators may produce NaN gradients
- **Surrogate gradients**: Use STE only when continuous relaxation is impractical
- **Clamping**: Clamp outputs of simulation steps to prevent explosions

## Applications

| Domain | Program | Differentiable Part |
|--------|---------|-------------------|
| Robotics | Forward dynamics | Controller parameters |
| CFD | Navier-Stokes solver | Boundary conditions |
| Rendering | Ray tracer | Scene parameters |
| Protein design | Molecular dynamics | Amino acid sequences |
| Control | MPC optimizer | Cost function weights |

## Limitations
- **Memory cost**: Unrolled computation graphs are memory intensive
- **Long horizons**: Differentiating through many simulation steps can explode gradients
- **Non-smoothness**: Contact, collision, and rendering remain challenging
- **Numerical error**: Forward errors accumulate and corrupt backward gradients
- **Library support**: Not all programming constructs are differentiable

## References
- Baydin, Pearlmutter, Radul, Siskind, "Automatic Differentiation in Machine Learning: a Survey", JMLR 2018
- Hu, Luke, Anderson, et al., "DiffTaichi: Differentiable Programming for Physical Simulation", ICLR 2020
- Amos & Kolter, "OptNet: Differentiable Optimization as a Layer", ICML 2017
- Li, Müller, et al., "Differentiable Physics: A Position Piece", 2022
- Ravi, Rezende, et al., "PyTorch3D: Differentiable 3D Rendering for Deep Learning", 2020
