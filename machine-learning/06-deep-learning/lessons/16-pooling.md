# 06.16 Pooling

## Learning Objectives
- Understand pooling operations for downsampling
- Implement max pooling, average pooling, and variants
- Apply ROI pooling and ROI align for object detection

## Pooling Operations

### Purpose
- Downsample spatial dimensions (reduce computation)
- Provide translation invariance
- Increase receptive field

## Max Pooling

### Operation
$$y[i, j] = \max_{p,q \in \text{window}} x[i \cdot S + p, j \cdot S + q]$$

- Takes maximum value in each window
- Preserves sharp features (edges, textures)
- Most common pooling for intermediate layers

### Properties
| Aspect | Value |
|--------|-------|
| Parameters | 0 |
| Output size | $(H - K)/S + 1$ |
| Gradient | Only flows through max element |
| Invariance | Small translation invariance |

## Average Pooling

### Operation
$$y[i, j] = \frac{1}{K^2} \sum_{p,q \in \text{window}} x[i \cdot S + p, j \cdot S + q]$$

- Smooths activations
- Less common than max pooling for intermediate layers
- Used in global average pooling for classifiers

## Global Pooling

### Global Average Pooling (GAP)
$$y[k] = \frac{1}{H \cdot W} \sum_{i,j} x[i, j, k]$$

Pool entire spatial map to one value per channel. Used to replace fully connected layers before classification:
- Reduces parameters significantly
- More interpretable (each channel corresponds to a class)
- No overfitting from FC layers

## Adaptive Pooling

Output size is specified; stride and kernel computed automatically:

```python
import torch.nn as nn

adaptive_pool = nn.AdaptiveAvgPool2d((7, 7))
output = adaptive_pool(input)  # Always produces (7, 7) spatial size
```

Useful for variable-size inputs in a fixed-size network.

## ROI Pooling

### Operation
Extract fixed-size feature maps from variable-sized regions of interest:

1. Project ROI coordinates to feature map
2. Divide ROI into $H \times W$ grid cells
3. Max pool each cell (with quantization)

### Quantization Issue
ROI coordinates are quantized (floor/ceil) causing misalignment between ROI and feature map. Small but measurable accuracy loss.

## ROI Align

### Improvement
Uses bilinear interpolation instead of quantization:

```python
def roi_align(feature_map, rois, output_size=(7, 7)):
    """
    feature_map: (B, C, H, W)
    rois: (N, 5) — batch_idx, x1, y1, x2, y2
    """
    results = []
    for roi in rois:
        batch_idx, x1, y1, x2, y2 = roi
        # Sample evenly spaced points in each bin
        for i in range(output_size[0]):
            for j in range(output_size[1]):
                # Bilinear interpolation at each sample point
                value = bilinear_interpolate(feature_map[batch_idx], 
                                            y1 + i * bin_size, 
                                            x1 + j * bin_size)
                results[batch_idx, :, i, j] = max(results[batch_idx, :, i, j], value)
    return results
```

Used in Mask R-CNN. Provides ~1-2% mAP improvement over ROI Pooling.

## Code: Max Pooling from Scratch

```python
import torch
import torch.nn.functional as F

def max_pool2d(x, kernel_size=2, stride=2):
    B, C, H, W = x.shape
    kH, kW = (kernel_size, kernel_size) if isinstance(kernel_size, int) else kernel_size
    sH, sW = (stride, stride) if isinstance(stride, int) else stride
    
    # Use unfold to extract patches
    patches = F.unfold(x, kernel_size=(kH, kW), stride=(sH, sW))
    # patches: (B, C*kH*kW, L)
    
    # Reshape and max pool
    B, Ck, L = patches.shape
    patches = patches.view(B, C, kH*kW, L)
    output, indices = patches.max(dim=2)
    
    H_out = (H - kH) // sH + 1
    W_out = (W - kW) // sW + 1
    return output.view(B, C, H_out, W_out), indices
```

## Pooling vs Strided Convolution

| Aspect | Pooling | Strided Conv |
|--------|---------|-------------|
| Parameters | 0 | Learnable |
| Computation | O(1) per pixel | O(K²) per pixel |
| Invariance | Built-in translation invariance | Learned |
| Modern usage | Less common (outside detection) | Preferred |

## References
- LeCun, Bottou, Bengio, Haffner, "Gradient-Based Learning Applied to Document Recognition (LeNet)", 1998
- Girshick, "Fast R-CNN (ROI Pooling)", ICCV 2015
- He, Gkioxari, Dollar, Girshick, "Mask R-CNN (ROI Align)", ICCV 2017
- Lin, Chen, Yan, "Network In Network (Global Average Pooling)", 2013
- Springenberg, Dosovitskiy, et al., "Striving for Simplicity: The All Convolutional Net", ICLR 2015
