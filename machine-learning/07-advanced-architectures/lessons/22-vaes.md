# Lesson 07.22: VAEs (All Variants)

## Learning Objectives
- Understand variational autoencoder (VAE) and the ELBO
- Implement the reparameterization trick for latent sampling
- Apply β-VAE, VQ-VAE, and other VAE variants
- Analyze the reconstruction-KL trade-off

## Theory
VAEs learn a latent variable model $p(x, z) = p(x|z)p(z)$ via variational inference.

### Evidence Lower Bound (ELBO)
$$\log p(x) \geq \mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)] - \text{KL}[q_\phi(z|x) \| p(z)] \equiv \mathcal{L}_{\text{ELBO}}$$

- **Reconstruction term**: $\mathbb{E}_q[\log p(x|z)]$ — how well decoder reconstructs input
- **KL term**: $\text{KL}[q(z|x) \| p(z)]$ — how close posterior is to prior

### Reparameterization Trick
$$z = \mu_\phi(x) + \sigma_\phi(x) \odot \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, I)$$

Enables backpropagation through sampling by separating stochasticity ($\varepsilon$) from parameters ($\mu, \sigma$).

### Standard VAE Architecture
```
Encoder: x → MLP → μ, log σ² → z = μ + σ ⊙ ε
Decoder: z → MLP → μ_x (and optionally σ_x)
```

## VAE Variants

### β-VAE
$$\mathcal{L}_{\beta} = \mathbb{E}_q[\log p(x|z)] - \beta \cdot \text{KL}[q(z|x) \| p(z)]$$

- $\beta > 1$: Encourages disentangled latent factors
- $\beta = 4-10$ typical for disentanglement
- Trade-off: Higher $\beta$ = more disentangled but lower reconstruction quality

### VQ-VAE (Vector Quantized VAE)
Discrete latent variables via vector quantization:

$$\mathcal{L} = \|x - D(z_q)\|_2^2 + \|\text{sg}[E(x)] - e_k\|_2^2 + \beta \|E(x) - \text{sg}[e_k]\|_2^2$$

- $z_q$: quantized latent from codebook
- $\text{sg}$: stop-gradient operator
- First term: reconstruction, Second: codebook learning, Third: encoder commitment

### VQ-VAE-2
Hierarchical VQ-VAE with multiple latent levels:
- Bottom level: local details (texture, edges)
- Top level: global structure (shape, layout)
- Prior: PixelCNN over discrete latents

### NVAE (Nouveau VAE)
Deep hierarchical VAE with:
- Residual cells in encoder/decoder
- Spectral normalization for stable training
- KL annealing: progressive KL weighting per layer
- Up to 30 latent groups (deep hierarchy)

### IWAE (Importance Weighted Autoencoder)
Tighter ELBO using $k$ importance-weighted samples:

$$\mathcal{L}_{\text{IWAE}} = \mathbb{E}_{\{z_i \sim q(z|x)\}} \left[ \log \frac{1}{k} \sum_{i=1}^k \frac{p(x, z_i)}{q(z_i|x)} \right]$$

- $k=5$ samples gives significantly tighter bound
- Gradients: Less gradient signal to encoder (posterior collapse less likely)

### CVAE (Conditional VAE)
Condition generation on label $c$:

$$\mathcal{L}_{\text{CVAE}} = \mathbb{E}_{q(z|x,c)}[\log p(x|z,c)] - \text{KL}[q(z|x,c) \| p(z|c)]$$

- Both encoder and decoder receive $c$ as input
- Used for class-conditional generation, missing data imputation

### AAE (Adversarial Autoencoder)
Replace KL with adversarial prior matching:

$$q(z) = \mathbb{E}_{p_{\text{data}}(x)}[q(z|x)] \approx p(z)$$

- Discriminator distinguishes $q(z)$ (from encoder) from $p(z)$ (samples from prior)
- No KL computation needed — works with any prior

## Code: Basic VAE

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class VAE(nn.Module):
    def __init__(self, input_dim=784, hidden_dim=256, latent_dim=20):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
        )
        self.mu = nn.Linear(hidden_dim, latent_dim)
        self.log_var = nn.Linear(hidden_dim, latent_dim)
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim),
            nn.Sigmoid(),
        )

    def encode(self, x):
        h = self.encoder(x)
        return self.mu(h), self.log_var(h)

    def reparameterize(self, mu, log_var):
        std = torch.exp(0.5 * log_var)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z):
        return self.decoder(z)

    def forward(self, x):
        mu, log_var = self.encode(x)
        z = self.reparameterize(mu, log_var)
        recon = self.decode(z)
        return recon, mu, log_var

    def loss(self, x, recon, mu, log_var):
        recon_loss = F.binary_cross_entropy(recon, x, reduction='sum')
        kl_loss = -0.5 * torch.sum(1 + log_var - mu.pow(2) - log_var.exp())
        return recon_loss + kl_loss
```

## Variant Comparison

| Variant | Key Innovation | Latent Type | Best For |
|---------|---------------|-------------|----------|
| VAE | Reparameterization trick | Continuous | General generation |
| β-VAE | KL weighting | Continuous | Disentanglement |
| VQ-VAE | Vector quantization | Discrete | High-quality images, audio |
| VQ-VAE-2 | Hierarchical VQ | Discrete (multi-scale) | Large images |
| NVAE | Deep hierarchy | Continuous (hierarchical) | Likelihood evaluation |
| IWAE | Importance weighting | Continuous | Tighter ELBO |
| CVAE | Conditional | Continuous | Conditional generation |

## Practical Considerations
- **KL annealing**: Gradually increase KL weight from 0 to 1 during training
- **Free bits**: Set KL minimum ($\lambda \cdot \max(\text{KL}, \varepsilon)$) to prevent posterior collapse
- **Architecture**: Use convolutional encoder/decoder for images
- **Beta scheduling**: High $\beta$ early, reduce later for β-VAE
- **Prior**: Standard normal works; learnable prior (VampPrior) improves ELBO

## Limitations
- **Posterior collapse**: Decoder ignores latents (especially with powerful decoders like PixelCNN)
- **Blurry samples**: Standard VAE produces blurry images compared to GANs/diffusion
- **ELBO gap**: ELBO may be far from true log-likelihood
- **Discrete data**: VAE works best with continuous data; discrete requires relaxation

## References
- Kingma & Welling, "Auto-Encoding Variational Bayes", ICLR 2014
- Higgins, Matthey, Pal, et al., "β-VAE: Learning Basic Visual Concepts with a Constrained Variational Framework", ICLR 2017
- van den Oord, Vinyals, Kavukcuoglu, "Neural Discrete Representation Learning (VQ-VAE)", NeurIPS 2017
- Vahdat & Kautz, "NVAE: A Deep Hierarchical Variational Autoencoder", NeurIPS 2020
- Burda, Grosse, Salakhutdinov, "Importance Weighted Autoencoders", ICLR 2016
