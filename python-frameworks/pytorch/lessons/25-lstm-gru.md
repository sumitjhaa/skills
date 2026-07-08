# 🏗️ LSTM and GRU
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** LSTM and GRU for better sequence modeling.

## LSTM

```python
lstm = nn.LSTM(input_size=8, hidden_size=16, num_layers=1)
out, (h_n, c_n) = lstm(x)
# h_n: hidden state, c_n: cell state
```

## GRU

```python
gru = nn.GRU(input_size=8, hidden_size=16)
out, h_n = gru(x)
# No separate cell state — fewer params
```

## Stacked RNNs

```python
rnn = nn.LSTM(8, 16, num_layers=2, dropout=0.3, batch_first=True)
```

## When to Use

| Problem | Recommended |
|---------|-------------|
| Short sequences (< 20) | RNN or GRU |
| Medium sequences | LSTM or GRU |
| Long sequences | LSTM (or Transformer) |
| Capturing long dependencies | LSTM (cell state helps) |

<!-- 🤔 LSTM has ~4x the params of a simple RNN. GRU has ~3x but similar performance to LSTM. -->

## Run the Code

```bash
python code/25-lstm-gru.py
```
