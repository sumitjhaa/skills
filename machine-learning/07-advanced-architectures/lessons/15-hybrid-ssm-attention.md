# Lesson 07.15: Hybrid SSM-Attention (Jamba, MambaFormer)

## Learning Objectives
- Understand hybrid architectures combining SSM and attention
- Implement interleaved SSM-attention blocks
- Apply MoE with SSMs for increased capacity
- Analyze trade-offs between efficiency and recall

## Motivation
SSMs and attention have complementary strengths:

| Operation | SSM | Attention |
|-----------|-----|-----------|
| Complexity | Linear in $L$ | Quadratic in $L$ |
| Content-based recall | Weak | Strong |
| Long-range mixing | Excellent (HiPPO/scan) | Excellent |
| Local mixing | Weak (via conv) | Strong (attention window) |
| Hardware efficiency | High (scan) | Moderate (FlashAttention) |

**Hybrid**: Use SSM for most tokens, attention when content-based recall matters.

## Jamba (AI21 Labs, 2024)

### Architecture
```
Input → [Mamba × M] → [Attention × 1] → [Mamba × M] → [MoE FFN] → ... → output
```

### Key Design Choices
1. **Layer interleaving**: Insert 1 attention layer per $M$ Mamba layers ($M=8$)
2. **Mixture-of-Experts (MoE)**: Replace dense FFN with top-2 MoE
3. **Sliding window attention**: $W=4096$ tokens window
4. **Hybrid scanning**: Mamba handles full context, attention handles recall

### Scaling
- 52B total parameters, 12B active (MoE)
- 256K token context length (Mamba handles long context, attention only slides)
- 1M tokens throughput on 8 GPUs

## MambaFormer

### Architecture
```
x → MambaBlock → LayerNorm → AttentionBlock → LayerNorm → FFN → output
```

- **Mamba block**: Handles sequence-level mixing (efficient)
- **Attention block**: Handles token-level interactions (recall)
- Applied in every layer (dense hybrid, not interleaved)

### Why Both in Every Layer?
- Mamba provides global context efficiently
- Attention provides precise token interactions
- FFN provides channel mixing

## S4ND (Multi-Dimensional SSM + Axial Attention)

### Multi-Dimensional SSM
Extend S4 to images/video by scanning along each dimension:

$$h_{t}^{(1)} = \bar{A}^{(1)} h_{t-1}^{(1)} + \bar{B}^{(1)} x_t \quad \text{(rows)}$$
$$h_{t}^{(2)} = \bar{A}^{(2)} h_{t-1}^{(2)} + \bar{B}^{(2)} x_t \quad \text{(cols)}$$

- **Independent SSMs** per dimension
- **Combined**: $y_t = C^{(1)} h_t^{(1)} + C^{(2)} h_t^{(2)} + D x_t$

### Axial Attention
Apply attention along one dimension at a time (row then column) — reduces $O(HW)$ to $O(H + W)$.

## Hybrid Configurations

| Configuration | SSM Layers | Attn Layers | MoE | Compute | Memory |
|-------------|-----------|-------------|-----|---------|--------|
| Pure Mamba | 100% | 0% | Optional | $O(L)$ | Low |
| Jamba-8 | 89% | 11% (every 8th) | Yes | $O(L + \frac{LW}{M})$ | Medium |
| Jamba-4 | 80% | 20% | Yes | $O(L + \frac{LW}{M})$ | Medium |
| MambaFormer | 50% | 50% (every layer) | No | $O(L + n^2)$ | High |
| Pure Transformer | 0% | 100% | Optional | $O(L^2)$ | High |

## Code: Jamba-Style Block

```python
import torch
import torch.nn as nn

class JambaBlock(nn.Module):
    def __init__(self, d_model, is_attention_layer=False, use_moe=False, n_experts=8):
        super().__init__()
        self.norm = nn.LayerNorm(d_model)
        
        if is_attention_layer:
            self.mixer = nn.MultiheadAttention(d_model, num_heads=8, 
                                               batch_first=True)
        else:
            from mamba import MambaBlock
            self.mixer = MambaBlock(d_model)
        
        self.ffn = nn.Sequential(
            nn.Linear(d_model, 4 * d_model),
            nn.SiLU(),
            nn.Linear(4 * d_model, d_model),
        ) if not use_moe else MoEBlock(d_model, n_experts)

    def forward(self, x, attn_mask=None):
        if isinstance(self.mixer, nn.MultiheadAttention):
            x = x + self.mixer(self.norm(x), self.norm(x), self.norm(x), 
                               attn_mask=attn_mask)[0]
        else:
            x = x + self.mixer(self.norm(x))
        x = x + self.ffn(self.norm(x))
        return x
```

## Empirical Findings
- **Quality**: Jamba 7B matches Llama 2 7B on most benchmarks, better on long-context tasks
- **Efficiency**: 3x throughput of pure transformer of same parameter count
- **Attention frequency**: $M=8$ (every 8th layer) finds sweet spot between efficiency and quality
- **Long context**: Hybrid model maintains perplexity at 256K tokens while pure transformer degrades

## Practical Considerations
- **Attention window**: Sliding window of 4096 tokens for attention layers
- **SSM context**: Full sequence (unlimited) via Mamba scan
- **Combined KV cache**: Mamba has no KV cache; attention has sliding window cache
- **MoE routing**: Top-2 experts, load-balanced with auxiliary loss
- **Hybrid parallelism**: Tensor parallelism + pipeline parallelism + expert parallelism

## Limitations
- **Engineering complexity**: Two different architectures to optimize
- **Custom kernels**: Mamba requires custom selective scan CUDA kernels
- **KV cache still needed**: Attention layers still require KV cache (though smaller)
- **Optimal ratio**: Best SSM:attention ratio depends on task and compute budget

## Future Directions
- **Learned routing**: Model decides per-layer or per-token whether to use SSM or attention
- **Quantization**: Hybrid models benefit from 8/4-bit quantization for both components
- **Multimodal**: Extend to images (S4ND) + text (Mamba) + attention for cross-modal interaction

## References
- Lieber, Sharir, et al., "Jamba: A Hybrid Transformer-Mamba Language Model", 2024
- Goyal, Pokle, et al., "MambaFormer: Combining Selective State Spaces and Attention", 2024
- Nguyen, Goel, Gu, et al., "S4ND: Modeling Images and Videos as Multidimensional Signals with State Spaces", NeurIPS 2022
- Fedus, Zoph, Shazeer, "Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity", JMLR 2022
- Dao, "FlashAttention: Efficient Exact Attention with IO-Awareness", NeurIPS 2022
