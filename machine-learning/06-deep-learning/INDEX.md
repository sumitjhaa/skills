# Phase 06 — Deep Learning

## 1. Phase Overview

| Field | Value |
|---|---|
| **Phase** | 06 — Deep Learning |
| **Lessons** | 32 |
| **Core topics** | Computational graphs, reverse-mode autograd, forward-mode autograd, full autograd framework, higher-order gradients, perceptron/MLP, activations, initialization, loss functions, optimizer zoo, LR schedulers, normalization layers, regularization, augmentation, convolutions, pooling, attention, transformer blocks, positional encodings, transformer variants, BPTT, RNN/LSTM/GRU, seq2seq, CNN backbones, skip connections, normalization alternatives, mixed precision, gradient accumulation/checkpointing, gradient noise/clipping, loss symmetries, CIFAR experiments, training pipeline |

## 2. Prerequisites

- **Prior phases:** [Phase 01](../01-linear-algebra/INDEX.md) (matmul, Jacobians as linear maps), [Phase 02](../02-calculus-optimization/INDEX.md) (backprop chain rule, optimizers), [Phase 03](../03-probability-statistics/INDEX.md) (cross-entropy as NLL, regularization as prior)
- **Python frameworks:** [`../../python-frameworks/pytorch/`](../../python-frameworks/pytorch/) (reference implementation), [`../../python-frameworks/numpy-pandas/`](../../python-frameworks/numpy-pandas/) (data handling)

## 3. Lesson Table

