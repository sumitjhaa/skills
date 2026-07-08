# 06.07 Activations

Activation functions introduce non-linearity into neural networks. Without them, stacked linear layers are equivalent to a single linear layer.

## Sigmoid

σ(x) = 1 / (1 + e^{-x})

Range: (0, 1). Suffers from vanishing gradient for large |x|. Historically used but now rare in hidden layers.

## Tanh

tanh(x) = (e^{x} - e^{-x}) / (e^{x} + e^{-x})

Range: (-1, 1). Zero-centered, but still saturating.

## ReLU (Rectified Linear Unit)

ReLU(x) = max(0, x)

Range: [0, ∞). Non-saturating, cheap, sparse. Dead neuron problem when weights never activate.

## Leaky ReLU / PReLU

LeakyReLU(x) = max(αx, x) for small α (e.g., 0.01). PReLU learns α.

## ELU / SELU

ELU: x if x > 0, else α(e^x - 1). Smooth for negative values. SELU is self-normalizing.

## Swish / SiLU

Swish(x) = x · σ(βx). Smooth, non-monotonic. Often outperforms ReLU in deep nets.

## GELU (Gaussian Error Linear Unit)

GELU(x) = x · Φ(x) where Φ is the standard Gaussian CDF.

Used in GPT, BERT, ViT. Smooth approximation: x · σ(1.702x).

## Comparison Table

| Function | Range | Smooth | Zero-Centered | Vanishing Grad |
|----------|-------|--------|---------------|----------------|
| Sigmoid  | (0,1) | Yes    | No            | Yes            |
| Tanh     | (-1,1)| Yes    | Yes           | Yes            |
| ReLU     | [0,∞) | No     | No            | No             |
| Leaky ReLU | (-∞,∞) | No  | No            | No             |
| GELU     | (-∞,∞)| Yes    | Approx        | No             |
| Swish    | (-∞,∞)| Yes    | No            | No             |

## Derivatives

Each activation has a simple derivative expression, critical for autograd:

- σ': σ(1-σ)
- tanh': 1 - tanh²
- ReLU': 0 if x < 0 else 1
- GELU': Φ(x) + x · φ(x) (approx)
