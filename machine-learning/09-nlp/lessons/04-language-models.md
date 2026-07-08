# 09.04 Language Models

## Learning Objectives
- Understand language modelling as next-token prediction
- Implement N-gram and neural language models
- Apply perplexity for model evaluation
- Analyze scaling laws in large language models

## Language Modelling

### Definition
$$P(w_1, w_2, \dots, w_T) = \prod_{t=1}^T P(w_t | w_{<t})$$

Assign probability to sequences of words.

## N-gram Models

### Markov Assumption
$$P(w_t | w_{<t}) \approx P(w_t | w_{t-n+1}^{t-1})$$

### Maximum Likelihood Estimation
$$P(w_t | w_{t-2}, w_{t-1}) = \frac{\text{Count}(w_{t-2}, w_{t-1}, w_t)}{\text{Count}(w_{t-2}, w_{t-1})}$$

### Smoothing
- **Laplace (add-1)**: Add 1 to all counts
- **Kneser-Ney**: Interpolate higher/lower-order distributions with discounting
- **Stupid Backoff**: $S(w_i | w_{i-k+1}^{i-1}) = \begin{cases} \frac{\text{count}}{n} & \text{if count} > 0 \\ \alpha S(w_i | w_{i-k+2}^{i-1}) & \text{otherwise} \end{cases}$

## Neural Language Models

### Feedforward LM (Bengio 2003)
$$P(w_t | w_{t-n+1}^{t-1}) = \text{softmax}(W \cdot \text{tanh}(E \cdot C + b))$$

- $E$: embedding matrix
- $C$: context of $n-1$ previous words

### RNN-LM (Mikolov 2010)
$$h_t = \text{tanh}(W_{xh} x_t + W_{hh} h_{t-1} + b_h)$$
$$P(w_t | w_{<t}) = \text{softmax}(W_{hy} h_t + b_y)$$

- Handles arbitrary context length (in theory)
- Suffers from vanishing/exploding gradients

### Transformer LM (GPT)
$$P(w_t | w_{<t}) = \text{softmax}(W \cdot \text{Transformer}_{\text{decoder}}(w_{<t}))$$

- Causal attention mask (no future tokens)
- Positional encodings
- Layer normalisation + residual connections

## Perplexity

### Definition
$$\text{PPL}(W) = \exp\left(-\frac{1}{T} \sum_{t=1}^T \log P(w_t | w_{<t})\right)$$

### Interpretation
- Lower is better
- $\text{PPL} = N$ means model is as confused as uniform distribution over $N$ tokens
- GPT-2: PPL 35 on WikiText-2 → model is confused as choosing uniformly among 35 tokens

## Scaling Laws (Kaplan et al.)

### Key Findings
$$\text{Loss} \propto N^{-\alpha_N}, \quad \alpha_N \approx 0.076$$
$$\text{Loss} \propto D^{-\alpha_D}, \quad \alpha_D \approx 0.095$$

- $N$: model parameters
- $D$: training data tokens

### Chinchilla Scaling
Compute-optimal training: $N_{\text{opt}} \propto C^{0.5}$, $D_{\text{opt}} \propto C^{0.5}$

- For a given compute budget $C$, train smaller models on more data
- Chinchilla (70B) trained on 1.4T tokens outperforms GPT-3 (175B, 300B tokens)

## Code: Simple RNN Language Model

```python
import torch
import torch.nn as nn

class RNNLM(nn.Module):
    def __init__(self, vocab_size, embed_dim=256, hidden_dim=512):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.rnn = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x, hidden=None):
        # x: (B, T)
        emb = self.embed(x)
        out, hidden = self.rnn(emb, hidden)
        logits = self.fc(out)  # (B, T, vocab_size)
        return logits, hidden

    def generate(self, start_token, max_len=100, temperature=1.0):
        self.eval()
        tokens = [start_token]
        hidden = None
        for _ in range(max_len):
            x = torch.tensor([[tokens[-1]]])
            logits, hidden = self.forward(x, hidden)
            probs = (logits[0, -1] / temperature).softmax(dim=-1)
            next_token = torch.multinomial(probs, 1).item()
            tokens.append(next_token)
            if next_token == self.eos_token_id:
                break
        return tokens
```

## Generation Strategies

| Method | Description | Temperature |
|--------|-------------|-------------|
| Greedy | Most likely token | 0 |
| Top-k | Sample from top K | 1.0 |
| Top-p (nucleus) | Sample from top cumulative p | 1.0 |
| Temperature sampling | Scale logits | 0.7-1.5 |

## References
- Bengio, Ducharme, Vincent, Jauvin, "A Neural Probabilistic Language Model", JMLR 2003
- Mikolov, Karafiát, Burget, Černocký, Khudanpur, "Recurrent neural network based language model", Interspeech 2010
- Radford et al., "Improving Language Understanding by Generative Pre-Training (GPT)", 2018
- Kaplan et al., "Scaling Laws for Neural Language Models", 2020
- Hoffmann et al., "Training Compute-Optimal Large Language Models (Chinchilla)", NeurIPS 2022
