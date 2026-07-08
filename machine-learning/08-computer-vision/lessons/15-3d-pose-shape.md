# Lesson 08.15: 3D Pose & Shape

## Learning Objectives
- Understand the SMPL parametric body model
- Implement HMR for human mesh recovery
- Apply temporal models for 4D human (VIBE)
- Analyze 3D pose lift from 2D keypoints

## SMPL Model

### Parameterization
$$M(\beta, \theta, \phi): \mathbb{R}^{|\beta| + |\theta| + |\phi|} \to \mathbb{R}^{6890 \times 3}$$

- $\beta \in \mathbb{R}^{10}$: Shape parameters (PCA coefficients from ~2000 body scans)
- $\theta \in \mathbb{R}^{72}$: Pose parameters (3 axis-angle rotations × 24 joints)
- $\phi \in \mathbb{R}^3$: Global translation

### Pose Blend Shapes
$$B_P(\theta) = \sum_{i=1}^{9K} (R_n(\theta) - R_n(\theta^*)) \cdot P_n$$

- $R_n(\theta) \in \mathbb{R}^{24 \times 3 \times 3}$: Joint rotation matrices
- $\theta^*$: Zero pose (T-pose)
- $P_n$: Corrective pose blend shapes

### Shape Blend Shapes
$$B_S(\beta) = \sum_{i=1}^{|\beta|} \beta_i \cdot S_i$$

- $S_i$: Shape components (from PCA of body shapes)

### Skinning
Linear blend skinning (LBS) with learned weights $W \in \mathbb{R}^{6890 \times 24}$:

$$\bar{T}(\beta, \theta) = \bar{T}_\mu + B_S(\beta) + B_P(\theta)$$
$$M(\beta, \theta, \phi) = \text{LBS}(\bar{T}(\beta, \theta), J(\beta), \theta, W)$$

## HMR (Human Mesh Recovery)

### Architecture
```
Image → Encoder (ResNet) → Iterative 3D regression → SMPL parameters → 3D mesh
```

### Regression Head
- 3 fully connected layers
- Predicts $\Theta = \{\beta, \theta, \phi, R, t\}$
- Camera parameters: $R$ (rotation), $t$ (translation), $s$ (scale)

### Reprojection Loss
Project 3D joints to 2D using weak-perspective camera:

$$J_{2D} = s \cdot \Pi(R \cdot J_{3D}) + t$$

- $\Pi$: orthographic projection (X, Y only)
- Loss: MSE between projected and detected 2D keypoints

### Loss Functions
$$\mathcal{L} = \mathcal{L}_{2D} + \lambda_{3D} \mathcal{L}_{3D} + \lambda_{\beta} \mathcal{L}_{\beta} + \lambda_{\theta} \mathcal{L}_{\theta} + \lambda_{\text{sm}} \mathcal{L}_{\text{sm}}$$

- $\mathcal{L}_{2D}$: 2D reprojection error
- $\mathcal{L}_{3D}$: 3D joint error (if 3D GT available)
- $\mathcal{L}_{\beta}$: Shape prior (Gaussian)
- $\mathcal{L}_{\theta}$: Pose prior (from MoCap data)
- $\mathcal{L}_{\text{sm}}$: Smoothness (for video)

## VIBE (Video Inference for Body Pose and Shape Estimation)

### Temporal Encoder
```
Frame features (ResNet) → GRU → Temporal features → SMPL head → Per-frame 3D mesh
```

### Discriminator
GRU-based discriminator distinguishes:
- Real: Sequences from AMASS (MoCap dataset)
- Fake: Generated sequences from VIBE

**Adversarial loss** ensures temporal coherence:

$$\mathcal{L}_{\text{adv}} = \mathbb{E}[\log D(\Theta_{\text{real}})] + \mathbb{E}[\log(1 - D(\Theta_{\text{gen}}))]$$

## Code: SMPL Parameter Regression

```python
import torch
import torch.nn as nn

class SMPLHead(nn.Module):
    def __init__(self, feature_dim=2048, n_smpl_betas=10, n_smpl_thetas=72):
        super().__init__()
        self.regressor = nn.Sequential(
            nn.Linear(feature_dim, 1024),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(1024, 1024),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(1024, n_smpl_betas + n_smpl_thetas + 3 + 3 + 1),
            # betas, thetas, camera_rot, camera_trans, camera_scale
        )

    def forward(self, features):
        params = self.regressor(features)
        betas = params[:, :10]
        thetas = params[:, 10:82]
        camera = params[:, 82:]
        return betas, thetas, camera
```

## 3D Pose Lifting

### 2D-to-3D Lifting
$$J_{3D} = \text{MLP}(J_{2D})$$

- **Simple**: MLP from 2D keypoints to 3D coordinates
- **Temporal**: Use 2D keypoint sequence → per-frame 3D pose (VideoPose3D)
- **Semi-supervised**: 2D keypoints from detector, 3D from limited MoCap data

## Evaluation Metrics

| Metric | Formula | Units |
|--------|---------|-------|
| MPJPE | $\frac{1}{N} \sum \|J_{3D} - J_{3D}^*\|_2$ | mm |
| PA-MPJPE | Procrustes-aligned MPJPE | mm |
| PVE | $\frac{1}{V} \sum \|V - V^*\|_2$ (vertex error) | mm |

## Practical Considerations
- **Camera model**: Weak-perspective for HMR, perspective for full accuracy
- **Data augmentation**: Random rotation, scaling, flipping for 2D detections
- **Initialization**: HMR initializes from 2D keypoints; start with high learning rate
- **Multiple people**: Detect person → crop → estimate single person mesh
- **Hands/face**: SMPL-X extends SMPL with hands+face articulation

## References
- Loper, Mahmood, Romero, Pons-Moll, Black, "SMPL: A Skinned Multi-Person Linear Model", ACM Trans. Graphics 2015
- Kanazawa, Black, Jacobs, Malik, "End-to-end Recovery of Human Shape and Pose (HMR)", CVPR 2018
- Kocabas, Athanasiou, Black, "VIBE: Video Inference for Human Body Pose and Shape Estimation", CVPR 2020
- Pavllo, Feichtenhofer, Grangier, Auli, "3D Human Pose Estimation in Video with Temporal Convolutions and Semi-Supervised Training (VideoPose3D)", CVPR 2019
- Martinez, Hossain, Romero, Little, "A Simple Yet Effective Baseline for 3D Human Pose Estimation", ICCV 2017
