# Lesson 07.07: Hypernetworks

## Learning Objectives
- Understand hypernetwork architecture for weight generation
- Implement static and dynamic hypernetworks
- Apply hypernetworks to meta-learning and multi-task learning
- Analyze parameter efficiency and capacity trade-offs

## Theory
A hypernetwork $\mathcal{H}_\phi$ generates weights $\theta$ for a target network $\mathcal{T}_\theta$:

$$\theta = \mathcal{H}_\phi(z)$$

- $z$: embedding (static or input-dependent)
- $\phi$: hypernetwork parameters
- $\theta$: target network parameters

## Why Hypernetworks?
| Challenge | Solution |
|-----------|----------|
| Many tasks, each needs separate model | Generate task-specific weights from task embedding |
| Large models, limited memory | Factorize weights via low-rank generation |
| Dynamic computation | Generate weights conditioned on input |
| Neural architecture search | Predict weights for candidate architectures |

## Static Hypernetworks
Learn a fixed mapping from embedding space to weights:

$$\theta = W_h z + b_h$$

- Training: jointly optimize $\phi$ and target network parameters
- After training: target network performs task with generated weights

### Factorization
For layer $l$ with weight matrix $W^{(l)} \in \mathbb{R}^{m \times n}$:

$$W^{(l)} = A^{(l)} B^{(l)\top}$$

- $A^{(l)} \in \mathbb{R}^{m \times k}$, $B^{(l)} \in \mathbb{R}^{n \times k}$
- $k \ll m, n$ — low-rank factorization
- Hypernetwork generates $A^{(l)}$ and $B^{(l)}$ from shared embedding $z$

## Dynamic Hypernetworks
Generate weights conditioned on the current input:

$$\theta_t = \mathcal{H}_\phi(z(x_t))$$

- $z(x_t)$: input-dependent embedding (e.g., from encoder)
- Enables adaptive computation per input
- Used in HyperRNN/HyperLSTM

### HyperRNN
$$h_t = \sigma(W_t^{(h)} x_t + U_t^{(h)} h_{t-1})$$

where $W_t^{(h)} = \mathcal{H}_\phi(z_t)$ depends on the current input.

## Meta-Learning with Hypernetworks
**Few-shot learning**: Task embedding $\tau$ from support set → generate task-specific classifier head:

$$\theta_{\text{classifier}} = \mathcal{H}_\phi(\tau)$$

- $\tau = \frac{1}{K} \sum_{k=1}^K f_\text{enc}(x_k, y_k)$: task representation
- No inner-loop fine-tuning needed

## Code: Simple Hypernetwork

```python
import torch
import torch.nn as nn

class Hypernetwork(nn.Module):
    def __init__(self, embedding_dim, target_shapes, hidden_dim=128):
        super().__init__()
        self.target_shapes = target_shapes
        total_params = sum(s[0] * s[1] for s in target_shapes)
        
        self.net = nn.Sequential(
            nn.Linear(embedding_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, total_params),
        )

    def forward(self, z):
        all_weights = self.net(z)
        weights = []
        offset = 0
        for shape in self.target_shapes:
            n = shape[0] * shape[1]
            weights.append(all_weights[offset:offset + n].reshape(shape))
            offset += n
        return weights

class TargetWithHyper(nn.Module):
    def __init__(self, hypernet, input_dim, output_dim):
        super().__init__()
        self.hypernet = hypernet
        self.input_dim = input_dim

    def forward(self, x, z):
        w1, b1, w2, b2 = self.hypernet(z)
        h = torch.relu(x @ w1 + b1)
        return h @ w2 + b2
```

## Parameter Efficiency

| Scenario | Direct params | Hypernetwork params | Ratio |
|----------|--------------|-------------------|-------|
| 10 tasks with 100K-param nets | 1M | 200K + 10K task emb | 4.8x |
| 100 tasks | 10M | 200K + 100K emb | 33x |
| Dynamic (per input) | N/A | 200K + encoder | Flexible |

## Advanced Variants

| Variant | Key Idea | Application |
|---------|----------|-------------|
| Chunked Hypernet | Generate weights progressively | Very large target nets |
| CoordConv Hyper | Hypernetwork takes coordinates | IR representations |
| Transformer Hyper | Cross-attention for weight generation | In-context learning |
| Gradient Hyper | Hypernetwork outputs learning rates | Optimization |

## Limitations
- **Training difficulty**: Two-level optimization can be unstable (especially dynamic)
- **Capacity bottleneck**: Hypernetwork capacity limits target network complexity
- **Generalization gap**: May not generalize to unseen task embeddings
- **Inference cost**: Generating weights adds forward pass overhead
- **Interpretability**: Generated weights are less interpretable than directly learned

## Practical Considerations
- **Embedding dimension**: 16-128 typically sufficient; larger for more tasks
- **Weight normalization**: Generated weights may need normalization for stable training
- **Shared embeddings**: Initialize task/sample embeddings randomly, train jointly
- **Progressive growing**: Start with small target net, gradually increase capacity
- **Bottleneck**: Use low-rank factorization to keep hypernetwork manageable

## References
- Ha, Dai, Le, "Hypernetworks", ICLR 2017
- von Oswald, Henning, Sacramento, "Continual Learning with Hypernetworks", ICLR 2020
- Littwin & Wolf, "The Mutex Dataset and the Performance of Hypernetworks", 2020
- Sendera et al., "On the Role of Hypernetworks in Learning", 2020
- Zhao et al., "Dynamic Hypernetworks for Neural Machine Translation", ACL 2020
