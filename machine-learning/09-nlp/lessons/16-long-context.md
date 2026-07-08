# 09.16 Long-Context LLMs

## Learning Objectives
- Understand context extension techniques (position interpolation, NTK-aware scaling)
- Implement YaRN (Yet another RoPE extensioN) for 128K+ context
- Apply Ring Attention and Flash Attention for long sequences
- Evaluate on long-context benchmarks (LongBench, RULER, Needle-in-a-Haystack)

## Context Extension Problem

### Goal
Extend pretrained LLMs (typically 2K-4K context) to 32K-128K+ tokens without full retraining.

## Position Interpolation (PI)

### Method
Scale position indices to match training range:

$$\text{RoPE}(\text{pos}'_i) = \text{RoPE}\left(\frac{L_{\text{train}}}{L_{\text{target}}} \cdot i\right)$$

- If $L_{\text{train}} = 4096$ and $L_{\text{target}} = 16384$: scale = 0.25
- Linear interpolation of positions

### Results
- Extends LLaMA from 2K → 32K with fine-tuning (1000 steps)
- Slight perplexity degradation at original length

## NTK-Aware Scaling

### Theory
High-frequency dimensions in RoPE encode local information (harder to interpolate).

### Method
Different scaling per dimension:

$$\lambda_i = \alpha - (\alpha - 1) \cdot \frac{i}{d/2}$$

- $\alpha$: scaling factor (e.g., 2 for 2x context)
- High-frequency dims scaled less (preserve local info)
- Low-frequency dims scaled more (capture long-range info)

### Code
```python
def ntk_scaled_rope(pos, dim, alpha=2.0):
    scale = alpha ** (torch.arange(0, dim, 2) / dim)
    theta = 10000.0 ** (-torch.arange(0, dim, 2) / dim)
    return torch.sin(pos * theta / scale), torch.cos(pos * theta / scale)
```

## YaRN (Yet another RoPE extensioN)

### Two Improvements over NTK
1. **NTK-aware interpolation**: Different scaling per dimension
2. **Temperature tuning**: Scale attention logits:
   $$\text{Attention}' = \text{softmax}\left(\frac{QK^\top}{\sqrt{d} \cdot t}\right)$$
   - $t = \sqrt{1/\text{scale}}$ to preserve entropy

### Results
- LLaMA-7B: 4K → 128K with < 1000 fine-tuning steps
- Perfect Needle-in-a-Haystack at 128K

## Ring Attention

### Problem
Standard attention on $n$ GPUs:
$$\text{each GPU: } O\left(\frac{n^2}{g}\right) \text{ memory, all-reduce}$$

### Solution
Distribute sequence across GPUs in a ring, overlap compute + communication:

```
GPU 0: tokens [0, n/4)  →  compute block attention  →  send to GPU 1
GPU 1: tokens [n/4, n/2) →  receive from GPU 0  →  compute  →  send to GPU 2
```

- Memory: $O(n/g)$ per GPU
- Scales to 4M+ tokens with 8 GPUs

## Long-Context Benchmarks

### Needle-in-a-Haystack
Insert target sentence at varying depth in long document → recall accuracy.

| Model | Training | Needle@4K | Needle@8K | Needle@16K | Needle@32K |
|-------|----------|-----------|-----------|------------|------------|
| LLaMA-2 (7B) | 4K | 100% | 0% | 0% | 0% |
| LLaMA-2 + PI | 8K | 100% | 99% | 0% | 0% |
| LLaMA-2 + YaRN | 8K | 100% | 100% | 99% | 82% |
| GPT-4 | 128K | 100% | 100% | 100% | 100% |

## Code: YaRN RoPE

```python
import torch
import math

def yarn_rope(x, seq_len, max_train_len=4096, alpha=8.0, beta=0.1):
    """Apply YaRN rotation to x: (B, T, H, D)"""
    B, T, H, D = x.shape
    dim = D // 2
    
    # Scale factor
    scale = max_train_len / seq_len
    t = scale ** (alpha / (alpha - 1))
    
    # Compute frequencies with NTK scaling
    freqs = 10000.0 ** (-torch.arange(0, D, 2) / D)
    temp_scale = scale ** (torch.arange(0, D, 2) / D)
    freqs = freqs / temp_scale
    
    # Apply rotation
    pos = torch.arange(T, device=x.device)
    angles = pos.unsqueeze(-1) * freqs.unsqueeze(0)
    cos = angles.cos().unsqueeze(0).unsqueeze(2)
    sin = angles.sin().unsqueeze(0).unsqueeze(2)
    
    # Rotate half
    x1, x2 = x[..., :dim], x[..., dim:]
    x_rot = torch.cat([x1 * cos - x2 * sin, x1 * sin + x2 * cos], dim=-1)
    
    return x_rot, t  # temperature for attention scaling
```

## Practical Considerations
- **Fine-tuning data**: Use long-context data (books, code, papers)
- **Attention sink**: Models attend heavily to first tokens → use special sink tokens
- **Window attention**: Combine local window + global tokens for efficiency
- **Training vs inference**: PI/YaRN work at inference with minimal fine-tuning

## References
- Chen, Wong, et al., "Extending Context Window of Large Language Models via Positional Interpolation", 2023
- bloc97, "NTK-Aware Scaled RoPE allows LLaMA models to have extended (8k+) context size without any fine-tuning", 2023
- Peng, Quesnelle, et al., "YaRN: Efficient Context Window Extension of Large Language Models", 2023
- Liu, Lin, et al., "Ring Attention with Blockwise Transformers for Near-Infinite Context", 2023
- Li, Chen, et al., "LongBench: A Bilingual, Multitask Benchmark for Long Context Understanding", 2024
