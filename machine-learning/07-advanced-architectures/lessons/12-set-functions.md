# Lesson 07.12: Set Functions (Deep Sets, PointNet, Set Transformer)

## Learning Objectives
- Understand permutation invariance for set-structured data
- Implement Deep Sets with sum/mean aggregation
- Apply PointNet for 3D point cloud processing
- Design Set Transformer with induced set attention

## Theory
A set function $f: 2^{\mathbb{R}^d} \to \mathbb{R}$ operates on unordered sets of elements.

### Permutation Invariance
$$f(\{x_1, \dots, x_n\}) = f(\{x_{\pi(1)}, \dots, x_{\pi(n)}\}) \quad \forall \pi \in S_n$$

### Representation Theorem (Zaheer et al., 2017)
Any permutation-invariant function can be decomposed as:

$$f(X) = \rho\left(\sum_{x \in X} \phi(x)\right)$$

- $\phi$: per-element feature transformation (MLP)
- $\rho$: aggregation-to-output transformation (MLP)
- Sum can be replaced by mean, max, or any commutative operation

## Deep Sets

### Architecture
```
Input set X → φ(x_i) = MLP(x_i) → sum/mean → ρ(r) = MLP(r) → output
```

### Why Sum, Not Mean?
- **Sum** preserves cardinality information (can tell if more elements = larger set)
- **Mean** is better when cardinality is irrelevant
- **Max** captures presence/absence of features

### Universal Approximation
Deep Sets with sum aggregation can approximate any permutation-invariant function given sufficient capacity in $\phi$ and $\rho$.

## PointNet

### Architecture
```
Input points (n × 3) → Shared MLP (64-64-64-128-1024) → Max pool → MLP (512-256-k) → output
```

### Key Innovations
- **Symmetric function**: Max pooling for permutation invariance
- **T-Net**: Small network predicting affine transformation for spatial alignment
- **Local + global**: Concatenate per-point features with global max-pooled feature for segmentation

### PointNet for Classification
```
n × 3 → T-Net(3) → MLP[64] → T-Net(64) → MLP[64,128,1024] → max pool (n,1024) → MLP[512,256,k]
```

### PointNet for Segmentation
```
Per-point features (n,1088) = concat[per-point (n,64), global (1,1024) repeated n times]
→ MLP[512,256,128,m] → per-point class scores
```

## Set Transformer

### Induced Set Attention Block (ISAB)
For very large sets, cross-attention with inducing points reduces complexity:

$$\text{ISAB}(X) = \text{MAB}(X, \text{MAB}(I, X))$$

- $I$: $m$ inducing points (learnable, $m \ll n$)
- $\text{MAB}(A, B) = \text{LayerNorm}(A + \text{Multihead}(A, B, B))$
- Complexity: $O(nm)$ instead of $O(n^2)$

### Pooling by Multi-Head Attention (PMA)
$$r = \text{MAB}(s, \text{ISAB}(X))$$

- $s$: learnable seed vector
- Produces fixed-size output regardless of set size

## Architecture Comparison

| Model | Aggregation | Complexity | Expressiveness | When to Use |
|-------|-------------|------------|---------------|-------------|
| Deep Sets | Sum/mean/max | $O(n)$ | Universal ($n \to \infty$) | Simple sets, small sets |
| PointNet | Max pool | $O(n)$ | Limited (only max) | Point clouds 3D |
| Set Transformer | Attention | $O(n^2)$ or $O(nm)$ | Very high | Complex sets, large sets |
| Equivariant | Group operations | $O(n)$ | Structured | Molecular data |

## Code: Deep Sets

```python
import torch
import torch.nn as nn

class DeepSets(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.phi = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
        )
        self.rho = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x, mask=None):
        # x: (B, N, D), mask: (B, N) where 1 = valid, 0 = padded
        phi_x = self.phi(x)  # (B, N, H)
        if mask is not None:
            phi_x = phi_x * mask.unsqueeze(-1)
            r = phi_x.sum(dim=1) / mask.sum(dim=1, keepdim=True).clamp(min=1)
        else:
            r = phi_x.mean(dim=1)  # (B, H)
        return self.rho(r)  # (B, O)
```

## Equivariance vs Invariance

| Property | Definition | Example |
|----------|------------|---------|
| Permutation invariance | $f(\pi X) = f(X)$ | Classification | 
| Permutation equivariance | $f(\pi X) = \pi f(X)$ | Segmentation (per-point) |

**Deep Sets**: $\phi$ is equivariant (per-element), $\rho$ is invariant (global).
**PointNet**: Shared MLP = equivariant, max pool = invariant. For segmentation: concat per-point + global for equivariant output.

## Practical Considerations
- **Variable set sizes**: Masking for batch processing; sorting not needed (permutation invariance)
- **Normalization**: Point clouds should be centered and normalized
- **Augmentation**: Random rotation, scaling, jitter for 3D point clouds
- **Memory**: Set Transformer $O(n^2)$ attention — use ISAB for large sets ($n > 512$)

## Applications
- **Point cloud classification/segmentation**: ModelNet40, ShapeNet, S3DIS
- **Anomaly detection**: Set-based representations of events
- **Drug discovery**: Molecules as sets of atoms
- **Social networks**: Graph nodes as sets of neighbors
- **Multi-instance learning**: Bag of instances

## References
- Zaheer, Kottur, Ravanbakhsh, Poczos, Salakhutdinov, Smola, "Deep Sets", NeurIPS 2017
- Qi, Su, Mo, Guibas, "PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation", CVPR 2017
- Lee, Lee, Hwangbo, Lee, Shin, "Set Transformer: A Framework for Attention-based Permutation-Invariant Neural Networks", ICML 2019
- Qi, Yi, Su, Guibas, "PointNet++: Deep Hierarchical Feature Learning on Point Sets in a Metric Space", NeurIPS 2017
- Wagstaff, Fuchs, Engelcke, Posner, Osborne, "On the Limitations of Representing Functions on Sets", ICML 2022
