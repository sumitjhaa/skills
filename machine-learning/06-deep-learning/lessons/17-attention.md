# 06.17 Attention

Attention mechanisms allow models to focus on relevant parts of the input when producing output.

## Scaled Dot-Product Attention

Attention(Q, K, V) = softmax(Q · K^T / √d_k) · V

- Q (query): what the model is looking for
- K (key): what each position offers
- V (value): what each position contributes
- √d_k: scaling factor prevents softmax saturation

## Additive Attention (Bahdanau)

Score(q, k) = v^T · tanh(W_q·q + W_k·k)

Used in the original seq2seq with attention. More expensive than dot-product.

## Multi-Head Attention

Split Q, K, V into h heads, compute attention separately, concatenate:

MultiHead(Q, K, V) = Concat(head₁, ..., head_h) · W_O

Each head can attend to different patterns.

## Self-Attention

Q, K, V all come from the same sequence. Each position attends to all positions. O(n²) complexity.

## Cross-Attention

Q from one sequence (e.g., decoder), K, V from another (e.g., encoder).

## Causal/Masked Attention

Prevents positions from attending to future positions. Used in autoregressive generation. Apply mask before softmax (-inf for masked positions).

## Attention Variants

| Variant | Complexity | Use Case |
|---------|------------|----------|
| Dot-product | O(n²) | Standard |
| Linear (Performer) | O(n) | Long sequences |
| Linformer | O(n) | Long sequences |
| Reformer (LSH) | O(n log n) | Very long sequences |
| Flash Attention | O(n²) but fast | Hardware-efficient |

## Applications

- Transformers (core mechanism)
- Sequence-to-sequence models
- Vision Transformers (ViT)
- Graph neural networks
- Memory-augmented networks
