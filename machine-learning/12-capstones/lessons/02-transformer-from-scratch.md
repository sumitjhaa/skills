# Lesson 12.02: Transformer from Scratch (GPT-2 Scale)

## Project Architecture

Implement a full GPT-2-style decoder-only transformer, train it on a text dataset, and generate coherent text.

```
Tokenizer (BPE / character-level)
  └── Embedding (token + position)
       └── Transformer Blocks × N
            ├── Multi-Head Self-Attention
            │    ├── Q, K, V projections
            │    ├── Scaled dot-product attention
            │    └── Output projection + residual
            ├── LayerNorm (pre-norm)
            ├── Feed-Forward (MLP with GELU)
            └── Residual connections
                 └── LM Head (tied weights / separate)
                      └── Softmax → Sampling (top-k, top-p)
```

## Design Decisions

### Tokenization
- Use character-level tokenization for simplicity (train on Shakespeare or similar)
- Each character maps to a unique integer ID
- Vocabulary ~100 tokens (printable ASCII)

### Embedding
- `TokenEmbedding(vocab_size, d_model)` — lookup table
- `PositionalEncoding(max_len, d_model)` — learned or sinusoidal
- Sinusoidal is preferable because it generalizes to longer sequences

### Attention
- Scaled dot-product: `softmax(Q K^T / sqrt(d_k)) V`
- Multi-head: split d_model into `n_heads` heads, each of dimension `d_k = d_model // n_heads`
- Causal masking: upper-triangular matrix of -inf
- Dropout on attention weights and output

### Transformer Block
- Pre-normalization (LayerNorm before attention and FFN) — stabler training
- Residual connections around each sub-layer
- Feed-forward: `d_model → d_ff → d_model` with GELU activation

### Training
- Input: sequence of token IDs; target: shifted-by-1 sequence
- Cross-entropy loss (ignore padding)
- Learning rate warmup + cosine decay
- Gradient clipping

### Generation
- Autoregressive: feed in prompt, sample next token, append, repeat
- Top-k sampling: sample only from the k most probable tokens
- Top-p (nucleus) sampling: sample from smallest set with cumulative prob > p

## Implementation Guide

1. **Implement sinusoidal positional encoding**
2. **Implement scaled dot-product attention (with causal mask)**
3. **Implement multi-head attention**
4. **Implement the feed-forward block (GELU)**
5. **Implement LayerNorm**
6. **Implement a single TransformerBlock**
7. **Implement the full GPT model** (embed + N blocks + LM head)
8. **Implement training loop** with data batching
9. **Implement generation** (top-k, top-p sampling)
10. **Train on a text corpus** and generate samples
11. **Plot loss curves and sample quality**

## Key Insights

- Attention is a communication mechanism; FFN is computation on each token
- Pre-norm is easier to train than post-norm
- The causal mask is what makes it autoregressive
- Larger d_model and more layers yield better results but need more data
