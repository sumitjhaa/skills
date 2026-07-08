# Lesson 07.18: Autoregressive Models (NADE, MADE, WaveNet)

## Learning Objectives
- Understand autoregressive factorization of joint distributions
- Implement MADE with autoregressive masking
- Apply WaveNet's dilated causal convolutions for audio
- Compare order-agnostic training and masked architectures

## Theory
Autoregressive models factorize the joint distribution using the probability chain rule:

$$p(x) = \prod_{i=1}^D p(x_i \mid x_{<i})$$

- $x_{<i}$: all dimensions before $i$
- $p(x_i \mid x_{<i})$: conditional distribution (e.g., Gaussian, categorical)
- **Ordering**: Requires a fixed ordering of dimensions (1, 2, ..., D)

## NADE (Neural Autoregressive Distribution Estimation)

### Architecture
$$p(x_i = 1 \mid x_{<i}) = \sigma(W_i \cdot h_i + b_i)$$
$$h_i = \sigma(V \cdot x_{<i} + c)$$

- **Parameter sharing**: $V$ and $c$ shared across conditionals
- **Complexity**: $O(D H)$ per conditional — $O(D^2 H)$ total

### Order-Agnostic Training
- Randomize dimension order during training
- Model learns to predict any dimension given any subset of others
- Enables efficient inference with missing data

## MADE (Masked Autoencoder for Distribution Estimation)

### Key Idea
Mask connections in a standard autoencoder to respect autoregressive ordering:

$$h_k(x) = \sigma\left(\sum_{j < m(k)} W_{kj} x_j + b_k\right)$$
$$\hat{x}_i = \sigma\left(\sum_{k < d(i)} V_{ik} h_k(x) + a_i\right)$$

### Masking Strategy
- Assign each hidden unit a "masking number" $m(k) \in \{1, \dots, D-1\}$
- Weight $W_{kj}$ is masked if $m(k) \leq j$
- Weight $V_{ik}$ is masked if $d(i) \leq m(k)$

### Complexity
$O(D H + H D)$ — single forward pass for all conditionals (unlike NADE's $O(D^2 H)$).

## WaveNet

### Dilated Causal Convolutions
$$h_t^{(l)} = \tanh(W_f^{(l)} * h_{t}^{(l-1)}) \odot \sigma(W_g^{(l)} * h_{t}^{(l-1)})$$

- **Causal**: $h_t$ depends only on $h_{\leq t-1}$ (prevents future leakage)
- **Dilated**: Factor $2^l$ dilation at layer $l$
- **Receptive field**: $2^L$ for $L$ layers (exponential growth)

### Architecture
```
Input → Causal conv (2) → Residual block × L → Post-net → Softmax (mu-law)
```

Each residual block:
```
Skip connection: h_out = h_in + (conv_output → 1x1 conv)
Residual: add h_in to output
```

### Mu-Law Quantization
8-bit mu-law encoding for raw audio waveforms:

$$f(x_t) = \text{sign}(x_t) \frac{\ln(1 + \mu |x_t|)}{\ln(1 + \mu)}, \quad \mu = 255$$

### Conditional WaveNet
$$p(x \mid h) = \prod_{t=1}^T p(x_t \mid x_{<t}, h)$$

Conditioning on $h$ (e.g., speaker embedding, linguistic features) via FiLM or bias.

## Code: MADE Implementation

```python
import torch
import torch.nn as nn

class MADE(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_masks=1):
        super().__init__()
        self.input_dim = input_dim
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim * 2),  # mu and log_sigma
        )
        self.register_buffer('mask', self.create_mask(input_dim, hidden_dim, num_masks))

    def create_mask(self, d, h, num_masks):
        m = torch.arange(1, d+1)
        mask = torch.ones(h, d)
        for k in range(h):
            mask[k] = (m < torch.randint(1, d+1, (1,)).item()).float()
        return mask

    def forward(self, x):
        h = x @ (self.net[0].weight.T * self.mask) + self.net[0].bias
        h = torch.relu(h)
        h = self.net[2](h)
        h = torch.relu(h)
        out = self.net[4](h)
        mu, log_sigma = out[:, :self.input_dim], out[:, self.input_dim:]
        return mu, log_sigma

    def log_prob(self, x):
        mu, log_sigma = self.forward(x)
        return -0.5 * torch.sum((x - mu) ** 2 * torch.exp(-2 * log_sigma) + 2 * log_sigma + np.log(2 * np.pi), dim=-1)
```

## Autoregressive Model Comparison

| Model | Complexity (forward) | Parallel? | Application |
|-------|---------------------|-----------|-------------|
| NADE | $O(D^2 H)$ | No (sequential) | Binary data |
| MADE | $O(D H)$ | Yes (single pass) | General density |
| WaveNet | $O(T)$ per sample | No (autoregressive) | Audio |
| PixelCNN | $O(HW)$ | No (sequential) | Images |
| Transformer-XL | $O(T^2)$ | No (train parallel) | Text |

## Practical Considerations
- **Ordering**: For images, raster scan (row-by-row) is standard
- **Conditioning**: Can condition on class labels, speaker ID, text
- **Temperature**: $\tau$ in softmax controls sample diversity: $p_\tau(x_i) \propto \exp(\log p(x_i)/\tau)$
- **Fast inference**: Caching hidden states (WaveNet's fast generation) speeds up sampling

## Limitations
- **Sequential sampling**: Generating one token at a time is slow (except MADE for density)
- **Fixed ordering**: Performance depends on chosen ordering; order-agnostic training helps
- **Long-range dependencies**: WaveNet's receptive field grows exponentially but still limited
- **Mode collapse**: Autoregressive models tend to produce repetitive samples

## References
- Larochelle & Murray, "The Neural Autoregressive Distribution Estimator", AISTATS 2011
- Germain, Gregor, Murray, Larochelle, "MADE: Masked Autoencoder for Distribution Estimation", ICML 2015
- van den Oord, Dieleman, Zen, Simonyan, Vinyals, Graves, Kalchbrenner, Senior, Kavukcuoglu, "WaveNet: A Generative Model for Raw Audio", 2016
- van den Oord, Kalchbrenner, Kavukcuoglu, "Pixel Recurrent Neural Networks", ICML 2016
- Uria, Côté, Gregor, Murray, Larochelle, "Neural Autoregressive Distribution Estimation", JMLR 2016
