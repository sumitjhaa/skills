# 06.15 Convolutions

## Learning Objectives
- Understand convolution operation for spatial data
- Implement various convolution types (depthwise, dilated, transposed)
- Apply group and 1x1 convolutions for efficient architectures

## Standard Conv2d

### Operation
$$y[i, j, k] = \sum_{c} \sum_{p=0}^{K-1} \sum_{q=0}^{K-1} x[i+p, j+q, c] \cdot W[p, q, c, k] + b[k]$$

### Output Size
$$O = \frac{H - K + 2P}{S} + 1$$

- $H$: input height, $K$: kernel size, $P$: padding, $S$: stride

### Parameters
$$n_{\text{params}} = K^2 \cdot C_{\text{in}} \cdot C_{\text{out}} + C_{\text{out}}$$

## Depthwise Convolution

Each input channel is convolved with its own filter (no cross-channel mixing):

$$y[i, j, k] = \sum_{p,q} x[i+p, j+q, k] \cdot W[p, q, k]$$

$$n_{\text{params}} = K^2 \cdot C_{\text{in}}$$

Used in MobileNet, EfficientNet. Typically combined with pointwise (1×1) convolution as depthwise separable convolution.

## Dilated/Atrous Convolution

Filters have gaps (holes), increasing receptive field without increasing parameters:

$$y[i, j] = \sum_{p,q} x[i + d \cdot p, j + d \cdot q] \cdot W[p, q]$$

- $d$: dilation rate
- Receptive field: $K + (K-1)(d-1)$

Used in DeepLab (semantic segmentation) and WaveNet (audio generation).

## Transposed Convolution

"Upsampling" convolution — the mathematical transpose of a standard convolution:

### Output Size
$$O = S \cdot (H - 1) + K - 2P$$

### Checkerboard Artifacts
Transposed convolution with non-uniform overlap produces checkerboard patterns. Mitigated by:
- Using stride=1, kernel size divisible by stride
- Followed by standard convolution
- Using resize + convolution instead

## Group Convolution

Split input channels into $G$ groups, convolve separately, concatenate:

$$C_{\text{out per group}} = \frac{C_{\text{out}}}{G}$$

$$n_{\text{params}} = K^2 \cdot \frac{C_{\text{in}}}{G} \cdot \frac{C_{\text{out}}}{G} \cdot G = \frac{K^2 \cdot C_{\text{in}} \cdot C_{\text{out}}}{G}$$

Used in ResNeXt, ShuffleNet.

## 1x1 Convolution (Pointwise)

Changes channel dimension without spatial processing:

$$y[i, j, k] = \sum_{c} x[i, j, c] \cdot W[1, 1, c, k] + b[k]$$

Used for:
- Bottleneck layers in ResNet (reduce channels before 3×3 conv)
- Inception modules (channel mixing)
- Depthwise separable convolutions

## Implementation: im2col

```python
import torch
import torch.nn.functional as F

def conv2d_im2col(x, weight, bias=None, stride=1, padding=0):
    """Implement Conv2d via im2col (unfold + matrix multiply)"""
    B, C, H, W = x.shape
    out_channels, _, kH, kW = weight.shape
    
    # Unfold: extract patches
    x_unfolded = F.unfold(x, kernel_size=(kH, kW), 
                          padding=padding, stride=stride)
    # x_unfolded: (B, C*kH*kW, L) where L is output spatial size
    
    # Reshape weight for matmul: (out_channels, C*kH*kW)
    w_flat = weight.view(out_channels, -1)
    
    # Matmul: (B, out_channels, L)
    out = w_flat @ x_unfolded
    
    # Reshape to (B, out_channels, H_out, W_out)
    H_out = (H + 2*padding - kH) // stride + 1
    W_out = (W + 2*padding - kW) // stride + 1
    out = out.view(B, out_channels, H_out, W_out)
    
    if bias is not None:
        out += bias.view(1, -1, 1, 1)
    return out
```

## Code: Depthwise Separable Conv

```python
class DepthwiseSeparableConv(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=3):
        super().__init__()
        self.depthwise = nn.Conv2d(in_channels, in_channels, kernel_size,
                                    padding=kernel_size//2, groups=in_channels)
        self.pointwise = nn.Conv2d(in_channels, out_channels, 1)

    def forward(self, x):
        return self.pointwise(self.depthwise(x))
```

## Application Summary

| Variant | Parameters | Receptive Field | Use Case |
|---------|-----------|----------------|----------|
| Standard Conv2d | $K^2 C_{\text{in}} C_{\text{out}}$ | $K$ | General purpose |
| Depthwise | $K^2 C_{\text{in}}$ | $K$ | Mobile models |
| Dilated | $K^2 C_{\text{in}} C_{\text{out}}$ | $K + (K-1)(d-1)$ | Segmentation |
| Transposed | $K^2 C_{\text{in}} C_{\text{out}}$ | $K$ | Upsampling |
| Group | $\frac{K^2 C_{\text{in}} C_{\text{out}}}{G}$ | $K$ | Parameter efficient |
| 1×1 | $C_{\text{in}} C_{\text{out}}$ | 1 | Channel mixing |

## References
- Krizhevsky, Sutskever, Hinton, "ImageNet Classification with Deep Convolutional Neural Networks (AlexNet)", NeurIPS 2012
- Howard, Zhu, et al., "MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications", 2017
- Chen, Papandreou, et al., "DeepLab: Semantic Image Segmentation with Deep Convolutional Nets, Atrous Convolution, and Fully Connected CRFs", TPAMI 2018
- Radford, Metz, Chintala, "Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks (transposed conv artifact discussion)", ICLR 2016
