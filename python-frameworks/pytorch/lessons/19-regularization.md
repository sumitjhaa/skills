# 🏗️ Regularization — Dropout & Weight Decay
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Prevent overfitting with dropout and weight decay.

## Dropout

```python
model = nn.Sequential(
    nn.Linear(20, 64),
    nn.ReLU(),
    nn.Dropout(0.5),     # 50% of neurons disabled during training
    nn.Linear(64, 32),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(32, 1),
)
# Dropout is automatically disabled during model.eval()
```

## Weight Decay (L2 Regularization)

```python
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)
```

## Training vs Evaluation

```python
model.train()   # enables dropout, batch norm updates
model.eval()    # disables dropout, freezes batch norm
```

<!-- 🤔 Dropout = 0.5 for large layers, 0.1-0.3 for smaller ones. weight_decay=1e-4 is a good default. -->

## Run the Code

```bash
python code/19-regularization.py
```
