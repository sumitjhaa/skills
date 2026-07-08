# Lesson 07.11: Neural Processes

## Learning Objectives
- Understand meta-learning with neural processes (NPs)
- Implement conditional and latent neural processes
- Apply attentive aggregation for better predictions
- Quantify uncertainty with stochastic process inference

## Theory
Neural processes combine the flexibility of neural networks with the uncertainty quantification of Gaussian Processes.

### Meta-Learning View
Train on a distribution of functions (tasks), predict for new functions given few context points:

- **Context set**: $C = \{(x_i, y_i)\}_{i=1}^{m}$ — observed points
- **Target set**: $T = \{(x_j, y_j)\}_{j=1}^{n}$ — points to predict (includes context)
- **Output**: Predictive distribution $p(y_T | x_T, C)$

## Conditional Neural Processes (CNP)

### Architecture
$$r = \bigoplus_{i=1}^{m} \text{enc}(x_i, y_i)$$
$$p(y_j | x_j, r) = \text{dec}(x_j, r)$$

- enc: MLP mapping $(x, y) \to h$
- $\bigoplus$: Aggregation operator (mean, sum) — must be permutation invariant
- dec: MLP mapping $(x, r) \to$ parameters of output distribution (e.g., $\mu, \sigma$ for Gaussian)

### Limitations
- **Underconfident**: CNPs are not stochastic — single deterministic path
- **Independent predictions**: Output distribution is factorized (no correlations between targets)
- **Limited expressiveness**: Aggregation captures only global information

## Latent Neural Processes (LNP)

### Architecture
$$z \sim \mathcal{N}(\mu_\phi(C), \sigma_\phi^2(C)) \quad \text{(latent path)}$$
$$r = \bigoplus_{i=1}^{m} \text{enc}(x_i, y_i) \quad \text{(deterministic path)}$$
$$p(y_T | x_T, C) = \mathcal{N}(\text{dec}_\mu(x_T, z, r), \text{dec}_\sigma(x_T, z, r))$$

- **Latent path**: Global latent variable $z$ captures task-level uncertainty
- **Deterministic path**: Local context for fine-grained predictions
- **ELBO training**: $\log p(y_T | x_T, C) \geq \mathbb{E}_{q(z|C)}[\log p(y_T | x_T, z, C)] - \text{KL}[q(z|C) \| p(z)]$

## Attentive Neural Processes (ANP)

### Attention-Based Aggregation
Replace mean aggregation with cross-attention:

$$r_j = \sum_{i=1}^{m} a_{ij} v_i \quad \text{where } a_{ij} = \frac{\exp(k_i \cdot q_j)}{\sum_{i'} \exp(k_{i'} \cdot q_j)}$$

- $k_i = W_K \text{enc}_k(x_i, y_i)$: key for context point $i$
- $q_j = W_Q \text{enc}_q(x_j)$: query for target point $j$
- $v_i = W_V \text{enc}_v(x_i, y_i)$: value for context point $i$

**Benefits**: Each target point attends to relevant context points — adaptive aggregation.

## Architecture Comparison

| Model | Uncertainty | Correlations | Aggregation | Complexity |
|-------|------------|-------------|-------------|------------|
| CNP | Predictive only | No (factorized) | Mean | $O(m + n)$ |
| LNP | Global latent + predictive | No | Mean | $O(m + n)$ |
| ANP | Predictive only | No (factorized) | Cross-attention | $O(mn)$ |
| ConvCNP | Predictive only | Local correlations | Convolution | $O((m+n)d)$ |
| Bootstrapping NP | Global + predictive | No | Mean | $O(mS)$ |

## Code: Conditional Neural Process

```python
import torch
import torch.nn as nn
import torch.distributions as D

class ConditionalNeuralProcess(nn.Module):
    def __init__(self, x_dim=1, y_dim=1, hidden_dim=64):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(x_dim + y_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
        )
        self.decoder = nn.Sequential(
            nn.Linear(x_dim + hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 2 * y_dim),  # mu and log_sigma
        )

    def forward(self, context_x, context_y, target_x):
        # Encode context
        h = self.encoder(torch.cat([context_x, context_y], dim=-1))
        r = h.mean(dim=1, keepdim=True).expand(-1, target_x.shape[1], -1)
        
        # Decode
        dec_input = torch.cat([target_x, r], dim=-1)
        out = self.decoder(dec_input)
        mu, log_sigma = out.chunk(2, dim=-1)
        return D.Normal(mu, torch.exp(log_sigma).clamp(min=1e-6))
```

## Training Objective (ELBO)

$$\mathcal{L} = -\mathbb{E}_{z \sim q_\phi(z|C)}[\log p_\theta(y_T | x_T, z, C)] + \beta \cdot \text{KL}[q_\phi(z|C) \| p(z)]$$

- $\beta$: KL weight (anneal from 0 to 1)
- $p(z) = \mathcal{N}(0, I)$: standard Gaussian prior
- Mini-batch: Sample $C$ and $T$ from each function in batch

## Practical Considerations
- **Context size**: 3-50 points typically; more context = more accurate
- **Aggregation**: Mean works well, but attention is better for heterogeneous functions
- **Output distribution**: Gaussian for regression, Bernoulli/Categorical for classification
- **Training**: NP training is unstable — use gradient clipping and learning rate warmup
- **Evaluation**: Log-likelihood on held-out target sets; uncertainty calibration (NLL vs coverage)

## Applications
- **Few-shot regression**: Predict function from a few observations
- **Bayesian optimization**: Surrogate model with uncertainty for acquisition
- **Image completion**: Pixel prediction conditioned on observed patches
- **Goal-conditioned RL**: World model conditioned on context trajectories

## References
- Garnelo, Rosenbaum, et al., "Conditional Neural Processes", ICML 2018
- Garnelo, Schwarz, et al., "Neural Processes", ICML 2018 Workshop
- Kim et al., "Attentive Neural Processes", ICLR 2019
- Gordon et al., "Convolutional Conditional Neural Processes", ICLR 2020
- Bruinsma et al., "Autoregressive Conditional Neural Processes", ICLR 2023
