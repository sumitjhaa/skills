# Lesson 07.03: Neural ODEs / CDEs / SDEs

## Learning Objectives
- Understand neural ODEs for continuous-depth models
- Implement the adjoint method for memory-efficient gradients
- Apply neural CDEs for irregularly-sampled time series
- Model uncertainty with neural SDEs

## Neural ODEs
Replace discrete residual blocks with continuous ODE:

$$h(t_1) = h(t_0) + \int_{t_0}^{t_1} f_\theta(h(t), t) \, dt$$

- $f_\theta$: neural network parameterizing the dynamics
- Integration via ODE solver (e.g., Dormand-Prince, RK45)
- **"Infinite depth"**: No explicit layer count — depth is a function of integration time

## Adjoint Method

### Forward Pass
Solve ODE from $t_0$ to $t_1$:
$$h(t_1) = \text{ODESolve}(f_\theta, h(t_0), t_0, t_1)$$

### Backward Pass (Memory Efficient)
Instead of backpropagating through solver steps, solve adjoint ODE backwards:

$$a(t) = \frac{\partial L}{\partial h(t)}$$
$$\frac{da(t)}{dt} = -a(t)^\top \frac{\partial f_\theta(h(t), t)}{\partial h}$$

**Gradient w.r.t. parameters**:

$$\frac{\partial L}{\partial \theta} = -\int_{t_1}^{t_0} a(t)^\top \frac{\partial f_\theta(h(t), t)}{\partial \theta} dt$$

**Memory**: $O(1)$ vs $O(L)$ for discrete nets (no need to store intermediate states).

### Algorithm
```
def odefunc(h, t):
    return f_theta(h, t)

# Forward
h1 = odesolve(odefunc, h0, t0, t1, solver='dopri5')

# Backward (adjoint)
a_t1 = dL_dh1  # gradient from loss
a_t0, grad_theta = adjoint_odesolve(odefunc, h1, a_t1, t1, t0)
```

## Neural CDEs

**Controlled differential equations** for time series:

$$h(t) = h(0) + \int_0^t f_\theta(h(s)) \, dX(s)$$

- $X(t)$: observed time series (possibly irregular)
- $dX(s)$: Riemann-Stieltjes integral w.r.t. path of $X$
- Handles missing, irregular, asynchronous data

### Key Advantage
- RNNs require evenly-spaced data
- Neural CDEs treat time as continuous — naturally handle gaps
- Theoretical guarantee: universal approximation for time series

## Neural SDEs

Add stochastic component for uncertainty:

$$dh(t) = \mu_\theta(h(t), t) \, dt + \sigma_\phi(h(t), t) \, dW(t)$$

- $\mu_\theta$: drift network
- $\sigma_\phi$: diffusion network
- $W(t)$: Wiener process (Brownian motion)

**Applications**:
- Uncertainty quantification in forecasting
- Generative modeling (latent SDEs)
- Option pricing, financial modeling

## Methodology Comparison

| Aspect | Neural ODE | Neural CDE | Neural SDE |
|--------|-----------|------------|------------|
| Input | Initial state | Continuous path | Initial state |
| Dynamics | Deterministic | Controlled | Stochastic |
| Output | Final state | Final state | Distribution |
| Memory | $O(1)$ (adjoint) | $O(1)$ | $O(1)$ |
| Key use | Image, density | Time series, events | Uncertainty, finance |

## Code: Neural ODE with torchdiffeq

```python
import torch
import torch.nn as nn
from torchdiffeq import odeint_adjoint

class ODEFunc(nn.Module):
    def __init__(self, hidden_dim=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(hidden_dim + 1, hidden_dim),  # +1 for time
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
        )
    
    def forward(self, t, h):
        t_embed = torch.full_like(h[:, :1], t)
        return self.net(torch.cat([h, t_embed], dim=-1))

class NeuralODEModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.encoder = nn.Linear(input_dim, hidden_dim)
        self.odefunc = ODEFunc(hidden_dim)
        self.decoder = nn.Linear(hidden_dim, output_dim)

    def forward(self, x, t_span):
        h0 = self.encoder(x)
        h_t = odeint_adjoint(self.odefunc, h0, t_span, method='dopri5')
        return self.decoder(h_t[-1])
```

## Continuous Normalizing Flows
Neural ODEs can parameterize normalizing flows:

$$\frac{\partial \log p(z(t))}{\partial t} = -\text{Tr}\left(\frac{\partial f_\theta}{\partial z(t)}\right)$$

- **FFJORD**: Free-form Jacobian of reversible dynamics (unrestricted $f_\theta$)
- Uses Hutchinson trace estimator: $\text{Tr}(J) = \mathbb{E}_\varepsilon[\varepsilon^\top J \varepsilon]$
- Avoids expensive Jacobian computation — $O(d)$ instead of $O(d^2)$

## Practical Considerations
- **ODESolve tolerance**: rtol=1e-3, atol=1e-6 for good accuracy/speed trade-off
- **Adjoint numerical error**: Lower tolerance makes gradients more accurate
- **Solver choice**: Dormand-Prince (dopri5) for adaptive stepping, RK4 for fixed
- **Stiff ODEs**: Use implicit solvers (e.g., BDF, radau) for stiff dynamics
- **Gradient checking**: Always verify adjoint gradients against finite differences

## Limitations
- **Slow training**: ODE solvers (especially adjoint) are slower than discrete layers
- **Non-smooth dynamics**: Sudden changes require many solver steps
- **Numerical stability**: Vanishing/exploding gradients in long integration
- **Scalability**: Each forward pass requires solving an ODE — expensive for large models

## References
- Chen et al., "Neural Ordinary Differential Equations", NeurIPS 2018
- Kidger et al., "Neural Controlled Differential Equations", ICLR 2021
- Li et al., "Neural Stochastic Differential Equations: Deep Hierarchical Mixed Models", 2020
- Grathwohl et al., "FFJORD: Free-form Continuous Dynamics for Scalable Reversible Generative Models", ICLR 2019
- Kidger, "On Neural Differential Equations", PhD Thesis, 2021
