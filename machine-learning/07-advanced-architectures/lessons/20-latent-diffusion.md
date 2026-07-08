# Lesson 07.20: Latent Diffusion (LDM, SD, DiT)

## Learning Objectives
- Understand latent diffusion for efficient image generation
- Implement cross-attention for text conditioning
- Apply classifier-free guidance for controlled generation
- Compare UNet-based (SD) with Transformer-based (DiT) diffusion

## Theory
Latent Diffusion Models (LDMs) perform diffusion in compressed latent space:

$$\text{Encoder: } z = \mathcal{E}(x), \quad \text{Decoder: } x' = \mathcal{D}(z)$$

### Perceptual Compression
- VAE encoder downsamples $H \times W \times 3 \to h \times w \times c$ (typically 8x-16x)
- **Loss**: $\mathcal{L}_{\text{VAE}} = \mathcal{L}_{\text{recon}} + \mathcal{L}_{\text{KL}} + \mathcal{L}_{\text{perceptual}}$
- $z$ is a continuous latent variable, not binary

### Why Latent Space?
| Factor | Pixel Space | Latent Space |
|--------|-------------|-------------|
| Dimensions | $256^2 \times 3 = 196K$ | $32^2 \times 4 = 4K$ |
| Compute per step | Very high | Low |
| UNet size | Large | Compact |
| Training cost | 1000+ GPU-days | 150 GPU-days |

## Stable Diffusion Architecture

```
Text → CLIP Text Encoder → text_embeddings
Noise → VAE Encoder → z_t → UNet (cond via cross-attn) → ε_θ → VAE Decoder → image
```

### Cross-Attention in UNet
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^\top}{\sqrt{d}}\right) V$$

- $Q = W_Q \cdot \phi(z_t)$: spatial features
- $K = W_K \cdot \tau_\theta(c)$: text embeddings
- $V = W_V \cdot \tau_\theta(c)$: text embeddings

### UNet Conditioning
Add timestep $t$ via:
- **Positional encoding** (sinusoidal)
- **Cross-attention** with text embeddings
- **Adaptive group norm** (FiLM-like scale/shift)

## Classifier-Free Guidance (CFG)

### Training
Train both conditional and unconditional score:

$$\varepsilon_\theta = \varepsilon_\theta(x_t, t, c) \quad \text{(conditional)}$$
$$\varepsilon_\theta(x_t, t, \varnothing) \quad \text{(unconditional, } c = \varnothing)$$

### Sampling
$$\tilde{\varepsilon}_\theta = \varepsilon_\theta(x_t, t, \varnothing) + w \cdot (\varepsilon_\theta(x_t, t, c) - \varepsilon_\theta(x_t, t, \varnothing))$$

- $w = 1$: standard conditional sampling
- $w > 1$: increased conditioning strength (e.g., $w=7.5$)
- **Trade-off**: Higher $w$ = better alignment, lower diversity

## DiT (Diffusion Transformer)

### Architecture
```
Latent patches → Patchify → Positional encoding → Transformer blocks → Unpatchify → Noise prediction
```

### Transformer Block
```
LayerNorm → Multihead Self-Attention → LayerNorm → MLP (GELU)
```

- **AdaLN**: Adaptive LayerNorm conditioned on timestep: $\text{AdaLN}(h, t) = a_t \cdot \text{LayerNorm}(h) + b_t$
- **Scalability**: DiT scales better with compute than UNet

### DiT vs UNet

| Aspect | UNet (SD) | DiT |
|--------|-----------|-----|
| Scalability | Plateaus | $L$aw of Diminishing Returns | Less plateaus |
| Parameter count | 860M-2.6B | 600M-3B |
| GFLOPs per step | 200-400 | 100-600 |
| Best for | Text-to-image | Class-conditioned |
| MLP design | Gated | Standard |

## Code: LDM Sampling

```python
import torch
import torch.nn as nn

class StableDiffusionSampler:
    def __init__(self, vae, unet, text_encoder, scheduler):
        self.vae = vae
        self.unet = unet
        self.text_encoder = text_encoder
        self.scheduler = scheduler

    @torch.no_grad()
    def sample(self, prompt, guidance_scale=7.5, num_steps=50, seed=None):
        if seed is not None:
            torch.manual_seed(seed)
        
        # Text encoding
        text_emb = self.text_encoder(prompt)  # (1, 77, 768)
        uncond_emb = self.text_encoder("")    # (1, 77, 768)
        text_emb = torch.cat([uncond_emb, text_emb], dim=0)  # (2, 77, 768)
        
        # Initialize latent noise
        z = torch.randn(1, 4, 64, 64)
        self.scheduler.set_timesteps(num_steps)
        
        for t in self.scheduler.timesteps:
            z_in = torch.cat([z] * 2)  # (2, 4, 64, 64) for cfg
            t_in = t.expand(2)
            noise_pred = self.unet(z_in, t_in, text_emb)  # (2, 4, 64, 64)
            noise_pred_uncond, noise_pred_text = noise_pred.chunk(2)
            noise_pred = noise_pred_uncond + guidance_scale * (noise_pred_text - noise_pred_uncond)
            z = self.scheduler.step(noise_pred, t, z).prev_sample
        
        # Decode to pixels
        return self.vae.decode(z / 0.18215)
```

## Practical Considerations
- **VAE scaling factor**: Multiply latent by 0.18215 to match training distribution
- **Guidance scale**: 7.0-12.0 for realistic images, 2.0-5.0 for diversity
- **Negative prompt**: Provide text for unconditional guidance (removes unwanted concepts)
- **Scheduler**: DDIM (50 steps) for speed, DPMSolver (10-20 steps) for faster sampling
- **Resolution**: SD is trained at 512x512; render at native resolution for best quality

## Limitations
- **Artifacts**: Hands, text, and fine details can be distorted
- **Concept composition**: Struggles with multiple subjects, complex scenes
- **Prompt following**: Not all prompt details are faithfully rendered
- **Bias**: Training data biases reflected in generated images
- **Safety**: NSFW filters needed for production deployment

## References
- Rombach, Blattmann, Lorenz, Esser, Ommer, "High-Resolution Image Synthesis with Latent Diffusion Models", CVPR 2022
- Peebles & Xie, "Scalable Diffusion Models with Transformers (DiT)", ICCV 2023
- Podell, English, Lacey, Blattmann, Dockhorn, Müller, Penna, Rombach, "SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis", 2023
- Ho & Salimans, "Classifier-Free Diffusion Guidance", NeurIPS 2021 Workshop
- Chen, Zhang, et al., "PixArt-α: Fast Training of Diffusion Transformer", 2023
