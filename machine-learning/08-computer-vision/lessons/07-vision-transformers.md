# Lesson 08.07: Vision Transformers (ViT, Swin, DeiT)

## Learning Objectives
- Understand ViT architecture for image classification
- Implement patch embedding and Transformer encoder
- Apply Swin Transformer's shifted window attention
- Analyze data requirements and distillation for ViTs

## ViT (Vision Transformer)

### Architecture
$$z_0 = [x_{\text{class}}; x_p^1 E; x_p^2 E; \dots; x_p^N E] + E_{\text{pos}}$$
$$z_\ell' = \text{MSA}(\text{LN}(z_{\ell-1})) + z_{\ell-1}$$
$$z_\ell = \text{MLP}(\text{LN}(z_\ell')) + z_\ell'$$
$$y = \text{LN}(z_L^0)$$

### Key Components
1. **Patch Embedding**: $E \in \mathbb{R}^{(P^2 C) \times D}$ — linear projection of $P \times P$ patches
2. **Positional Encoding**: Learnable 1D embeddings (no 2D structure assumed)
3. **Class Token**: $x_{\text{class}}$ — learnable token appended to sequence, output = image representation
4. **Transformer Encoder**: Alternating MSA + MLP with residual connections

### Inductive Bias
ViT has less image-specific inductive bias than CNNs:
- No translation equivariance (learned from data)
- No locality (self-attention is global)
- Requires more data to compensate

## Swin Transformer

### Hierarchical Feature Maps
```
H/4 × W/4 → H/8 × W/8 → H/16 × W/16 → H/32 × W/32
```

Patch merging at each stage (like CNN downsampling).

### Shifted Window Attention
- **Local windows**: Attention within $M \times M$ windows ($M=7$)
- **Shifted windows**: Shift by $\lfloor M/2 \rfloor$ pixels in successive layers
- **Cyclic shift**: Efficient batch computation with masked attention

### Relative Position Bias
$$A = QK^\top / \sqrt{d} + B$$

- $B$: learnable relative position bias (size $(2M-1) \times (2M-1)$)
- Better than absolute position encoding for local windows

## DeiT (Data-efficient Image Transformers)

### Knowledge Distillation
Teacher (ConvNet) → Student (ViT):

$$\mathcal{L} = \lambda \mathcal{L}_{\text{CE}}(\text{softmax}(Z_s), y) + (1-\lambda) \mathcal{L}_{\text{KL}}(\text{softmax}(Z_s/\tau), \text{softmax}(Z_t/\tau))$$

- **Hard distillation**: Use teacher's hard prediction as label
- **Distillation token**: Learnable token (similar to class token)
- **Result**: ViT trained on ImageNet-1k only (no JFT-300M)

## Code: ViT Patch Embedding

```python
import torch
import torch.nn as nn

class PatchEmbed(nn.Module):
    def __init__(self, img_size=224, patch_size=16, in_channels=3, embed_dim=768):
        super().__init__()
        self.num_patches = (img_size // patch_size) ** 2
        self.proj = nn.Conv2d(in_channels, embed_dim, 
                              kernel_size=patch_size, stride=patch_size)

    def forward(self, x):
        x = self.proj(x)  # (B, D, H/P, W/P)
        x = x.flatten(2).transpose(1, 2)  # (B, N, D)
        return x

class ViTEncoder(nn.Module):
    def __init__(self, embed_dim=768, num_heads=12, mlp_ratio=4, depth=12):
        super().__init__()
        self.layers = nn.ModuleList([
            nn.TransformerEncoderLayer(
                d_model=embed_dim, nhead=num_heads,
                dim_feedforward=int(embed_dim * mlp_ratio),
                activation='gelu', batch_first=True
            ) for _ in range(depth)
        ])

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x
```

## ViT Variants

| Model | Parameters | ImageNet Top-1 | Pretraining Data |
|-------|-----------|----------------|-----------------|
| ViT-B/16 | 86M | 78.5% (IN-1k) | JFT-300M |
| ViT-L/16 | 307M | 76.5% (IN-1k) | JFT-300M |
| ViT-H/14 | 632M | 88.6% (JFT) | JFT-3B |
| DeiT-B | 86M | 81.8% (IN-1k) | IN-1k only |
| Swin-B | 88M | 83.5% (IN-1k) | IN-22k |
| SwinV2-G | 3B | 90.2% | IN-22k + 70M private |

## Practical Considerations
- **Patch size**: 16×16 standard (14×14 for ViT-H); smaller patches → more tokens → slower
- **Position encoding**: Interpolate for higher resolution (ViT) or use relative bias (Swin)
- **Learning rate**: ViT needs lower LR (0.001) and longer warmup than CNNs
- **Augmentation**: Heavy augmentation (RandAugment, Mixup, CutMix) critical for ViT
- **Optimizer**: AdamW with weight decay 0.05-0.1
- **Gradient accumulation**: ViT benefits from large effective batch size (2048+)

## Limitations
- **Quadratic complexity**: Self-attention is $O(n^2)$ in patches — 14×14 grid = 196 tokens is OK, dense prediction is expensive
- **Data hungry**: Without pretraining on large data, ViT underperforms ResNet
- **Fine-tuning sensitivity**: ViT is sensitive to LR and augmentation during fine-tuning
- **Position encoding**: Cannot easily handle arbitrary resolutions

## References
- Dosovitskiy, Beyer, Kolesnikov, et al., "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale", ICLR 2021
- Liu, Lin, Cao, et al., "Swin Transformer: Hierarchical Vision Transformer using Shifted Windows", ICCV 2021
- Touvron, Cord, Douze, Massa, Sablayrolles, Jégou, "Training data-efficient image transformers & distillation through attention (DeiT)", ICML 2021
- Caron, Touvron, et al., "Emerging Properties in Self-Supervised Vision Transformers (DINO)", ICCV 2021
- Liu, Hu, Lin, et al., "Swin Transformer V2: Scaling Up Capacity and Resolution", CVPR 2022
