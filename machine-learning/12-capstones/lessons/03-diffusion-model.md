# Lesson 12.03: Diffusion Model from Scratch

## Project Architecture

Implement a denoising diffusion probabilistic model (DDPM) and train it on CIFAR-10 or MNIST.

```
Forward Process (fixed)
  x_0 → x_1 → ... → x_T (add Gaussian noise)
  q(x_t | x_{t-1}) = N(x_t; sqrt(1-β_t) x_{t-1}, β_t I)

Reverse Process (learned)
  x_T → x_T-1 → ... → x_0 (denoise)
  p_θ(x_{t-1} | x_t) = N(x_{t-1}; μ_θ(x_t, t), Σ_t I)

Training: L_simple = E_{t,x_0,ε} [ || ε - ε_θ(x_t, t) ||^2 ]

Sampling: x_{t-1} = 1/sqrt(α_t) (x_t - (1-α_t)/sqrt(1-α̅_t) ε_θ) + σ_t z
```

## Design Decisions

### Noise schedule
- Linear beta schedule: β_1 to β_T (typically 1e-4 to 0.02)
- Precompute α_t = 1 - β_t, α̅_t = cumprod(α_1...α_t)
- T = 1000 timesteps

### U-Net architecture (ε_θ)
- Encoder: convolutional blocks with downsampling
- Bottleneck: middle block
- Decoder: upsampling with skip connections from encoder
- Time embedding: sinusoidal encoding + MLP projected into each block
- Use GroupNorm or BatchNorm throughout

### Loss
- Simple loss: MSE between predicted noise ε_θ and actual noise ε
- Weighted uniformly across timesteps

### Sampling
- DDPM sampling: iterate t=T down to 1, predict noise, remove it, add new noise
- Can skip steps for faster sampling (DDIM)

## Implementation Guide

1. **Implement the forward diffusion process** (add noise given image and t)
2. **Implement sinusoidal time embeddings**
3. **Implement a single convolutional block** (Conv2D + GN + SiLU)
4. **Implement the U-Net encoder** (down blocks)
5. **Implement the U-Net decoder** (up blocks with skip connections)
6. **Implement the full U-Net model** with time conditioning
7. **Implement training loop** (sample t, add noise, predict noise, compute loss)
8. **Implement DDPM sampling loop**
9. **Implement DDIM sampling** (optional, for faster generation)
10. **Train on MNIST/CIFAR-10 and generate samples**
11. **Plot generated images and FID score approximation**

## Key Insights

- The training objective is simple: predict the noise that was added
- U-Net skip connections preserve high-frequency detail
- Time conditioning lets the model know which noise level it sees
- Using fewer sampling steps (DDIM) trades quality for speed
- The reverse process is a learned Langevin dynamics
