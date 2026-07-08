# 08.30 Multi-modal Generation

## Learning Objectives
- Understand autoregressive text-to-image generation (DALL-E)
- Implement latent diffusion models (Stable Diffusion)
- Apply composable diffusion (CoDi) for any-to-any generation
- Compare generation quality with FID, CLIP score, human evaluation

## DALL-E (Decoder-Only Transformer)

### dVAE (discrete VAE)
Compress image $x \in \mathbb{R}^{256 \times 256 \times 3}$ to discrete tokens $z \in \{1, \dots, 8192\}^{32 \times 32}$:

- Encoder: 32× downsampling with continuous output → Gumbel-softmax
- Decoder: 32× upsampling to reconstruct image
- Training: ELBO with uniform prior

### Autoregressive Transformer
Generate image tokens $z$ conditioned on text $y$:

$$p(z | y) = \prod_{i=1}^{1024} p(z_i | z_{<i}, y)$$

- 12B parameters (full model)
- Text: BPE-encoded with 16,384 vocab (256 tokens)
- Image: 1024 tokens (32×32 grid)

### DALL-E 2 (unCLIP)
Two-stage model:
1. **Prior**: CLIP text embedding → CLIP image embedding (diffusion)
2. **Decoder**: CLIP image embedding → image (diffusion)

### DALL-E 3
Improved captioning: re-caption images with detailed descriptions → text-to-image trained on aligned captions → better prompt following.

## Stable Diffusion (Latent Diffusion)

### Perceptual Compression
Use VAE to compress images to latent space:

$$z = \mathcal{E}(x), \quad \hat{x} = \mathcal{D}(z)$$

- Compression: 8× (256×256 → 32×32 latent)
- Latent dimension: 4 channels
- Trained with VQGAN/perceptual loss

### Denoising U-Net
Denoise in latent space:

$$\mathcal{L}_{\text{LDM}} = \mathbb{E}_{z_t, c, t}[\|\epsilon - \epsilon_\theta(z_t, t, c)\|_2^2]$$

- $c$: text conditioning (CLIP text embeddings)
- $t$: time step (uniform)
- $\epsilon$: Gaussian noise

### Cross-Attention
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^\top}{\sqrt{d}}\right) V$$

- $Q$: from spatial features (latent)
- $K, V$: from text embeddings

### Classifier-Free Guidance
$$\epsilon_\theta(z_t, t, c) = \epsilon_\theta(z_t, t, \emptyset) + w \cdot (\epsilon_\theta(z_t, t, c) - \epsilon_\theta(z_t, t, \emptyset))$$

- $w$: guidance scale (7-12 typical)
- $\emptyset$: null/unconditional (10% dropout during training)

## Imagen

### Text Encoder
T5-XXL (11B parameters) — text-only LLM as text encoder:

- Better than CLIP text encoder for text-image alignment
- Frozen weights (not fine-tuned)

### Cascaded Generation
```
64×64 → Super-resolution ×1 → 256×256 → Super-resolution ×2 → 1024×1024
```

Each stage is a conditional diffusion model.

## CoDi (Composable Diffusion)

### Architecture
Multiple encoders/decoders sharing a unified latent space:

- **Input**: Text, image, video, audio
- **Output**: Text, image, video, audio
- **Core**: Shared diffusion backbone with modality-specific encoders/decoders

### Training
1. Train unimodal generation (text→image, text→audio, etc.)
2. Align latent spaces minimising modality gap
3. Enable cross-modal generation (video→audio, image→text)

## Code: Stable Diffusion Sampling

```python
import torch
import torch.nn as nn

def sample_ddim(model, text_embeddings, num_steps=50, guidance_scale=7.5):
    """DDIM sampling for Stable Diffusion"""
    batch_size = text_embeddings.shape[0]
    z = torch.randn(batch_size, 4, 64, 64, device=text_embeddings.device)
    null_emb = torch.zeros_like(text_embeddings)
    
    timesteps = torch.linspace(999, 0, num_steps, dtype=torch.long)
    for t in range(num_steps - 1):
        t_tensor = torch.full((batch_size,), timesteps[t], device=z.device)
        
        # Classifier-free guidance
        noise_uncond = model(z, t_tensor, null_emb)
        noise_cond = model(z, t_tensor, text_embeddings)
        noise = noise_uncond + guidance_scale * (noise_cond - noise_uncond)
        
        # DDIM step
        alpha_bar_t = model.scheduler.alphas_cumprod[t]
        alpha_bar_next = model.scheduler.alphas_cumprod[t + 1]
        z = (z - (1 - alpha_bar_t).sqrt() * noise) / alpha_bar_t.sqrt()
        z = alpha_bar_next.sqrt() * z + (1 - alpha_bar_next).sqrt() * noise
    
    return z
```

## Evaluation

| Model | FID-30K (COCO) | CLIP Score | Inference Time | Parameters |
|-------|---------------|------------|----------------|-----------|
| DALL-E 2 | 10.4 | 0.352 | 12s | 3.5B |
| Stable Diffusion 1.5 | 12.6 | 0.337 | 4s | 1.2B |
| Stable Diffusion XL | 8.9 | 0.351 | 8s | 3.5B |
| Imagen | 7.3 | 0.369 | 25s | 3.0B |
| DALL-E 3 | — | 0.367 | — | Proprietary |

## Practical Considerations
- **Prompt engineering**: Specific, detailed prompts produce better results
- **Negative prompts**: Exclude unwanted concepts ("bad hands", "blurry")
- **Safety filtering**: NSFW detectors and concept erasure (ESD, SLD)
- **Inpainting**: Modify parts of an image by masking and re-sampling
- **LoRA fine-tuning**: Efficient model personalisation with low-rank adapters

## References
- Ramesh, et al., "Zero-Shot Text-to-Image Generation (DALL-E)", ICML 2021
- Ramesh, Dhariwal, Nichol, et al., "Hierarchical Text-Conditional Image Generation with CLIP Latents (DALL-E 2)", 2022
- Rombach, Blattmann, et al., "High-Resolution Image Synthesis with Latent Diffusion Models (Stable Diffusion)", CVPR 2022
- Saharia, Chan, et al., "Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding (Imagen)", NeurIPS 2022
- Tang, Li, et al., "CoDi: Any-to-Any Generation via Composable Diffusion", 2023
