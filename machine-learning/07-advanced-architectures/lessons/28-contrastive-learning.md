# Lesson 07.28: Contrastive Learning

## Learning Objectives
- Understand contrastive loss (InfoNCE) and its variants
- Implement SimCLR, MoCo, and BYOL
- Apply contrastive learning to vision, language, and multimodal tasks
- Analyze the role of negatives, batch size, and temperature

## Theory
Contrastive learning learns representations by pulling positive pairs together and pushing negative pairs apart.

### InfoNCE Loss
$$\mathcal{L}_{i,j} = -\log \frac{\exp(\text{sim}(z_i, z_j) / \tau)}{\sum_{k=1}^{2N} \mathbb{1}_{[k \neq i]} \exp(\text{sim}(z_i, z_k) / \tau)}$$

- $z_i, z_j$: normalized embeddings of positive pair (two augmentations of same image)
- $\tau$: temperature (controls softmax sharpness)
- $2N$: batch size after data augmentation (negative pairs = other $2N-2$ samples)
- sim: Cosine similarity (or dot product of L2-normalized vectors)

## SimCLR

### Architecture
```
Image x → Augmentation(t) → x̃ → Encoder f(·) → h → Projection g(·) → z → InfoNCE loss
```

### Key Components
1. **Data augmentation**: Random crop, color jitter, Gaussian blur, horizontal flip
2. **Encoder**: ResNet-50 (or similar)
3. **Projection head**: 2-layer MLP (ReLU), mapping $h$ to $z$
4. **InfoNCE loss**: With batch negatives

### Findings
- Large batch size (4096+) provides enough negatives
- Stronger augmentation improves representations
- Projection head prevents information loss in representation $h$

## MoCo (Momentum Contrast)

### Architecture
```
Query encoder (θ_q) → z_q → contrastive loss
Momentum encoder (θ_k) → z_k → queue dictionary
```

### Momentum Update
$$\theta_k \leftarrow m \cdot \theta_k + (1 - m) \cdot \theta_q$$

- $m$: momentum coefficient (typically 0.999)
- **Queue**: Store negative keys from previous batches (decouples batch size from negatives)

### Key Difference from SimCLR
MoCo uses a queue of negatives (size up to 65536) — no need for large batch.

## SimSiam

### Siamese Network without Negatives
```
x → aug1 → encoder → predictor → z1
x → aug2 → encoder (stop-grad) → z2
Loss: -cosine_sim(stop_grad(z1), predictor(z2)) - cosine_sim(stop_grad(z2), predictor(z1))
```

### Why It Works Without Negatives
- **Stop-gradient**: Prevents collapse to trivial solution
- **Predictor**: Asymmetric architecture prevents collapse
- **Empirical**: Works with batch size as low as 256

## BYOL (Bootstrap Your Own Latent)

### Architecture
```
Online: x → aug → encoder → projector → predictor → q(z_online)
Target: x → aug' → encoder (momentum) → projector → z_target (stop-grad)
Loss: ||q(z_online) - z_target||²
```

### Key Features
- No negative pairs needed
- Target network updated via EMA (exponential moving average)
- Predictor prevents collapse
- Works with small batch sizes

## CLIP (Contrastive Language-Image Pre-training)

### Multi-Modal Contrastive Learning
$$\text{maximize } \frac{1}{N} \sum_{i=1}^N \frac{\exp(\text{sim}(I_i, T_i) / \tau)}{\sum_{j=1}^N \exp(\text{sim}(I_i, T_j) / \tau)}$$

- $I_i$: image embedding (ViT or ResNet)
- $T_i$: text embedding (Transformer)
- **Batch**: 32,768 image-text pairs

## Code: SimCLR Loss

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SimCLRLoss(nn.Module):
    def __init__(self, temperature=0.5):
        super().__init__()
        self.temperature = temperature

    def forward(self, z):
        """z: (2N, D) — first N are view 1, next N are view 2"""
        N = z.shape[0] // 2
        z = F.normalize(z, dim=-1)
        
        # Similarity matrix
        sim = z @ z.T / self.temperature  # (2N, 2N)
        
        # Labels: positive pairs are (i, i+N) and (i+N, i)
        labels = torch.cat([torch.arange(N, 2*N), torch.arange(N)]).to(z.device)
        
        # Mask out self-similarity
        mask = torch.eye(2*N, dtype=torch.bool, device=z.device)
        sim = sim.masked_fill(mask, -1e9)
        
        return F.cross_entropy(sim, labels)
```

## Method Comparison

| Method | Negatives | Batch Size | Memory Bank | Target Network | Key Innovation |
|--------|-----------|------------|-------------|----------------|----------------|
| SimCLR | Batch | 4096+ | No | No | Simple, effective |
| MoCo | Queue | 256+ | Queue | Momentum | Decouples batch/negatives |
| BYOL | None | 256+ | No | Momentum | No negatives needed |
| SimSiam | None | 256+ | No | Stop-grad only | Simplest architecture |
| CLIP | Batch | 32K+ | No | No | Multi-modal |
| SupCon | Batch (labels) | Flexible | No | No | Uses labels for positives |

## Practical Considerations
- **Temperature**: $\tau \approx 0.1-0.5$ (lower = harder negative separation, more peaky)
- **Augmentation**: Strong augmentations are critical for SSL; weak augmentations hurt
- **Projection head**: Always use a projection head; remove for downstream tasks
- **Global vs local**: Contrastive loss is global (global features); best for classification
- **Fine-tuning**: Linear evaluation (freeze backbone) vs full fine-tuning

## Limitations
- **False negatives**: Semantically similar images may be treated as negatives (esp. ImageNet)
- **Batch composition**: Random batch composition can create biased negatives
- **Uniformity-tolerance trade-off**: Too much uniformity kills features useful for fine-grained tasks
- **Object-centric bias**: Contrastive SSL works poorly on scene-centric datasets

## References
- Chen, Kornblith, Norouzi, Hinton, "SimCLR: A Simple Framework for Contrastive Learning of Visual Representations", ICML 2020
- He, Fan, Wu, Xie, Girshick, "Momentum Contrast for Unsupervised Visual Representation Learning (MoCo)", CVPR 2020
- Chen & He, "Exploring Simple Siamese Representation Learning (SimSiam)", CVPR 2021
- Grill, Strub, Altché, et al., "Bootstrap Your Own Latent — A New Approach to Self-Supervised Learning (BYOL)", NeurIPS 2020
- Radford, Kim, Hallacy, et al., "Learning Transferable Visual Models From Natural Language Supervision (CLIP)", ICML 2021
