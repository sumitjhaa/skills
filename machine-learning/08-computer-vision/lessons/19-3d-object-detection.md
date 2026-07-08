# Lesson 08.19: 3D Object Detection

## Learning Objectives
- Understand point-based (PointRCNN) and voxel-based (VoxelNet) detectors
- Implement PointPillars for real-time 3D detection
- Apply BEVFormer for camera-based 3D detection
- Compare LiDAR and camera-based 3D detection approaches

## Point-Based: PointRCNN

### Stage 1: Proposal Generation
1. **Point features**: PointNet++ on raw points
2. **Foreground segmentation**: Binary classification per point
3. **Box proposal**: Per foreground point, predict 3D box

### Stage 2: Refinement
1. **RoI pooling**: Pool point features for each proposal
2. **Canonical transform**: Transform points to proposal coordinate frame
3. **Box refinement**: Refine position, size, orientation

## Voxel-Based: VoxelNet

### Voxel Feature Encoding (VFE)
1. Divide point cloud into voxels ($D \times H \times W$)
2. Per voxel: PointNet over points in voxel → voxel feature
3. Process: 3D Conv → 2D BEV feature → RPN

### Limitations
- 3D convolutions are memory intensive
- Resolution limited: typical voxel size 0.1-0.2m

## Pillar-Based: PointPillars

### Architecture
```
Points → Stacked Pillars → PointNet per pillar → 2D Conv → Detection head
```

### Pillars
- Vertical columns (no 3D voxel depth)
- Each pillar: $N$ points × $(x,y,z,r,x_c,y_c,z_c,x_p,y_p)$

### Advantages
- **Fast**: No 3D convolutions (all 2D after pillar encoding)
- **Efficient**: ~62 FPS on single GPU
- **Competitive**: Comparable accuracy to VoxelNet

## BEV-Based: BEVFormer

### Camera-to-BEV Transformation
Multi-camera images → Transform to Bird's Eye View via deformable attention:

1. **Camera features**: ResNet/ViT per camera
2. **BEV queries**: Learnable grid in BEV space
3. **Deformable attention**: Each query attends to image regions based on camera geometry

### Temporal Fusion
Concatenate BEV features from previous frame → current BEV queries:

$$\text{BEV}_t = \text{BEVFormer}(\text{IMGs}_t, \text{BEV}_{t-1})$$

## Code: PointPillars Pillar Encoding

```python
import torch
import torch.nn as nn

class PillarFeatureNet(nn.Module):
    def __init__(self, num_input=9, num_filters=64):
        super().__init__()
        self.pfn = nn.Sequential(
            nn.Linear(num_input, num_filters),
            nn.BatchNorm1d(num_filters),
            nn.ReLU(),
            nn.Linear(num_filters, num_filters),
            nn.BatchNorm1d(num_filters),
            nn.ReLU(),
        )

    def forward(self, pillars, mask):
        # pillars: (B, P, N, C) — batch, pillars, points per pillar, features
        # mask: (B, P, N) — valid points
        features = self.pfn(pillars) * mask.unsqueeze(-1)
        # Max pooling over points in each pillar
        pillar_features = features.max(dim=2)[0]  # (B, P, F)
        return pillar_features
```

## 3D Detection Comparison

| Method | Modality | Backbone | mAP (BEV) | FPS |
|--------|----------|----------|-----------|-----|
| PointRCNN | LiDAR | PointNet++ | 78.7 | 10 |
| VoxelNet | LiDAR | 3D Conv | 78.5 | 5 |
| SECOND | LiDAR | Sparse 3D Conv | 79.7 | 25 |
| PointPillars | LiDAR | Pillar + 2D Conv | 77.9 | 62 |
| BEVFormer | Camera | Transformer | 65.8 (nuScenes NDS) | 10 |
| FSD (Fully Sparse) | LiDAR | Sparse Conv | 81.3 | 30 |

## Evaluation Metrics

### KITTI
| Metric | Easy | Moderate | Hard |
|--------|------|----------|------|
| Car AP (3D) | 89.5 | 78.9 | 76.5 |
| Car AP (BEV) | 90.8 | 87.6 | 85.3 |
| Pedestrian AP (3D) | 53.8 | 49.6 | 45.3 |

### nuScenes
- **NDS (nuScenes Detection Score)**: Combines AP with translation/scale/orientation/velocity errors
- **mAP**: Over 10 classes

## Practical Considerations
- **Point cloud range**: Typically 70-100m for cars, shorter for pedestrians
- **Anchor design**: K-means on training set boxes for anchor priors
- **Data augmentation**: Random flipping, rotation (z-axis), scaling, ground-truth sampling
- **NMS**: 3D IoU NMS (axis-aligned or oriented)
- **Multi-modal fusion**: Camera provides texture, LiDAR provides geometry

## References
- Shi, Wang, Li, "PointRCNN: 3D Object Proposal Generation and Detection from Point Cloud", CVPR 2019
- Zhou & Tuzel, "VoxelNet: End-to-End Learning for Point Cloud Based 3D Object Detection", CVPR 2018
- Lang, Vora, Caesar, Zhou, Yang, Beijbom, "PointPillars: Fast Encoders for Object Detection from Point Clouds", CVPR 2019
- Li, Ge, Yu, et al., "BEVFormer: Learning Bird's-Eye-View Representation from Multi-Camera Images via Spatiotemporal Transformers", ECCV 2022
- Caesar, Bankiti, Lang, et al., "nuScenes: A Multimodal Dataset for Autonomous Driving", CVPR 2020
