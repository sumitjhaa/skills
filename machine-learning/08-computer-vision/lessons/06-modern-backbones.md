# Lesson 08.06: Modern Backbones (DenseNet, ConvNeXt, RegNet)

## Learning Objectives
- Understand dense connectivity in DenseNet
- Implement ConvNeXt with modernized ResNet design
- Apply RegNet design space analysis
- Compare modern CNN backbones with vision transformers

## DenseNet

### Dense Connectivity
Each layer receives feature maps from all preceding layers:

$$x_\ell = H_\ell([x_0, x_1, \dots, x_{\ell-1}])$$

- $H_\ell$: BN-ReLU-Conv(3×3)
- $[\dots]$: channel-wise concatenation

### Dense Block
```
Input → [BN → ReLU → Conv(3x3)] × L → Concatenate → Transition layer
```

### Transition Layer
```
BN → 1x1 Conv (reduce channels) → 2x2 AvgPool
```

### Growth Rate $k$
Each layer adds $k$ channels (typically 12-32). Total channels grow as $k \times (L+1)$.

### Advantages
- **Parameter efficient**: No redundant feature maps
- **Gradient flow**: Direct paths from early to late layers
- **Feature reuse**: Implicit deep supervision
- **Regularization**: Dense connections reduce overfitting

## ConvNeXt

### Modernizing ResNet
Borrow design choices from Swin Transformer while staying fully convolutional:

| Component | ResNet | ConvNeXt |
|-----------|--------|----------|
| Activation | ReLU | GELU |
| Normalization | BN | LayerNorm (per channel) |
| Convolution | 3×3 | 7×7 depthwise |
| Bottleneck | Wide → Narrow | Narrow → Wide (inverted) |
| Downsampling | stride 2 conv | LayerNorm + stride 2 conv |
| Stage compute ratio | [3,4,6,3] | [3,3,9,3] (Swin-like) |

### Key Changes
- **Patchify stem**: 4×4 conv stride 4 (like ViT patch embedding)
- **Large kernel**: 7×7 depthwise conv (large receptive field)
- **Inverted bottleneck**: 4× expansion in hidden dim (like MobileNetV2)
- **Fewer activation/norm**: Remove GELU and LN from certain positions

## RegNet

### Design Space Analysis
Start with any network (AnyNet) → constrain to regular structure (RegNet):

$$\text{RegNet}(d, w_0, w_a, w_m, b, g)$$

- $d$: depth (number of blocks)
- $w_0$: initial width
- $w_a, w_m$: width growth parameters
- $b$: bottleneck ratio
- $g$: group width

### Key Finding
Best architectures have **log-linear width growth**: $w_j = w_0 \cdot w_a^{j/d}$

### RegNet Design Principles
1. Depth $d \approx 20-30$ blocks
2. Width grows linearly with depth
3. Bottleneck ratio $b = 1.0$ (no bottleneck)
4. Group width $g \approx 8-64$

## Code: Dense Block

```python
import torch
import torch.nn as nn

class DenseLayer(nn.Module):
    def __init__(self, in_channels, growth_rate=32):
        super().__init__()
        self.bn1 = nn.BatchNorm2d(in_channels)
        self.conv1 = nn.Conv2d(in_channels, 4 * growth_rate, 1, bias=False)
        self.bn2 = nn.BatchNorm2d(4 * growth_rate)
        self.conv2 = nn.Conv2d(4 * growth_rate, growth_rate, 3, padding=1, bias=False)

    def forward(self, x):
        out = self.conv1(torch.relu(self.bn1(x)))
        out = self.conv2(torch.relu(self.bn2(out)))
        return torch.cat([x, out], dim=1)

class DenseBlock(nn.Module):
    def __init__(self, in_channels, num_layers, growth_rate=32):
        super().__init__()
        self.layers = nn.ModuleList([
            DenseLayer(in_channels + i * growth_rate, growth_rate)
            for i in range(num_layers)
        ])

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x
```

## Backbone Comparison

| Backbone | Year | Params | FLOPs | Top-1 | Architecture Type |
|----------|------|--------|-------|-------|-------------------|
| DenseNet-201 | 2017 | 20M | 8B | 77.3 | Dense connections |
| ResNeXt-101 | 2017 | 84M | 32B | 79.3 | Group conv |
| EfficientNet-B4 | 2019 | 19M | 8B | 82.9 | Compound scaling |
| RegNetY-8GF | 2020 | 34M | 8B | 79.9 | Design space |
| ConvNeXt-B | 2022 | 89M | 30B | 84.1 | Modernized Conv |
| Swin-B | 2021 | 88M | 28B | 83.5 | Hierarchical ViT |

## Practical Considerations
- **DenseNet**: Memory intensive (feature map concatenation); use checkpointing
- **ConvNeXt**: Best CNN on ImageNet; excellent dense prediction tasks
- **RegNet**: Systematic design; less ad-hoc than manual architectures
- **Complementarity**: CNNs often better for dense prediction (detection, segmentation) than ViT

## References
- Huang, Liu, van der Maaten, Weinberger, "Densely Connected Convolutional Networks", CVPR 2017
- Liu, Mao, Wu, et al., "A ConvNet for the 2020s", CVPR 2022
- Radosavovic, Kosaraju, Girshick, He, Dollar, "Designing Network Design Spaces", CVPR 2020
- Xie, Girshick, Dollar, Tu, He, "Aggregated Residual Transformations for Deep Neural Networks (ResNeXt)", CVPR 2017
- Tan & Le, "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks", ICML 2019
