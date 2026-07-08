# Lesson 07.16: EBMs (Energy-Based Models)

## Learning Objectives
- Understand energy-based modeling and the partition function
- Implement contrastive divergence for RBM training
- Apply score matching and denoising score matching
- Compare EBM training methods: CD, PCD, score matching, NCE

## Theory
EBMs define a probability distribution via an energy function:

$$p(x; \theta) = \frac{\exp(-E_\theta(x))}{Z(\theta)}$$

- $E_\theta(x)$: energy function (scalar output, low for likely data, high for unlikely)
- $Z(\theta) = \int \exp(-E_\theta(x)) dx$: partition function (intractable for high D)

## Training Challenge
The log-likelihood gradient is:
$$\nabla_\theta \log p(x) = -\nabla_\theta E(x) + \mathbb{E}_{p(x)}[\nabla_\theta E(x)]$$

- First term: decrease energy at data points ("push down")
- Second term: increase energy at model samples ("push up")
- Intractable expectation requires MCMC sampling

## Contrastive Divergence (CD-k)

### Algorithm
1. Start with data sample $x^0$
2. Run $k$ steps of Gibbs sampling: $x^1 \to x^2 \to \dots \to x^k$
3. Approximate gradient:
   $$\nabla_\theta \log p(x^0) \approx -\nabla_\theta E(x^0) + \nabla_\theta E(x^k)$$

- **k=1** often sufficient (bias is small)
- Bias: gradient is biased but works well in practice

### Persistent CD (PCD)
Maintain persistent Markov chains across gradient steps:
- Keep $x_k$ from last update
- Run 1 step of Gibbs from $x_k$ to get $x_{k+1}$
- Use as negative sample

## Score Matching

### Score Function
$$\psi(x) = \nabla_x \log p(x) = -\nabla_x E(x)$$

**Idea**: Match model score to data score without computing $Z$.

### Fisher Divergence
$$L(\theta) = \mathbb{E}_{p_{\text{data}}(x)} \left[ \frac{1}{2} \|\psi_{\text{model}}(x) - \psi_{\text{data}}(x)\|^2 \right]$$

- Integration by parts removes dependence on $\psi_{\text{data}}$:
  $$L(\theta) = \mathbb{E}_{p_{\text{data}}} \left[ \text{Tr}(\nabla_x \psi_\theta(x)) + \frac{1}{2} \|\psi_\theta(x)\|^2 \right] + \text{const}$$

### Denoising Score Matching
Add noise to data and match score of noisy distribution:

$$L(\theta) = \mathbb{E}_{p_\sigma(\tilde{x}|x) p_{\text{data}}(x)} \left[ \frac{1}{2} \|\psi_\theta(\tilde{x}) - \nabla_{\tilde{x}} \log p_\sigma(\tilde{x}|x)\|^2 \right]$$

- $p_\sigma(\tilde{x}|x) = \mathcal{N}(x, \sigma^2 I)$
- $\nabla_{\tilde{x}} \log p_\sigma(\tilde{x}|x) = -(x - \tilde{x}) / \sigma^2$

## Noise Contrastive Estimation (NCE)
Distinguish data from noise samples via logistic regression:

$$L(\theta) = \mathbb{E}_{p_{\text{data}}}[\log \sigma(-E_\theta(x))] + \mathbb{E}_{p_{\text{noise}}}[\log(1 - \sigma(-E_\theta(x)))]$$

- No MCMC sampling needed
- Only works if noise distribution is close to data distribution

## RBM (Restricted Boltzmann Machine)

### Energy
$$E(v, h) = -v^\top W h - b^\top v - c^\top h$$

### Conditional Distributions
$$p(h_j = 1 | v) = \sigma(W_{:,j}^\top v + c_j)$$
$$p(v_i = 1 | h) = \sigma(W_{i,:} h + b_i)$$

### CD-1 Update
$$\Delta W = \mathbb{E}_{\text{data}}[v h^\top] - \mathbb{E}_{\text{recon}}[v h^\top]$$

## Training Method Comparison

| Method | MCMC needed | Bias | Gradient variance | When to use |
|--------|-----------|------|-------------------|-------------|
| CD-k | Short run ($k$ steps) | High (small $k$) | Low | Quick prototyping |
| PCD | Persistent chains | Low (long run) | Medium | More accurate |
| Score matching | No | Zero | High (Hessian) | Continuous data |
| Denoising SM | No | Zero | Medium | Images, continuous |
| NCE | No | Zero (if noise good) | Low | When good noise model known |

## Code: RBM with CD-1

```python
import torch
import torch.nn as nn

class RBM(nn.Module):
    def __init__(self, n_visible, n_hidden):
        super().__init__()
        self.W = nn.Parameter(torch.randn(n_visible, n_hidden) * 0.1)
        self.b = nn.Parameter(torch.zeros(n_visible))
        self.c = nn.Parameter(torch.zeros(n_hidden))

    def sample_h(self, v):
        p_h = torch.sigmoid(v @ self.W + self.c)
        return p_h, torch.bernoulli(p_h)

    def sample_v(self, h):
        p_v = torch.sigmoid(h @ self.W.T + self.b)
        return p_v, torch.bernoulli(p_v)

    def forward(self, v):
        # CD-1
        p_h0, h0 = self.sample_h(v)
        p_v1, v1 = self.sample_v(h0)
        p_h1, _ = self.sample_h(v1)
        
        # Positive and negative phase
        positive = v.T @ p_h0
        negative = v1.T @ p_h1
        
        # Gradients
        dW = positive - negative
        db = (v - v1).sum(dim=0)
        dc = (p_h0 - p_h1).sum(dim=0)
        
        return -torch.mean(v * torch.log(p_v1 + 1e-8) + 
                          (1 - v) * torch.log(1 - p_v1 + 1e-8))
```

## Practical Considerations
- **Initialization**: Small random weights; zero visible/hidden biases
- **Momentum**: Use Nesterov momentum for faster convergence
- **Gibbs steps**: CD-1 for most tasks; CD-3 or PCD for better quality
- **Free energy**: Monitor $F(v) = -b^\top v - \sum_j \log(1 + \exp(W^\top v + c)_j)$
- **Reconstruction error**: Poor proxy for log-likelihood; use AIS for evaluation

## Limitations
- **Intractable likelihood**: Can't compute $p(x)$ exactly; requires AIS for evaluation
- **MCMC mixing**: Complex distributions require many Gibbs steps to mix
- **High dimension**: Harder to scale than likelihood-based models (flows, diffusion)
- **Mode covering**: EBMs tend to cover all modes but may spread probability mass too thin

## References
- Hinton, "Training Products of Experts by Minimizing Contrastive Divergence", Neural Computation 2002
- LeCun, Chopra, Hadsell, Ranzato, Huang, "A Tutorial on Energy-Based Learning", 2006
- Song & Ermon, "Generative Modeling by Estimating Gradients of the Data Distribution", NeurIPS 2019
- Hyvärinen, "Estimation of Non-Normalized Statistical Models by Score Matching", JMLR 2005
- Gutmann & Hyvärinen, "Noise-Contrastive Estimation of Unnormalized Statistical Models", JMLR 2012
