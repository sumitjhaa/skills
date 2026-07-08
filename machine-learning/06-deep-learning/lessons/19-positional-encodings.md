# 06.19 Positional Encodings

Since attention is permutation-invariant (set operation), positional information must be explicitly added.

## Sinusoidal Positional Encoding

PE(pos, 2i) = sin(pos / 10000^{2i/d})
PE(pos, 2i+1) = cos(pos / 10000^{2i/d})

- pos: position in sequence
- i: dimension index
- d: model dimension

Properties:
- Relative positions can be learned through linear combinations
- Extrapolates to unseen sequence lengths
- Fixed, not learned

## Learned Positional Encoding

Embedding lookup: learn a vector for each position.

Used in BERT, GPT. Limited to max training length. Requires interpolation for longer sequences.

## Rotary Position Embedding (RoPE)

Rotates query and key vectors by angle proportional to position:

f{q,k}(x_m, m) = R(Θ, m) · W_{q,k} · x_m

Applies rotation matrix to pairs of dimensions. Naturally captures relative positions in dot product attention.

Used in: Llama, PaLM, GPT-NeoX.

## ALiBi (Attention with Linear Biases)

Adds a bias to attention scores proportional to distance:

score(i, j) = q_i · k_j - m · |i - j|

m is a head-specific slope. Simple, extrapolates well. No learned position parameters.

Used in: BLOOM, MPT.

## Relative Positional Encoding

Attention scores incorporate relative position biases:

score(i, j) = (x_i W_Q)(x_j W_K)^T + a_{i-j}

Learn a separate bias matrix for each relative offset.

## Comparison

| Method | Extrapolates | Learned | Complexity |
|--------|-------------|---------|------------|
| Sinusoidal | Yes | No | O(1) |
| Learned | No | Yes | O(n) |
| RoPE | Yes | No* | O(n) |
| ALiBi | Yes | No | O(1) |
| Relative | No | Yes | O(n²) |

*RoPE has learned W_q, W_k but rotation itself is fixed.
