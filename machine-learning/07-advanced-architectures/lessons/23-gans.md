# Lesson 07.23: GANs (All Variants)

## Learning Objectives
- Understand the GAN minimax game and Nash equilibrium
- Implement DCGAN, WGAN-GP, and StyleGAN
- Apply techniques for stable GAN training
- Analyze mode collapse and mitigation strategies

## Theory
GANs consist of two networks competing in a minimax game:

### Objective
$$\min_G \max_D V(D,G) = \mathbb{E}_{x \sim p_{\text{data}}}[\log D(x)] + \mathbb{E}_{z \sim p(z)}[\log(1 - D(G(z)))]$$

- **Discriminator $D$**: Maximizes ability to distinguish real from fake
- **Generator $G$**: Minimizes discriminator's accuracy

### Nash Equilibrium
$G$ matches data distribution: $p_G = p_{\text{data}}$. At equilibrium:
- $D(x) = 0.5$ for all $x$
- Both networks cannot improve

## Key Challenges

| Challenge | Cause | Mitigation |
|-----------|-------|------------|
| Mode collapse | Generator finds few modes that fool $D$ | Mini-batch discrimination, unrolled GANs |
| Vanishing gradient | $D$ too strong, $G$ gets no signal | WGAN loss, least squares loss |
| Non-convergence | Oscillating dynamics | Two-timescale update rule (TTUR) |
| Unstable training | Poor architecture choices | DCGAN guidelines, spectral norm |

## Architectures

### DCGAN
Guidelines for stable Conv GANs:
- Replace pooling with strided convolutions
- Use BatchNorm in both G and D
- Remove fully connected hidden layers
- ReLU for G (except Tanh output), LeakyReLU for D
- Adam optimizer (lr=0.0002, β=0.5)

### WGAN (Wasserstein GAN)
Critic instead of discriminator — outputs real number, not probability:

$$L = \mathbb{E}_{x \sim p_{\text{data}}}[C(x)] - \mathbb{E}_{z \sim p(z)}[C(G(z))]$$

- **Wasserstein distance**: $W(p_{\text{data}}, p_G) = \sup_{\|C\|_L \leq 1} \mathbb{E}[C(x)] - \mathbb{E}[C(G(z))]$
- **Weight clipping**: $C$ weights clipped to $[-c, c]$ to enforce 1-Lipschitz

### WGAN-GP
Gradient penalty replaces weight clipping for better stability:

$$L_{\text{GP}} = \mathbb{E}_{\hat{x} \sim p_{\hat{x}}} \left[ (\|\nabla_{\hat{x}} C(\hat{x})\|_2 - 1)^2 \right]$$

- $\hat{x}$ = interpolated points between real and fake
- Balances gradient norm at 1 (Lipschitz constraint)

### StyleGAN (Style-Based Generator)

**Architecture**:
```
Latent z → Mapping Network (8-layer MLP) → Styles w → AdaIN → Synthesis Network → Image
```

**Key Innovations**:
- **AdaIN** (Adaptive Instance Normalization): $\text{AdaIN}(x_i, y) = y_{s,i} \frac{x_i - \mu(x_i)}{\sigma(x_i)} + y_{b,i}$
- **Mixing regularization**: Randomly use different $w$ at different layers
- **Noise injection**: Per-pixel Gaussian noise for stochastic detail
- **Style mixing**: Different styles control different levels (coarse → fine)

### StyleGAN2
Improved with:
- **Weight demodulation**: Remove normalization artifact in AdaIN
- **Path length regularization**: Encourage smooth latent space
- **Progressive growing removed**: Train at full resolution directly

### BigGAN
Large-scale GAN with:
- **Self-attention**: Long-range dependencies
- **Shared embeddings**: Class embeddings in both G and D
- **Truncation trick**: Truncate $z$ noise for controlled sample quality
- **Orthogonal regularization**: Prevent overfitting

## Code: WGAN-GP

```python
import torch
import torch.nn as nn

class WGAN_GP:
    def __init__(self, generator, critic, lambda_gp=10):
        self.G = generator
        self.C = critic
        self.lambda_gp = lambda_gp

    def gradient_penalty(self, real, fake):
        batch = real.shape[0]
        alpha = torch.rand(batch, *([1] * (real.ndim - 1)), device=real.device)
        interpolates = alpha * real + (1 - alpha) * fake
        interpolates.requires_grad_(True)
        d_interpolates = self.C(interpolates)
        grad = torch.autograd.grad(
            outputs=d_interpolates, inputs=interpolates,
            grad_outputs=torch.ones_like(d_interpolates),
            create_graph=True, retain_graph=True,
        )[0]
        grad = grad.view(batch, -1)
        gp = ((grad.norm(2, dim=1) - 1) ** 2).mean()
        return gp * self.lambda_gp

    def critic_loss(self, real, fake):
        return self.C(fake).mean() - self.C(real).mean() + self.gradient_penalty(real, fake)

    def generator_loss(self, fake):
        return -self.C(fake).mean()
```

## Loss Function Comparison

| Loss | Objective | Gradient at $D=0.5$ | Mode Coverage |
|------|-----------|--------------------|--------------|
| Minmax (original) | $\log(1-D(G(z)))$ | Zero (vanishing) | Poor |
| Non-saturating | $-\log(D(G(z)))$ | Non-zero | Better |
| LSGAN | $(D(G(z))-1)^2$ | Non-zero | Good |
| WGAN | $-C(G(z))$ | Non-zero | Very good |
| Hinge | $-\min(0, C(G(z))-1)$ | Non-zero | Very good |

## Practical Considerations
- **Balanced training**: Update critic $n_{\text{critic}}$ times per generator update (5:1 ratio)
- **Label smoothing**: Use 0.9 for real, 0.1 for fake
- **Spectral normalization**: Normalize weight matrices by spectral norm for Lipschitz
- **Adaptive discriminator augmentation**: Augment real/fake identically
- **Exponential moving average**: Average generator weights for sampling

## Limitations
- **Unstable training**: Requires careful hyperparameter tuning
- **Mode dropping**: GANs may not cover full data distribution
- **Evaluation**: Inception Score (IS) and FID have known biases
- **Low diversity under high guidance**: Truncation trick reduces variety
- **Computational cost**: Large GANs like BigGAN require 256+ TPU cores

## References
- Goodfellow, Pouget-Abadie, Mirza, et al., "Generative Adversarial Nets", NeurIPS 2014
- Radford, Metz, Chintala, "Unsupervised Representation Learning with Deep Convolutional GANs (DCGAN)", ICLR 2016
- Arjovsky, Chintala, Bottou, "Wasserstein GAN (WGAN)", ICML 2017
- Gulrajani, Ahmed, Arjovsky, Dumoulin, Courville, "Improved Training of WGANs (WGAN-GP)", NeurIPS 2017
- Karras, Laine, Aila, "A Style-Based Generator Architecture for GANs (StyleGAN)", CVPR 2019
- Brock, Donahue, Simonyan, "Large Scale GAN Training for High Fidelity Natural Image Synthesis (BigGAN)", ICLR 2019
