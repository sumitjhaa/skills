# Lesson 07.27: NAS (Neural Architecture Search)

## Learning Objectives
- Understand NAS search spaces and strategies
- Implement DARTS with bi-level optimization
- Apply ENAS for efficient architecture search
- Analyze search-evaluation gap and regularization

## Theory
NAS automates neural network architecture design:

$$\alpha^* = \arg\max_{\alpha \in \mathcal{A}} \text{ValAcc}(f_{\alpha, w^*})$$
$$\text{s.t. } w^* = \arg\min_w \mathcal{L}_{\text{train}}(f_{\alpha, w})$$

- $\alpha$: architecture parameters
- $w$: network weights

## Search Space Design

### Macro Search
Search entire network topology (layer types, connections, skip connections).

### Cell-Based Search
Search a cell (motif) repeated throughout network:

```
Normal cell: preserve resolution → extract features
Reduction cell: reduce resolution → double channels
```

### Search Space Types

| Search Space | Size | When to Use |
|-------------|------|-------------|
| Chain | O(ops × layers) | Simple tasks |
| Cell-based (NASNet) | O(ops^edges) | Image classification |
| Hierarchical | O(levels^ops) | Large-scale |
| Graph-based | Variable | Complex topologies |

## Search Strategies

### Reinforcement Learning (NASNet)
Controller (RNN) generates architecture strings:
```
RNN hidden → softmax over ops → softmax over skip connections → architecture
```

- Reward: validation accuracy after training
- REINFORCE rule: $\nabla \log p(\alpha) \cdot \text{Reward}$
- **Expensive**: ~20,000 GPU-hours for NASNet

### Evolutionary (AmoebaNet)
```
Population → Tournament selection → Mutation/Crossover → New architectures
```

- **Aging evolution**: Remove oldest architectures
- **Regularized evolution**: Prefer newer architectures with same accuracy
- **Mutation**: Change one operation or skip connection

### DARTS (Differentiable Architecture Search)

Continuous relaxation of discrete choices:

$$\bar{o}^{(i,j)}(x) = \sum_{o \in \mathcal{O}} \frac{\exp(\alpha_o^{(i,j)})}{\sum_{o'} \exp(\alpha_{o'}^{(i,j)})} \cdot o(x)$$

- $\alpha_o^{(i,j)}$: weight of operation $o$ between node $i$ and $j$
- After search: discretize by argmax

#### Bi-Level Optimization
$$\min_\alpha \mathcal{L}_{\text{val}}(w^*(\alpha), \alpha)$$
$$\text{s.t. } w^*(\alpha) = \arg\min_w \mathcal{L}_{\text{train}}(w, \alpha)$$

**Approximation**: Single step of $w$ update between $\alpha$ updates:

$$\nabla_\alpha \mathcal{L}_{\text{val}} \approx \nabla_\alpha \mathcal{L}_{\text{val}} - \xi \nabla^2_{\alpha, w} \mathcal{L}_{\text{val}} \cdot \nabla_w \mathcal{L}_{\text{train}}$$

### ENAS (Efficient NAS)
Share weights across all architectures:
- DAG controller samples subgraph
- Shared weights trained on all sampled architectures
- **Cost**: ~1 GPU-day (vs 20000 for NASNet)

## Code: DARTS Continuous Relaxation

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class MixedOp(nn.Module):
    """Continuous relaxation of discrete operation choice"""
    def __init__(self, C_in, C_out, stride):
        super().__init__()
        self._ops = nn.ModuleList()
        for op in ['sep_conv_3x3', 'sep_conv_5x5', 'avg_pool_3x3', 
                    'max_pool_3x3', 'skip_connect']:
            self._ops.append(OPS[op](C_in, C_out, stride))

    def forward(self, x, weights):
        # weights: softmax over ops for this edge
        return sum(w * op(x) for w, op in zip(weights, self._ops))

class DARTSCell(nn.Module):
    def __init__(self, C_in, C_out, n_nodes=4):
        super().__init__()
        self.preproc0 = nn.Sequential(nn.ReLU(), nn.Conv2d(C_in, C_out, 1))
        self.preproc1 = nn.Sequential(nn.ReLU(), nn.Conv2d(C_out, C_out, 1))
        self._ops = nn.ModuleList()
        self._n_nodes = n_nodes
        for i in range(n_nodes):
            for j in range(2 + i):  # connections from previous nodes
                op = MixedOp(C_out, C_out, 1)
                self._ops.append(op)

    def forward(self, s0, s1, weights):
        s0 = self.preproc0(s0)
        s1 = self.preproc1(s1)
        states = [s0, s1]
        offset = 0
        for i in range(self._n_nodes):
            s = sum(self._ops[offset + j](h, weights[offset + j])
                    for j, h in enumerate(states))
            offset += len(states)
            states.append(s)
        return torch.cat(states[-self._n_nodes:], dim=1)
```

## Evaluation Strategies

| Strategy | Description | Cost | Accuracy correlation |
|----------|-------------|------|---------------------|
| Full training | Train each architecture fully | Very high | Perfect |
| Weight sharing | Shared weights across architectures | Low | Moderate |
| Network morphism | Grow from known good architecture | Moderate | Good |
| Proxy task | Small dataset, few epochs | Low | Moderate |
| One-shot | Supernet + weight sharing | Very low | Moderate |

## Practical Considerations
- **Search-evaluation gap**: Best architecture in search may not be best after full training
- **DARTS failure modes**: Skip connections dominate (over-regularization); use auxiliary losses
- **Regularization**: Dropout, weight decay, and auxiliary towers for fair comparison
- **Latency constraints**: Add FLOPs/latency to loss for edge deployment
- **Multi-objective NAS**: Optimize accuracy + latency + energy

## Limitations
- **Computational cost**: Even efficient NAS (ENAS) requires 1+ GPU-days
- **Transferability**: Cell found on CIFAR may not transfer to other domains
- **Evaluation noise**: Validation accuracy variance makes comparison unreliable
- **Search space bias**: Results depend heavily on search space design
- **Overfitting**: May find architectures that overfit to specific augmentations

## References
- Zoph & Le, "Neural Architecture Search with Reinforcement Learning", ICLR 2017
- Liu, Simonyan, Yang, "DARTS: Differentiable Architecture Search", ICLR 2019
- Pham, Guan, Uszkoreit, Efros, "Efficient Neural Architecture Search via Parameter Sharing (ENAS)", ICML 2018
- Real, Aggarwal, Huang, Le, "Regularized Evolution for Image Classifier Architecture Search (AmoebaNet)", AAAI 2019
- Tan, Chen, Pang, et al., "MnasNet: Platform-Aware Neural Architecture Search for Mobile", CVPR 2019
