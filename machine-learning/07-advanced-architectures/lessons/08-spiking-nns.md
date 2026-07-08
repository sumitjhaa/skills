# Lesson 07.08: Spiking Neural Networks

## Learning Objectives
- Understand LIF neuron dynamics and spike generation
- Implement surrogate gradient training (STBP, SuperSpike)
- Apply SNNs for temporal sequence processing
- Analyze energy efficiency of event-driven computation

## Theory
SNNs process information via discrete spike events over time, mimicking biological neurons.

## Leaky Integrate-and-Fire (LIF) Neuron

### Membrane Potential Dynamics
$$\tau \frac{dV(t)}{dt} = -V(t) + I(t)$$

- $V(t)$: membrane potential
- $\tau$: membrane time constant
- $I(t)$: input current (from pre-synaptic spikes)

### Spike Generation
$$V(t) \geq V_{\text{th}} \implies \text{fire spike}, V(t) \leftarrow V_{\text{reset}}$$

### Discrete Formulation
$$V[t] = \beta V[t-1] + W X[t] - V_{\text{th}} \cdot S[t-1]$$

- $\beta = e^{-\Delta t / \tau}$: decay factor
- $X[t]$: input at time $t$
- $S[t]$: output spike: $S[t] = H(V[t] - V_{\text{th}})$ where $H$ is Heaviside step

## Surrogate Gradients
The Heaviside step function has zero gradient almost everywhere — need surrogate:

### Straight-Through Estimator (STE)
$$\frac{\partial S}{\partial V} \approx \sigma'(V - V_{\text{th}})$$

Common choices for $\sigma'$:
- **Rectangular**: $1_{|V - V_{\text{th}}| < 0.5}$
- **Sigmoid**: $\sigma(V - V_{\text{th}}) \cdot (1 - \sigma(V - V_{\text{th}}))$
- **Fast sigmoid**: $\frac{1}{(1 + \beta|V - V_{\text{th}}|)^2}$

### STBP (Spatio-Temporal Backpropagation)
Backpropagate through both spatial (layer) and temporal (time step) dimensions.

## Neuron Models Comparison

| Model | Equations | Firing Patterns | Computational Cost |
|-------|-----------|----------------|-------------------|
| LIF | $\tau \dot{V} = -V + I$ | Regular spiking | Low |
| Izhikevich | $\dot{v} = 0.04v^2 + 5v + 140 - u + I$, $\dot{u} = a(bv - u)$ | 20+ patterns | Medium |
| Hodgkin-Huxley | 4 coupled ODEs | Biophysical | High |

## Training Methods

| Method | Description | Accuracy |
|--------|-------------|----------|
| ANN-to-SNN | Convert ReLU ANN to SNN by replacing with IF neurons | High (no gradient) |
| Surrogate gradient | Backprop through surrogate in time | Highest |
| STDP | Local unsupervised learning | Moderate |
| SpikeProp | Early BP for SNNs (too slow) | Low |

### ANN-to-SNN Conversion
1. Train ANN with ReLU
2. Replace ReLU with Integrate-and-Fire (IF) neurons
3. Scale thresholds: $\theta = \max$ activation per layer
4. **Trade-off**: More time steps $\to$ higher accuracy (lower approximation error)

## Code: LIF Neuron with Surrogate Gradient

```python
import torch
import torch.nn as nn

class LIFNeuron(nn.Module):
    def __init__(self, threshold=1.0, decay=0.5):
        super().__init__()
        self.threshold = threshold
        self.decay = decay

    def surrogate_grad(self, v):
        """Fast sigmoid surrogate gradient"""
        return 1.0 / (1.0 + self.beta * torch.abs(v - self.threshold)) ** 2

    def forward(self, x, state=None):
        batch, timesteps = x.shape[0], x.shape[1]
        if state is None:
            v = torch.zeros(batch, self.hidden, device=x.device)
        else:
            v = state.view(batch, self.hidden)

        spikes = []
        for t in range(timesteps):
            v = self.decay * v + self.fc(x[:, t])
            spk = (v > self.threshold).float()
            v = v - spk * self.threshold
            spikes.append(spk)

        return torch.stack(spikes, dim=1)
```

## Temporal Coding
Information encoded in spike timing:

| Coding scheme | Representation | Advantage |
|--------------|---------------|-----------|
| Rate coding | Spike count over window | Robust to noise |
| Temporal coding | Precise spike times | Efficient (fewer spikes) |
| First-spike | Time to first spike | Fast inference |
| Rank coding | Order of spike arrival | Invariant to intensity |

## Energy Efficiency
- **Event-driven**: Compute only when spikes occur
- **Multiply-accumulate (MAC)** $\to$ **accumulate (AC)**: $w \cdot x$ with binary $x$ reduces to addition
- **Neuromorphic hardware**: Loihi, TrueNorth, Speck — $10^5\times$ energy reduction

### Energy Comparison
| Operation | ANN (MAC) | SNN (AC) | Ratio |
|-----------|-----------|----------|-------|
| 32-bit add | 0.9 pJ | 0.1 pJ | 9x |
| 32-bit multiply | 3.1 pJ | N/A | N/A |
| 1 inference | 10 mJ | 0.1 mJ (sparse) | 100x |

## Applications
- **Event-based vision**: DVS camera data (asynchronous pixel changes)
- **Speech recognition**: Temporal patterns in audio
- **Reinforcement learning**: Energy-efficient robot control
- **Edge AI**: On-device inference with neuromorphic chips

## Practical Considerations
- **Simulation time steps**: 10-100 for most tasks; more steps = more accurate but slower
- **Reset mechanism**: Subtract threshold (soft reset) vs set to zero (hard reset)
- **Initial membrane potential**: Zero is default; learnable initial state helps
- **Batch normalization**: Need temporal BN (separate stats per time step)
- **Skip connections**: Help gradient flow through many time steps

## Limitations
- **Training complexity**: Surrogate gradients introduce bias in gradient estimates
- **Latency**: Need multiple time steps for rate-based codes
- **Hardware**: Neuromorphic chips not widely available
- **Accuracy gap**: SNNs lag behind ANNs on ImageNet (though gap is closing)

## References
- Maass, "Networks of spiking neurons: the third generation of neural network models", Neural Networks 1997
- Neftci, Mostafa, Gerstner, "Surrogate Gradient Learning in Spiking Neural Networks", IEEE Signal Processing Magazine 2019
- Wu et al., "Spatio-temporal backpropagation for SNN training", Advances in Neural Information Processing Systems 2018
- Zenke & Ganguli, "SuperSpike: Supervised Learning in Multilayer Spiking Neural Networks", Neural Computation 2018
- Gerstner & Kistler, "Spiking Neuron Models", Cambridge University Press 2002
