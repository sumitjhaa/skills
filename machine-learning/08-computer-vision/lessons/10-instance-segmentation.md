# Lesson 08.10: Instance Segmentation

## Learning Objectives
- Understand Mask R-CNN architecture and RoIAlign
- Implement real-time instance segmentation with YOLACT
- Apply SOLO for fully convolutional instance segmentation
- Compare instance vs semantic vs panoptic segmentation

## Mask R-CNN

### Architecture
Extends Faster R-CNN with parallel mask head:

```
Image → Backbone → FPN → RPN → RoIAlign → [cls, bbox, mask] heads
```

### RoIAlign
Bilinear interpolation to extract features at precise RoI locations:

$$F(i, j) = \sum_{u=0}^1 \sum_{v=0}^1 w_u w_v \cdot G(i + u, j + v)$$

- Eliminates quantization of RoIPool
- Maintains spatial correspondence (critical for mask prediction)

### Mask Head
```
RoI features (14x14) → Conv layers → 28x28 → Sigmoid → Binary mask per class (K)
```

- **Binary masks**: Predict $K$ binary masks (one per class) per RoI
- **Loss**: $\mathcal{L}_{\text{mask}}$ only for ground-truth class (no competition between classes)

### Multi-Task Loss
$$\mathcal{L} = \mathcal{L}_{\text{cls}} + \mathcal{L}_{\text{box}} + \mathcal{L}_{\text{mask}}$$

## YOLACT (You Only Look At CoefficienTs)

### Real-time Instance Segmentation
```
Image → Backbone → FPN → Protonet (prototype masks) + Prediction head (mask coefficients)
Masks = Prototypes × Coefficients → Crop with bounding box → Threshold
```

### Key Components
- **Protonet**: FCN generating $k$ prototype masks ($k=32$)
- **Mask coefficients**: $k$ scalars per instance (from prediction head)
- **Assembly**: $\text{Mask} = \sigma(\text{Prototypes} \times \text{Coefficients})$
- **Crop**: Mask with predicted bounding box (remove inter-instance interference)

### Speed
- 30+ FPS on Titan X (real-time)
- Trade-off: Quality is lower than Mask R-CNN

## SOLO (Segmenting Objects by Locations)

### Fully Convolutional
No RoI operations, no bounding boxes:

- **Grid**: Divide image into $S \times S$ grids
- **Category branch**: $S \times S \times C$ (semantic class per grid cell)
- **Mask branch**: $S \times S \times H \times W$ (binary mask per grid cell)
- **Assign**: Each object assigned to a specific grid cell based on center location

### SOLOv2
- **Dynamic convolution**: Mask kernel dynamically generated per grid cell
- **Matrix NMS**: Parallel NMS for mask overlaps (fast)

## Code: Mask R-CNN Mask Head

```python
import torch
import torch.nn as nn

class MaskHead(nn.Module):
    def __init__(self, in_channels=256, num_classes=80):
        super().__init__()
        self.convs = nn.Sequential(
            nn.Conv2d(in_channels, in_channels, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels, in_channels, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels, in_channels, 3, padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(in_channels, in_channels, 2, stride=2),
            nn.ReLU(),
            nn.Conv2d(in_channels, num_classes, 1),
        )

    def forward(self, x):
        # x: (B, C, 14, 14) from RoIAlign
        return self.convs(x)  # (B, num_classes, 28, 28)
```

## Segmentation Types

| Type | Description | What each pixel gets |
|------|-------------|---------------------|
| Semantic Segmentation | Class labels per pixel | $c_i \in \{1, \dots, K\}$ |
| Instance Segmentation | Object instance per pixel | $(c_i, id_i)$ |
| Panoptic Segmentation | Semantic + instance | Stuff (semantic) + things (instance) |

### Panoptic Segmentation
$$\text{Panoptic Quality (PQ)} = \frac{\sum_{(p,g) \in TP} \text{IoU}(p,g)}{|TP| + \frac{1}{2}|FP| + \frac{1}{2}|FN|}$$

- **Stuff**: Amorphous regions (sky, grass, road) — semantic only
- **Things**: Countable objects (people, cars) — instance masks

## Instance Segmentation Comparison

| Method | Backbone | AP mask | FPS | Key Feature |
|--------|----------|---------|-----|-------------|
| Mask R-CNN | ResNet-101 | 37.1 | 5 | RoIAlign |
| YOLACT | ResNet-101 | 31.2 | 33 | Prototype masks |
| SOLOv2 | ResNet-101 | 37.8 | 12 | Fully conv, no RoI |
| CenterMask | ResNet-101 | 38.3 | 10 | Anchor-free |
| Mask2Former | Swin-B | 50.1 | 12 | Masked attention Transformer |

## Evaluation Metrics
- **AP (Average Precision)**: Precision-recall over mask IoU thresholds
- **AP@50**: IoU threshold 0.5
- **AP@75**: IoU threshold 0.75
- **AP_small/medium/large**: AP for objects by size

## Practical Considerations
- **Mask resolution**: 28×28 is standard; higher res (56×56) improves small objects
- **Loss weighting**: $\lambda_{\text{mask}}$ typically same as $\lambda_{\text{cls}}$ (1:1)
- **Post-processing**: NMS on masks using predicted box IoU
- **Mask format**: COCO uses RLE (run-length encoding) for efficient storage
- **Ground truth**: Polygons in COCO (converted to masks during training)

## References
- He, Gkioxari, Dollar, Girshick, "Mask R-CNN", ICCV 2017
- Bolya, Zhou, Xiao, Lee, "YOLACT: Real-time Instance Segmentation", ICCV 2019
- Wang, Chen, Hoi, et al., "SOLO: Segmenting Objects by Locations", ECCV 2020
- Cheng, Schwing, Kirillov, "Per-Pixel Classification is Not All You Need for Semantic Segmentation (MaskFormer)", NeurIPS 2021
- Cheng, Misra, Schwing, Kirillov, Girdhar, "Masked-attention Mask Transformer for Universal Image Segmentation (Mask2Former)", CVPR 2022
