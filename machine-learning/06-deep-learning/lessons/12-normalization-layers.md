# 06.12 Normalization Layers

Normalization layers stabilize training by re-centering and re-scaling activations.

## Batch Normalization

y = γ · (x - μ_B) / √(σ_B² + ε) + β

Normalizes across the batch dimension. Uses running statistics at inference. Reduces internal covariate shift. Enables higher LR.

- Pros: Faster convergence, regularizing effect
- Cons: Batch size dependent, tricky with small batches or RNNs

## Layer Normalization

y = γ · (x - μ_L) / √(σ_L² + ε) + β

Normalizes across feature dimension (per sample). Used in transformers (GPT, BERT). Independent of batch size.

- Pros: Works for any batch size, good for RNNs
- Cons: Less studied for CNNs

## Instance Normalization

y = γ · (x - μ_I) / √(σ_I² + ε) + β

Normalizes per channel per sample. Used in style transfer. Removes instance-specific contrast.

## Group Normalization

y = γ · (x - μ_G) / √(σ_G² + ε) + β

Divides channels into groups, normalizes within each. Between LN (1 group) and IN (C groups). Effective for small batches.

## Comparison

| Layer | Axis | Batch Dependent | Used In |
|-------|------|-----------------|---------|
| BatchNorm | Batch | Yes | CNNs (ResNet) |
| LayerNorm | Features | No | Transformers |
| InstanceNorm | Spatial | No | Style Transfer |
| GroupNorm | Channel groups | No | Small batch CNNs |

## Learnable Parameters

γ (scale) and β (shift) are learnable — default γ=1, β=0. Without them, normalization would remove the layer's representational power.

## Implementation Details

- Track running mean/var for inference (BatchNorm)
- ε prevents division by zero (≈1e-5)
- Gradient flows through both normalization and affine transform
