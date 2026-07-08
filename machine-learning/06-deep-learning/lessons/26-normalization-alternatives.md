# 06.26 Normalization Alternatives

Alternatives to Batch/Layer/Instance/Group normalization for specialized use cases.

## RMSNorm

y = x / √(mean(x²) + ε) · γ

Only uses root mean square (no mean subtraction). Simpler than LayerNorm. Used in Llama. Reduces computation by O(d) per layer.

## ScaleNorm

y = x / ||x|| · g

Divide by L2 norm, multiply by learnable scalar g. Even simpler than RMSNorm. Used in some transformer variants.

## Adaptive Normalization (AdaLN)

Dynamically predicts normalization parameters (γ, β) from some conditioning signal:

γ = f_γ(cond), β = f_β(cond)

Used in diffusion models (DiT). The conditioning signal (e.g., timestep embedding) controls the affine transform.

## Weight Normalization

Reparameterizes weight vector as direction × magnitude:

w = g · v / ||v||

g (scalar): learnable magnitude
v (vector): learnable direction

Decouples learning rate from weight scale. Simpler than batch norm but less effective in practice.

## Spectral Normalization

Normalizes weights by their spectral norm:

W = W / σ(W)

σ(W) = max singular value (computed via power iteration). Enforces Lipschitz constraint (≤ 1). Used in GANs for training stability.

## Response Normalization (Local)

Older normalization (AlexNet). Normalizes over adjacent channels:

b_{i,j}^k = a_{i,j}^k / (1 + α · Σ_{k'=k-n/2}^{k+n/2} (a_{i,j}^{k'})²)^β

Rarely used today (BatchNorm is better).

## Comparison

| Method | Computation | Mean Subtraction | Scale | Conditioning |
|--------|------------|-----------------|-------|-------------|
| RMSNorm | O(d) | No | Per-dim γ | No |
| ScaleNorm | O(d) | No | Scalar g | No |
| AdaLN | O(d) | Yes | Per-dim γ,β | Yes |
| WeightNorm | O(|W|) | No | Per-weight g | No |
| SpectralNorm | O(power iter) | No | σ(W) | No |
