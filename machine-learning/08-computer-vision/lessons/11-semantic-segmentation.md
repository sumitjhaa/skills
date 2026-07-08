# Lesson 08.11: Semantic Segmentation

## Learning Objectives
- Understand fully convolutional networks for pixel-wise classification
- Implement U-Net with skip connections for biomedical segmentation
- Apply DeepLab's atrous spatial pyramid pooling (ASPP)
- Compare FCN, U-Net, DeepLab, and Transformer-based segmentation

## Fully Convolutional Network (FCN)

### Key Idea
Replace FC layers with $1 \times 1$ convolutions + spatial upsampling:

```
Conv layers → 1x1 conv (C classes) → Upsample (bilinear or deconv) → per-pixel softmax
```

### FCN Architecture Variants
| Variant | Skip connections | Output stride | Detail |
|---------|-----------------|--------------|--------|
| FCN-32s | None (direct upsampling) | 32 | Coarse |
| FCN-16s | Pool4 → upsampled → combined | 16 | Medium |
| FCN-8s | Pool3 + Pool4 → upsampled | 8 | Best |

## U-Net

### Encoder-Decoder Architecture
```
Encoder (down): Conv(3x3) → ReLU → MaxPool(x2) [4 stages]
Decoder (up): UpConv → Concat(encoder features) → Conv(3x3) → ReLU
```

### Skip Connections
Concatenate feature maps from encoder to corresponding decoder:

$$x_{\text{dec}}^{(i)} = \text{Up}\left(x_{\text{dec}}^{(i+1)}\right) \oplus x_{\text{enc}}^{(i)}$$

- Preserves spatial detail lost during downsampling
- Critical for good boundary segmentation
- **Especially effective with limited data** (biomedical imaging)

### Data Augmentation
U-Net paper introduced elastic deformations for data augmentation — effective with few training samples.

## DeepLab

### Atrous (Dilated) Convolutions
$$y[i] = \sum_k x[i + r \cdot k] w[k]$$

- $r$: dilation rate
- Larger receptive field without downsampling
- **Atrous = A trous** (French for "with holes")

### Atrous Spatial Pyramid Pooling (ASPP)
Parallel atrous convolutions at multiple rates:

$$\text{ASPP}(x) = \text{Conv}_{1\times1}(x) \oplus \text{Conv}_{3\times3, r=6}(x) \oplus \text{Conv}_{3\times3, r=12}(x) \oplus \text{Conv}_{3\times3, r=18}(x) \oplus \text{ImagePool}(x)$$

- Captures multi-scale context
- Image-level features (global average pooling) provide scene-level context

### DeepLabV3+
Adds decoder module (like U-Net) for better boundary detail.

## Code: U-Net Block

```python
import torch
import torch.nn as nn

class UNetBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(out_channels)

    def forward(self, x):
        x = torch.relu(self.bn1(self.conv1(x)))
        return torch.relu(self.bn2(self.conv2(x)))

class UNet(nn.Module):
    def __init__(self, in_channels=3, out_channels=1, features=64):
        super().__init__()
        self.downs = nn.ModuleList()
        self.ups = nn.ModuleList()
        
        for i in range(4):
            self.downs.append(UNetBlock(in_channels, features))
            in_channels = features
            features *= 2
        
        self.bottleneck = UNetBlock(features // 2, features)
        
        for i in range(4):
            features //= 2
            self.ups.append(nn.ConvTranspose2d(features*2, features, 2, stride=2))
            self.ups.append(UNetBlock(features*2, features))

    def forward(self, x):
        skip_connections = []
        for down in self.downs:
            x = down(x)
            skip_connections.append(x)
            x = nn.MaxPool2d(2)(x)
        x = self.bottleneck(x)
        skip_connections = skip_connections[::-1]
        for idx in range(0, len(self.ups), 2):
            x = self.ups[idx](x)
            x = torch.cat([x, skip_connections[idx//2]], dim=1)
            x = self.ups[idx + 1](x)
        return x
```

## Segmentation Architectures Comparison

| Model | Params | FLOPs | mIoU (Cityscapes) | Key Feature |
|-------|--------|-------|-------------------|-------------|
| FCN-8s | 134M | 340B | 65.3 | First FCN |
| U-Net | 31M | 94B | 72.0 (medical) | Skip connections |
| DeepLabV3+ | 60M | 178B | 82.1 | ASPP + decoder |
| SegFormer-B3 | 45M | 83B | 83.5 | Hierarchical Transformer |
| Mask2Former | 109M | 195B | 86.3 | Masked attention |

## Loss Functions

| Loss | Formula | Properties |
|------|---------|------------|
| Cross-entropy | $-\sum_c y_c \log p_c$ | Standard, class imbalance issue |
| Weighted CE | $-\sum_c w_c y_c \log p_c$ | Handles class imbalance |
| Dice | $1 - \frac{2|y \cap \hat{y}|}{|y| + |\hat{y}|}$ | Overlap-based, good for medical |
| Focal | $-(1-p)^\gamma \log p$ | Focus on hard examples |

## Evaluation Metrics
- **mIoU (Mean Intersection over Union)**: $\frac{1}{C} \sum_{c=1}^C \frac{TP_c}{TP_c + FP_c + FN_c}$
- **Pixel accuracy**: $\frac{\text{correct pixels}}{\text{total pixels}}$
- **Dice coefficient**: $2|X \cap Y| / (|X| + |Y|)$

## Practical Considerations
- **Input size**: Downsample factor (output stride) = 8-32; smaller = better detail but more memory
- **Boundary refinement**: CRF post-processing (DeepLabV1) or boundary loss
- **Data imbalance**: Weighted loss or median frequency balancing
- **Test time augmentation**: Horizontal flip + multi-scale fusion (+2-3% mIoU)
- **FP16 training**: Most segmentation models fit in 16-bit with gradient scaling

## References
- Long, Shelhamer, Darrell, "Fully Convolutional Networks for Semantic Segmentation", CVPR 2015
- Ronneberger, Fischer, Brox, "U-Net: Convolutional Networks for Biomedical Image Segmentation", MICCAI 2015
- Chen, Papandreou, Kokkinos, Murphy, Yuille, "DeepLab: Semantic Image Segmentation with Deep Convolutional Nets, Atrous Convolution, and Fully Connected CRFs", TPAMI 2017
- Chen, Zhu, Papandreou, et al., "Encoder-Decoder with Atrous Separable Convolution for Semantic Image Segmentation (DeepLabV3+)", ECCV 2018
- Xie, Wang, Yu, et al., "SegFormer: Simple and Efficient Design for Semantic Segmentation with Transformers", NeurIPS 2021
