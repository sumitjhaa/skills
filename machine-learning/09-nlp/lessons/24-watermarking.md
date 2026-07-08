# 09.24 Watermarking

## Learning Objectives
- Understand watermarking for detecting AI-generated text
- Implement soft watermark (Kirchenbauer et al.) and undetectable watermarks
- Apply watermarking for copyright protection
- Analyze robustness against paraphrasing attacks

## Why Watermark?

### Problem
Detecting whether text is AI-generated is important for:
- Academic integrity
- Misinformation detection
- Copyright attribution
- Plagiarism detection

## Soft Watermark (Kirchenbauer 2023)

### Algorithm
1. **Red list / green list split**: For each token, randomly split vocabulary into red/green using hash of previous token.
2. **Biased sampling**: Boost green list token probability:
   $$p_{\text{watermarked}}(w) = \text{softmax}(\text{logits} + \delta \cdot \mathbb{1}_{\text{green}}(w))$$
3. **Detection**: Count green tokens; if count > expected, AI-generated.

### Implementation
```python
import hashlib

def hash_token(prev_token_id, vocab_size, seed):
    h = hashlib.sha256(f"{prev_token_id}:{seed}".encode()).digest()
    rng = int.from_bytes(h[:8], 'big')
    return rng % vocab_size
```

### Detection
$$z = \frac{\text{green\_count} - \gamma \cdot T}{\sqrt{T \cdot \gamma \cdot (1 - \gamma)}} \sim \mathcal{N}(0, 1)$$

- $\gamma = 0.5$: green list fraction
- $T$: total tokens
- $z > 4$: strong evidence of watermarking

## Undetectable Watermarks (Christ 2023)

### Problem
Soft watermark can be detected statistically (distribution is biased).

### Solution
- **Gumbel-max watermark**: Sample tokens using Gumbel noise seeded by hash
- **Inverse transform sampling**: Use hash to determine rank in distribution

## Robustness

### Attacks
| Attack | Description | Effect on Soft Watermark |
|--------|-------------|-------------------------|
| Paraphrasing | Rewrite text with different words | Decreases detection |
| Back-translation | Translate and back | Modifies token sequence |
| Word substitution | Replace synonyms | Partial removal |
| Insertion/deletion | Add/remove words | Shifts alignment |

### Detection Rate
| Watermark | No Attack | Paraphrase | Back-Translate |
|-----------|-----------|------------|---------------|
| Soft (δ=2) | 99.9% | 67% | 55% |
| Gumbel-max | 99.9% | 81% | 72% |
| Unigram | 99.9% | 74% | 63% |

## Code: Soft Watermark

```python
import torch
import torch.nn.functional as F
from typing import List

class WatermarkGenerator:
    def __init__(self, model, tokenizer, gamma=0.5, delta=2.0, seed=42):
        self.model = model
        self.tokenizer = tokenizer
        self.gamma = gamma
        self.delta = delta
        self.seed = seed
        self.vocab_size = tokenizer.vocab_size

    def _get_greenlist_ids(self, prev_token_id):
        import hashlib
        h = hashlib.sha256(f"{prev_token_id}:{self.seed}".encode()).digest()
        rng = int.from_bytes(h[:8], 'big')
        # Generate green list using random permutation
        perm = torch.randperm(self.vocab_size, generator=torch.Generator().manual_seed(rng))
        green_size = int(self.vocab_size * self.gamma)
        return perm[:green_size]

    def generate(self, input_ids, max_length=100):
        for _ in range(max_length):
            logits = self.model(input_ids).logits[0, -1]
            
            if input_ids.size(1) > 1:
                prev_token = input_ids[0, -1].item()
                green_ids = self._get_greenlist_ids(prev_token)
                logits[green_ids] += self.delta
            
            probs = F.softmax(logits, dim=-1)
            next_token = torch.multinomial(probs, 1)
            input_ids = torch.cat([input_ids, next_token.unsqueeze(0)], dim=-1)
            
            if next_token.item() == self.tokenizer.eos_token_id:
                break
        return input_ids

    def detect(self, token_ids: List[int]) -> float:
        green_count = 0
        for i in range(1, len(token_ids)):
            green_ids = self._get_greenlist_ids(token_ids[i-1])
            if token_ids[i] in green_ids:
                green_count += 1
        
        T = len(token_ids) - 1
        gamma = self.gamma
        z = (green_count - gamma * T) / (T * gamma * (1 - gamma)) ** 0.5
        return z  # z > 4 → likely watermarked
```

## Watermark Detection Benchmarks

| Dataset | Length | Soft Watermark (δ=2) | Gumbel-max | Unigram |
|---------|--------|---------------------|------------|---------|
| XSum (summaries) | 50 | 99.9% (z > 4) | 99.9% | 99.9% |
| News (generated) | 200 | 99.9% | 99.9% | 99.9% |
| Paraphrased news | 200 | 67% | 81% | 74% |
| Human-written | 200 | 5% false positive | 5% | 5% |

## Practical Considerations
- **False positive rate**: Set z-threshold for acceptable FPR (typically 1%)
- **Multi-model detection**: Different models need different detectors
- **Steganography**: Hiding watermark in generated text is an arms race
- **Watermark removal**: LLMs can be prompted to "de-watermark" text
- **Perplexity increase**: Watermarking slightly increases perplexity (+0.5 PPL)

## References
- Kirchenbauer, Geiping, et al., "A Watermark for Large Language Models", ICML 2023
- Christ, Gunn, Zamir, "Undetectable Watermarks for Language Models", 2023
- Zhao, Anantharamakrishnan, et al., "On the Robustness of Text Watermarks for Large Language Models", 2023
- Kuditipudi, Thickstun, et al., "Robust Watermarking of Language Model Outputs", 2023
- Aaronson, "Watermarking of Large Language Models", 2023
