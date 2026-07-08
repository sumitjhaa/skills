# 09.09 Positional Encodings

## Learning Objectives
- Understand why Transformers need positional information
- Implement sinusoidal and learned positional encodings
- Apply RoPE (Rotary Position Embedding) and AliBi
- Analyze positional encoding effects on length generalisation

## Motivation

### Why Positional Encodings?
Self-attention is permutation-invariant:

$$\text{Attention}(Q, K, V) = \text{softmax}(QK^\top)V$$

Without position information, "dog bites man" == "man bites dog".

## Sinusoidal Encodings (Vaswani 2017)

### Formula
$$PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)$$
$$PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)$$

### Properties
- Each dimension is a sinusoid with different frequency
- $PE_{pos+k}$ can be expressed as linear function of $PE_{pos}$
- No learned parameters (fixed)
- Extrapolates to unseen sequence lengths

## Learned Positional Encodings (BERT/GPT)

### Embedding Table
```python
self.pos_embed = nn.Embedding(max_len, d_model)
pos = torch.arange(max_len)
x = x + self.pos_embed(pos)
```

- Each position learns independent vector
- Cannot extrapolate beyond max training length (e.g., BERT 512 tokens)
- BERT/GPT-2 use learned embeddings

## Relative Positional Encodings

### Shaw et al. (2018)
$$a_{ij} = q_i^\top k_j + q_i^\top w_{i-j}$$

- $w_{i-j}$: learnable relative position embedding
- Clipped: $|i-j| \leq k$ (beyond k, use same embedding)

### Transformer-XL
$$a_{ij} = q_i^\top k_j + q_i^\top \tilde{W} p_{i-j} + \tilde{u}^\top k_j + \tilde{v}^\top \tilde{W} p_{i-j}$$

- $p_{i-j}$: sinusoid-based relative encoding (fixed)
- $\tilde{u}, \tilde{v}$: learned global biases

## RoPE (Rotary Position Embedding)

### Rotation
$$\Theta(x_m, m) = R_m x_m$$

- $R_m$: rotation matrix that depends on position $m$
- Rotation angle = $m \cdot \theta_i$ where $\theta_i = 10000^{-2i/d}$

### Key Property
$$q_m^\top k_n = (R_m q)^\top (R_n k) = q^\top R_{n-m} k$$

- Attention depends only on relative position $n-m$
- Used in LLaMA, GPT-NeoX, PaLM

## AliBi (Attention with Linear Biases)

### Bias Addition
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}} + m \cdot B\right) V$$

- $B$: static bias matrix where $B_{i,j} = -|i - j|$
- $m$: head-specific slope (geometric sequence: $2^{-2^{-k}}$)

### Advantages
- No learned positional parameters
- Extrapolates very well to longer sequences
- Used in MPT, Bloom

## Code: Sinusoidal Encoding

```python
import torch
import torch.nn as nn
import math

class SinusoidalPosEncoding(nn.Module):
    def __init__(self, d_model, max_len=2048):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * 
                             (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe.unsqueeze(0))

    def forward(self, x):
        # x: (B, T, D)
        return x + self.pe[:, :x.size(1)]
```

## Extrapolation Comparison

| Method | Train Length | Eval Length (perplexity) | Notes |
|--------|-------------|-------------------------|-------|
| Sinusoidal | 512 | 512: 18, 1024: 18 | Extrapolates well |
| Learned (BERT) | 512 | 512: 18, 1024: 1000+ | Fails beyond 512 |
| RoPE | 2048 | 2048: 10, 4096: 11 | Good extrapolation |
| AliBi | 2048 | 2048: 10, 8192: 11 | Excellent extrapolation |

## Practical Considerations
- **Short vs long models**: Sinusoidal/RoPE/AliBi for variable length, learned for fixed length
- **Fine-tuning longer**: Position interpolation (PI) extends RoPE to 2-4x training length
- **NTK-aware scaling**: Better RoPE interpolation using Neural Tangent Kernel theory
- **Combined approaches**: Some models use absolute + relative encodings

## References
- Vaswani, Shazeer, Parmar, et al., "Attention Is All You Need (sinusoidal PE)", NeurIPS 2017
- Shaw, Uszkoreit, Vaswani, "Self-Attention with Relative Position Representations", NAACL 2018
- Su, Lu, et al., "RoFormer: Enhanced Transformer with Rotary Position Embedding (RoPE)", 2021
- Press, Smith, Lewis, "Train Short, Test Long: Attention with Linear Biases (AliBi) Enables Input Length Extrapolation", ICLR 2022
- Chen, Wong, et al., "Extending Context Window of Large Language Models via Positional Interpolation", 2023
