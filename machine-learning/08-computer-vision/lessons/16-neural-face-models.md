# Lesson 08.16: Neural Face Models

## Learning Objectives
- Understand 3D Morphable Models (3DMM) for face
- Implement FLAME face model with blendshapes
- Apply GAN inversion for real face editing
- Analyze face reenactment with FOMM and MegaPortraits

## 3D Morphable Model (3DMM)

### Face Shape and Texture
PCA-based model from 200+ 3D face scans:

$$S = \bar{S} + A_{\text{shape}} \alpha, \quad \alpha \in \mathbb{R}^{199}$$

$$T = \bar{T} + A_{\text{tex}} \beta, \quad \beta \in \mathbb{R}^{199}$$

- $\bar{S}$: mean shape (vertices)
- $A_{\text{shape}}$: shape PCA components
- $\bar{T}$: mean texture (RGB per vertex)
- $A_{\text{tex}}$: texture PCA components

### Rendering Pipeline
1. Shape + texture parameters → 3D mesh
2. Camera parameters (R, t, f) → 2D projection
3. Illumination model (Phong) → final image

### Basel Face Model (BFM)
Standard 3DMM with ~50K vertices.

## FLAME (Faces Learned with an Articulated Model and Expressions)

### Model
$$M(\beta, \theta, \psi) = \text{LBS}(T_P(\beta, \theta, \psi), J(\beta), \theta, W)$$

- $\beta$: shape (300 components)
- $\theta$: pose (jaw, neck, eye balls — axis-angle)
- $\psi$: expression (100 blendshapes)

### Blend Shapes
$$T_P(\beta, \theta, \psi) = \bar{T} + B_S(\beta) + B_P(\theta) + B_E(\psi)$$

- $B_S$: shape blendshapes
- $B_P$: pose blendshapes (corrective for joint rotation)
- $B_E$: expression blendshapes (from FaceWarehouse)

### Landmark Fitting
FLAME has 68 face landmarks for fitting to images.

## StyleGAN for Faces

### Architecture
Mapping network $f: \mathcal{Z} \to \mathcal{W}$ + Synthesis network:

$$
\begin{aligned}
z &\in \mathcal{Z} \sim \mathcal{N}(0, I) \to w \in \mathcal{W} \\
w &\to \text{AdaIN} \to \text{Synthesis}(\text{Conv} \to \text{AdaIN} \to \text{Noise}) \\
\end{aligned}
$$

### StyleCLIP
Edit face images via text prompts:
1. **Latent optimization**: $w^* = \arg\min_w \|F(w) - t_{\text{CLIP}}\|_2^2$
2. **Global direction**: Find direction $\Delta w$ in StyleGAN space corresponding to text
3. **Mapper network**: Learn text → $\Delta w$ mapping

## GAN Inversion

### Encoder-Based
$$w = E(x)$$

- e4e (encoder for editing): Train encoder mapping image to $\mathcal{W}+$ space
- Restyle encoder: Iterative refinement

### Optimization-Based
$$w^* = \arg\min_w \|G(w) - x\|_2^2 + \lambda_{\text{LPIPS}} \cdot \text{LPIPS}(G(w), x)$$

- Slower but potentially more accurate
- Regularize with $w$ in $\mathcal{W}+$ (18 separate $w$ vectors, one per layer)

## Face Reenactment

### FOMM (First Order Motion Model)
Self-supervised keypoint detection + motion transfer:

1. **Keypoint detector**: Predict sparse keypoints on source and driving face
2. **Motion prediction**: Compute optical flow from keypoint differences
3. **Occlusion-aware**: Predict which parts are visible
4. **Generator**: Warp source features using predicted flow

### MegaPortraits
High-resolution face reenactment with:
- 3D-aware face representation
- Separate identity and expression codes
- Mega-tracker for temporal consistency

## Code: 3DMM Fitting

```python
import torch
import torch.nn as nn

class FaceFittingLoss(nn.Module):
    def __init__(self, landmark_indices):
        super().__init__()
        self.landmark_indices = landmark_indices  # indices of 68 landmarks

    def forward(self, shape_params, tex_params, camera, landmarks_2d):
        # shape_params: (B, 199), tex_params: (B, 199)
        # camera: (B, 6) = [R_axis_angle, t, f]
        # landmarks_2d: (B, 68, 2)
        
        # Build mesh from PCA
        shape = self.mean_shape + self.shape_pca @ shape_params.T
        shape = shape.T.view(-1, 50_000, 3)
        
        # Project landmarks
        landmarks_3d = shape[:, self.landmark_indices]
        landmarks_proj = self.project(landmarks_3d, camera)
        
        # Landmark loss
        landmark_loss = ((landmarks_proj - landmarks_2d) ** 2).sum(dim=-1).mean()
        
        # Regularization
        shape_reg = (shape_params ** 2).sum() * 3e-5
        tex_reg = (tex_params ** 2).sum() * 3e-5
        
        return landmark_loss + shape_reg + tex_reg
```

## Evaluation Metrics
| Metric | What it Measures |
|--------|-----------------|
| Identity preservation | Cosine similarity of ArcFace embeddings |
| Expression accuracy | Landmark distance between source and reenacted |
| Pose accuracy | Head orientation error |
| FID | Image quality (realism) |
| LPIPS | Perceptual similarity |
| CSIM | Cosine similarity for identity preservation |

## Practical Considerations
- **Tracking**: Face tracking in video requires temporal smoothness regularization
- **Occlusion**: Facial hair, glasses, and hands cause fitting artifacts
- **Lighting**: 3DMM lighting model assumes Lambertian + spherical harmonics
- **Expression transfer**: Identity-independent expression transfer requires decoupling

## References
- Paysan, Knothe, Amberg, Romdhani, Vetter, "A 3D Face Model for Pose and Illumination Invariant Face Recognition", AVSS 2009
- Li, Bolkart, Black, "FLAME: Learning a lightweight 3D face model from large-scale data", ACM Trans. Graphics 2017
- Karras, Laine, Aila, "A Style-Based Generator Architecture for GANs for Face Generation", CVPR 2019
- Patashnik, Wu, Shechtman, Cohen-Or, Lischinski, "StyleCLIP: Text-Driven Manipulation of StyleGAN Imagery", ICCV 2021
- Siarohin, Lathuiliere, Tulyakov, Ricci, Sebe, "First Order Motion Model for Image Animation", NeurIPS 2019
