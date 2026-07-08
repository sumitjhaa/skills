# Lesson 07.04: PINNs (Physics-Informed Neural Networks)

## Learning Objectives
- Understand how to embed PDE constraints into neural network loss
- Implement PINNs for forward and inverse problems
- Use automatic differentiation for PDE residuals
- Apply PINNs to Navier-Stokes, Burger's equation, and parameter discovery

## Theory
PINNs solve PDEs by training a neural network $u_\theta(x,t)$ to satisfy:

$$\mathcal{N}[u](x,t) = 0, \quad x \in \Omega, t \in [0,T]$$
$$\mathcal{B}[u](x,t) = 0, \quad x \in \partial\Omega $$
$$\mathcal{I}[u](x,0) = g(x) $$

where $\mathcal{N}$ is the PDE operator, $\mathcal{B}$ boundary conditions, $\mathcal{I}$ initial conditions.

## Loss Function
$$\mathcal{L}_{\text{total}} = \lambda_{\text{PDE}} \mathcal{L}_{\text{PDE}} + \lambda_{\text{BC}} \mathcal{L}_{\text{BC}} + \lambda_{\text{IC}} \mathcal{L}_{\text{IC}} + \lambda_{\text{data}} \mathcal{L}_{\text{data}}$$

### PDE Loss
$$\mathcal{L}_{\text{PDE}} = \frac{1}{N_f} \sum_{i=1}^{N_f} \left| \mathcal{N}[u_\theta](x_f^i, t_f^i) \right|^2$$

- Collocation points $(x_f^i, t_f^i)$ sampled randomly in domain
- $\mathcal{N}[u_\theta]$ computed via automatic differentiation

### Boundary / Initial Condition Loss
$$\mathcal{L}_{\text{BC}} = \frac{1}{N_b} \sum_{i=1}^{N_b} \left| u_\theta(x_b^i, t_b^i) - u_{\text{BC}}(x_b^i, t_b^i) \right|^2$$
$$\mathcal{L}_{\text{IC}} = \frac{1}{N_0} \sum_{i=1}^{N_0} \left| u_\theta(x_0^i, 0) - g(x_0^i) \right|^2$$

### Data Loss (Inverse Problems)
$$\mathcal{L}_{\text{data}} = \frac{1}{N_d} \sum_{i=1}^{N_d} \left| u_\theta(x_d^i, t_d^i) - u_{\text{obs}}^i \right|^2$$

## Example: Burger's Equation
$$u_t + u u_x = \nu u_{xx}, \quad x \in [-1,1], t \in [0,1]$$

$$\mathcal{L}_{\text{PDE}} = \frac{1}{N_f} \sum_i \left| u_t^{(i)} + u^{(i)} u_x^{(i)} - \nu u_{xx}^{(i)} \right|^2$$

## Code: PINN for Burger's Equation

```python
import torch
import torch.nn as nn

class PINN(nn.Module):
    def __init__(self, layers=[2, 64, 64, 64, 1]):
        super().__init__()
        self.net = nn.ModuleList()
        for i in range(len(layers) - 1):
            self.net.append(nn.Linear(layers[i], layers[i+1]))
            if i < len(layers) - 2:
                self.net.append(nn.Tanh())

    def forward(self, x, t):
        u = torch.cat([x, t], dim=1)
        for layer in self.net:
            u = layer(u)
        return u

    def pde_loss(self, x, t, nu=0.01):
        x.requires_grad_(True)
        t.requires_grad_(True)
        u = self.forward(x, t)
        u_t = torch.autograd.grad(u, t, grad_outputs=torch.ones_like(u), 
                                  create_graph=True)[0]
        u_x = torch.autograd.grad(u, x, grad_outputs=torch.ones_like(u),
                                  create_graph=True)[0]
        u_xx = torch.autograd.grad(u_x, x, grad_outputs=torch.ones_like(u_x),
                                   create_graph=True)[0]
        residual = u_t + u * u_x - nu * u_xx
        return torch.mean(residual ** 2)

    def bc_ic_loss(self, x_bc, t_bc, u_bc):
        u_pred = self.forward(x_bc, t_bc)
        return torch.mean((u_pred - u_bc) ** 2)
```

## Training Strategy
1. **Adam pretraining**: 10k-50k steps with large learning rate for initial convergence
2. **L-BFGS fine-tuning**: Use full-batch L-BFGS for precise PDE satisfaction
3. **Adaptive collocation**: Refine collocation points near high-residual regions (RAR — Residual-based Adaptive Refinement)
4. **Learning rate annealing**: Automatically adjust $\lambda$ weights to balance loss terms

## Applications

| Application | PDE | Notable Work |
|------------|-----|-------------|
| Fluid dynamics | Navier-Stokes | Raissi et al., JCP 2019 |
| Solid mechanics | Elasticity, hyperelasticity | Haghighat et al., 2021 |
| Heat transfer | Heat equation | Lu et al., DeepXDE 2021 |
| Quantum mechanics | Schrödinger equation | Raissi, 2018 |
| Inverse problems | Parameter discovery | Tartakovsky et al., 2020 |

## Limitations
- **Training difficulty**: Multi-objective loss is hard to balance; gradient pathologies common
- **High-dimensional**: Curse of dimensionality for PDEs in $d > 3$
- **Discontinuities**: Shock waves and steep gradients challenge smooth neural networks
- **No convergence guarantees**: Unlike FEM/FDM, PINNs may not converge to correct solution
- **Boundary complexity**: Complex geometry requires specialized sampling

## Practical Considerations
- **Architecture**: 4-8 hidden layers, 64-256 neurons, Tanh/Sine activations
- **Normalization**: Normalize domain to $[-1,1]$ for stable training
- **Collocation points**: Start with Latin hypercube sampling, refine adaptively
- **Multi-GPU**: Distributed collocation point computation
- **Hybrid approaches**: PINNs + traditional solvers (e.g., Fourier feature embeddings)

## References
- Raissi, Perdikaris, Karniadakis, "Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear PDEs", JCP 2019
- Lu, Meng, Karniadakis, "DeepXDE: A deep learning library for solving differential equations", SIAM Review 2021
- Karniadakis et al., "Physics-informed machine learning", Nature Reviews Physics 2021
- Wang et al., "When and why PINNs fail to train: A neural tangent kernel perspective", JCP 2022
- Cuomo et al., "Scientific Machine Learning through Physics-Informed Neural Networks", 2022
