# Lesson 08.09: Object Detection

## Learning Objectives
- Understand two-stage (R-CNN family) and one-stage (YOLO) detection
- Implement Faster R-CNN with RPN and RoI heads
- Apply YOLOv8's anchor-free detection pipeline
- Compare detection architectures on speed/accuracy trade-offs

## Two-Stage Detectors

### R-CNN (Region-based CNN)
1. Selective search → 2000 region proposals
2. Warp each region to fixed size
3. CNN → SVM classifier + bounding box regression
4. **Slow**: 47s per image (redundant CNN forward passes)

### Fast R-CNN
1. Single CNN forward pass on whole image
2. **RoI Pooling**: Project region proposals onto feature map, pool to fixed size
3. Multi-task loss: $\mathcal{L} = \mathcal{L}_{\text{cls}} + \lambda \mathcal{L}_{\text{box}}$
4. **Faster**: 0.3s per image

### Faster R-CNN
```
Image → CNN backbone → Feature map → RPN → RoIs → RoI Head → detections
```

### Region Proposal Network (RPN)
- **Anchors**: $k$ boxes per spatial location (3 scales × 3 aspect ratios = 9 anchors)
- **Classification**: object vs not-object (binary)
- **Regression**: refine anchor to proposal
- **NMS**: Non-maximum suppression to reduce proposals from ~200K to 2K

### RoI Head
```python
# For each RoI:
roi_features = RoIAlign(feature_map, proposals, output_size=7x7)
roi_features = Flatten()(roi_features)
cls_score = FC(roi_features)  # softmax over K+1 classes
bbox_reg = FC(roi_features)   # offset for each of K classes
```

## One-Stage Detectors

### YOLO (You Only Look Once)
Divide image into $S \times S$ grid. Each cell predicts:
- $B$ bounding boxes (4 coords + objectness confidence)
- $C$ class probabilities

### YOLOv3
- **Darknet-53 backbone**: 53 conv layers with residual connections
- **Multi-scale predictions**: 3 scales (large, medium, small objects)
- **Spatial pyramid pooling**: Enrich features at multiple scales
- **Loss**: Binary cross-entropy for class + objectness, MSE for box coords

### YOLOv8
- **Anchor-free**: Center-based detection (no predefined anchors)
- **Decoupled head**: Separate classification and regression branches
- **Task-aligned assigner**: Assign samples based on classification + IoU
- **Mosaic augmentation**: Stitch 4 images for context diversity
- **CIoU loss**: Complete IoU for box regression

## Loss Functions

### Classification
- **Focal Loss** (RetinaNet): $\text{FL}(p_t) = -\alpha_t (1-p_t)^\gamma \log(p_t)$
  - Down-weights easy examples, focuses on hard examples
  - $\gamma = 2.0$ reduces loss for well-classified samples
- **BCE**: Binary cross-entropy per class (YOLO)

### Localization
| Loss | Formula | Properties |
|------|---------|------------|
| Smooth L1 | $\begin{cases} 0.5x^2 & \|x\| < 1 \\ \|x\| - 0.5 & \text{otherwise} \end{cases}$ | Less sensitive to outliers |
| IoU | $1 - \frac{|B \cap B^{gt}|}{|B \cup B^{gt}|}$ | Scale invariant |
| GIoU | $IoU - \frac{|C \setminus (B \cup B^{gt})|}{|C|}$ | Handles non-overlapping boxes |
| CIoU | $GIoU + \alpha v$ | Aspect ratio + center distance |

## Code: Faster R-CNN RPN

```python
import torch
import torch.nn as nn

class RPN(nn.Module):
    def __init__(self, in_channels=512, mid_channels=512, num_anchors=9):
        super().__init__()
        self.conv = nn.Conv2d(in_channels, mid_channels, 3, padding=1)
        self.cls_logits = nn.Conv2d(mid_channels, num_anchors, 1)
        self.bbox_pred = nn.Conv2d(mid_channels, 4 * num_anchors, 1)

    def forward(self, x):
        # x: (B, C, H, W)
        t = torch.relu(self.conv(x))
        scores = self.cls_logits(t)    # (B, A, H, W)
        deltas = self.bbox_pred(t)     # (B, 4A, H, W)
        return scores, deltas
```

## Detector Comparison

| Detector | Backbone | FPS | AP (COCO) | Type |
|----------|----------|-----|-----------|------|
| Faster R-CNN | ResNet-101 | 5 | 38.2 | Two-stage |
| RetinaNet | ResNet-101 | 5 | 39.1 | One-stage |
| YOLOv3 | Darknet-53 | 20 | 33.0 | One-stage |
| YOLOv8-x | - | 15 | 54.0 | One-stage |
| DINO | Swin-L | 2 | 63.3 | Transformer |
| RT-DETR | ResNet-50 | 108 | 53.1 | Real-time Transformer |

## Evaluation: mAP

### Average Precision (AP)
1. Rank detections by confidence
2. Compute precision-recall curve
3. AP = area under P-R curve (interpolated 11-point or all-points)

### mAP
Mean AP across IoU thresholds:
- **AP@50**: IoU threshold 0.5
- **AP@75**: IoU threshold 0.75
- **AP**: Average across IoU from 0.5 to 0.95 (step 0.05)

## Practical Considerations
- **NMS threshold**: 0.5-0.7 IoU; lower = fewer detections, higher = more overlap
- **Score threshold**: 0.05 for evaluation (COCO), 0.5 for visualization
- **Multi-scale testing**: Test at 3 scales (0.5, 1.0, 1.5) boosts AP by 1-2 points
- **Soft NMS**: Decay scores of overlapping boxes instead of removing
- **Data augmentation**: Mosaic, mixup, random affine for YOLO
- **Anchor design**: K-means on training set boxes for YOLO anchors

## References
- Girshick, Donahue, Darrell, Malik, "Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation (R-CNN)", CVPR 2014
- Ren, He, Girshick, Sun, "Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks", NeurIPS 2015
- Redmon, Divvala, Girshick, Farhadi, "You Only Look Once: Unified, Real-Time Object Detection", CVPR 2016
- Lin, Goyal, Girshick, He, Dollar, "Focal Loss for Dense Object Detection (RetinaNet)", ICCV 2017
- Zhang, Li, et al., "DINO: DETR with Improved DeNoising AnchOr Boxes for End-to-End Object Detection", ICLR 2023
