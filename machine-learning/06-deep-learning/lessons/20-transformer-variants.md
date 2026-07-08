# 06.20 Transformer Variants

Different architectures building on the transformer block for different modalities and efficiency.

## GPT (Generative Pre-trained Transformer)

- Decoder-only architecture
- Causal (masked) self-attention
- Autoregressive language modeling
- Trained on next-token prediction

Architecture: Embed → N×DecoderBlock → LayerNorm → LM Head → Softmax

## BERT (Bidirectional Encoder Representations from Transformers)

- Encoder-only architecture
- Bidirectional self-attention
- MLM (Masked Language Modeling) + NSP training
- Great for understanding tasks

## Vision Transformer (ViT)

- Applies transformer to image patches
- Split image into 16x16 patches, linearly project
- Add positional embeddings (learned)
- Classification token (CLS) for prediction
- Scales with compute (better than CNNs at scale)

## Performer (FAVOR+)

- Replaces softmax attention with kernel approximation
- O(n) complexity instead of O(n²)
- Uses random feature maps (positive orthogonal features)
- Can handle sequences > 100K tokens

## Linformer

- Projects keys and values to lower dimension (n → k)
- Self-attention becomes O(nk) instead of O(n²)
- k is fixed (e.g., 256), so effectively O(n)
- Assumes attention matrix is low-rank

## Reformer

- Locality-sensitive hashing (LSH) for approximate attention
- Reversible layers (no need to store activations)
- Chunked feedforward processing
- Memory efficient for long sequences

## Comparison

| Model | Complexity | Memory | Task |
|-------|-----------|--------|------|
| GPT | O(n²) | High | Text generation |
| BERT | O(n²) | High | Understanding |
| ViT | O(n²) | High | Image classification |
| Performer | O(n) | Low | Very long sequences |
| Linformer | O(n) | Low | Very long sequences |
| Reformer | O(n log n) | Very low | Long sequences |
