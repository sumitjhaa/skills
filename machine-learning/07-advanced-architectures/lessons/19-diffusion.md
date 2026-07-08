# Lesson 07.19: Diffusion Models (DDPM, DDIM, Flow Matching)

## Learning Objectives
- Understand forward/reverse diffusion processes
- Implement DDPM noise prediction with UNet
- Apply DDIM for deterministic and accelerated sampling
- Compare diffusion with score matching and flow matching

## Theory
Diffusion models learn to reverse a gradual noising process.

### Forward Process (Fixed)
$$q(x_t \mid x_{t-1}) = \mathcal{N}(\sqrt{1-\beta_t} x_{t-1}, \beta_t I)$$

- $\beta_1, \dots, \beta_T$: variance schedule (linear, cosine, or sigmoid)
- Reparameterization: $x_t = \sqrt{\bar{\alpha}_t} x_0 + \sqrt{1-\bar{\alpha}_t} \varepsilon$, $\varepsilon \sim \mathcal{N}(0, I)$
- $\alpha_t = 1 - \beta_t$, $\bar{\alpha}_t = \prod_{s=1}^t \alpha_s$

### Reverse Process (Learned)
$$p_\theta(x_{t-1} \mid x_t) = \mathcal{N}(\mu_\theta(x_t, t), \Sigma_\theta(x_t, t))$$

- Typically fix $\Sigma_t = \beta_t$ (or learn diagonal)
- Predict $\mu_\theta$ via noise prediction $\varepsilon_\theta(x_t, t)$:
  $$\mu_\theta(x_t, t) = \frac{1}{\sqrt{\alpha_t}}\left(x_t - \frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}} \varepsilon_\theta(x_t, t)\right)$$

## DDPM (Denoising Diffusion Probabilistic Models)

### Loss
$$\mathcal{L}_{\text{simple}} = \mathbb{E}_{t \sim [1,T], x_0, \varepsilon} \left[ \|\varepsilon - \varepsilon_\theta(\sqrt{\bar{\alpha}_t} x_0 + \sqrt{1-\bar{\alpha}_t} \varepsilon, t)\|^2 \right]$$

- Train noise prediction network $\varepsilon_\theta$ (typically UNet)
- $t$ uniformly sampled: emphasizes all noise levels

### Sampling
```
x_T ~ N(0, I)
for t = T down to 1:
    z ~ N(0, I) if t > 1 else 0
    x_{t-1} = (1/√α_t)(x_t - β_t/√(1-ᾱ_t) ε_θ(x_t, t)) + σ_t z
```

## DDIM (Denoising Diffusion Implicit Models)

### Deterministic Sampling
$$x_{t-1} = \sqrt{\bar{\alpha}_{t-1}} \underbrace{\left(\frac{x_t - \sqrt{1-\bar{\alpha}_t} \varepsilon_\theta}{\sqrt{\bar{\alpha}_t}}\right)}_{\text{predicted } x_0} + \sqrt{1-\bar{\alpha}_{t-1}} \varepsilon_\theta$$

- No noise addition: deterministic mapping $x_T \to x_0$
- Same training objective as DDPM
- Can skip steps: sample every $S$ steps (e.g., $T=50$ instead of $1000$)

### Benefits
- **10-50x faster** sampling than DDPM
- **Interpolation**: Linear interpolation in $x_T$ space gives smooth transitions in $x_0$
- **Consistency**: Same $x_T$ always produces same $x_0$

## Score Matching View

### Score Function
$$s_\theta(x_t, t) = \nabla_{x_t} \log p(x_t) \approx -\frac{\varepsilon_\theta(x_t, t)}{\sqrt{1-\bar{\alpha}_t}}$$

- **Denoising score matching**: Train $s_\theta$ to match score of noise-perturbed data
- **Langevin dynamics**: Sample from $p(x)$ by iterating $x_{k+1} = x_k + \eta s_\theta(x_k) + \sqrt{2\eta} z$

## Flow Matching

### Continuous Transport
Replace discrete steps with continuous ODE:

$$\frac{dx}{dt} = v_\theta(x(t), t)$$

- $v_\theta$: learned velocity field
- $t \in [0, 1]$: data ($t=0$) to noise ($t=1$)
- **Straight paths**: Ideal flow follows $x_t = (1-t) x_0 + t \varepsilon$
- **CFM (Conditional Flow Matching)**: Train on $v_t(x_t \mid x_0, \varepsilon)$

## Code: DDPM Noise Prediction

```python
import torch
import torch.nn as nn

class DiffusionModel(nn.Module):
    def __init__(self, unet, T=1000, beta_schedule='linear'):
        super().__init__()
        self.unet = unet
        self.T = T
        if beta_schedule == 'linear':
            beta = torch.linspace(1e-4, 0.02, T)
        elif beta_schedule == 'cosine':
            t = torch.linspace(0, T, T+1)
            f_t = torch.cos((t / T + 0.008) / 1.008 * torch.pi / 2) ** 2
            alpha_bar = f_t / f_t[0]
            beta = 1 - alpha_bar[1:] / alpha_bar[:-1]
            beta = beta.clamp(max=0.999)
        
        self.register_buffer('beta', beta)
        self.register_buffer('alpha', 1 - beta)
        self.register_buffer('alpha_bar', torch.cumprod(self.alpha, dim=0))

    def forward(self, x0):
        t = torch.randint(0, self.T, (x0.shape[0],), device=x0.device)
        eps = torch.randn_like(x0)
        sqrt_alpha_bar = torch.sqrt(self.alpha_bar[t])[:, None, None, None]
        sqrt_one_minus = torch.sqrt(1 - self.alpha_bar[t])[:, None, None, None]
        xt = sqrt_alpha_bar * x0 + sqrt_one_minus * eps
        eps_pred = self.unet(xt, t)
        return nn.functional.mse_loss(eps_pred, eps)
```

## Architecture Comparison

| Model | Steps | Deterministic? | Quality | Speed |
|-------|-------|---------------|---------|-------|
| DDPM | 1000 | No | Best | Slow |
| DDIM | 50-100 | Yes | Good | Fast |
| Score SDE | 1000 | No | Best | Slow |
| Flow Matching | 50-100 | Yes | Excellent | Fast |
| Consistency | 1-2 | Yes | Good | Very fast |

## Practical Considerations
- **Variance schedule**: Cosine schedule works better than linear for high-res images
- **Architecture**: UNet with attention (or DiT) for image generation
- **Guidance scale**: Classifier-free guidance: $\tilde{\varepsilon} = (1+w) \varepsilon_\theta(x_t, c) - w \varepsilon_\theta(x_t)$
- **Mixed precision**: Diffusion training is memory-intensive; use mixed precision and gradient checkpointing
- **EMA**: Exponential moving average of weights for stable sampling

## References
- Ho, Jain, Abbeel, "Denoising Diffusion Probabilistic Models (DDPM)", NeurIPS 2020
- Song, Meng, Ermon, "Denoising Diffusion Implicit Models (DDIM)", ICLR 2021
- Song, Sohl-Dickstein, Kingma, Kumar, Ermon, Poole, "Score-Based Generative Modeling through Stochastic Differential Equations", NeurIPS 2020
- Lipman, Chen, Ben-Hamu, Nickel, Le, "Flow Matching for Generative Modeling", ICLR 2023
- Song, Meng, Ermon, "Consistency Models", ICML 2023
