# Lesson 08.08: Self-Supervised Vision (SimCLR, DINO, MAE)

## Learning Objectives
- Understand contrastive and non-contrastive self-supervised learning
- Implement SimCLR, BYOL, and DINO
- Apply Masked Autoencoders (MAE) for visual representation learning
- Evaluate SSL representations via linear probing and fine-tuning

## Contrastive Learning

### SimCLR
Maximize agreement between augmented views of same image:

$$\ell_{i,j} = -\log \frac{\exp(\text{sim}(z_i, z_j)/\tau)}{\sum_{k=1}^{2N} \mathbb{1}_{[k \neq i]} \exp(\text{sim}(z_i, z_k)/\tau)}$$

**Key components**: Strong augmentation, large batch (4096+), projection head.

### MoCo (Momentum Contrast)
- **Queue**: Maintain large dictionary of negative samples
- **Momentum encoder**: Slow-moving target encoder for consistency
- Decouples negative count from batch size

## Non-Contrastive Learning

### BYOL (Bootstrap Your Own Latent)
No negative pairs needed:
```
Online: x → aug → encoder → projector → predictor → q(z_online)
Target: x → aug' → encoder (momentum) → projector → z_target
Loss: ||q(z_online) - stop_grad(z_target)||²
```

### DINO (Self-Distillation with No Labels)
Self-supervised learning with ViT:

**Architecture**:
```
Student (ViT-S/16) + momentum Teacher (ViT-S/16)
Centering + sharpening to prevent collapse
```

**Key finding**: DINO's ViT [CLS] token naturally learns semantic segmentation — individual attention heads correspond to object parts.

### DINO Loss
$$P_s(x)^\top \log P_t(x')$$

- Cross-entropy between student output and teacher output
- Teacher updated via EMA: $\theta_t \leftarrow \lambda \theta_t + (1-\lambda) \theta_s$
- Centering: $\theta_t.\text{center} = \text{EMA}(\mathbb{E}[P_t(x)])$

## Masked Image Modeling (MAE)

### Architecture
```
Image → Mask random patches (75%) → Encoder (visible patches only) → Decoder (full set) → Reconstruct pixels
```

### Key Design Choices
- **High masking ratio** (75%): Remove redundancy, force learning of holistic representations
- **Asymmetric encoder-decoder**: Encoder processes only visible patches (lightweight); decoder is lightweight
- **Latent reconstruction**: Decoder works in latent space (normalized pixel targets)

### Loss
$$\mathcal{L} = \frac{1}{\Omega_m} \sum_{i \in \text{masked}} \|x_i - \hat{x}_i\|_2^2$$

- Only compute loss on masked patches
- Target: normalized pixel values (mean 0, variance 1 per patch)

## Code: DINO-Style Self-Distillation

```python
import torch
import torch.nn as nn

class DINOLoss(nn.Module):
    def __init__(self, out_dim, teacher_temp=0.04, student_temp=0.1):
        super().__init__()
        self.student_temp = student_temp
        self.teacher_temp = teacher_temp
        self.center = nn.Parameter(torch.zeros(1, out_dim), requires_grad=False)

    def forward(self, student_output, teacher_output):
        # Softmax with temperature
        s = torch.softmax(student_output / self.student_temp, dim=-1)
        t = torch.softmax((teacher_output - self.center) / self.teacher_temp, dim=-1)
        
        # Cross-entropy (student vs teacher)
        loss = -(t * torch.log(s + 1e-8)).sum(dim=-1).mean()
        
        # Update center (EMA)
        with torch.no_grad():
            self.center = 0.9 * self.center + 0.1 * teacher_output.mean(dim=0, keepdim=True)
        
        return loss
```

## Evaluation Protocol

| Method | Linear Probe | Fine-tune | k-NN | When to Use |
|--------|-------------|-----------|------|-------------|
| SimCLR | 69.3% (R-50) | 76.4% | 59.5% | Strong representations |
| MoCo v3 | 72.5% (R-50) | 77.5% | 63.2% | Low-batch regime |
| BYOL | 71.8% (R-50) | 77.4% | 62.3% | No negatives needed |
| DINO | 75.3% (ViT-S) | 78.2% | 67.5% | Semantic segmentation |
| MAE | 68.0% (ViT-B) | 83.6% | 47.2% | Scalable, sparse computation |

## Practical Considerations
- **Augmentation**: Critical for SSL — always use multiple crop strategies
- **Batch size**: Contrastive methods need large batch (4096+); BYOL/DINO work with 256
- **Projector head**: Always use MLP projector (remove for linear eval)
- **EMA momentum**: 0.996 (slow) to 0.999 (depends on batch size)
- **Training epochs**: SSL benefits from more epochs (400-1600 vs 90 for supervised)

## Limitations
- **Object-centric bias**: SSL works well on ImageNet (single object), poorly on scene-centric
- **Computational cost**: SSL training is 2-4× more expensive than supervised
- **Hyperparameter sensitivity**: Temperature, augmentation strength require tuning
- **Evaluation gap**: Linear probe may not reflect fine-tuning performance

## References
- Chen, Kornblith, Norouzi, Hinton, "A Simple Framework for Contrastive Learning of Visual Representations (SimCLR)", ICML 2020
- He, Fan, Wu, Xie, Girshick, "Momentum Contrast for Unsupervised Visual Representation Learning (MoCo)", CVPR 2020
- Grill, Strub, Altché, et al., "Bootstrap Your Own Latent (BYOL)", NeurIPS 2020
- Caron, Touvron, et al., "Emerging Properties in Self-Supervised Vision Transformers (DINO)", ICCV 2021
- He, Chen, Xie, et al., "Masked Autoencoders Are Scalable Vision Learners (MAE)", CVPR 2022
