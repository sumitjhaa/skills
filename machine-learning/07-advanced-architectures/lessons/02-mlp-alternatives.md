# Lesson 07.02: MLP Alternatives (MLP-Mixer, gMLP, FNet)

## Learning Objectives
- Understand MLP-Mixer's token/channel mixing architecture
- Implement gMLP with spatial gating units
- Compare attention-free architectures with transformers
- Analyze trade-offs between MLP alternatives and attention

## Motivation
Transformers dominate NLP and vision, but their self-attention is $O(n^2)$. MLP alternatives aim to match performance with simpler, faster operations.

## MLP-Mixer

### Architecture
**Mixer layer** = token mixing + channel mixing, both via MLPs:

$$U_{*,i} = X_{*,i} + W_2 \sigma(W_1 \text{LayerNorm}(X)_{*,i}) \quad \text{(channel-mixing)}$$
$$Y_{j,*} = U_{j,*} + W_4 \sigma(W_3 \text{LayerNorm}(U)_{j,*}) \quad \text{(token-mixing)}$$

- Channel-mixing: per-location MLP (mixes channels within same spatial location)
- Token-mixing: per-channel MLP (mixes spatial locations for same channel)
- Both are **applied transposed**: token-mixing MLP operates on $X^\top$

### Scaling
- Per-patch embeddings (similar to ViT)
- No positional encoding needed (token mixing is position-aware)
- Mixer-B/16: ~600M FLOPs (comparable to ViT-B/16)

## gMLP (Pay Attention to MLPs)

### Spatial Gating Unit (SGU)
$$z = \sigma(X u) \odot (W X + b)$$
- $u$: projection to scalar gate
- $W$: spatial mixing matrix (linear across tokens)
- $\odot$: elementwise gating

### gMLP Block
$$X = X + \text{SGU}(\text{LayerNorm}(X))$$
$$X = X + \text{MLP}(\text{LayerNorm}(X))$$

**Key insight**: Gating with linear spatial mixing is sufficient — no attention needed.

### Comparison with Transformer

| Aspect | Transformer | gMLP | MLP-Mixer |
|--------|-------------|------|-----------|
| Mixing | Self-attention | Linear gating | Per-channel MLP |
| Complexity | $O(n^2 d)$ | $O(n^2)$ (but simpler) | $O(n^2)$ |
| Parameters | $4d^2$ per layer | $3d^2$ per layer | $2d^2 + 2n^2$ |
| Position encoding | Required | Not needed | Not needed |

## FNet (Fourier Transform Networks)

Replace attention with 2D FFT:

$$Y = \mathcal{F}^{-1}_{\text{col}}(\mathcal{F}^{-1}_{\text{row}}(\mathcal{F}_{\text{col}}(\mathcal{F}_{\text{row}}(X))))$$

- Token mixing via Fourier transform (global, linear)
- Then pass through feed-forward MLP
- **Speed**: 80% faster than BERT, but 92-97% of accuracy

### Why Fourier Works
- Fourier transforms are global (each output depends on all inputs)
- Low frequencies capture coarse structure, high frequencies fine details
- No learnable parameters for mixing — pure operations

## Code: MLP-Mixer Block

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class MixerBlock(nn.Module):
    def __init__(self, dim, num_patches, expansion=4):
        super().__init__()
        self.norm1 = nn.LayerNorm(dim)
        self.token_mix = nn.Sequential(
            nn.Linear(num_patches, num_patches * expansion),
            nn.GELU(),
            nn.Linear(num_patches * expansion, num_patches),
        )
        self.norm2 = nn.LayerNorm(dim)
        self.channel_mix = nn.Sequential(
            nn.Linear(dim, dim * expansion),
            nn.GELU(),
            nn.Linear(dim * expansion, dim),
        )

    def forward(self, x):
        # x: (B, N, D)
        y = self.norm1(x)
        y = y.transpose(1, 2)  # (B, D, N)
        y = self.token_mix(y)
        y = y.transpose(1, 2)  # (B, N, D)
        x = x + y
        x = x + self.channel_mix(self.norm2(x))
        return x
```

## Empirical Findings
- **Vision**: MLP-Mixer matches ViT at large scale (JFT-300M pretraining)
- **NLP**: gMLP matches BERT on GLUE but underperforms on translation/SQuAD
- **Scaling law**: MLP alternatives improve more slowly with compute than transformers
- **Hybrid**: 1-2 attention layers + Mixer layers best of both worlds

## Limitations
- **Efficiency gap**: MLP-Mixer's transposed MLP is $O(n^2 d)$ — same as attention asymptotically
- **Quality ceiling**: On language tasks, attention-free models plateau earlier
- **Data hungry**: More pretraining data needed to match transformers
- **No inductive bias for sequences**: Unlike attention's key-query matching

## References
- Tolstikhin et al., "MLP-Mixer: An all-MLP Architecture for Vision", NeurIPS 2021
- Liu et al., "Pay Attention to MLPs (gMLP)", NeurIPS 2021
- Lee-Thorp et al., "FNet: Mixing Tokens with Fourier Transforms", ACL 2022
- Dosovitskiy et al., "An Image is Worth 16x16 Words: Transformers for Image Recognition", ICLR 2021
- Tay et al., "Efficient Transformers: A Survey", ACM Computing Surveys 2022
