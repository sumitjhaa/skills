# 09.08 Efficient Attention

## Learning Objectives
- Understand quadratic complexity bottleneck in self-attention
- Implement sparse and linear attention mechanisms
- Apply Performer (FAVOR+) and Reformer (LSH) for efficiency
- Analyze trade-offs between speed, memory, and quality

## Self-Attention Complexity

### Standard Attention
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right) V$$

- Time: $O(n^2 d)$ where $n$ is sequence length
- Memory: $O(n^2)$ for attention matrix
- At $n=4096$, 16GB GPU runs out of memory for single head

## Sparse Attention

### Fixed Patterns
- **Strided**: Attend to every $k$-th token
- **Fixed**: Attend to tokens at fixed positions
- **Combined**: Strided + fixed patterns (Sparse Transformer)

### ImageGPT Style
- 2D attention patterns: attend to local + row + column

## Reformer (LSH Attention)

### Locality-Sensitive Hashing
$$h(x) = \arg\max([xR; -xR])$$

- $R$: random projection matrix
- Hash similar queries/keys to same bucket
- Only attend within buckets

### Chunked Feedforward
Reverse the layers to allow reversible computation:
$$y_1 = x_1 + \text{FFN}(x_2)$$
$$y_2 = x_2 + \text{Attention}(y_1)$$

Reversible: $x_2 = y_2 - \text{Attention}(y_1)$, $x_1 = y_1 - \text{FFN}(x_2)$

## Performer (FAVOR+)

### Linear Attention via Kernel Trick
$$\text{Attention}(Q, K, V)_i = \frac{\sum_j \phi(q_i)^\top \phi(k_j) v_j}{\sum_j \phi(q_i)^\top \phi(k_j)}$$

- $\phi$: feature map (positive orthogonal random features)
- $\phi(x) = \frac{1}{\sqrt{m}} f(Wx + b)$ where $f$ is elementwise positive

### Complexity
- Time: $O(ndm)$ where $m$ is feature dimension
- Typically $m = 64$ (much smaller than $n$)

## Linear Transformers (Katharopoulos 2020)

### Causal Linear Attention
$$V_i' = \frac{Q_i \odot (S_i)}{Z_i}, \quad S_i = S_{i-1} + K_i \otimes V_i, \quad Z_i = Z_{i-1} + K_i$$

- $S_i$: cumulative sum of $K_j \otimes V_j$ (outer product)
- $Z_i$: cumulative sum of $K_j$
- $Q_i \odot S_i$: elementwise multiplication

## Code: Linear Attention

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class LinearAttention(nn.Module):
    def __init__(self, dim, num_heads=8):
        super().__init__()
        self.num_heads = num_heads
        self.scale = (dim // num_heads) ** -0.5
        self.qkv = nn.Linear(dim, dim * 3)
        self.proj = nn.Linear(dim, dim)

    def forward(self, x, mask=None):
        B, T, D = x.shape
        qkv = self.qkv(x).reshape(B, T, 3, self.num_heads, -1)
        q, k, v = qkv.permute(2, 0, 3, 1, 4).unbind(0)
        
        # Apply ELU + 1 for positive features
        q = F.elu(q) + 1
        k = F.elu(k) + 1
        
        # Causal linear attention
        kv = (k.unsqueeze(-1) * v.unsqueeze(-2)).cumsum(dim=2)
        z = k.cumsum(dim=2)
        
        # Normalise
        attn = (q.unsqueeze(-2) * kv).sum(dim=-1)
        norm = (q.unsqueeze(-2) * z.unsqueeze(-1)).sum(dim=-1)
        out = attn / (norm + 1e-6)
        
        out = out.transpose(1, 2).reshape(B, T, D)
        return self.proj(out)
```

## FlashAttention

### Tiling
Compute attention without materialising $n \times n$ matrix:

1. Tile $Q, K, V$ into blocks that fit in SRAM
2. Compute attention per block
3. Accumulate outputs online (safe softmax)

### IO-Awareness
- HBM bandwidth is bottleneck (not FLOPs)
- FlashAttention: $O(n^2)$ FLOPs but $O(n)$ HBM reads

## Comparison

| Method | Time | Memory | Quality (LRA avg) | Best For |
|--------|------|--------|-------------------|----------|
| Full Attention | $O(n^2)$ | $O(n^2)$ | 54.8 | Short sequences |
| Reformer (LSH) | $O(n \log n)$ | $O(n)$ | 52.7 | Very long sequences |
| Performer | $O(n)$ | $O(n)$ | 61.3 | General purpose |
| Linear Transformer | $O(n)$ | $O(n)$ | 57.3 | Causal generation |
| FlashAttention | $O(n^2)$ | $O(n)$ | 54.8 | GPU-optimised short |

## Practical Considerations
- **Quality loss**: Linear attention degrades on tasks requiring precise alignment
- **Hardware**: FlashAttention is best on GPU; Performer works on CPU/TPU
- **Sequence length**: For n < 1024, full attention is fine
- **Training vs inference**: Linear attention benefits training more than autoregressive decoding

## References
- Kitaev, Kaiser, Levskaya, "Reformer: The Efficient Transformer", ICLR 2020
- Choromanski, Likhosherstov, et al., "Rethinking Attention with Performers", ICLR 2021
- Katharopoulos, Vyas, et al., "Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention", ICML 2020
- Dao, Fu, et al., "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness", NeurIPS 2022
- Child, Gray, Radford, Sutskever, "Generating Long Sequences with Sparse Transformers", 2019
