# 🏗️ Loss Functions
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Common loss functions and when to use each.

## Regression Losses

```python
loss = nn.MSELoss()         # mean squared error
loss = nn.L1Loss()          # mean absolute error
loss = nn.HuberLoss()       # Huber (smooth L1)
```

## Classification Losses

```python
loss = nn.BCEWithLogitsLoss()  # binary cross-entropy (logits)
loss = nn.CrossEntropyLoss()   # multi-class (logits)
loss = nn.NLLLoss()            # negative log-likelihood (after log_softmax)
```

## Usage Pattern

```python
criterion = nn.MSELoss()
output = model(x)
loss = criterion(output, target)
```

## Key Rule

- `CrossEntropyLoss` expects raw logits (not softmax)
- `BCEWithLogitsLoss` expects raw logits (not sigmoid)
- Both combine the activation and loss for numerical stability

<!-- 🤔 Always use the `WithLogits` variants — they're numerically stable. -->

## Run the Code

```bash
python code/08-loss-functions.py
```
