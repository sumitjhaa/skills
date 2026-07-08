# 06.23 Seq2Seq

Sequence-to-sequence models transform an input sequence into an output sequence of potentially different length.

## Encoder-Decoder Architecture

```
Input:  [x₁, x₂, ..., x_T]
Encoder: RNN/LSTM → produces context vector c
Decoder: RNN/LSTM → produces [y₁, y₂, ..., y_T']

Training: teacher forcing (feed ground truth y_{t-1})
Inference: feed predicted ŷ_{t-1}
```

## Context Vector

The encoder compresses the entire input sequence into a fixed-size context vector c (final hidden state). This is a bottleneck for long sequences.

## Seq2Seq with Attention

Attention allows the decoder to look at all encoder hidden states instead of just the final one.

At each decoder step t:
1. Compute alignment scores: e_{t,i} = score(s_{t-1}, h_i)
2. Attention weights: α_{t,i} = softmax(e_{t,i})
3. Context vector: c_t = Σ_i α_{t,i} · h_i
4. Decoder input: [y_{t-1}; c_t]

## Beam Search

Instead of greedy decoding (pick highest probability token at each step), maintain top-k hypotheses:

- At each step, expand each hypothesis with vocabulary
- Keep top-k by cumulative log probability
- Normalize by length to avoid preferring short sequences

## Teacher Forcing vs Scheduled Sampling

- **Teacher forcing**: feed ground truth as next input. Fast convergence but exposure bias.
- **Scheduled sampling**: gradually mix ground truth and model predictions during training.

## Bleu Score

Evaluation metric for seq2seq. Measures n-gram overlap between generated and reference sequences. Range [0, 1] (usually reported as 0-100).

## Applications

- Machine translation
- Text summarization
- Speech recognition
- Image captioning
