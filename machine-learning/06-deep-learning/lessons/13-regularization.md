# 06.13 Regularization

Regularization techniques prevent overfitting by constraining model capacity or adding noise during training.

## L1 Regularization (Lasso)

Loss = original_loss + λ · Σ|w_i|

Encourages sparsity — many weights become exactly zero. Non-differentiable at zero (use subgradient).

## L2 Regularization (Weight Decay)

Loss = original_loss + (λ/2) · Σ w_i²

Penalizes large weights. Shrinks weights proportionally to their magnitude. Differentiable everywhere.

## Elastic Net

Combines L1 + L2: λ₁Σ|w_i| + λ₂Σ w_i²

## Dropout

During training, randomly zero out neurons with probability p:

y = mask · x / (1-p)  (inverted dropout)

Prevents co-adaptation of features. Acts as ensemble of sub-networks.

## DropConnect

Drop weights instead of activations. Finer-grained than dropout.

## Stochastic Depth

Randomly drop entire layers during training. Used in deep ResNets. Shortens effective network depth.

## Early Stopping

Stop training when validation loss stops improving. Implicit regularization — prevents over-optimization.

## Data Augmentation

Generate modified versions of training data (see Lesson 06.14). Increases effective dataset size.

## Label Smoothing

Replace hard targets (0, 1) with soft targets (ε/(K-1), 1-ε). Prevents overconfidence.

## Noise Injection

Add Gaussian noise to inputs, activations, or weights. Encourages robustness.

## Practical Guide

| Technique | Use Case |
|-----------|----------|
| L2 | Always (small λ=1e-4) |
| Dropout | Large fully-connected layers |
| Label Smoothing | Classification (ε=0.1) |
| Early Stopping | Always monitor validation |
| Stochastic Depth | Very deep nets (100+ layers) |
