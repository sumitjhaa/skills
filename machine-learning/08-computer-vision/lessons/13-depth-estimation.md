# Lesson 08.13: Depth Estimation

## Learning Objectives
- Understand stereo disparity for depth computation
- Implement monocular depth estimation with MiDaS
- Apply Depth Anything for zero-shot depth estimation
- Analyze scale-invariant losses and evaluation metrics

## Stereo Disparity

### Geometry
$$d = x_l - x_r, \quad Z = \frac{f \cdot B}{d}$$

- $f$: focal length
- $B$: baseline (distance between cameras)
- $d$: disparity (pixel shift between left/right images)

### Correspondence Matching
1. **Block matching**: SSD/SAD over sliding window
2. **Cost volume**: Concatenate features at all disparity levels
3. **Siamese network**: ConvNet features for matching

### Semi-Global Matching (SGM)
Optimize disparity via:
- Matching cost
- Smoothness term (penalize disparity changes)
- 8-direction DP

## Monocular Depth Estimation

### Challenge
Single image → depth is **ill-posed**: infinite 3D scenes produce the same 2D image.

### Learned Approach
Dataset of (RGB, depth) pairs → train CNN/Transformer:

$$\text{depth} = \text{model}(\text{RGB})$$

### MiDaS (Mixed Depth and Surface normals)

**Training**: Mix multiple datasets with different depth ranges:
- **Loss**: Scale-and-shift invariant loss:

$$L = \frac{1}{n} \sum_i (\log d_i - \log d_i^* + \alpha)^2, \quad \alpha = \frac{1}{n} \sum_i (\log d_i^* - \log d_i)$$

- **Architecture**: Encoder-decoder with classification depth head
- **Discretize depth**: $D$ bins (e.g., 256), predict distribution per pixel

### Depth Anything

**Knowledge distillation**:
1. Teacher: MiDaS trained on 1.5M labeled images
2. Student: DINOv2 backbone → depth head
3. Train on 62M unlabeled images with pseudo-labels from teacher

**Key findings**:
- Large-scale unlabeled data significantly improves generalization
- DINOv2 pretraining provides strong features
- Zero-shot transfer to unseen datasets

## Loss Functions

| Loss | Formula | Properties |
|------|---------|------------|
| L1 | $\|d - d^*\|$ | Simple, sensitive to scale |
| Scale-invariant log | $\frac{1}{n}\sum d^2 - \frac{\lambda}{n^2}(\sum d)^2$, $d = \log y - \log y^*$ | Invariant to global scale |
| BerHu | $\begin{cases} |x| & \|x\| \le c \\ \frac{x^2 + c^2}{2c} & \|x\| > c \end{cases}$ | L1 for outliers, L2 for small errors |
| Silog | $ \frac{1}{n} \sum d^2 - \frac{1}{n^2}(\sum d)^2$, $d = \log y - \log y^*$ | Scale invariant |

## Code: Scale-Invariant Depth Loss

```python
import torch
import torch.nn as nn

class ScaleInvariantLogLoss(nn.Module):
    def __init__(self, lamb=0.5):
        super().__init__()
        self.lamb = lamb

    def forward(self, pred, target):
        # pred, target: depth maps (B, 1, H, W)
        d = torch.log(pred + 1e-8) - torch.log(target + 1e-8)
        n = d.numel() // d.shape[0]
        
        term1 = (d ** 2).sum(dim=(1, 2, 3)) / n
        term2 = (d.sum(dim=(1, 2, 3)) ** 2) / (n ** 2)
        
        loss = term1 - self.lamb * term2
        return loss.mean()
```

## Evaluation Metrics

| Metric | Formula | Focus |
|--------|---------|-------|
| Abs Rel | $\frac{1}{n} \sum \|d - d^*\| / d^*$ | Relative error |
| Sq Rel | $\frac{1}{n} \sum \|d - d^*\|^2 / d^*$ | Squared relative error |
| RMSE | $\sqrt{\frac{1}{n} \sum (d - d^*)^2}$ | Absolute error |
| $\delta_{1.25}$ | $\%\ \text{of}\ \max(d/d^*, d^*/d) < 1.25$ | Accuracy threshold |
| $\delta_{1.25^2}$ | Threshold 1.25$^2$ | Coarser accuracy |

## Depth Estimation Comparison

| Method | Type | Abs Rel (KITTI) | RMSE | FPS |
|--------|------|----------------|-------|-----|
| MiDaS v3.1 | Monocular | 0.078 | 3.93 | 10 |
| Depth Anything | Monocular | 0.057 | 2.74 | 15 |
| RAFT-Stereo | Stereo | 0.033 | 1.43 | 5 |
| DPT | Monocular | 0.082 | 4.11 | 8 |

## Practical Considerations
- **Depth range**: Models predict disparity or inverse depth (range $[0, 1]$); rescale to actual meters using median matching
- **Focal length**: For stereo, accurate calibration is critical; for monocular, assume reasonable FOV
- **Depth normalization**: Normalize depth to [0, 1] using max depth in training set
- **Edge-aware smoothness**: Regularization: $|\partial_x d| e^{-|\partial_x I|} + |\partial_y d| e^{-|\partial_y I|}$
- **Uncertainty**: Predict depth + log variance (aleatoric uncertainty)

## References
- Ranftl, Lasinger, Hafner, Schindler, Koltun, "Towards Robust Monocular Depth Estimation: Mixing Datasets for Zero-shot Cross-dataset Transfer", TPAMI 2022 (MiDaS)
- Yang, Kang, Huang, Xu, Feng, Lin, "Depth Anything: Unleashing the Power of Large-Scale Unlabeled Data", 2024
- Li, Snavely, Huttenlocher, "Depth and Surface Normal Estimation from Monocular Images", CVPR 2015
- Eigen, Puhrsch, Fergus, "Depth Map Prediction from a Single Image using a Multi-Scale Deep Network", NeurIPS 2014
- Godard, Mac Aodha, Brostow, "Unsupervised Monocular Depth Estimation with Left-Right Consistency", CVPR 2017
