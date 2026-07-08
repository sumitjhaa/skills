# Lesson 08.18: Point Cloud Processing

## Learning Objectives
- Understand point cloud representations and challenges
- Implement PointNet for classification and segmentation
- Apply PointNet++ hierarchical feature learning
- Analyze 3D registration with ICP

## Representations

### Point Cloud
$$P = \{p_1, \dots, p_N\}, \quad p_i \in \mathbb{R}^3$$

- Unordered, sparse, possibly varying density
- Lacks topology information

### Voxel Grid
$$V \in \mathbb{R}^{D \times H \times W}$$

- Regular structure (compatible with 3D conv)
- Memory: $O(N^3)$ — impractical at high resolution
- Sparse voxels: Only store occupied voxels (MinkowskiEngine)

### Octree
- Adaptive hierarchical subdivision
- Efficient for sparse scenes
- Used in O-CNN, OctFormer

## PointNet

### Permutation Invariance
$$f(x_1, \dots, x_n) = \gamma \left( \max_{i=1,\dots,n} h(x_i) \right)$$

- $h$: MLP (shared per point)
- $\max$: Symmetric function (max pooling)
- $\gamma$: MLP for global feature

### T-Net (Spatial Transformer)
Predict affine transformation matrix to align point cloud:

$$T = \text{MLP}(global\_features) \in \mathbb{R}^{3 \times 3} \ (\text{or } \mathbb{R}^{64 \times 64})$$

### Architecture for Classification
```
Input (N×3) → T-Net (3×3) → MLP(64,64) → T-Net (64×64) → MLP(64,128,1024) → MaxPool → MLP(512,256,k)
```

### Architecture for Segmentation
```
Per-point features (N×1088) = concat[local (N×64), global (1×1024) repeated N] → MLP(512,256,128,m)
```

## PointNet++

### Hierarchical Feature Learning
```
Set Abstraction Level 1: FPS (N→N/4) → Ball query (r=0.2) → PointNet → (N/4, C1)
Set Abstraction Level 2: FPS (N/4→N/16) → Ball query (r=0.4) → PointNet → (N/16, C2)
```

### Farthest Point Sampling (FPS)
```
Select first point randomly
for _ in range(k):
    select point farthest from all selected points
```

### Ball Query vs KNN
| Method | Selection | Density Invariance |
|--------|-----------|-------------------|
| Ball query | All points within radius | Adaptive #neighbors |
| KNN | Fixed K neighbors | Varies region size |

### Multi-Scale Grouping (MSG)
Combine features from multiple ball query radii:

$$f_{\text{combined}} = \text{concat}(f_{r_1}, f_{r_2}, f_{r_3})$$

## ICP (Iterative Closest Point)

### Algorithm
```
while not converged:
    for each point in source:
        find nearest neighbor in target
    compute (R, t) minimizing sum of squared distances
    apply transform to source
```

### Point-to-Point ICP
$$\min_{R,t} \sum_i \|R p_i + t - q_i\|^2$$

- Closed-form solution via SVD

### Point-to-Plane ICP
$$\min_{R,t} \sum_i \|(R p_i + t - q_i) \cdot n_i\|^2$$

- Faster convergence for smooth surfaces

## Code: PointNet Classification

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class PointNet(nn.Module):
    def __init__(self, num_classes=40):
        super().__init__()
        self.mlp1 = nn.Sequential(
            nn.Conv1d(3, 64, 1), nn.BatchNorm1d(64), nn.ReLU(),
            nn.Conv1d(64, 64, 1), nn.BatchNorm1d(64), nn.ReLU(),
        )
        self.mlp2 = nn.Sequential(
            nn.Conv1d(64, 64, 1), nn.BatchNorm1d(64), nn.ReLU(),
            nn.Conv1d(64, 128, 1), nn.BatchNorm1d(128), nn.ReLU(),
            nn.Conv1d(128, 1024, 1), nn.BatchNorm1d(1024), nn.ReLU(),
        )
        self.fc = nn.Sequential(
            nn.Linear(1024, 512), nn.BatchNorm1d(512), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(512, 256), nn.BatchNorm1d(256), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(256, num_classes),
        )

    def forward(self, x):
        # x: (B, 3, N)
        x = self.mlp1(x)
        x = self.mlp2(x)
        x = F.max_pool1d(x, x.shape[-1]).squeeze(-1)  # (B, 1024)
        return self.fc(x)
```

## Point Cloud Benchmarks

| Dataset | Task | Metrics | Size |
|---------|------|---------|------|
| ModelNet40 | Classification | Acc (90.2%) | 12K CAD models |
| ShapeNet | Segmentation | mIoU (85.5%) | 16K shapes |
| S3DIS | Indoor segmentation | mIoU (76.2%) | 6 indoor areas |
| KITTI | 3D detection | AP (82.4% BEV) | 7.5K scenes |
| ScanNet | 3D segmentation | mIoU (72.1%) | 1.5K scans |

## Practical Considerations
- **Normalization**: Center and scale point cloud to unit sphere
- **Augmentation**: Random rotation (z-axis), jitter, scaling, dropout
- **Density**: Varying density handled by ball query (PointNet++) or FPS
- **Color**: Include RGB as additional per-point features (6D input)
- **Memory**: Point clouds are sparse — use sparse convolution for large scenes

## References
- Qi, Su, Mo, Guibas, "PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation", CVPR 2017
- Qi, Yi, Su, Guibas, "PointNet++: Deep Hierarchical Feature Learning on Point Sets in a Metric Space", NeurIPS 2017
- Choy, Gwak, Savarese, "4D Spatio-Temporal ConvNets: Minkowski Convolutional Neural Networks", CVPR 2019
- Besl & McKay, "A Method for Registration of 3-D Shapes (ICP)", TPAMI 1992
- Maturana & Scherer, "VoxNet: A 3D Convolutional Neural Network for real-time object recognition", IROS 2015
