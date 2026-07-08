# 09.07 Long-Range Dependencies

## Learning Objectives
- Understand vanishing/exploding gradients in RNNs
- Implement LSTMs and GRUs for long sequences
- Apply Transformer-XL and Longformer for long documents
- Analyze memory and attention mechanisms for long context

## Vanishing & Exploding Gradients

### Problem
$$\frac{\partial \mathcal{L}_T}{\partial \theta} = \sum_{t=1}^T \frac{\partial \mathcal{L}_T}{\partial h_T} \left( \prod_{k=t}^{T-1} \frac{\partial h_{k+1}}{\partial h_k} \right) \frac{\partial h_t}{\partial \theta}$$

- If eigenvalues of $\frac{\partial h}{\partial h}$ are $< 1$, gradient → 0 (vanishing)
- If eigenvalues are $> 1$, gradient → $\infty$ (exploding)

### Solutions
- Gradient clipping: $\|g\| \leftarrow \min(\|g\|, \text{clip})$
- Gated architectures (LSTM, GRU)
- Residual connections
- Proper initialisation (Xavier, He)

## LSTM (Long Short-Term Memory)

### Gates
$$\begin{aligned}
i_t &= \sigma(W_{xi} x_t + W_{hi} h_{t-1} + b_i) \\
f_t &= \sigma(W_{xf} x_t + W_{hf} h_{t-1} + b_f) \\
o_t &= \sigma(W_{xo} x_t + W_{ho} h_{t-1} + b_o) \\
g_t &= \tanh(W_{xg} x_t + W_{hg} h_{t-1} + b_g) \\
c_t &= f_t \odot c_{t-1} + i_t \odot g_t \\
h_t &= o_t \odot \tanh(c_t)
\end{aligned}$$

- $i_t$: input gate (what to write)
- $f_t$: forget gate (what to erase)
- $o_t$: output gate (what to expose)
- $c_t$: cell state (memory)

## GRU (Gated Recurrent Unit)

### Simplified Gates
$$\begin{aligned}
z_t &= \sigma(W_{xz} x_t + W_{hz} h_{t-1} + b_z) \\
r_t &= \sigma(W_{xr} x_t + W_{hr} h_{t-1} + b_r) \\
n_t &= \tanh(W_{xn} x_t + W_{hn} (r_t \odot h_{t-1}) + b_n) \\
h_t &= (1 - z_t) \odot h_{t-1} + z_t \odot n_t
\end{aligned}$$

- Fewer parameters than LSTM
- Comparable performance for many tasks

## Transformer-XL

### Segment-Level Recurrence
Cache previous segment's hidden states:

$$\tilde{h}_\tau = [\text{SG}(h_{\tau-1}), h_\tau]$$

- $h_{\tau-1}$: cached (gradients stopped)
- $h_\tau$: current segment
- Context: up to 2× segment length

### Relative Positional Encodings
$$a_{ij} = q_i^\top k_j + q_i^\top \tilde{W} p_{i-j} + \tilde{u}^\top k_j + \tilde{v}^\top \tilde{W} p_{i-j}$$

- $p_{i-j}$: learnable relative position embedding
- No absolute position encoding needed

## Longformer

### Attention Pattern
```
Local window (w) + Global tokens + Dilated sliding
```

- **Local**: Each token attends to $w$ neighbours (w=512)
- **Global**: Select tokens attend to all (e.g., [CLS] tokens)
- **Dilated**: Skip tokens to expand receptive field

### Complexity
- Full attention: $O(n^2)$
- Longformer: $O(n \cdot w)$

## Code: LSTM Implementation

```python
import torch
import torch.nn as nn

class LSTMCell(nn.Module):
    def __init__(self, input_size, hidden_size):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.gates = nn.Linear(input_size + hidden_size, 4 * hidden_size)

    def forward(self, x, state):
        h, c = state
        combined = torch.cat([x, h], dim=-1)
        gates = self.gates(combined)
        i, f, o, g = gates.chunk(4, dim=-1)
        i, f, o, g = torch.sigmoid(i), torch.sigmoid(f), torch.sigmoid(o), torch.tanh(g)
        c_next = f * c + i * g
        h_next = o * torch.tanh(c_next)
        return h_next, (h_next, c_next)
```

## Long-Range Arena (LRA) Benchmark

| Model | ListOps | Text | Retrieval | Image | Pathfinder | Avg |
|-------|---------|------|-----------|-------|-----------|-----|
| Transformer | 36.4% | 63.6% | 70.2% | 41.9% | 62.1% | 54.8% |
| Longformer | 35.6% | 63.2% | 56.2% | 42.1% | 67.7% | 53.0% |
| BigBird | 36.8% | 63.4% | 59.6% | 42.4% | 74.2% | 55.3% |
| Performer | 37.1% | 64.3% | 77.9% | 41.8% | 85.2% | 61.3% |
| S4 | 59.6% | 86.8% | 90.9% | 88.6% | 94.2% | 84.0% |

## References
- Hochreiter & Schmidhuber, "Long Short-Term Memory", Neural Computation 1997
- Cho, van Merrienboer, et al., "Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation (GRU)", EMNLP 2014
- Dai, Yang, et al., "Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context", ACL 2019
- Beltagy, Peters, Cohan, "Longformer: The Long-Document Transformer", 2020
- Tay, Dehghani, et al., "Long Range Arena: A Benchmark for Efficient Transformers", ICLR 2021
