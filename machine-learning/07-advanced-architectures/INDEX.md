# Phase 07 — Advanced Architectures

## 1. Phase Overview

| Field | Value |
|---|---|
| **Phase** | 07 — Advanced Architectures |
| **Lessons** | 30 |
| **Core topics** | KAN, MLP alternatives, neural ODEs, PINNs, DEQs, implicit neural representations, hypernetworks, spiking NNs, liquid NNs, capsule networks, neural processes, set functions, state-space models (SSMs), SSM variants, hybrid SSM-attention, energy-based models, normalizing flows, autoregressive models, diffusion models, latent diffusion, flow matching, VAEs, GANs, MCMC-based deep learning, differentiable programming, neuro-symbolic, NAS, contrastive learning, ML for science, SOTA reproduction |

## 2. Prerequisites

- **Prior phases:** [Phase 01](../01-linear-algebra/INDEX.md) (matrix decompositions), [Phase 02](../02-calculus-optimization/INDEX.md) (gradients, variational methods), [Phase 03](../03-probability-statistics/INDEX.md) (likelihood, Bayesian inference), [Phase 04](../04-advanced-math/INDEX.md) (divergences, geometry), [Phase 06](../06-deep-learning/INDEX.md) (backprop, transformers, CNNs, autograd)
- **Python frameworks:** [`../../python-frameworks/pytorch/`](../../python-frameworks/pytorch/) (reference)

## 3. Lesson Table

