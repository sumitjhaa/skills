# 09.05 Encoder-Decoder Models

## Learning Objectives
- Understand encoder-decoder architecture for sequence transduction
- Implement Transformer (Vaswani et al.) for NMT
- Apply BERT for natural language understanding
- Compare encoder-only, decoder-only, and encoder-decoder models

## Sequence-to-Sequence

### Architecture
```
Encoder:  (x_1, ..., x_n) → (h_1, ..., h_n)
Decoder:  (h_1, ..., h_n, y_<t) → y_t
```

### RNN Encoder-Decoder (Sutskever 2014)
```python
# Encoder: read source sequence
for x in source:
    h = rnn_cell(x, h)

# Decoder: generate target
y = <sos>
for t in range(max_len):
    h, y = decoder_cell(y, h)
    tokens.append(y)
```

## Attention (Bahdanau 2015)

### Alignment
$$e_{ij} = v_a^\top \text{tanh}(W_a s_{i-1} + U_a h_j)$$
$$\alpha_{ij} = \frac{\exp(e_{ij})}{\sum_k \exp(e_{ik})}$$
$$c_i = \sum_j \alpha_{ij} h_j$$

### Context Vector
$c_i$ is a weighted sum of encoder hidden states, allowing decoder to "look at" relevant source positions.

## Transformer

### Scaled Dot-Product Attention
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right) V$$

### Multi-Head Attention
$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h) W^O$$
$$\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$$

### Encoder Stack
```
Input → Embedding → Positional Encoding → N× {Self-Attention → Add & Norm → FFN → Add & Norm}
```

### Decoder Stack
```
Input → Embedding → Positional Encoding → N× {Masked Self-Attention → Add & Norm
→ Cross-Attention → Add & Norm → FFN → Add & Norm}
```

## BERT (Encoder-Only)

### MLM (Masked Language Model)
$$p(w_{\text{masked}} | w_{\text{context}})$$

- Mask 15% of tokens (80% [MASK], 10% random, 10% unchanged)
- Bidirectional context

### NSP (Next Sentence Prediction)
$$p(\text{is_next} | \text{sentence}_A, \text{sentence}_B)$$

## Code: Transformer Encoder Block

```python
import torch
import torch.nn as nn

class TransformerEncoderBlock(nn.Module):
    def __init__(self, d_model=512, nhead=8, dim_ff=2048, dropout=0.1):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(d_model, nhead, dropout=dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, dim_ff),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(dim_ff, d_model),
        )
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        # Self-attention + residual
        attn_out, _ = self.self_attn(x, x, x, attn_mask=mask)
        x = self.norm1(x + self.dropout(attn_out))
        # FFN + residual
        ffn_out = self.ffn(x)
        x = self.norm2(x + self.dropout(ffn_out))
        return x
```

## Model Comparison

| Architecture | Model Examples | Tasks | Parameters |
|-------------|---------------|-------|-----------|
| Encoder-only | BERT, RoBERTa, ALBERT | Classification, QA | 110M-340M |
| Decoder-only | GPT, LLaMA, PaLM | Generation | 125M-540B |
| Encoder-decoder | T5, BART, M2M-100 | Translation, Summarisation | 60M-11B |

## Evaluation

### BLEU (Machine Translation)
n-gram precision with brevity penalty:

$$\text{BLEU} = \text{BP} \cdot \exp\left(\sum_{n=1}^4 \frac{1}{4} \log p_n\right)$$

### ROUGE (Summarisation)
Recall-oriented: measures overlap of n-grams, LCS, skip-bigrams.

## References
- Sutskever, Vinyals, Le, "Sequence to Sequence Learning with Neural Networks", NeurIPS 2014
- Bahdanau, Cho, Bengio, "Neural Machine Translation by Jointly Learning to Align and Translate", ICLR 2015
- Vaswani, Shazeer, Parmar, et al., "Attention Is All You Need", NeurIPS 2017
- Devlin, Chang, Lee, Toutanova, "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding", NAACL 2019
- Raffel, Shazeer, et al., "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer (T5)", JMLR 2020
