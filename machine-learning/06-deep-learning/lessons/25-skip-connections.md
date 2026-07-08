# 06.25 Skip Connections

Skip connections (also called shortcut or residual connections) let gradients bypass layers, enabling very deep networks.

## Residual Connections

y = F(x, {W_i}) + x

F(x) is typically 2-3 conv layers. The shortcut just passes x through (identity). If dimensions don't match, project x with a 1x1 conv.

**Benefits**:
- Gradients flow directly to earlier layers
- Solves the degradation problem (deeper nets have lower training error)
- Ensembles shallower paths (unlike a single deep path)

## Dense Connections (DenseNet)

Each layer connects to every subsequent layer:

x_l = H_l([x_0, x_1, ..., x_{l-1}])

Concatenation instead of addition. Avoids learning redundant features.

- N layers → N(N+1)/2 connections
- Parameter efficient
- Better gradient flow
- Memory intensive (all feature maps stored)

## Highway Networks

Gating mechanism controls how much information flows through:

y = g(x) ⊙ F(x) + (1 - g(x)) ⊙ x

g(x) = σ(W_g · x + b_g) — learned transform gate. Allows some paths to be "open" or "closed".

## U-Net

Encoder-decoder with skip connections between corresponding levels:

```
Encoder: downsampling path
Decoder: upsampling path
Skip: concatenate encoder features to decoder at same resolution
```

Used for segmentation. Preserves spatial details lost during downsampling.

## Why Skip Connections Work

1. **Gradient highway**: ∂L/∂x = ∂L/∂y · (∂F/∂x + 1) — the "+1" term ensures gradients can flow backward even if F has small gradients.

2. **Ensemble effect**: A ResNet with N blocks behaves like 2^N implicit ensembles of different-depth networks.

3. **Shattered gradients**: Random initialization causes gradients to decorrelate. Skip connections reduce this effect.
