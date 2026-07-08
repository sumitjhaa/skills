# 09.14 Mixture of Experts (MoE)

## Learning Objectives
- Understand mixture-of-experts architecture
- Implement sparse MoE with top-k routing
- Apply MoE in Transformers (Switch Transformer, Mixtral)
- Analyze load balancing and expert capacity

## MoE Architecture

### Layer Definition
$$\text{MoE}(x) = \sum_{i=1}^{E} g_i(x) \cdot E_i(x)$$

- $E_i$: expert networks (typically FFN layers)
- $g_i(x)$: gating/routing function
- $E$: number of experts

### Sparse Routing (Top-k)
$$g(x) = \text{softmax}(\text{TopK}(W_g x, k))$$

- Only top-$k$ experts are activated
- $k=2$ for most implementations
- $E=8$ to $64$ experts typical

## Switch Transformer

### Simplification
$$g(x) = \text{softmax}(W_g x)$$

- Route to single expert ($k=1$)
- Simpler routing, less computation
- Better load balancing

### Expert Capacity
$$\text{Capacity} = \frac{\text{tokens per batch}}{\text{num experts}} \times \text{capacity factor}$$

- Capacity factor: 1.0-2.0
- Higher = more buffer for imbalanced routing
- Overflow: tokens not routed (dropped)

### Load Balancing Loss
$$\mathcal{L}_{\text{aux}} = \alpha \cdot E \cdot \sum_{i=1}^E f_i \cdot P_i$$

- $f_i$: fraction of tokens routed to expert $i$
- $P_i$: fraction of router probability allocated to expert $i$
- $\alpha$: auxiliary loss coefficient (typically 0.01)

## Mixtral 8x7B

### Architecture
- 8 experts, top-2 routing
- Each expert has ~7B parameters (but same as dense 7B)
- Mixtral: 47B total, ~13B active per token

### Performance
- Matches LLaMA-70B with 4x fewer active parameters
- Outperforms GPT-3.5 on most benchmarks

## Expert Parallelism

### Distributed Setup
```
GPU 0: Experts 0, 1, 2
GPU 1: Experts 3, 4, 5
GPU 2: Experts 6, 7
GPU 3: No experts (shared)
```

- All-to-all communication for expert routing
- Each GPU computes its assigned experts
- Results merged via all-reduce

## Code: Sparse MoE Layer

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SparseMoE(nn.Module):
    def __init__(self, d_model, d_ff, num_experts=8, top_k=2):
        super().__init__()
        self.num_experts = num_experts
        self.top_k = top_k
        self.gate = nn.Linear(d_model, num_experts, bias=False)
        self.experts = nn.ModuleList([
            nn.Sequential(
                nn.Linear(d_model, d_ff),
                nn.ReLU(),
                nn.Linear(d_ff, d_model),
            ) for _ in range(num_experts)
        ])

    def forward(self, x):
        B, T, D = x.shape
        x_flat = x.reshape(-1, D)
        
        # Gating
        gate_logits = self.gate(x_flat)  # (B*T, E)
        weights, indices = gate_logits.topk(self.top_k, dim=-1)
        weights = F.softmax(weights, dim=-1)
        
        # Route tokens to experts
        output = torch.zeros_like(x_flat)
        for expert_idx in range(self.num_experts):
            mask = (indices == expert_idx).any(dim=-1)
            if not mask.any():
                continue
            expert_input = x_flat[mask]
            expert_output = self.experts[expert_idx](expert_input)
            # Sum weighted outputs
            w = weights[mask][indices[mask] == expert_idx]
            output[mask] += w * expert_output
        
        return output.reshape(B, T, D)
```

## Load Balancing Techniques

| Method | Description | Pros | Cons |
|--------|-------------|------|------|
| Auxiliary loss | Add routing balance to loss | Simple | Small quality impact |
| Expert capacity | Cap tokens per expert | Prevents overflow | Dropped tokens |
| Z-loss | Penalise large gate logits | Stable training | Extra hyperparameter |
| Batch prioritisation | Route high-confidence tokens first | Better use | Complex implementation |

## MoE Benchmarks

| Model | Active Params | Total Params | MMLU | Reasoning |
|-------|--------------|-------------|------|-----------|
| Switch-Base | 0.5B | 3.5B (7 experts) | — | — |
| Switch-Large | 2.8B | 28B (7 experts) | — | — |
| Mixtral 8x7B | 13B | 47B | 70.6 | Outperforms GPT-3.5 |
| DeepSeek-V2 | 21B | 236B | 78.5 | Fine-grained MoE |

## Practical Considerations
- **Batch size**: Larger batches help load balancing (more tokens to distribute)
- **Expert count**: 8-64 experts typical; more experts = sparser = harder to train
- **Communication overhead**: All-to-all is expensive; overlap computation with communication
- **Hardware**: MoE benefits from high bandwidth (NVLink > InfiniBand)
- **Stable training**: Use lower learning rate, auxiliary loss, and gradient clipping

## References
- Shazeer, Mirhoseini, et al., "Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer", ICLR 2017
- Fedus, Zoph, Shazeer, "Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity", JMLR 2022
- Jiang, Sablayrolles, et al., "Mixtral of Experts", 2024
- Lepikhin, Lee, et al., "GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding", ICLR 2021
- DeepSeek-AI, "DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model", 2024
