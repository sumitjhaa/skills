# 06.29 Gradient Noise / Clipping

Stabilizing training dynamics by modifying gradients before the optimizer step.

## Gradient Clipping

Limit the gradient magnitude to prevent exploding gradients:

**Clip by value**: g_i = clamp(g_i, -clip_value, clip_value)

**Clip by norm**: g = g · (clip_norm / ||g||) if ||g|| > clip_norm

Norm clipping is preferred — preserves direction, only rescales magnitude.

```python
total_norm = sqrt(Σ ||g_i||² for each parameter)
if total_norm > clip_norm:
    for g in gradients:
        g *= clip_norm / total_norm
```

Common values: 0.5-10.0. 1.0 is typical for transformers, 5.0 for RNNs.

## Why Clipping Works

Gradients can explode due to:
- Sharp loss landscapes
- Poor conditioning
- Long-range dependencies (RNNs)

Clipping ensures every step stays within a trust region.

## Gradient Noise

Add Gaussian noise to gradients:

g = g + N(0, σ² · η_t)

where σ² controls noise magnitude and η_t is the learning rate at step t.

Benefits:
- Regularization (similar to SGD's implicit noise)
- May help escape sharp minima
- Improves generalization

From Neelakantan et al. (2015): adding noise to gradients improves training of deep networks.

## Gradient Gaussianization

Replace gradient distribution with Gaussian (via rank-preserving transform). Stabilizes training for non-Gaussian gradient distributions.

## Gradient Centralization

g = g - mean(g)

Subtract mean gradient. Zero-centering improves training stability. Related to batch normalization's effect.

## Adaptive Gradient Clipping (AGC)

Clip based on parameter norm rather than gradient norm:

clip = param_norm / grad_norm * clip_value

If gradient is large relative to parameter norm, clip more. Used in NFNets (Normalizer-Free networks).

## When to Use

| Technique | When |
|-----------|------|
| Norm clipping | RNNs, Transformers, GANs |
| Value clipping | Simple networks, sanity check |
| Gradient noise | Improving generalization |
| AGC | Normalizer-free networks |
