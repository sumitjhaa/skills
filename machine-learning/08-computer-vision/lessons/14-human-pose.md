# Lesson 08.14: Human Pose Estimation

## Learning Objectives
- Understand heatmap-based 2D keypoint detection
- Implement HRNet with parallel multi-resolution streams
- Apply ViTPose for Transformer-based pose estimation
- Analyze architectures for accuracy vs speed trade-offs

## 2D Keypoint Detection

### Heatmap Representation
Ground truth: Gaussian heatmap centered at each keypoint:

$$H_k(x, y) = \exp\left(-\frac{(x - x_k)^2 + (y - y_k)^2}{2\sigma^2}\right)$$

- $\sigma$: typically 2-4 pixels
- **Loss**: MSE between predicted and ground truth heatmaps

### Sub-Pixel Precision (Soft-Argmax)
$$\hat{p} = \frac{\sum_u e^{\beta H(u)} u}{\sum_u e^{\beta H(u)}}$$

- $\beta$: temperature (higher = sharper)
- Differentiable alternative to argmax

### DARK (Distribution-Aware Keypoint)
Refine heatmap by fitting Gaussian distribution:

1. Find maximum heatmap location
2. Fit 2D Gaussian using second-order Taylor expansion
3. Sub-pixel offset = $-\left(\nabla^2 H\right)^{-1} \nabla H$

## Architectures

### SimpleBaseline
```
ResNet backbone → 3 deconvolutional layers (256 channels, 4x stride) → 1x1 conv (k channels)
```

- Deconv layers upsample from stride 32 to stride 4
- Simple but effective baseline

### Stacked Hourglass
Repeated encoder-decoder with intermediate supervision:

```
Stacked hourglass modules → intermediate heatmap prediction → next module refinement
```

- Each hourglass: down to 4x4 → up to 64x64
- Intermediate supervision at each stack

### HRNet (High-Resolution Net)

**Key idea**: Maintain high-resolution features throughout, not just in decoder:

```
Stage 1: 4x (64 channels)
Stage 2: 4x + 8x (64 + 128)
Stage 3: 4x + 8x + 16x (64 + 128 + 256)
Stage 4: 4x + 8x + 16x + 32x (64 + 128 + 256 + 512)
```

### Multi-Resolution Fusion
Exchange information across resolutions via up/down sampling:

$$f_{\text{new}}^{(i)} = \sum_{j} \text{resample}(f^{(j)}, \text{scale}_j \to \text{scale}_i)$$

### ViTPose
ViT-based pose estimation:

- **ViT encoder**: Process image as sequence of patches
- **Decoder**: Transposed convolutions to upsample to heatmap resolution
- **Simple**: No FPN, no multi-resolution fusion needed
- **Scalable**: Larger ViT (H/14) → better accuracy

## Code: SimpleBaseline Decoder

```python
import torch
import torch.nn as nn

class PoseResNet(nn.Module):
    def __init__(self, backbone, num_joints=17):
        super().__init__()
        self.backbone = backbone  # ResNet
        self.deconv = nn.Sequential(
            nn.ConvTranspose2d(2048, 256, 4, stride=2, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.ConvTranspose2d(256, 256, 4, stride=2, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.ConvTranspose2d(256, 256, 4, stride=2, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
        )
        self.final = nn.Conv2d(256, num_joints, 1)

    def forward(self, x):
        x = self.backbone(x)
        x = self.deconv(x)
        return self.final(x)  # (B, 17, H', W')
```

## Pose Estimation Results (COCO)

| Method | Backbone | AP | AP_50 | FPS |
|--------|----------|-----|-------|-----|
| SimpleBaseline | ResNet-152 | 73.7 | 91.2 | 15 |
| HRNet-W48 | HRNet | 75.5 | 92.5 | 10 |
| Stacked Hourglass | 8x Hourglass | 66.9 | 89.3 | 5 |
| ViTPose-B | ViT-B | 76.6 | 92.6 | 20 |
| ViTPose-H | ViT-H | 81.1 | 93.1 | 5 |

## Evaluation Metrics

### OKS (Object Keypoint Similarity)
$$\text{OKS} = \frac{\sum_i \exp(-d_i^2 / 2s^2 k_i^2) \cdot \delta(v_i > 0)}{\sum_i \delta(v_i > 0)}$$

- $d_i$: Euclidean distance between predicted and GT keypoint
- $s$: object scale (sqrt(area))
- $k_i$: per-keypoint falloff constant

### AP (Average Precision)
- Based on OKS thresholds (0.50, 0.55, ..., 0.95)
- **AP**: Mean over OKS thresholds
- **AP_50**: OKS threshold at 0.50

## Practical Considerations
- **Input resolution**: 256×192 or 384×288; higher = better AP but slower
- **Flip test**: Horizontal flip + average heatmaps (+1-2 AP)
- **Multi-scale testing**: Test at [0.5, 0.75, 1.0, 1.25] scales
- **Heatmap aggregation**: Max instead of average at occluded joints
- **NMS**: For multi-person, use bottom-up (associate keypoints) or top-down (detect person first)

## References
- Newell, Yang, Deng, "Stacked Hourglass Networks for Human Pose Estimation", ECCV 2016
- Sun, Xiao, Liu, Wang, "Deep High-Resolution Representation Learning for Human Pose Estimation (HRNet)", CVPR 2019
- Xiao, Wu, Wei, "Simple Baselines for Human Pose Estimation and Tracking", ECCV 2018
- Xu, Zhang, Zhang, et al., "ViTPose: Simple Vision Transformer Baselines for Human Pose Estimation", NeurIPS 2022
- Zhang, Zheng, Liu, et al., "Distribution-Aware Coordinate Representation for Human Pose Estimation (DARK)", CVPR 2020
