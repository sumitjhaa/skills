# 08.25 Medical Imaging

## Learning Objectives
- Understand imaging modalities (X-ray, CT, MRI, ultrasound, histopathology)
- Implement U-Net for medical image segmentation
- Apply nnU-Net for self-configuring segmentation pipelines
- Analyze detection and classification tasks (CheXNet, EyePACS)

## Imaging Modalities

### X-ray
- 2D projection radiography
- Attenuation based on tissue density (bone = white, air = black)
- Common: Chest X-ray (CXR), mammography, bone X-ray

### CT (Computed Tomography)
- 3D volume from multiple X-ray projections (180-360°)
- Hounsfield Units (HU): -1000 (air), 0 (water), +1000 (bone)
- Window/level adjustment for viewing different tissues:
  - Lung window: W=1500, L=-500
  - Soft tissue window: W=400, L=40
  - Bone window: W=1500, L=300

### MRI (Magnetic Resonance Imaging)
- Multiple sequences with different contrast:
  - **T1-weighted**: Fat bright, water dark (anatomy)
  - **T2-weighted**: Water bright, fat dark (pathology)
  - **FLAIR**: Suppresses CSF, highlights periventricular lesions
  - **DWI**: Measures water diffusion (stroke detection)

### Ultrasound
- Real-time, no radiation
- Speckle noise, operator-dependent
- Common: Obstetrics, cardiology, abdominal

### Histopathology
- Whole-slide images (WSI): Gigapixel resolution (100K×100K+)
- Staining: H&E (Hematoxylin & Eosin) — standard
- Immunohistochemistry (IHC): Protein-specific markers

## Segmentation: U-Net

### Architecture
```
Encoder (down):
Conv(3×3) → ReLU → Conv(3×3) → ReLU → MaxPool(2×2) → ...
Decoder (up):
UpConv(2×2) → Concat(skip) → Conv(3×3) → ReLU → Conv(3×3) → ReLU → ...
Final: Conv(1×1) → sigmoid/softmax
```

### 3D U-Net
Replace 2D conv/pool with 3D for volumetric data (CT/MRI).

### Attention U-Net
Add attention gates at skip connections:

$$\alpha = \sigma(\text{Conv}(\text{ReLU}(\text{Conv}(x) + \text{Conv}(g))))$$

### nnU-Net (No New U-Net)
Self-configuring pipeline:
- Automatically determines architecture (2D, 3D, or cascade)
- Heuristic-based pre-processing (resampling, normalisation)
- Ensemble of 2D + 3D U-Nets via majority voting

## Detection & Classification

### CheXNet
DenseNet-121 trained on ChestX-ray14:
- 112,120 frontal-view chest X-rays
- 14 disease labels (atelectasis, cardiomegaly, effusion, etc.)
- AUC > 0.98 for cardiomegaly

### EyePACS
Diabetic retinopathy detection from retinal fundus images:
- 88,702 images
- 5-class grading (0: no DR — 4: proliferative DR)
- Deep learning matches ophthalmologist performance

### COVID-19 Detection
- Chest X-ray/CT for COVID-19 pneumonia
- Challenges: dataset size, domain shift across hospitals

## Registration (Image Alignment)

### Types
1. **Rigid**: 6 DOF (3 rotation + 3 translation)
2. **Affine**: 12 DOF (rotation, translation, scaling, shear)
3. **Deformable/Non-rigid**: Per-voxel displacement field

### Loss Functions
- **Mutual Information (MI)**: For multi-modal registration (CT→MR)
  $$MI(A, B) = H(A) + H(B) - H(A, B)$$
- **Normalised Cross-Correlation (NCC)**: For same modality
- **Dice loss**: For segmentation-based registration

### VoxelMorph (Learning-Based)
CNN predicts deformation field directly:

$$\phi = f_\theta(I, J)$$

## Code: 3D U-Net Block

```python
import torch
import torch.nn as nn

class UNet3D(nn.Module):
    def __init__(self, in_channels=1, out_channels=3):
        super().__init__()
        self.enc1 = self.conv_block(in_channels, 32)
        self.enc2 = self.conv_block(32, 64)
        self.enc3 = self.conv_block(64, 128)
        self.bottleneck = self.conv_block(128, 256)
        self.dec3 = self.upconv_block(256, 128)
        self.dec2 = self.upconv_block(128, 64)
        self.dec1 = self.upconv_block(64, 32)
        self.final = nn.Conv3d(32, out_channels, 1)

    def conv_block(self, in_c, out_c):
        return nn.Sequential(
            nn.Conv3d(in_c, out_c, 3, padding=1), nn.InstanceNorm3d(out_c), nn.ReLU(),
            nn.Conv3d(out_c, out_c, 3, padding=1), nn.InstanceNorm3d(out_c), nn.ReLU(),
        )

    def upconv_block(self, in_c, out_c):
        return nn.Sequential(
            nn.Upsample(scale_factor=2),
            nn.Conv3d(in_c, out_c, 3, padding=1), nn.InstanceNorm3d(out_c), nn.ReLU(),
        )

    def forward(self, x):
        e1 = self.enc1(x)
        e2 = self.enc2(nn.MaxPool3d(2)(e1))
        e3 = self.enc3(nn.MaxPool3d(2)(e2))
        b = self.bottleneck(nn.MaxPool3d(2)(e3))
        d3 = self.dec3(b)
        d3 = torch.cat([d3, e3], dim=1)
        d2 = self.dec2(d3)
        d2 = torch.cat([d2, e2], dim=1)
        d1 = self.dec1(d2)
        d1 = torch.cat([d1, e1], dim=1)
        return self.final(d1)
```

## Challenges in Medical Imaging
- **Data scarcity**: Annotated medical images are expensive to obtain
- **Class imbalance**: Pathology is rare (e.g., 1% pneumonia vs 99% normal)
- **Domain shift**: Different hospitals, scanners, protocols
- **Regulation**: FDA clearance required for clinical deployment
- **Interpretability**: Clinicians need explainable predictions

## References
- Ronneberger, Fischer, Brox, "U-Net: Convolutional Networks for Biomedical Image Segmentation", MICCAI 2015
- Çiçek, Abdulkadir, Lienkamp, Brox, Ronneberger, "3D U-Net: Learning Dense Volumetric Segmentation from Sparse Annotation", MICCAI 2016
- Isensee, Jaeger, Kohl, Petersen, Maier-Hein, "nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation", Nature Methods 2021
- Rajpurkar, Irvin, et al., "CheXNet: Radiologist-Level Pneumonia Detection on Chest X-Rays with Deep Learning", 2017
- Balakrishnan, Zhao, Sabuncu, Guttag, Dalca, "VoxelMorph: A Learning Framework for Deformable Medical Image Registration", TMI 2019