| # | Title | What You'll Learn | Lesson | Code | Cross-References |
|---|---|---|---|---|---|
| 01 | KAN | Kolmogorov–Arnold networks, spline-based | [lesson](lessons/01-kan.md) | [code](code/01-kan.py) | Used in: Phase 06 (MLP alternatives) |
| 02 | MLP Alternatives | Fourier features, SIREN, gated MLP | [lesson](lessons/02-mlp-alternatives.md) | [code](code/02-mlp-alternatives.py) | Used in: Phase 08 (implicit neural) |
| 03 | Neural ODEs | ODE solvers as layers, adjoint sensitivity | [lesson](lessons/03-neural-odes.md) | [code](code/03-neural-odes.py) | Used in: Phase 02 (calculus of variations) |
| 04 | PINNs | Physics-informed neural networks | [lesson](lessons/04-pinns.md) | [code](code/04-pinns.py) | Used in: Phase 12 (ML for science) |
| 05 | DEQs | Deep equilibrium models, implicit layers | [lesson](lessons/05-deq.md) | [code](code/05-deq.py) | Used in: Phase 06 (implicit differentiation) |
| 06 | Implicit Neural | NeRF, SDFs, coordinate-based MLPs | [lesson](lessons/06-implicit-neural.md) | [code](code/06-implicit-neural.py) | Used in: Phase 08 (neural rendering) |
| 07 | Hypernetworks | Weight generation, dynamic networks | [lesson](lessons/07-hypernetworks.md) | [code](code/07-hypernetworks.py) | Used in: Phase 06 (meta-learning) |
| 08 | Spiking NNs | Leaky integrate-and-fire, surrogate gradients | [lesson](lessons/08-spiking-nns.md) | [code](code/08-spiking-nns.py) | Used in: Phase 10 (neuromorphic RL) |
| 09 | Liquid NNs | Liquid time-constant networks | [lesson](lessons/09-liquid-nns.md) | [code](code/09-liquid-nns.py) | Used in: Phase 10 (continuous control) |
| 10 | Capsule Networks | Routing-by-agreement, equivariance | [lesson](lessons/10-capsule-networks.md) | [code](code/10-capsule-networks.py) | Used in: Phase 08 (vision) |
| 11 | Neural Processes | Meta-learning, stochastic processes | [lesson](lessons/11-neural-processes.md) | [code](code/11-neural-processes.py) | Used in: Phase 03 (GP alternatives) |
| 12 | Set Functions | Deep sets, set transformers, permutation invariance | [lesson](lessons/12-set-functions.md) | [code](code/12-set-functions.py) | Used in: Phase 09 (point cloud) |
| 13 | SSMs | S4, structured state-space models | [lesson](lessons/13-ssms.md) | [code](code/13-ssms.py) | Used in: Phase 09 (long-range models) |
| 14 | SSM Variants | Mamba, S6, S5, DSS | [lesson](lessons/14-ssm-variants.md) | [code](code/14-ssm-variants.py) | Used in: Phase 12 (Mamba capstone) |
| 15 | Hybrid SSM-Attention | Combining SSMs and attention | [lesson](lessons/15-hybrid-ssm-attention.md) | [code](code/15-hybrid-ssm-attention.py) | Used in: Phase 09 (efficient transformers) |
| 16 | EBMs | Energy-based models, Langevin dynamics | [lesson](lessons/16-ebms.md) | [code](code/16-ebms.py) | Used in: Phase 04 (stat-mech) |
| 17 | Normalizing Flows | Change of variables, coupling, affine | [lesson](lessons/17-normalizing-flows.md) | [code](code/17-normalizing-flows.py) | Used in: Phase 03 (density estimation) |
| 18 | Autoregressive Models | PixelCNN, WaveNet, causal convolutions | [lesson](lessons/18-autoregressive.md) | [code](code/18-autoregressive.py) | Used in: Phase 08 (image gen) |
| 19 | Diffusion Models | DDPM, DDIM, noise schedules | [lesson](lessons/19-diffusion.md) | [code](code/19-diffusion.py) | Used in: Phase 08 (image gen), Phase 12 (diffusion capstone) |
| 20 | Latent Diffusion | LDM, cross-attention conditioning | [lesson](lessons/20-latent-diffusion.md) | [code](code/20-latent-diffusion.py) | Used in: Phase 08 (text-to-image) |
| 21 | Flow Matching | Continuous normalizing flows, optimal transport | [lesson](lessons/21-flow-matching.md) | [code](code/21-flow-matching.py) | Used in: Phase 04 (optimal transport) |
| 22 | VAEs | Variational autoencoders, reparameterization | [lesson](lessons/22-vaes.md) | [code](code/22-vaes.py) | Used in: Phase 03 (variational inference) |
| 23 | GANs | Adversarial training, DCGAN, StyleGAN | [lesson](lessons/23-gans.md) | [code](code/23-gans.py) | Used in: Phase 08 (image gen), Phase 04 (game theory) |
| 24 | MCMC Deep Learning | Bayesian deep learning via MCMC | [lesson](lessons/24-mcmc.md) | [code](code/24-mcmc.py) | Used in: Phase 03 (Bayesian inference) |
| 25 | Differentiable Programming | Differentiable primitives, JAX-style | [lesson](lessons/25-differentiable-programming.md) | [code](code/25-differentiable-programming.py) | Used in: Phase 12 (autograd capstone) |
| 26 | Neuro-Symbolic | Logic + neural, differentiable reasoning | [lesson](lessons/26-neural-symbolic.md) | [code](code/26-neural-symbolic.py) | Used in: Phase 09 (reasoning) |
| 27 | NAS | DARTS, ENAS, evolutionary NAS | [lesson](lessons/27-nas.md) | [code](code/27-nas.py) | Used in: Phase 05 (AutoML) |
| 28 | Contrastive Learning | SimCLR, MoCo, BYOL, CLIP | [lesson](lessons/28-contrastive-learning.md) | [code](code/28-contrastive-learning.py) | Used in: Phase 08 (self-supervised vision), Phase 09 (multimodal) |
| 29 | ML for Science | Scientific ML, inverse problems | [lesson](lessons/29-ml-for-science.md) | [code](code/29-ml-for-science.py) | Used in: Phase 12 (novel contribution) |
| 30 | SOTA Reproduction | Reproducing published results | [lesson](lessons/30-sota-reproduction.md) | [code](code/30-sota-reproduction.py) | Used in: Phase 12 (reproduce paper capstone) |

## 4. Builds Toward

- **Phase 08** (implicit neural for NeRF, diffusion for vision, GANs for generation)
- **Phase 09** (SSMs for long-range, diffusion for text, contrastive for multimodal)
- **Phase 10** (neural ODEs for continuous control, hypernetworks for meta-RL)
- **Phase 12** (diffusion, Mamba, autograd capstones all connect to Phase 07)

## 5. Quick Start

```bash
python3 code/01-kan.py
```
