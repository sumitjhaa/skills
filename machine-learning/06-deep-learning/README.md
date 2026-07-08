# Phase 06: Deep Learning Foundations — Build Your Own Framework

Build a complete deep learning framework from scratch using NumPy. Covers automatic differentiation, modern architectures, and full training pipelines.

| # | Lesson | Topic |
|---|--------|-------|
| 06.01 | Computational Graphs | DAG construction and topological ordering |
| 06.02 | Reverse-Mode Autograd | Backpropagation via gradient accumulation |
| 06.03 | Forward-Mode Autograd | Dual numbers and directional derivatives |
| 06.04 | Full Autograd Framework | Tensor class with gradient tape |
| 06.05 | Higher-Order Gradients | Hessian-vector products and double backprop |
| 06.06 | Perceptron / MLP | Dense layers and universal approximation |
| 06.07 | Activations | Sigmoid, Tanh, ReLU, Leaky ReLU, ELU, Swish, GELU |
| 06.08 | Initialization Methods | Xavier, He, Orthogonal, LeCun |
| 06.09 | Loss Functions | MSE, Cross-Entropy, Hinge, Huber, Focal |
| 06.10 | Optimizer Zoo | SGD, Momentum, NAG, AdaGrad, RMSprop, Adam, AdamW |
| 06.11 | LR Schedulers | Step, Cosine, OneCycle, Warmup, ReduceOnPlateau |
| 06.12 | Normalization Layers | BatchNorm, LayerNorm, InstanceNorm, GroupNorm |
| 06.13 | Regularization | L1/L2 weight decay, Dropout, DropConnect, Stochastic Depth |
| 06.14 | Augmentation | Flip, rotate, crop, noise, color jitter, mixup, cutout |
| 06.15 | Convolutions | Conv2d, depthwise, dilated, transposed, group conv |
| 06.16 | Pooling | Max, Average, Global, Adaptive, ROI |
| 06.17 | Attention | Scaled dot-product, additive, multi-head |
| 06.18 | Transformer Blocks | Encoder/decoder with self/cross attention |
| 06.19 | Positional Encodings | Sinusoidal, learned, RoPE, ALiBi |
| 06.20 | Transformer Variants | GPT, BERT, ViT, Performer, Linformer |
| 06.21 | BPTT | Backpropagation through time |
| 06.22 | RNN / LSTM / GRU | Recurrent cells and gating mechanisms |
| 06.23 | Seq2Seq | Encoder-decoder with attention |
| 06.24 | CNN Backbones | LeNet-5, AlexNet, VGG, ResNet, EfficientNet |
| 06.25 | Skip Connections | Residual, dense, highway connections |
| 06.26 | Normalization Alternatives | RMSNorm, ScaleNorm, AdaptiveNorm |
| 06.27 | Mixed Precision | FP16/FP32 training, loss scaling |
| 06.28 | Gradient Accumulation / Checkpointing | Memory-efficient training |
| 06.29 | Gradient Noise / Clipping | Stabilizing training dynamics |
| 06.30 | Loss Symmetries | Label smoothing, margin, contrastive, triplet |
| 06.31 | CIFAR Experiments | Full experiment tracking and ablation |
| 06.32 | Full Training Pipeline | End-to-end training with all components |

### Structure

```
lessons/          — 32 markdown lesson files (01-32)
code/             — 32 standalone runnable Python implementations
practice/         — Exercise file for self-assessment
```

### Getting Started

```bash
pip install numpy scipy matplotlib
python code/01.py   # computational graphs
python code/04.py   # autograd framework (core)
python code/32.py   # full training pipeline
```
