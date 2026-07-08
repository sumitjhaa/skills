# 08.23 Image-to-Image Translation

## Learning Objectives
- Understand conditional GANs for paired image translation
- Implement CycleGAN for unpaired translation
- Apply diffusion-based translation (InstructPix2Pix, Palette)
- Evaluate with FID, LPIPS, and user studies

## Pix2Pix (Paired Translation)

### Conditional GAN
Generator $G$ takes input image $x$ + noise $z$ → output $\hat{y}$:

$$\mathcal{L}_{cGAN}(G, D) = \mathbb{E}_{x,y}[\log D(x, y)] + \mathbb{E}_{x,z}[\log(1 - D(x, G(x, z)))]$$

### L1 Loss (Encourages sharp results)
$$\mathcal{L}_{L1}(G) = \mathbb{E}_{x,y,z}[\|y - G(x, z)\|_1]$$

### Final Objective
$$G^* = \arg\min_G \max_D \mathcal{L}_{cGAN}(G, D) + \lambda \mathcal{L}_{L1}(G)$$

### U-Net Generator
- Encoder → bottleneck → decoder with skip connections
- Skip connections preserve spatial details

### PatchGAN Discriminator
- Classify $N \times N$ patches as real/fake (not whole image)
- Patch size 70×70 balances quality vs computation

## CycleGAN (Unpaired Translation)

### Cycle-Consistency Loss
Forward translation $G: X \to Y$, backward $F: Y \to X$:

$$\mathcal{L}_{\text{cycle}}(G, F) = \mathbb{E}_{x \sim X}[\|F(G(x)) - x\|_1] + \mathbb{E}_{y \sim Y}[\|G(F(y)) - y\|_1]$$

### Full Objective
$$\mathcal{L}(G, F, D_X, D_Y) = \mathcal{L}_{\text{GAN}}(G, D_Y, X, Y) + \mathcal{L}_{\text{GAN}}(F, D_X, Y, X) + \lambda \mathcal{L}_{\text{cycle}}(G, F)$$

### Identity Loss (Optional)
$$\mathcal{L}_{\text{id}}(G, F) = \mathbb{E}_{y \sim Y}[\|G(y) - y\|_1] + \mathbb{E}_{x \sim X}[\|F(x) - x\|_1]$$

### Applications
- Season transfer (summer ↔ winter)
- Style transfer (photo ↔ Monet)
- Animal morphing (zebra ↔ horse)

## Diffusion-Based Translation

### Palette
Conditional diffusion model for multiple tasks with same architecture:

$$p(x_t | x_{t-1}, c) = \mathcal{N}(x_t; \mu_\theta(x_{t-1}, t, c), \Sigma_\theta(x_{t-1}, t, c))$$

Tasks: colorization, inpainting, uncropping, JPEG restoration.

### InstructPix2Pix
Edit images using language instructions:

1. **Dataset**: GPT-3 generates editing instructions → Prompt-to-Prompt generates before/after pairs
2. **Conditioning**: Input image $c_I$ + editing instruction $c_T$
3. **Architecture**: Stable Diffusion with extra input channel for $c_I$

$$\epsilon_\theta(z_t, t, c_I, c_T)$$

### ControlNet
Add spatial control (edges, poses, depth) to pretrained diffusion models:

- Trainable copy of encoder layers
- Zero convolution connections (initialised to 0)
- Preserves original model weights

## Code: CycleGAN Generator Block

```python
import torch
import torch.nn as nn

class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.net = nn.Sequential(
            nn.ReflectionPad2d(1),
            nn.Conv2d(channels, channels, 3),
            nn.InstanceNorm2d(channels),
            nn.ReLU(True),
            nn.ReflectionPad2d(1),
            nn.Conv2d(channels, channels, 3),
            nn.InstanceNorm2d(channels),
        )

    def forward(self, x):
        return x + self.net(x)

class ResNetGenerator(nn.Module):
    def __init__(self, in_channels=3, out_channels=3, n_res=9):
        super().__init__()
        model = [
            nn.ReflectionPad2d(3),
            nn.Conv2d(in_channels, 64, 7), nn.InstanceNorm2d(64), nn.ReLU(True),
            nn.Conv2d(64, 128, 3, stride=2, padding=1), nn.InstanceNorm2d(128), nn.ReLU(True),
            nn.Conv2d(128, 256, 3, stride=2, padding=1), nn.InstanceNorm2d(256), nn.ReLU(True),
        ]
        model += [ResidualBlock(256) for _ in range(n_res)]
        model += [
            nn.Upsample(scale_factor=2),
            nn.Conv2d(256, 128, 3, padding=1), nn.InstanceNorm2d(128), nn.ReLU(True),
            nn.Upsample(scale_factor=2),
            nn.Conv2d(128, 64, 3, padding=1), nn.InstanceNorm2d(64), nn.ReLU(True),
            nn.ReflectionPad2d(3),
            nn.Conv2d(64, out_channels, 7),
            nn.Tanh(),
        ]
        self.model = nn.Sequential(*model)

    def forward(self, x):
        return self.model(x)
```

## Evaluation

| Metric | What it Measures | Pix2Pix | CycleGAN |
|--------|-----------------|---------|----------|
| FID | Distributional similarity (realism) | 25.3 (edges→shoes) | 48.9 (photo→Monet) |
| LPIPS | Perceptual similarity to ground truth | 0.12 | N/A (no GT) |
| User study | Human preference | 78% | 65% |
| KID | Similar to FID, unbiased | 0.015 | 0.032 |

## Practical Considerations
- **Mode collapse**: GAN training can collapse — use spectral normalisation
- **Patch size**: Larger patches = more global consistency but more computation
- **Paired vs unpaired**: Paired is better when available; unpaired relies on cycle consistency
- **Identity loss**: Prevents unnecessary colour/gender changes (e.g., person's photorealistic face becoming anime)

## References
- Isola, Zhu, Zhou, Efros, "Image-to-Image Translation with Conditional Adversarial Networks", CVPR 2017
- Zhu, Park, Isola, Efros, "Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks", ICCV 2017
- Saharia, Chan, et al., "Palette: Image-to-Image Diffusion Models", SIGGRAPH 2022
- Brooks, Holynski, Efros, "InstructPix2Pix: Learning to Follow Image Editing Instructions", CVPR 2023
- Zhang, Rao, Agrawala, "Adding Conditional Control to Text-to-Image Diffusion Models (ControlNet)", ICCV 2023
