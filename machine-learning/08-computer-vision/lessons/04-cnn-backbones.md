# Lesson 08.04: CNN Backbones

## Learning Objectives
- Understand convolution operation and its properties
- Implement LeNet, AlexNet, VGG, and ResNet
- Analyze residual connections for deep network training
- Apply bottleneck design for efficient computation

## Convolutional Layer
$$y_{i,j,k} = \sum_{c=0}^{C_{in}-1} \sum_{u=0}^{H_k-1} \sum_{v=0}^{W_k-1} x_{i+u, j+v, c} \, w_{u,v,c,k} + b_k$$

### Key Properties
- **Locality**: Each neuron connects to local region (receptive field)
- **Weight sharing**: Same kernel applied across spatial dimensions
- **Translation equivariance**: $f(\text{shift}(x)) = \text{shift}(f(x))$

## LeNet-5 (1998)

```
Conv(5x5, 6) → Pool(2x2) → Conv(5x5, 16) → Pool(2x2) → FC(120) → FC(84) → FC(10)
```

- 60k parameters
- Input: 32x32 grayscale
- Activation: tanh / sigmoid
- **Significance**: First successful CNN for digit recognition (MNIST)

## AlexNet (2012)

```
Conv(11x11, 96, stride 4) → MaxPool(3x3, stride 2)
→ Conv(5x5, 256) → MaxPool → Conv(3x3, 384)
→ Conv(3x3, 384) → Conv(3x3, 256) → MaxPool
→ FC(4096) → FC(4096) → FC(1000)
```

### Innovations
- ReLU activation (faster training than tanh)
- Dropout (0.5 on FC layers)
- Local Response Normalization (LRN)
- Data augmentation (translation, flip, color)
- Overlapping pooling (stride < kernel size)

## VGG (2014)

Simple, uniform design: only $3 \times 3$ convolutions with stride 1, padding 1:

### VGG-16 Architecture
```
[Conv3-64] × 2 → MaxPool
[Conv3-128] × 2 → MaxPool
[Conv3-256] × 3 → MaxPool
[Conv3-512] × 3 → MaxPool
[Conv3-512] × 3 → MaxPool
FC(4096) → FC(4096) → FC(1000)
```

### Why 3x3 Convolutions?
- Stack of 3×3 (stride 1) has receptive field 7×7 with 3× fewer parameters than 7×7
- More non-linearity (3 ReLUs vs 1)

## ResNet (2015)

### Residual Block
$$y = \mathcal{F}(x, \{W_i\}) + x$$

- $\mathcal{F}$: residual mapping (typically 2-3 conv layers)
- Identity skip connection: $+x$

### Why Residuals?
- **Vanishing gradient**: Gradient flows directly through skip connections
- **Identity mapping**: Enables training 100+ layers
- **Ensemble effect**: ResNet behaves as ensemble of shallower networks

### Bottleneck Block
$$1 \times 1 \to 3 \times 3 \to 1 \times 1$$

- 1×1 reduce dim (e.g., 256 → 64) → 3×3 (64 → 64) → 1×1 expand (64 → 256)
- **FLOPs**: 4× cheaper than two 3×3 layers with same channels

### ResNet Architectures
| Variant | Layers | Blocks | Top-1 ImageNet |
|---------|--------|--------|----------------|
| ResNet-18 | 18 | [2,2,2,2] | 70.3% |
| ResNet-34 | 34 | [3,4,6,3] | 73.3% |
| ResNet-50 | 50 | [3,4,6,3] bottleneck | 76.0% |
| ResNet-101 | 101 | [3,4,23,3] bottleneck | 77.3% |
| ResNet-152 | 152 | [3,8,36,3] bottleneck | 77.8% |

## Code: Residual Block

```python
import torch
import torch.nn as nn

class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, stride, padding=1)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1, stride),
                nn.BatchNorm2d(out_channels),
            )

    def forward(self, x):
        out = torch.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        return torch.relu(out)
```

## Architecture Design Principles
- **Depth**: More layers → more capacity (ResNet-152 vs ResNet-50)
- **Width**: More channels → more capacity per layer (Wide ResNet)
- **Cardinality**: Grouped convolutions → ResNeXt
- **Attention**: Squeeze-and-Excitation → SE-ResNet
- **Compound scaling**: EfficientNet

## Backbone Comparison

| Backbone | Year | Params | FLOPs | Top-1 | Key Innovation |
|----------|------|--------|-------|-------|---------------|
| AlexNet | 2012 | 60M | 1.5B | 57.1 | ReLU, Dropout |
| VGG-16 | 2014 | 138M | 31B | 71.6 | Very deep (3×3) |
| ResNet-50 | 2015 | 26M | 8B | 76.0 | Residual connections |
| ResNeXt-101 | 2017 | 84M | 32B | 79.3 | Group convolutions |
| DenseNet-201 | 2017 | 20M | 8B | 77.3 | Dense connections |
| EfficientNet-B7 | 2019 | 66M | 75B | 84.4 | NAS + compound scaling |

## References
- LeCun, Bottou, Bengio, Haffner, "Gradient-Based Learning Applied to Document Recognition", IEEE 1998
- Krizhevsky, Sutskever, Hinton, "ImageNet Classification with Deep Convolutional Neural Networks", NeurIPS 2012
- Simonyan & Zisserman, "Very Deep Convolutional Networks for Large-Scale Image Recognition", ICLR 2015
- He, Zhang, Ren, Sun, "Deep Residual Learning for Image Recognition", CVPR 2016
- Huang, Liu, van der Maaten, Weinberger, "Densely Connected Convolutional Networks", CVPR 2017
