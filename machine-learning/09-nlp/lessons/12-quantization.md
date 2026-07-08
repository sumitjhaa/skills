# 09.12 Quantization

## Learning Objectives
- Understand quantization for model compression and speed
- Implement post-training quantization (PTQ) and quantization-aware training (QAT)
- Apply INT8 and INT4 quantization to LLMs
- Analyze perplexity degradation under quantization

## Quantization Basics

### Definition
Map floating-point weights/activations to lower precision:

$$q = \text{round}\left(\frac{r}{\Delta}\right) + z$$

- $r$: real value
- $q$: quantized integer
- $\Delta = \frac{r_{\max} - r_{\min}}{2^b - 1}$: scale factor
- $z$: zero-point

## Post-Training Quantization (PTQ)

### Weight Quantization
- Quantize weights to INT8/INT4
- Typically per-channel (different scale per output channel)
- Minimal accuracy loss at INT8 for most models

### Dynamic Quantization
- Quantize weights statically (offline)
- Quantize activations dynamically at runtime (per batch)
- No calibration data needed

```python
import torch
quantized_model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)
```

### Static Quantization
- Quantize both weights and activations
- Requires calibration data to determine activation ranges
- Faster inference (INT8 matrix multiply)

## Quantization-Aware Training (QAT)

### Method
Simulate quantization during training:

```python
class FakeQuantize(nn.Module):
    def forward(self, x):
        # Quantize + dequantize (simulates hardware)
        q = torch.round(x / self.scale + self.zero_point)
        q = torch.clamp(q, 0, 255)
        return (q - self.zero_point) * self.scale
```

- Insert fake quantization nodes in forward pass
- Backward through straight-through estimator (STE):
  $$\frac{\partial \mathcal{L}}{\partial x} \approx \frac{\partial \mathcal{L}}{\partial \hat{x}}$$

## LLM Quantization

### GPTQ (Optimal Brain Quantization)

**Approach**: Layer-wise quantization using Hessian information:

1. Compute Hessian $H = 2XX^\top$ for each layer
2. Quantize weights greedily, compensating remaining weights:
   $$\delta_w = -\frac{w_q - w}{[H^{-1}]_{qq}} H^{-1}_{:,q}$$

### AWQ (Activation-Aware Weight Quantization)

**Key insight**: Protect important weights based on activation magnitudes:

- Scale up salient channels before quantization
- Per-channel importance: $\text{importance}_i = \text{mean}(|X_i|)$

### Bitsandbytes (QLoRA)

**NF4 quantization**: NormalFloat4 — information-theoretically optimal for normally distributed weights:

$$q = \text{quantile\_normalise}(w, \text{FP4\_levels})$$

### LLM.int8()
- Matrix multiplication at INT8
- Outlier detection (activations > 6σ) processed at FP16
- No accuracy degradation for models up to 175B

## Code: Simple Quantization

```python
import torch
import torch.nn as nn

def quantize_tensor(x, num_bits=8):
    qmin, qmax = 0, 2**num_bits - 1
    min_val, max_val = x.min(), x.max()
    scale = (max_val - min_val) / (qmax - qmin)
    zero_point = qmin - min_val / scale
    q = torch.round(x / scale + zero_point)
    q = torch.clamp(q, qmin, qmax)
    return q, scale, zero_point

def dequantize_tensor(q, scale, zero_point):
    return (q - zero_point) * scale

class QuantizedLinear(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.register_buffer('weight_int8', torch.zeros(out_features, in_features, dtype=torch.int8))
        self.register_buffer('scale', torch.ones(out_features))
        self.register_buffer('zero_point', torch.zeros(out_features, dtype=torch.int8))

    @classmethod
    def from_float(cls, linear_layer):
        module = cls(linear_layer.in_features, linear_layer.out_features)
        w = linear_layer.weight.data
        q, scale, zp = quantize_tensor(w)
        module.weight_int8 = q
        module.scale = scale
        module.zero_point = zp
        return module

    def forward(self, x):
        w = dequantize_tensor(self.weight_int8, self.scale, self.zero_point)
        return nn.functional.linear(x, w)
```

## Quantization Results

### LLM Perplexity (WikiText-2)

| Model | FP16 | INT8 | INT4 (GPTQ) | INT4 (AWQ) |
|-------|------|------|-------------|------------|
| LLaMA-7B | 10.6 | 10.6 | 10.8 | 10.7 |
| LLaMA-13B | 9.6 | 9.6 | 9.8 | 9.7 |
| LLaMA-65B | 8.1 | 8.1 | 8.3 | 8.2 |
| OPT-175B | 8.3 | 8.3 | — | — |

### Memory Reduction
| Model | FP16 | INT8 | INT4 |
|-------|------|------|------|
| LLaMA-7B | 14 GB | 7 GB | 3.5 GB |
| LLaMA-65B | 130 GB | 65 GB | 32.5 GB |
| GPT-175B | 350 GB | 175 GB | 87.5 GB |

## Practical Considerations
- **Perplexity vs task accuracy**: 0.1-0.3 PPL increase is typically acceptable
- **Group size**: INT4 with group size 32 vs 128 vs channel-wise
- **GPU support**: INT8 matrix multiply (Turing+); INT4 (Ampere+)
- **CPU vs GPU**: CPU supports INT8 well; GPU needs CUDA cores with INT8 tensor cores

## References
- Jacob, Kligys, et al., "Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference", CVPR 2018
- Frantar, Ashkboos, et al., "GPTQ: Accurate Post-Training Quantization for Generative Pre-Trained Transformers", ICLR 2023
- Lin, Tang, et al., "AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration", MLSys 2024
- Dettmers, Lewis, Belkada, Zettlemoyer, "LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale", NeurIPS 2022
- Dettmers, Pagnoni, et al., "QLoRA: Efficient Finetuning of Quantized Language Models", NeurIPS 2023
