# Lesson 08.05: Efficient Backbones (MobileNet, ShuffleNet, EfficientNet)

## Learning Objectives
- Understand depthwise separable convolutions
- Implement MobileNetV2 inverted residuals
- Apply compound scaling with EfficientNet
- Analyze efficiency-accuracy trade-offs for mobile/edge deployment

## MobileNetV1: Depthwise Separable Convolution

### Standard Convolution
FLOPs: $D_k^2 \cdot M \cdot N \cdot D_F^2$

### Depthwise Separable
Depthwise: $D_k^2 \cdot M \cdot D_F^2$ + Pointwise: $M \cdot N \cdot D_F^2$

**FLOPs ratio**: $\frac{1}{N} + \frac{1}{D_k^2}$

At $3 \times 3$: ~8-9× cheaper than standard convolution.

### Architecture
```
Conv(3x3) → Depthwise Conv(3x3) → Pointwise Conv(1x1) → Pool → ...
```

Width multiplier $\alpha$: reduce channels uniformly (e.g., 0.75, 0.5, 0.25).

## MobileNetV2: Inverted Residual with Linear Bottleneck

### Inverted Residual
```
Expansion (1x1, t× channels) → Depthwise (3x3) → Projection (1x1, original channels)
```

- **Expansion factor**: $t = 6$ (expand channels 6× before depthwise)
- **Linear bottleneck**: No ReLU after projection (preserves information in low-dim space)

### Why Inverted?
- Standard ResNet: thin → wide → thin (skip connects thin layers)
- MobileNetV2: thin → wide → thin (skip connects **thin** layers)
- Depthwise conv operates in high-dimensional space

### Key Parameters
- Input: $h \times w \times k$
- Expansion: $h \times w \times tk$
- Depthwise: $h \times w \times tk$
- Projection: $h \times w \times k'$

## ShuffleNet

### Group Convolution Limitation
Group convolutions have no cross-group communication:
```
Channel 0-3 → Group 0, Channel 4-7 → Group 1, ...
```

### Channel Shuffle
Permute channels across groups before next group convolution:

$$\text{shuffle}(\text{reshape}(x, G, C//G) \to \text{transpose} \to \text{reshape})$$

### ShuffleNet Unit
```
Pointwise Group Conv → Channel Shuffle → Depthwise → Pointwise Group Conv
```

## EfficientNet

### Compound Scaling
Scale depth ($d$), width ($w$), and resolution ($r$) jointly:

$$d = \alpha^\phi, \quad w = \beta^\phi, \quad r = \gamma^\phi$$
$$\text{s.t. } \alpha \cdot \beta^2 \cdot \gamma^2 \approx 2$$

- $\phi$: compound coefficient (user-specified)
- $\alpha, \beta, \gamma$: constants determined by small grid search on baseline

### NAS Discovered Baseline
MBConv blocks (MobileNetV2-style) with Squeeze-and-Excitation:

```
MBConv1(k3×3, exp_ratio=1) → MBConv6(k3×3, exp=6) → MBConv6(k5×5, exp=6) → ...
```

## Efficiency Comparison

| Model | Params | FLOPs | Top-1 ImageNet | Relative Speed |
|-------|--------|-------|---------------|----------------|
| MobileNetV1 | 4.2M | 0.6B | 70.9% | 1.0× |
| MobileNetV2 | 3.5M | 0.3B | 72.0% | 1.1× |
| ShuffleNet | 2.3M | 0.5B | 71.8% | 1.1× |
| EfficientNet-B0 | 5.3M | 0.4B | 76.3% | 0.8× |
| EfficientNet-B7 | 66M | 75B | 84.4% | 0.02× |
| ResNet-50 | 26M | 8B | 76.0% | 0.1× |

## Code: Depthwise Separable Conv

```python
import torch
import torch.nn as nn

class DepthwiseSeparableConv(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=3, stride=1):
        super().__init__()
        self.depthwise = nn.Conv2d(
            in_channels, in_channels, kernel_size,
            stride, padding=kernel_size//2, groups=in_channels,
            bias=False
        )
        self.pointwise = nn.Conv2d(
            in_channels, out_channels, 1, bias=False
        )
        self.bn1 = nn.BatchNorm2d(in_channels)
        self.bn2 = nn.BatchNorm2d(out_channels)

    def forward(self, x):
        x = torch.relu(self.bn1(self.depthwise(x)))
        x = torch.relu(self.bn2(self.pointwise(x)))
        return x

class InvertedResidual(nn.Module):
    def __init__(self, in_channels, out_channels, stride, expand_ratio=6):
        super().__init__()
        hidden_dim = in_channels * expand_ratio
        self.use_residual = stride == 1 and in_channels == out_channels
        
        layers = []
        if expand_ratio != 1:
            layers.extend([
                nn.Conv2d(in_channels, hidden_dim, 1, bias=False),
                nn.BatchNorm2d(hidden_dim),
                nn.ReLU6(),
            ])
        layers.extend([
            nn.Conv2d(hidden_dim, hidden_dim, 3, stride, 1, 
                      groups=hidden_dim, bias=False),
            nn.BatchNorm2d(hidden_dim),
            nn.ReLU6(),
            nn.Conv2d(hidden_dim, out_channels, 1, bias=False),
            nn.BatchNorm2d(out_channels),
        ])
        self.conv = nn.Sequential(*layers)

    def forward(self, x):
        if self.use_residual:
            return x + self.conv(x)
        return self.conv(x)
```

## Practical Considerations
- **Latency vs FLOPs**: FLOPs don't perfectly predict speed (memory bandwidth, parallelism)
- **Hardware targeting**: MobileNet works well on mobile, EfficientNet on GPUs
- **Quantization**: 8-bit quantized models are 2-4× faster with minimal accuracy loss
- **Neural Architecture Search**: Platform-aware NAS (MnasNet, ProxylessNAS) finds hardware-specific ops
- **Knowledge distillation**: Small student models trained on large teacher outputs

## References
- Howard, Zhu, Chen, et al., "MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications", CVPR 2017
- Sandler, Howard, Zhu, Zhmoginov, Chen, "MobileNetV2: Inverted Residuals and Linear Bottlenecks", CVPR 2018
- Zhang, Zhou, Lin, Sun, "ShuffleNet: An Extremely Efficient Convolutional Neural Network for Mobile Devices", CVPR 2018
- Tan & Le, "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks", ICML 2019
- Howard, Sandler, Chu, et al., "Searching for MobileNetV3", ICCV 2019
