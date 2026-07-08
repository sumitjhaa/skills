# 09.10 Efficient Fine-Tuning

## Learning Objectives
- Understand parameter-efficient fine-tuning (PEFT) methods
- Implement LoRA (Low-Rank Adaptation) for LLMs
- Apply prefix tuning and adapter layers
- Compare full fine-tuning vs PEFT for memory and performance

## Full Fine-Tuning

### Limitations
- Full parameter update: 7B model → 28GB (fp16) for parameters + gradients + optimizer states
- Memory: ~4x model size (Adam: 2x for moments, 1x for gradients, 1x for params)
- Storage: One checkpoint per task (7B each)

## LoRA (Low-Rank Adaptation)

### Method
$$W' = W + BA$$

- $W \in \mathbb{R}^{d \times k}$: frozen pretrained weight
- $B \in \mathbb{R}^{d \times r}$, $A \in \mathbb{R}^{r \times k}$: trainable low-rank matrices
- $r \ll \min(d, k)$, typically $r = 8$ or $16$

### Initialisation
- $A \sim \mathcal{N}(0, \sigma^2)$, $B = 0$ (so $W' = W$ at start)
- Scaling: $\frac{\alpha}{r}$ for forward pass (adjust learning rate)

### Apply to Attention
```python
self.q_proj = Linear(d, d)  # frozen
self.k_proj = Linear(d, d)  # frozen
self.v_proj = Linear(d, d)  # frozen
self.o_proj = Linear(d, d)  # frozen

# LoRA on q_proj and v_proj (common choice)
self.q_lora = LoRALayer(d, d, r=8)
self.v_lora = LoRALayer(d, d, r=8)
```

### Memory Savings
| Model | Full FT | LoRA (r=8) |
|-------|---------|------------|
| LLaMA-7B | 112 GB | 16 GB |
| LLaMA-13B | 208 GB | 26 GB |
| LLaMA-65B | 1040 GB | 96 GB |

## Adapters

### Architecture
```
LayerNorm → Down-project (d → m) → ReLU → Up-project (m → d) → Residual
```

- $m$: bottleneck dimension (64-512)
- Insert after each Transformer sublayer
- Bottleneck add ~3-5% parameters

## Prefix Tuning

### Method
Prepend $k$ learnable virtual tokens to input:

$$z = [PREFIX; x]$$

- $PREFIX \in \mathbb{R}^{k \times d}$: trainable prefix vectors
- Only prefix parameters are updated
- $k = 10$ typically sufficient

## Prompt Tuning

### Simplified Prefix Tuning
- Only prepend to input embeddings (not every layer)
- 1-100 virtual tokens
- Comparable to full fine-tuning for large models (100B+)

## Code: LoRA Layer

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class LoRALayer(nn.Module):
    def __init__(self, in_features, out_features, r=8, alpha=16):
        super().__init__()
        self.lora_a = nn.Parameter(torch.randn(in_features, r) * 0.01)
        self.lora_b = nn.Parameter(torch.zeros(r, out_features))
        self.scaling = alpha / r

    def forward(self, x):
        return (x @ self.lora_a @ self.lora_b) * self.scaling

class LoRALinear(nn.Module):
    def __init__(self, original_linear, r=8, alpha=16):
        super().__init__()
        self.linear = original_linear  # frozen
        self.linear.weight.requires_grad = False
        self.lora = LoRALayer(
            original_linear.in_features,
            original_linear.out_features,
            r, alpha
        )

    def forward(self, x):
        return self.linear(x) + self.lora(x)
```

## PEFT Comparison

| Method | Trainable Params | Memory | Performance vs Full FT | 
|--------|-----------------|--------|----------------------|
| Adapter | ~3-5% | Low | ~95-100% |
| LoRA (r=8) | ~0.5-1% | Very low | ~96-100% |
| Prefix Tuning | ~0.1% | Low | ~90-98% |
| Prompt Tuning | ~0.01% | Very low | ~80-95% |
| Full FT | 100% | High | 100% |

## Practical Considerations
- **Which layers**: Apply LoRA to attention projection matrices (q, v best)
- **Rank selection**: r=8 for most tasks; r=64 for complex tasks
- **Combining adapters**: Merge multiple LoRA modules for multi-task inference
- **Quantization + LoRA**: QLoRA (4-bit quantisation + LoRA) enables 65B model on single GPU

## References
- Hu, Shen, et al., "LoRA: Low-Rank Adaptation of Large Language Models", ICLR 2022
- Houlsby, Giurgiu, et al., "Parameter-Efficient Transfer Learning for NLP (Adapters)", ICML 2019
- Li & Liang, "Prefix-Tuning: Optimizing Continuous Prompts for Generation", ACL 2021
- Lester, Al-Rfou, Constant, "The Power of Scale for Parameter-Efficient Prompt Tuning", EMNLP 2021
- Dettmers, Pagnoni, et al., "QLoRA: Efficient Finetuning of Quantized Language Models", NeurIPS 2023
