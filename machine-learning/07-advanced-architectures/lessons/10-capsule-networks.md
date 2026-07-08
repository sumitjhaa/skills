# Lesson 07.10: Capsule Networks

## Learning Objectives
- Understand capsule representation and routing-by-agreement
- Implement dynamic routing between capsules
- Apply margin loss for capsule classification
- Compare with CNNs on viewpoint invariance and part-whole relationships

## Theory
Capsules are groups of neurons that encode the instantiation parameters of an entity (position, size, orientation, etc.).

### Capsule Vector
$$u_i \in \mathbb{R}^d \quad \text{with } \|u_i\| = p_i \in [0,1]$$

- **Direction**: Encodes entity properties (pose)
- **Norm**: Probability that the entity exists

## Dynamic Routing (Sabour et al., 2017)

### Prediction Vectors
Each capsule $i$ in layer $l$ predicts the output of capsule $j$ in layer $l+1$:

$$\hat{u}_{j|i} = W_{ij} u_i$$

- $W_{ij}$: transformation matrix (learned)
- $\hat{u}_{j|i}$: "vote" from lower capsule $i$ for higher capsule $j$

### Routing Coefficients
$$c_{ij} = \frac{\exp(b_{ij})}{\sum_k \exp(b_{ik})}$$

- $b_{ij}$: log prior (initially 0)
- Updated iteratively based on agreement

### Agreement
$$a_{ij} = \hat{u}_{j|i} \cdot v_j$$

- Dot product between prediction and output capsule
- Positive = agreement (increase $b_{ij}$)
- Negative = disagreement (decrease $b_{ij}$)

### Routing Algorithm
```
for _ in range(routing_iterations):
    c = softmax(b)
    s_j = sum_i c_{ij} * hat_u_{j|i}
    v_j = squash(s_j)
    b_{ij} += hat_u_{j|i} · v_j
```

### Squash Function
$$v_j = \frac{\|s_j\|^2}{1 + \|s_j\|^2} \cdot \frac{s_j}{\|s_j\|}$$

- First factor: unit scaling (conditional on norm)
- Second factor: unit vector in direction of $s_j$

## Margin Loss
Separate loss for each capsule class $k$:

$$L_k = T_k \max(0, m^+ - \|v_k\|)^2 + \lambda (1 - T_k) \max(0, \|v_k\| - m^-)^2$$

- $T_k = 1$ if class $k$ is present
- $m^+ = 0.9$, $m^- = 0.1$
- $\lambda = 0.5$: down-weighting of absent classes

## Matrix Capsules with EM Routing (Hinton et al., 2018)

### Capsule Representation
- **Pose matrix**: $M \in \mathbb{R}^{4 \times 4}$ (entity pose)
- **Activation probability**: $a \in [0,1]$ (entity existence)

### EM Routing
Treat lower capsules as producing votes for higher capsules:
1. **E-step**: Assign lower capsules to higher capsules based on likelihood
2. **M-step**: Update higher capsule parameters (mean, variance, activation)

**Gaussian mixture view**: Each higher capsule is a Gaussian cluster in vote space.

## Architecture: CapsNet

### Encoder
```
Conv1 (9x9, 32, stride 1) → PrimaryCaps (32×8D capsules)
→ DigitCaps (16D capsules, 10 classes) → ||v_k|| → class
```

### Decoder (Reconstruction Regularizer)
```
DigitCaps (16D) → FC1 (512) → FC2 (1024) → FC3 (784 = 28x28)
```

- Mask: Only feed correct class capsule vector during training
- Reconstruction loss (MSE) as regularizer

## Code: Capsule Layer with Dynamic Routing

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

def squash(s):
    norm = torch.norm(s, dim=-1, keepdim=True)
    return (norm ** 2 / (1 + norm ** 2)) * (s / (norm + 1e-8))

class CapsuleLayer(nn.Module):
    def __init__(self, in_caps, out_caps, in_dim, out_dim, routing_iter=3):
        super().__init__()
        self.in_caps = in_caps
        self.out_caps = out_caps
        self.routing_iter = routing_iter
        self.W = nn.Parameter(0.1 * torch.randn(out_caps, in_caps, in_dim, out_dim))

    def forward(self, u):
        # u: (B, in_caps, in_dim)
        u = u.unsqueeze(1).expand(-1, self.out_caps, -1, -1)
        # u_hat: (B, out_caps, in_caps, out_dim)
        u_hat = torch.einsum('bocd,ocdi->boci', u, self.W)

        b = torch.zeros(u.shape[0], self.out_caps, self.in_caps, device=u.device)
        for _ in range(self.routing_iter):
            c = F.softmax(b, dim=1)
            s = (c.unsqueeze(-1) * u_hat).sum(dim=2)
            v = squash(s)
            agreement = (u_hat * v.unsqueeze(2)).sum(dim=-1)
            b = b + agreement

        return v
```

## Comparison with CNN

| Aspect | CNN | CapsNet |
|--------|-----|---------|
| Unit | Scalar feature map | Vector capsule |
| Hierarchy | Max pooling | Routing-by-agreement |
| Equivariance | Translation only | Affine (viewpoint) |
| Pose encoding | Implicit in pooling | Explicit in capsule vectors |
| Training | SGD + cross-entropy | Margin loss + reconstruction |
| Routing | None (pooling) | Iterative (3 iterations) |

## Strengths
- **Viewpoint invariance**: Better generalization to novel rotations/affine transforms
- **Part-whole relationships**: Explicit modeling of part-to-whole hierarchies
- **Adversarial robustness**: More robust than CNNs of similar parameter count
- **Reconstruction**: Decoder provides interpretable capsule dimensions

## Limitations
- **Scalability**: Routing is $O(N^2)$ between capsule layers — doesn't scale to large images
- **Speed**: CapsNet is slower than comparable CNNs (routing iterations)
- **Small images only**: Best results on MNIST, modest on CIFAR, poor on ImageNet
- **Capacities**: Capsules underperform attention mechanisms on large-scale vision

## Practical Considerations
- **Routing iterations**: 3 is standard; more may overfit, fewer reduces accuracy
- **Initialization**: Xavier for transformation matrices
- **Regularization**: Reconstruction loss is crucial for clean capsule representations
- **Coordinate addition**: Add one-hot location coordinates to PrimaryCaps for spatial awareness

## References
- Sabour, Frosst, Hinton, "Dynamic Routing Between Capsules", NeurIPS 2017
- Hinton, Sabour, Frosst, "Matrix Capsules with EM Routing", ICLR 2018
- Kosiorek, Sabour, Teh, Hinton, "Stacked Capsule Autoencoders", NeurIPS 2019
- Rajasegaran et al., "DeepCaps: Going Deeper with Capsule Networks", CVPR 2019
- Paik, "Capsule Networks Need an Improved Routing Algorithm", 2020
