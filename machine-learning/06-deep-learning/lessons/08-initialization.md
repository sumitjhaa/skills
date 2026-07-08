# 06.08 Initialization Methods

Proper weight initialization prevents vanishing/exploding gradients and accelerates convergence.

## The Problem

Poor initialization causes:
- Activations to saturate (sigmoid/tanh) → zero gradients
- Variance to explode or vanish across layers
- Slow or failed convergence

## Xavier/Glorot Initialization

W ∼ Uniform(-√(6/(n_in + n_out)), √(6/(n_in + n_out)))

or Normal(0, √(2/(n_in + n_out)))

**Idea**: Maintain variance of activations and gradients across layers. Derived for tanh/sigmoid activations.

## He/Kaiming Initialization

W ∼ Normal(0, √(2/n_in))

**Idea**: For ReLU activations, which zero out half the neurons, variance needs to be √2 times larger than Xavier.

## Orthogonal Initialization

W is a random orthogonal matrix. Preserves norm of activations. Useful for RNNs.

## LeCun Initialization

W ∼ Normal(0, √(1/n_in))

Designed for SELU activations to maintain self-normalizing property.

## Bias Initialization

Biases are typically initialized to 0. For ReLU, sometimes initialized to a small positive value (0.01) to reduce dead neurons.

## Practical Guidelines

| Activation | Recommended Init |
|------------|------------------|
| Sigmoid/Tanh | Xavier |
| ReLU/PReLU | He |
| ELU | He |
| SELU | LeCun |
| Swish/GELU | He (works well) |

## Empirical Validation

Check the mean and std of activations at initialization across layers. They should remain roughly constant.
