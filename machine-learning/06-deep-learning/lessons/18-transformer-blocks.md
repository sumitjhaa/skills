# 06.18 Transformer Blocks

The Transformer block combines attention with feedforward layers, residual connections, and normalization.

## Encoder Block

```
x → [LayerNorm → Multi-Head Self-Attention] → + → Dropout
  → [LayerNorm → FeedForward] → + → Dropout → output
```

Each sub-layer has:
- Pre-normalization (LayerNorm before the sub-layer)
- Residual connection (add input to output)
- Dropout after addition

## FeedForward Network (FFN)

FFN(x) = W₂ · ReLU(W₁ · x + b₁) + b₂

Two linear layers with a non-linearity. Inner dimension is typically 4x the model dimension.

## Decoder Block

```
x → [LayerNorm → Masked Self-Attention] → +
  → [LayerNorm → Cross-Attention (K,V from encoder)]
  → + → [LayerNorm → FFN] → + → output
```

Has an additional cross-attention sub-layer. Self-attention is masked for autoregressive generation.

## Key Design Choices

- **Pre-norm vs Post-norm**: Pre-norm (LayerNorm before sub-layer) is more stable and common in modern transformers
- **Number of heads**: Typically 8-16 for base models
- **FFN ratio**: Usually 4 (d_model → 4·d_model → d_model)
- **Dropout**: Typically 0.1

## Complexity

Each block: O(n² · d + n · d²) per layer
- n: sequence length
- d: model dimension

## Gradient Flow

Residual connections ensure gradients flow directly backward. LayerNorm prevents activation explosion.

## Code Reference

`code/18.py`: Full transformer encoder/decoder block implementation.
