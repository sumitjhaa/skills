# Lesson 07.09: Liquid Neural Networks (LTC, NCP)

## Learning Objectives
- Understand liquid time-constant (LTC) networks
- Implement closed-form continuous-time neural networks (CfC)
- Design sparse neural circuit policies (NCP)
- Analyze stability, causality, and parameter efficiency

## Theory
Liquid neural networks are continuous-time dynamical systems with input-dependent time constants, enabling adaptive temporal processing with very few parameters.

## Liquid Time-Constant (LTC) Networks

### Dynamics
$$\tau(x, t) \frac{dh}{dt} = -h(t) + f_\theta(h(t), x(t), t)$$

- $\tau(x, t)$: **Input-dependent** time constant (unlike RNNs with fixed $\tau$)
- $f_\theta$: Neural network for nonlinear dynamics

### Why Liquid?
- "Liquid" because the effective time constant varies with input
- Faster response to salient inputs, slower to stable signals
- Causal — output depends only on past (no future info)

### Closed-Form Solution (CfC)
Approximate the ODE with a closed form:

$$h(t) = \text{LTC}(x(t), h(0)) \approx \sigma(-\text{net}(x)) \cdot h(0) + (1 - \sigma(-\text{net}(x))) \cdot \text{net}(x)$$

**Result**: CfC matches LTC accuracy while being 100x faster for training/inference.

## Neural Circuit Policies (NCP)
Inspired by the *C. elegans* connectome — sparse, biologically-inspired wiring:

### Architecture
```
Sensory neurons → Interneurons → Command neurons → Motor neurons
```

- **Sensory layer**: $N_{\text{sensory}}$ neurons (input)
- **Interneurons**: Sparse recurrent connectivity (most computation)
- **Command layer**: Small set of integrating neurons
- **Motor layer**: $N_{\text{motor}}$ neurons (output)

### Sparsity
NCPs use only 19-60 neurons with 1000-3000 synapses — orders of magnitude fewer than typical RNNs.

### Wiring Constraints
- Fixed number of synapses per neuron (e.g., 10-50)
- Sparse random connectivity with biological motifs (feedforward, recurrent, lateral inhibition)
- Learning adjusts synapse weights, not connectivity pattern

## Key Differences from RNNs

| Property | LSTM | LTC | NCP |
|----------|------|-----|-----|
| Time constant | Fixed (sigmoid gates) | Input-dependent | Input-dependent |
| Parameters | $O(n^2)$ | $O(n^2)$ but smaller $n$ | $O(n)$ |
| Synaptic connections | Dense | Dense | Sparse |
| Training speed | Fast (discrete) | Slow (ODE solve) | Slow (ODE solve) |
| Interpretability | Low | Medium | High (wiring) |

## Code: CfC Cell

```python
import torch
import torch.nn as nn

class CfCCell(nn.Module):
    """Closed-form continuous-time cell"""
    def __init__(self, input_dim, hidden_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim + hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
        )
        self.time_net = nn.Sequential(
            nn.Linear(input_dim + hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, x, h, dt=None):
        inp = torch.cat([x, h], dim=-1)
        f_val = self.net(inp)
        tau_val = torch.sigmoid(self.time_net(inp))
        
        # Closed-form update
        h_new = (1 - tau_val) * h + tau_val * f_val
        return h_new, h_new
```

## Stability Analysis

### Lyapunov Stability
System $\dot{h} = -h + f_\theta(h, x)$ is stable if:

$$\|f_\theta(h_1, x) - f_\theta(h_2, x)\| \leq \alpha \|h_1 - h_2\|, \quad \alpha < 1$$

- Ensures bounded outputs and no oscillations
- Satisfied by weight normalization

### Input-Output Stability
Bounded input $\Rightarrow$ bounded output (BIBO stable) for contractive $f_\theta$.

## What Makes LTC "Liquid"?
- **Adaptive dynamics**: Time constant changes per sample and per time step
- **Continuous depth**: Can be queried at any time point (not just discrete steps)
- **Causal**: No look-ahead, suitable for real-time control
- **Robustness**: Small perturbations in input don't cause catastrophic forgetting

## Applications

| Domain | Task | NCP Size | Parameter Reduction |
|--------|------|----------|-------------------|
| Autonomous driving | Lane-keeping | 19 neurons | 100x vs LSTM |
| Robotics | Legged locomotion | 30 neurons | 50x vs MLP |
| Climate | Weather prediction | 60 neurons | 20x vs LSTM |
| Medical | EEG classification | 40 neurons | 30x vs Transformer |

## Practical Considerations
- **ODE solver**: Use explicit RK4 for LTC (CfC bypasses the solver)
- **Initialization**: Initialize time-constant network to output $\tau \approx 1$
- **Regularization**: L1 on weights for sparsity (already sparse in NCP)
- **Memory**: CfC uses $O(T)$ memory (vs $O(TS)$ for ODE solver)
- **Parallelism**: CfC enables batch-parallel training across time steps

## Limitations
- **Capacity**: Very few parameters may not capture complex patterns in large datasets
- **ODE training**: LTC requires adjoint method or ODE solver (slower)
- **Scalability**: Sparse connectivity limits representational capacity
- **Overshooting**: CfC may overshoot in extrapolation beyond training time range
- **Hardware**: Continuous-time design targets neuromorphic chips (not widely available)

## References
- Hasani, Lechner, Amini, Rus, Grosu, "Liquid Time-Constant Networks", AAAI 2021
- Hasani, Lechner, Amini, Liebenwein, Ray, Rus, Grosu, "Closed-form continuous-time neural networks", Nature Machine Intelligence 2022
- Lechner, Hasani, Grosu, Rus, "Neural Circuit Policies", AAAI 2020
- Lechner, Hasani, Amini, Grosu, Rus, "Gated Graph Neural Circuit Policies", ICRA 2021
- Hasani et al., "Liquid Structural State-Space Models", ICLR 2023