| # | Title | What You'll Learn | Lesson | Code | Cross-References |
|---|---|---|---|---|---|
| 01 | Computational Graphs | DAG representation, topological order | [lesson](lessons/01-computational-graphs.md) | [code](code/01.py) | Foundation for all of Phase 06 |
| 02 | Reverse-Mode Autograd | Backpropagation, gradient computation | [lesson](lessons/02-reverse-mode-autograd.md) | [code](code/02.py) | Used in: Phase 12 (autograd capstone) |
| 03 | Forward-Mode Autograd | Jacobian-vector products, dual numbers | [lesson](lessons/03-forward-mode-autograd.md) | [code](code/03.py) | Used in: Phase 07 (neural ODEs) |
| 04 | Full Autograd Framework | Building an autograd engine | [lesson](lessons/04-full-autograd-framework.md) | [code](code/04.py) | Used in: Phase 12 (autograd from scratch) |
| 05 | Higher-Order Gradients | Hessian-vector products, double backprop | [lesson](lessons/05-higher-order-gradients.md) | [code](code/05.py) | Used in: Phase 02 (Hessians), Phase 07 |
| 06 | Perceptron / MLP | Universal approximation, forward/backward | [lesson](lessons/06-perceptron-mlp.md) | [code](code/06.py) | Foundation for all deep models |
| 07 | Activations | ReLU, sigmoid, tanh, GELU, Swish | [lesson](lessons/07-activations.md) | [code](code/07.py) | Used in: Phase 07 (KAN, alternatives) |
| 08 | Initialization | Xavier, Kaiming, orthogonal, layer-sequential | [lesson](lessons/08-initialization.md) | [code](code/08.py) | Used in: Phase 01 (random matrix theory) |
| 09 | Loss Functions | Cross-entropy, MSE, MAE, Huber, contrastive | [lesson](lessons/09-loss-functions.md) | [code](code/09.py) | Used in: Phase 05 (proper losses) |
| 10 | Optimizer Zoo | SGD, Adam, AdamW, Lion, Sophia | [lesson](lessons/10-optimizer-zoo.md) | [code](code/10.py) | Used in: Phase 02 (optimizer zoo) |
| 11 | LR Schedulers | Cosine, warmup, Step, OneCycle | [lesson](lessons/11-lr-schedulers.md) | [code](code/11.py) | Used in: Phase 10 (RL training) |
| 12 | Normalization Layers | Batch, layer, instance, group norm | [lesson](lessons/12-normalization-layers.md) | [code](code/12.py) | Used in: Phase 08 (CNN training) |
| 13 | Regularization | Dropout, weight decay, label smoothing | [lesson](lessons/13-regularization.md) | [code](code/13.py) | Used in: Phase 05 (regularization) |
| 14 | Augmentation | Cutout, mixup, RandAugment, AutoAugment | [lesson](lessons/14-augmentation.md) | [code](code/14.py) | Used in: Phase 08 (CV pipelines) |
| 15 | Convolutions | Conv2d, depthwise, dilated, transposed | [lesson](lessons/15-convolutions.md) | [code](code/15.py) | Used in: Phase 08 (all CV models) |
| 16 | Pooling | Max, avg, global, adaptive | [lesson](lessons/16-pooling.md) | [code](code/16.py) | Used in: Phase 08 (feature maps) |
| 17 | Attention | Scaled dot-product, self-attention, multi-head | [lesson](lessons/17-attention.md) | [code](code/17.py) | Used in: Phase 09 (all of NLP) |
| 18 | Transformer Blocks | Pre/post-LN, FFN, residual | [lesson](lessons/18-transformer-blocks.md) | [code](code/18.py) | Used in: Phase 09 (LLMs), Phase 08 (ViT) |
| 19 | Positional Encodings | Sinusoidal, learned, RoPE, ALiBi | [lesson](lessons/19-positional-encodings.md) | [code](code/19.py) | Used in: Phase 09 (position-aware models) |
| 20 | Transformer Variants | Efficient, sparse, linear attention | [lesson](lessons/20-transformer-variants.md) | [code](code/20.py) | Used in: Phase 07 (SSMs, hybrid) |
| 21 | BPTT | Backprop through time, truncated BPTT | [lesson](lessons/21-bptt.md) | [code](code/21.py) | Used in: Phase 09 (sequence models) |
| 22 | RNN / LSTM / GRU | RNN, LSTM, GRU, bidirectional | [lesson](lessons/22-rnn-lstm-gru.md) | [code](code/22.py) | Used in: Phase 09 (seq modeling) |
| 23 | Seq2Seq | Encoder-decoder, teacher forcing, beam search | [lesson](lessons/23-seq2seq.md) | [code](code/23.py) | Used in: Phase 09 (translation) |
| 24 | CNN Backbones | AlexNet, VGG, ResNet, DenseNet, EfficientNet | [lesson](lessons/24-cnn-backbones.md) | [code](code/24.py) | Used in: Phase 08 (CV backbones) |
| 25 | Skip Connections | Residual, dense, highway connections | [lesson](lessons/25-skip-connections.md) | [code](code/25.py) | Used in: Phase 08 (deep CNNs) |
| 26 | Normalization Alternatives | RMSNorm, LayerNorm, BatchNorm variants | [lesson](lessons/26-normalization-alternatives.md) | [code](code/26.py) | Used in: Phase 09 (LLM training) |
| 27 | Mixed Precision | FP16, BF16, AMP, loss scaling | [lesson](lessons/27-mixed-precision.md) | [code](code/27.py) | Used in: Phase 11 (GPU optimization) |
| 28 | Gradient Accumulation / Checkpointing | Memory-efficient training | [lesson](lessons/28-gradient-accumulation-checkpointing.md) | [code](code/28.py) | Used in: Phase 11 (large-scale training) |
| 29 | Gradient Noise / Clipping | Gradient clipping, noise injection | [lesson](lessons/29-gradient-noise-clipping.md) | [code](code/29.py) | Used in: Phase 10 (RL stability) |
| 30 | Loss Symmetries | Gauge symmetries, invariances in loss landscape | [lesson](lessons/30-loss-symmetries.md) | [code](code/30.py) | Used in: Phase 02 (loss landscape) |
| 31 | CIFAR Experiments | Full training pipeline on CIFAR | [lesson](lessons/31-cifar-experiments.md) | [code](code/31.py) | Used in: Phase 08 (vision baselines) |
| 32 | Training Pipeline | Data loading, logging, checkpointing, eval | [lesson](lessons/32-training-pipeline.md) | [code](code/32.py) | Used in: Phase 11 (MLOps pipeline) |

## 4. Builds Toward

- **Phase 07** (advanced architectures build on deep learning primitives)
- **Phase 08** (CNN backbones, ViTs, self-supervised vision)
- **Phase 09** (transformers, RNNs, seq2seq for NLP)
- **Phase 10** (deep RL with policy networks, DQN)
- **Phase 12** (all capstones: autograd, transformer, diffusion, Mamba, RLHF, distributed)

## 5. Quick Start

```bash
python3 code/06.py
```
