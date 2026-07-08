# 09.15 Inference Optimization

## Learning Objectives
- Understand key-value (KV) caching for autoregressive decoding
- Implement speculative decoding for faster generation
- Apply continuous batching and PagedAttention (vLLM)
- Analyze latency and throughput trade-offs

## KV Caching

### Problem
During decoding, each token's attention recomputes all previous key/value vectors.

### Solution
Cache $K$ and $V$ from previous steps:

```python
# Step t:
k_t = projection_k(x_t)    # (1, d_k)
v_t = projection_v(x_t)    # (1, d_v)
K = torch.cat([K_cache, k_t], dim=1)
V = torch.cat([V_cache, v_t], dim=1)
output = attention(q_t, K, V)
```

### Memory
- Each layer: $2 \times \text{seq\_len} \times d_k$ per head
- LLaMA-7B (32 layers, 32 heads, 128 d_head):
  - 2 × 1024 × 128 × 32 × 32 = 256 MB per sequence at 1024 tokens

### Multi-Query Attention (MQA)
Shared key/value heads reduce KV cache:

$$\text{MQA}: K, V \in \mathbb{R}^{1 \times d_k} \text{ (one head)}, Q \in \mathbb{R}^{h \times d_k}$$

- Reduces KV cache by $h$ times
- LLaMA-70B uses grouped-query attention (GQA), a middle ground

## Speculative Decoding

### Draft Model + Target Model
1. Draft model generates $K$ candidate tokens quickly
2. Target model validates all $K$ tokens in one forward pass
3. Accepted tokens: no quality loss, faster wall-clock time

### Acceptance Rate
$$\mathbb{E}[\text{tokens/step}] = \sum_{t=1}^K P(\text{accept} \geq t)$$

- With good draft model: 2-3x speedup
- Quality identical to target model alone

### Rejection Sampling
Accept token if $q(x) / p(x) \geq U(0,1)$ where:
- $p$: target model distribution
- $q$: draft model distribution

## Continuous Batching

### Static Batching
```
[Request A] → [Request A] → [Request A] → done
[Request B] → wait → [Request B] → [Request B] → done
```

### Continuous Batching
```
[A] [A] [B] [A] [B] [C] [A] [C] [B] [C] [C] [B] done
```

- Add/remove sequences from batch as they finish
- Maximises GPU utilisation
- Used in vLLM, TensorRT-LLM

## PagedAttention (vLLM)

### Problem
KV cache is fragmented (like OS memory).

### Solution
- Block-level memory management (16-32 tokens per block)
- Virtual memory allocation: logical → physical pages
- Copy-on-write for shared prefixes (beam search)

### Performance
- Up to 24x throughput over HuggingFace Transformers
- Near-zero waste: 99%+ KV cache utilisation

## Code: KV Cache with GQA

```python
import torch
import torch.nn as nn

class AttentionWithKVCache(nn.Module):
    def __init__(self, dim, num_heads, num_kv_heads):
        super().__init__()
        self.num_heads = num_heads
        self.num_kv_heads = num_kv_heads
        self.head_dim = dim // num_heads
        self.q_proj = nn.Linear(dim, num_heads * self.head_dim)
        self.k_proj = nn.Linear(dim, num_kv_heads * self.head_dim)
        self.v_proj = nn.Linear(dim, num_kv_heads * self.head_dim)
        self.o_proj = nn.Linear(num_heads * self.head_dim, dim)

    def forward(self, x, kv_cache=None, start_pos=0):
        B, T, _ = x.shape
        q = self.q_proj(x).view(B, T, self.num_heads, -1)
        k = self.k_proj(x).view(B, T, self.num_kv_heads, -1)
        v = self.v_proj(x).view(B, T, self.num_kv_heads, -1)
        
        # KV cache
        if kv_cache is not None:
            k_cache, v_cache = kv_cache
            k = torch.cat([k_cache, k], dim=1)
            v = torch.cat([v_cache, v], dim=1)
        
        # GQA: expand kv heads to match q heads
        k = k.repeat_interleave(self.num_heads // self.num_kv_heads, dim=2)
        v = v.repeat_interleave(self.num_heads // self.num_kv_heads, dim=2)
        
        out = F.scaled_dot_product_attention(
            q.transpose(1, 2),
            k.transpose(1, 2),
            v.transpose(1, 2),
            is_causal=(T > 1)
        ).transpose(1, 2).reshape(B, T, -1)
        
        return self.o_proj(out), (k, v)
```

## Inference Frameworks Comparison

| Framework | Technique | Throughput | Latency | Ease of Use |
|-----------|----------|-----------|---------|-------------|
| HuggingFace | Static batching | 1x | Fast | Easy |
| vLLM | PagedAttention | 10-24x | Fast | Easy |
| TensorRT-LLM | Custom kernels | 15-30x | Fastest | Hard |
| TGI (HF) | Continuous batching | 5-10x | Fast | Medium |

## Practical Considerations
- **Prefix caching**: Cache shared prefixes (e.g., system prompt) across requests
- **FlashAttention**: Reduces memory via tiling (essential for long contexts)
- **Quantization**: INT8/FP8 KV cache reduces memory by 2x at negligible quality loss
- **Block size**: 16-32 tokens per block balances fragmentation and overhead

## References
- Pope, Douglas, et al., "Efficiently Scaling Transformer Inference", MLSys 2023
- Kwon, Li, et al., "Efficient Memory Management for Large Language Model Serving with PagedAttention", SOSP 2023
- Leviathan, Kalman, Matias, "Fast Inference from Transformers via Speculative Decoding", ICML 2023
- Stern, Shazeer, Uszkoreit, "Blockwise Parallel Decoding for Deep Autoregressive Models", NeurIPS 2018
- Shazeer, "Fast Transformer Decoding: One Write-Head is All You Need (MQA)", 2019
