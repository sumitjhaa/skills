# 08.22 Video Generation

## Learning Objectives
- Understand autoregressive and diffusion-based video generation
- Implement Video Diffusion Models with 3D U-Net
- Apply Make-A-Video and VideoLDM for text-to-video
- Evaluate with FVD and CLIP score

## Autoregressive Models

### PixelRNN/PixelCNN (Video Extension)
Generate each pixel conditioned on previous pixels and past frames:

$$p(x_t | x_{<t}, x_{1:t-1}) = \prod_{i,j} p(x_t^{i,j} | x_t^{<i,<j}, x_{1:t-1})$$

### Video Transformer (VideoGPT)
Tokenise video with VQ-VAE → autoregressive transformer over tokens.

## Video Diffusion Models (VDM)

### Forward Process
Add Gaussian noise over spacetime:

$$q(z_t | z_0) = \mathcal{N}(z_t; \sqrt{\bar{\alpha}_t} z_0, (1 - \bar{\alpha}_t) I)$$

### Reverse Process
Jointly denoise all frames with 3D U-Net:

$$p_\theta(z_{t-1} | z_t) = \mathcal{N}(z_{t-1}; \mu_\theta(z_t, t), \Sigma_\theta(z_t, t))$$

### 3D U-Net Architecture
```
Input (T×H×W×C) → 3D Conv ↓ → 3D ResBlock × N → Bottleneck → 3D ResBlock × N → 3D Conv ↑ → Output
```

Temporal attention inserted between spatial attention blocks.

## Make-A-Video

### Three-Stage Pipeline
1. **Text-to-image prior**: Map text embedding to image embedding (same as DALL-E 2)
2. **Spatio-temporal decoder**: Image diffusion model + temporal layers (inflated from image)
3. **Frame interpolation**: Generate intermediate frames for higher FPS

### Super-Resolution
- Spatial SR: 64 px → 256 px
- Temporal SR: Interpolation network for 2× frame count

## VideoLDM (Latent Diffusion)

### 3D Autoencoder
Encode video to latent space:

$$z = \mathcal{E}(x_{1:T}), \quad \hat{x}_{1:T} = \mathcal{D}(z)$$

Temporal compression via 3D convolutions in encoder/decoder.

### Temporal Attention
In denoising U-Net, add self-attention across time dimension:

```python
# Spatial: attend over H×W within each frame
# Temporal: attend over T for each spatial position
x = spatial_attention(x)   # (B*T, N, D)
x = x.permute(0,2,1,3)     # (B, N, T, D)
x = temporal_attention(x)  # attend over T
```

## Consistency Techniques

### Noise Sharing
Use same noise map across frames (except motion-specific):

$$z_T^{(i)} = z_T^{(0)} + \delta^{(i)}$$

### Optical Flow Warping
Warp generated frames using optical flow for temporal smoothness.

## Evaluation: FVD (Fréchet Video Distance)

### Computation
$$\text{FVD} = \|\mu_r - \mu_g\|_2^2 + \text{Tr}(\Sigma_r + \Sigma_g - 2(\Sigma_r \Sigma_g)^{1/2})$$

- Features from I3D network (pre-trained on Kinetics)
- Captures both frame quality and temporal consistency

## Code: Temporal Attention Mask

```python
import torch
import torch.nn as nn

class TemporalAttention(nn.Module):
    def __init__(self, dim, num_heads=8):
        super().__init__()
        self.num_heads = num_heads
        self.scale = (dim // num_heads) ** -0.5
        self.qkv = nn.Linear(dim, dim * 3)
        self.proj = nn.Linear(dim, dim)

    def forward(self, x):
        B, T, N, D = x.shape
        x = x.reshape(B * T, N, D)  # merge batch + time
        qkv = self.qkv(x).reshape(B * T, N, 3, self.num_heads, -1)
        q, k, v = qkv.permute(2, 0, 3, 1, 4).unbind(0)
        attn = (q @ k.transpose(-2, -1)) * self.scale
        x = (attn.softmax(-1) @ v).transpose(1, 2).reshape(B * T, N, -1)
        x = self.proj(x).reshape(B, T, N, D)
        return x
```

## Video Generation Benchmarks

| Model | Resolution | Upsampling Steps | FVD ↓ (UCF101) | Parameters |
|-------|-----------|-----------------|----------------|-----------|
| Video Diffusion | 64×64 | No | 270 | 3B |
| Make-A-Video | 256×256 | 2-stage | 367 | 2.2B |
| VideoLDM | 256×256 | No | 246 | 1.7B |
| Gen-2 (Runway) | 768×432 | — | — | Proprietary |
| Sora (OpenAI) | 1920×1080 | — | — | Proprietary |

## Practical Considerations
- **Temporal flickering**: Use temporal attention + noise sharing + optical flow loss
- **Motion magnitude**: Small motions are harder to learn; increase temporal resolution
- **Text alignment**: Classifier-free guidance works for video (scale=7-12)
- **Long videos**: Autoregressive generation over chunks with conditioning

## References
- Ho, Salimans, et al., "Video Diffusion Models", NeurIPS 2022
- Singer, Polyak, et al., "Make-A-Video: Text-to-Video Generation without Text-Video Data", NeurIPS 2022
- Blattmann, Dockhorn, et al., "Align your Latents: High-Resolution Video Synthesis with Latent Diffusion Models", CVPR 2023
- Yan, Zhang, et al., "VideoGPT: Video Generation using VQ-VAE and Transformers", 2021
- Unterthiner, van Steenkiste, et al., "Towards Accurate Generative Models of Video: A New Metric and Challenges", 2018
