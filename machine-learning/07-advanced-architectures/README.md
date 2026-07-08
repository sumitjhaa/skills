# Phase 07: Advanced Architectures & Frontier Models

## Overview

| # | Lesson | Code | Topic |
|---|--------|------|-------|
| 07.01 | [KAN](./lessons/01-kan.md) | [code](./code/01-kan.py) | Kolmogorov-Arnold Networks |
| 07.02 | [MLP alternatives](./lessons/02-mlp-alternatives.md) | [code](./code/02-mlp-alternatives.py) | MLP-Mixer, gMLP |
| 07.03 | [Neural ODEs](./lessons/03-neural-odes.md) | [code](./code/03-neural-odes.py) | Neural ODEs/CDEs/SDEs |
| 07.04 | [PINNs](./lessons/04-pinns.md) | [code](./code/04-pinns.py) | Physics-Informed Neural Networks |
| 07.05 | [DEQ](./lessons/05-deq.md) | [code](./code/05-deq.py) | Deep Equilibrium Models |
| 07.06 | [Implicit Neural Repr.](./lessons/06-implicit-neural.md) | [code](./code/06-implicit-neural.py) | NeRF, SIREN |
| 07.07 | [Hypernetworks](./lessons/07-hypernetworks.md) | [code](./code/07-hypernetworks.py) | Hypernetworks |
| 07.08 | [Spiking NNs](./lessons/08-spiking-nns.md) | [code](./code/08-spiking-nns.py) | Spiking Neural Networks |
| 07.09 | [Liquid NNs](./lessons/09-liquid-nns.md) | [code](./code/09-liquid-nns.py) | LTC, NCP |
| 07.10 | [Capsule Networks](./lessons/10-capsule-networks.md) | [code](./code/10-capsule-networks.py) | Capsule Networks |
| 07.11 | [Neural Processes](./lessons/11-neural-processes.md) | [code](./code/11-neural-processes.py) | Neural Processes |
| 07.12 | [Set Functions](./lessons/12-set-functions.md) | [code](./code/12-set-functions.py) | Deep Sets, PointNet |
| 07.13 | [SSMs](./lessons/13-ssms.md) | [code](./code/13-ssms.py) | S4, Mamba |
| 07.14 | [SSM variants](./lessons/14-ssm-variants.md) | [code](./code/14-ssm-variants.py) | H3, Hyena, RWKV |
| 07.15 | [Hybrid SSM-Attention](./lessons/15-hybrid-ssm-attention.md) | [code](./code/15-hybrid-ssm-attention.py) | Jamba, MambaFormer |
| 07.16 | [EBMs](./lessons/16-ebms.md) | [code](./code/16-ebms.py) | Energy-Based Models |
| 07.17 | [Normalizing Flows](./lessons/17-normalizing-flows.md) | [code](./code/17-normalizing-flows.py) | Normalizing Flows |
| 07.18 | [Autoregressive](./lessons/18-autoregressive.md) | [code](./code/18-autoregressive.py) | NADE, MADE, WaveNet |
| 07.19 | [Diffusion](./lessons/19-diffusion.md) | [code](./code/19-diffusion.py) | DDPM, DDIM, flow matching |
| 07.20 | [Latent Diffusion](./lessons/20-latent-diffusion.md) | [code](./code/20-latent-diffusion.py) | LDM, SD, DiT |
| 07.21 | [Flow Matching](./lessons/21-flow-matching.md) | [code](./code/21-flow-matching.py) | Flow Matching & Rectified Flow |
| 07.22 | [VAEs](./lessons/22-vaes.md) | [code](./code/22-vaes.py) | VAEs (all variants) |
| 07.23 | [GANs](./lessons/23-gans.md) | [code](./code/23-gans.py) | GANs (all variants) |
| 07.24 | [MCMC for DL](./lessons/24-mcmc.md) | [code](./code/24-mcmc.py) | MCMC for Deep Learning |
| 07.25 | [Differentiable Prog.](./lessons/25-differentiable-programming.md) | [code](./code/25-differentiable-programming.py) | Differentiable programming |
| 07.26 | [Neural-Symbolic](./lessons/26-neural-symbolic.md) | [code](./code/26-neural-symbolic.py) | Neural-Symbolic |
| 07.27 | [NAS](./lessons/27-nas.md) | [code](./code/27-nas.py) | Neural Architecture Search |
| 07.28 | [Contrastive Learning](./lessons/28-contrastive-learning.md) | [code](./code/28-contrastive-learning.py) | Contrastive learning |
| 07.29 | [ML for Science](./lessons/29-ml-for-science.md) | [code](./code/29-ml-for-science.py) | AlphaFold, ESM |
| 07.30 | [SOTA Reproduction](./lessons/30-sota-reproduction.md) | [code](./code/30-sota-reproduction.py) | SOTA reproduction |

## Prerequisites
- Phase 01-06 foundations
- Solid understanding of calculus, linear algebra, probability
- Python with numpy, scipy, matplotlib

## Getting Started

```bash
# Run any lesson's code
python code/01-kan.py

# Read a lesson
cat lessons/01-kan.md

# Practice exercises
code practice/phase07-exercises.md
```

## Learning Objectives
By the end of this phase you will be able to:
- Implement and explain 30 advanced neural architectures
- Reproduce simplified versions of frontier model components
- Understand the theoretical foundations of each architecture
- Apply appropriate architectures to complex problem domains
