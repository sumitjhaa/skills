# 🏗️ Recurrent Neural Networks (RNN)
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Process sequences with RNNs.

## RNN Cell

```python
rnn = nn.RNN(input_size=8, hidden_size=16, batch_first=False)
# Input:  (seq_len, batch, input_size)
# Output: (seq_len, batch, hidden_size)
# Hidden: (1, batch, hidden_size)
```

## batch_first

```python
rnn = nn.RNN(8, 16, batch_first=True)
# Input:  (batch, seq_len, input_size)
# Output: (batch, seq_len, hidden_size)
```

## Using Last Hidden State

```python
out, h_n = rnn(x)
last_output = out[-1]     # batch_first=False
last_output = out[:, -1]  # batch_first=True
classifier = nn.Linear(16, 1)
pred = classifier(last_output)
```

<!-- 🤔 RNNs struggle with long sequences due to vanishing gradients. LSTM/GRU solve this. -->

## Run the Code

```bash
python code/24-rnn-basics.py
```
