# Lesson 07.13: SSMs (S4, Mamba)

## Learning Objectives
- Understand state space models for sequence modeling
- Derive S4 discretization with HiPPO theory
- Implement Mamba's selective scan algorithm
- Compare SSM complexity with transformers

## Theory
State Space Models (SSMs) represent sequences via continuous-time latent dynamics:

$$\dot{h}(t) = A h(t) + B x(t)$$
$$y(t) = C h(t) + D x(t)$$

- $h(t) \in \mathbb{R}^N$: latent state
- $x(t)$: input signal
- $y(t)$: output signal
- $A$: evolution matrix, $B$: input matrix, $C$: output matrix, $D$: skip connection

## Discretization

### Zero-Order Hold (ZOH)
$$\bar{A} = \exp(\Delta A)$$
$$\bar{B} = (\bar{A} - I) A^{-1} B$$

### Bilinear (Tustin) Transform
$$\bar{A} = (I + \Delta A/2)(I - \Delta A/2)^{-1}$$
$$\bar{B} = \Delta (I + \Delta A/2)^{-1} B$$

### Discrete Recurrence
$$h_k = \bar{A} h_{k-1} + \bar{B} x_k$$
$$y_k = C h_k + D x_k$$

## HiPPO Theory
Initializes $A$ to store input history as coefficients of orthogonal polynomials (Legendre):

$$A_{nk} = -(2n+1)^{1/2}(2k+1)^{1/2}, \quad n > k$$
$$A_{nn} = -(n+1)$$
$$B_n = (2n+1)^{1/2}$$

**Key property**: HiPPO matrix ensures the state $h(t)$ memorizes the full history of $x(t)$ compressed into $N$ coefficients.

## S4 (Structured State Space)

### Normal Plus Low-Rank (NPLR)
$$\bar{A} = \Lambda - P Q^\top$$

- $\Lambda$: diagonal matrix (complex-valued)
- $P, Q$: low-rank factors
- Enables $O(N)$ computation via Woodbury identity

### Training Mode: Convolution
$$y = \bar{C} \odot \text{FFT}^{-1}(\text{FFT}(\bar{K}) \odot \text{FFT}(x))$$
$$\bar{K} = (\bar{C} \bar{B}, \bar{C} \bar{A} \bar{B}, \dots, \bar{C} \bar{A}^{L-1} \bar{B})$$

- **Parallel training**: Entire sequence processed at once via convolution
- $O(L \log L)$ with FFT, or $O(L)$ with recurrence

### Inference Mode: Recurrence
Step-by-step $O(1)$ per timestep — linear in sequence length.

## Mamba (Selective State Space)

### Selection Mechanism
Standard SSMs have input-independent $(\bar{A}, \bar{B}, \bar{C})$. Mamba makes them **input-dependent**:

$$\Delta = \text{softplus}(W_\Delta x + b_\Delta)$$
$$B = W_B x + b_B$$
$$C = W_C x + b_C$$

**Effect**: Model selectively filters/ignores input tokens based on content.

### Hardware-Aware Parallel Scan
1. **Kernel fusion**: Avoid materializing full $\bar{A}, \bar{B}$ tensors in HBM
2. **Parallel associative scan**: $O(\log L)$ depth on GPU via binary tree reduction
3. **SRAM optimization**: Store scan state in fast on-chip memory

## S4 vs Mamba

| Aspect | S4 | Mamba |
|--------|-----|-------|
| Parameters | Static $A,B,C,\Delta$ | Input-dependent $B,C,\Delta$ |
| Context | Full (HiPPO memory) | Selective (content-based filtering) |
| Training | Convolution (FFT) | Parallel scan |
| Inference | $O(1)$ per step | $O(1)$ per step |
| Long-range | Excellent (HiPPO) | Excellent (selectivity) |
| Language modeling | Good | SOTA (matches Transformers) |

## Code: Simplified Mamba Block

```python
import torch
import torch.nn as nn

class MambaBlock(nn.Module):
    def __init__(self, d_model, d_state=16, d_conv=4):
        super().__init__()
        self.in_proj = nn.Linear(d_model, 2 * d_model)
        self.conv1d = nn.Conv1d(d_model, d_model, d_conv, padding=d_conv-1, groups=d_model)
        self.x_proj = nn.Linear(d_model, d_state * 2 + 1)
        self.dt_proj = nn.Linear(d_model, d_model)
        self.A = nn.Parameter(torch.randn(d_model, d_state))
        self.out_proj = nn.Linear(d_model, d_model)

    def selective_scan(self, x, delta, B, C):
        # Simplified selective scan (parallel version much more complex)
        h = torch.zeros(x.shape[0], self.A.shape[0], x.shape[1], device=x.device)
        y = []
        for t in range(x.shape[2]):
            dt = delta[:, :, t].unsqueeze(-1)
            A_bar = torch.exp(dt * self.A)
            B_bar = dt * B[:, :, t].unsqueeze(1)
            h = A_bar * h + B_bar * x[:, :, t].unsqueeze(-1)
            y_t = (h * C[:, :, t].unsqueeze(1)).sum(dim=-1)
            y.append(y_t)
        return torch.stack(y, dim=-1)

    def forward(self, x):
        # x: (B, L, D)
        x_res = x
        x = self.in_proj(x)
        x, gate = x.chunk(2, dim=-1)
        x = x.transpose(1, 2)
        x = self.conv1d(x)[:, :, :x.shape[2]]
        x = nn.SiLU()(x.transpose(1, 2))
        delta, B, C = self.x_proj(x).split([1, d_state, d_state], dim=-1)
        delta = nn.functional.softplus(self.dt_proj(delta))
        y = self.selective_scan(x, delta, B, C)
        return self.out_proj(y * nn.SiLU()(gate)) + x_res
```

## Practical Considerations
- **State dimension**: $N = 16$ typically sufficient (vs 512-1024 for RNN hidden states)
- **Convolution kernel**: $d_{\text{conv}} = 4$ for local context mixing before SSM
- **Resolution**: $\Delta$ controls how discretization step is parameterized
- **Numerical stability**: Log-space parameterization of $\bar{A}$ to avoid exploding eigenvalues

## Limitations
- **No content-based recall**: SSMs mix inputs linearly — can't look up specific tokens like attention
- **Hardware optimization**: Selective scan requires custom CUDA kernels (not off-the-shelf)
- **Pretraining overhead**: Mamba's parallel scan uses more memory than transformer at very long sequences
- **Modal flexibility**: Less studied for images, video, graphs compared to transformers

## References
- Gu, Goel, Re, "Efficiently Modeling Long Sequences with Structured State Spaces (S4)", ICLR 2022
- Gu, Johnson, Goel, Saab, Dao, Rudra, Re, "Combining Recurrent, Convolutional, and Continuous-time Models with the Linear State Space Layer (LSSL)", NeurIPS 2021
- Gu, Dao, "Mamba: Linear-Time Sequence Modeling with Selective State Spaces", 2023
- Gu, "HiPPO: Recurrent Memory with Optimal Polynomial Projections", NeurIPS 2020
- Dao, Gu, "Transformers are SSMs: Generalized Models and Efficient Algorithms", 2024
