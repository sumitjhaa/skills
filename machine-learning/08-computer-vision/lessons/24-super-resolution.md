# 08.24 Super-Resolution

## Learning Objectives
- Understand classical (SRCNN) and generative (SRGAN) super-resolution
- Implement SwinIR with Swin Transformer blocks
- Apply diffusion-based super-resolution (SR3)
- Evaluate with PSNR, SSIM, LPIPS

## SRCNN

### Pipeline
```mermaid
Low-res input → Bicubic upsampling → Patch extraction → Non-linear mapping → Reconstruction → High-res output
```

### Architecture
1. **Patch extraction**: $f_1 \times f_1$ conv, $n_1$ filters
2. **Non-linear mapping**: $1 \times 1$ conv, $n_2$ filters
3. **Reconstruction**: $f_3 \times f_3$ conv, 3 filters

### Training
$$\mathcal{L} = \frac{1}{N} \sum_{i=1}^N \|F(Y_i; \Theta) - X_i\|_2^2$$

- $Y_i$: bicubic upsampled input
- $X_i$: ground truth high-res
- Dataset: 91 images (ImageNet patches)

### Limitations
- Simple 3-layer network limits capacity
- Bicubic upsampling introduces artifacts before learning

## SRGAN

### Generator
Residual blocks (16×) + sub-pixel convolution (pixel shuffle):

$$I^{\text{SR}} = G(I^{\text{LR}}; \theta_G)$$

### Discriminator
Standard 2D CNN classifying real vs generated SR images.

### Perceptual Loss
$$\mathcal{L}^{\text{SR}} = \mathcal{L}_{\text{MSE}} + \lambda \mathcal{L}_VGG + \eta \mathcal{L}_{\text{adv}}$$

- $\mathcal{L}_{VGG} = \frac{1}{N} \|\phi(I^{\text{HR}}) - \phi(I^{\text{SR}})\|_2^2$
- $\phi$: VGG-19 feature maps (layer conv5_4)

### ESRGAN (Enhanced SRGAN)
- **RRDB**: Residual-in-Residual Dense Block (dense connections within residual)
- **Relativistic discriminator**: $D(x_r, x_f) = \sigma(C(x_r) - \mathbb{E}[C(x_f)])$
- **Perceptual loss**: Use features before activation

## SwinIR

### Architecture
```
Low-res → Shallow feature extraction (Conv) → Deep feature extraction (Swin Transformer blocks) → Reconstruction (Upsample + Conv) → High-res
```

### Swin Transformer Block
- W-MSA (Window Multi-head Self-Attention)
- SW-MSA (Shifted Window MSA)
- Residual connection + LayerNorm

### Three Variants
| Variant | Use | Blocks | Channels |
|---------|-----|--------|----------|
| Lightweight | Real-world SR | 4 | 60 |
| Standard | Classical SR | 6 | 180 |
| Large | High quality | 6 | 180 (bigger MLP) |

## Diffusion-Based (SR3)

### Forward Process
Corrupt high-res $x_0$ to noise $x_T$ conditioned on low-res $y$:

$$q(x_t | x_0) = \mathcal{N}(x_t; \sqrt{\bar{\alpha}_t} x_0, (1 - \bar{\alpha}_t)I)$$

### Reverse Process
Denoise conditioned on low-res $y$:

$$p_\theta(x_{t-1} | x_t, y) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t, y), \Sigma_\theta(x_t, t, y))$$

### Upsampling
- SR3 achieves 8× upsampling
- Cascaded: 64→256→1024

## Code: Pixel Shuffle (Sub-pixel Conv)

```python
import torch
import torch.nn as nn

class SubPixelConv(nn.Module):
    def __init__(self, in_channels, upscale_factor=2):
        super().__init__()
        self.conv = nn.Conv2d(
            in_channels,
            in_channels * upscale_factor ** 2,
            kernel_size=3, padding=1
        )
        self.shuffle = nn.PixelShuffle(upscale_factor)

    def forward(self, x):
        return self.shuffle(self.conv(x))
        # e.g., (B, C, H, W) → (B, C*r^2, H, W) → (B, C, H*r, W*r)
```

## Evaluation Metrics

### PSNR
$$\text{PSNR} = 10 \cdot \log_{10} \left(\frac{MAX^2}{\text{MSE}}\right)$$

- $MAX = 255$ for 8-bit images
- Higher is better
- Correlates poorly with perceptual quality

### SSIM
$$\text{SSIM}(x, y) = \frac{(2\mu_x\mu_y + C_1)(2\sigma_{xy} + C_2)}{(\mu_x^2 + \mu_y^2 + C_1)(\sigma_x^2 + \sigma_y^2 + C_2)}$$

- Measures luminance, contrast, structure
- Range [-1, 1]

### LPIPS
Learned Perceptual Image Patch Similarity:

$$\text{LPIPS}(x, y) = \sum_l \frac{1}{H_l W_l} \sum_{h,w} \|\phi_l(x) - \phi_l(y)\|_2^2$$

- Lower is more similar
- Uses AlexNet/VGG features (trained on human judgments)

## Benchmark Results

| Method | Set5 (PSNR/SSIM) | Set14 | Urban100 | BSD100 |
|--------|------------------|-------|----------|--------|
| SRCNN | 32.75 / 0.9246 | 29.19 | 26.21 | 28.77 |
| SRGAN | 29.40 / 0.8472 | 26.02 | 24.38 | 25.16 |
| ESRGAN | 30.45 / 0.8659 | 26.28 | 24.33 | 25.49 |
| SwinIR | 32.92 / 0.9344 | 29.09 | 27.45 | 29.12 |
| SR3 | — | — | — | — |

## Practical Considerations
- **PSNR vs perceptual quality**: GAN/diffusion methods have lower PSNR but look better
- **Real-world SR**: Add blur, noise, compression to training data
- **Blind SR**: Estimate degradation kernel during inference
- **Reference-based SR**: Use exemplar images for texture transfer

## References
- Dong, Loy, He, Tang, "Image Super-Resolution Using Deep Convolutional Networks", TPAMI 2016
- Ledig, Theis, et al., "Photo-Realistic Single Image Super-Resolution Using a Generative Adversarial Network", CVPR 2017
- Wang, Yu, et al., "ESRGAN: Enhanced Super-Resolution Generative Adversarial Networks", ECCV 2018
- Liang, Cao, Sun, Zhang, Van Gool, Timofte, "SwinIR: Image Restoration Using Swin Transformer", ICCV 2021
- Saharia, Ho, Chan, et al., "Image Super-Resolution via Iterative Refinement", TPAMI 2022
