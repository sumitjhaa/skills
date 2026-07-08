# 09.13 Pruning

## Learning Objectives
- Understand magnitude-based and structured pruning
- Implement gradual pruning during training
- Apply SparseGPT for one-shot LLM pruning
- Analyze accuracy-sparsity trade-offs

## Pruning Basics

### Types
- **Unstructured**: Remove individual weights (produces sparse matrices)
- **Structured**: Remove entire neurons, heads, or layers (hardware-friendly)
- **Semi-structured**: N:M sparsity (2 out of 4 weights non-zero)

### Magnitude Pruning
Remove weights with smallest absolute value:

$$w_i = \begin{cases} w_i & \text{if } |w_i| > \text{threshold} \\ 0 & \text{otherwise} \end{cases}$$

Keep top $k\%$ by magnitude → $k$% sparsity.

## Gradual Pruning

### Schedule
Sparsity increases over training:

$$s_t = S_f + (S_i - S_f) \left(1 - \frac{t - t_0}{\Delta t}\right)^3$$

- $S_i$: initial sparsity (0%)
- $S_f$: final sparsity (90%)
- Cubic schedule works well

### Rewinding
After pruning, rewind weights to pre-training values (Lottery Ticket Hypothesis).

## Movement Pruning

### Criteria
$$\text{importance}(w_i) = \left| \frac{\partial \mathcal{L}}{\partial w_i} \cdot w_i \right|$$

- Prune weights with smallest importance score
- Accounts for both magnitude and gradient

## Structured Pruning

### Attention Head Pruning
Remove least important heads:

$$\text{importance}(h) = \mathbb{E}_{x \sim D} [\|A_h(x)\|]$$

- Prune heads with low attention norm
- Multi-head attention can tolerate head removal

### Layer Drop
Remove entire layers (e.g., 24→12 layers):
- Importance based on output similarity between consecutive layers
- Drop layers with high cosine similarity

## SparseGPT

### One-Shot Pruning
Prune LLM weights without retraining:

**Approach**: Layer-wise Hessian-based pruning:
1. Compute Hessian $H = 2XX^\top$ for layer weights
2. Prune weights with minimal reconstruction error:
   $$w^* = \arg\min_{w} \|w - \hat{w}\|_H^2$$
3. Adapt remaining weights to compensate for pruned ones

### Results
| Model | Dense PPL | 50% Sparse PPL | 60% Sparse PPL |
|-------|----------|----------------|----------------|
| OPT-125M | 27.4 | 28.2 | 29.5 |
| LLaMA-7B | 10.6 | 11.0 | 11.5 |
| LLaMA-65B | 8.1 | 8.3 | 8.7 |

## N:M Sparsity (NVIDIA)

### Pattern
In each group of $M$ weights, exactly $N$ are non-zero:

- 2:4 sparsity: 50% sparsity, 4-element groups
- Supported on Ampere+ GPU tensor cores

### Inference Speedup
2:4 sparse matrix multiply is 2x faster than dense (theoretical).

## Code: Magnitude Pruning

```python
import torch
import torch.nn as nn
import torch.nn.utils.prune as prune

class PruningManager:
    def __init__(self, model, sparsity=0.9):
        self.model = model
        self.sparsity = sparsity
        self.pruned_params = []

    def apply_global_l1_unstructured(self):
        # Collect all weight tensors
        parameters_to_prune = []
        for name, module in self.model.named_modules():
            if isinstance(module, nn.Linear):
                parameters_to_prune.append((module, 'weight'))
        
        prune.global_unstructured(
            parameters_to_prune,
            pruning_method=prune.L1Unstructured,
            amount=self.sparsity,
        )
        self.pruned_params = parameters_to_prune

    def remove_pruning(self):
        # Make pruning permanent
        for module, name in self.pruned_params:
            prune.remove(module, name)

    def apply_structured(self, amount=0.3):
        # Structured: prune entire neurons (L2 norm of weights)
        for name, module in self.model.named_modules():
            if isinstance(module, nn.Linear):
                prune.ln_structured(
                    module, 'weight', amount=amount, n=2, dim=0
                )

def count_sparsity(model):
    total = 0
    nonzero = 0
    for param in model.parameters():
        total += param.numel()
        nonzero += param.count_nonzero().item()
    return 1 - nonzero / total
```

## Practical Considerations
- **Sparsity level**: 50-70% for minimal accuracy loss; >80% significant degradation
- **Hardware support**: Unstructured sparsity needs custom kernels (not widely supported)
- **N:M sparsity**: Only NVIDIA Ampere+; 2:4 gives 2x speedup
- **Pruning + quantization**: Combine for maximum compression
- **Retraining**: Gradual pruning with retraining outperforms one-shot

## References
- Han, Pool, Tran, Dally, "Learning both Weights and Connections for Efficient Neural Networks", NeurIPS 2015
- Zhu, Gupta, "To Prune, or Not to Prune: Exploring the Efficacy of Pruning for Model Compression", ICLR 2018
- Frankle & Carbin, "The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks", ICLR 2019
- Frantar & Alistarh, "SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot", ICML 2023
- Mishra, Latorre, et al., "Accelerating Sparse Deep Neural Networks (N:M Sparsity)", 2021
