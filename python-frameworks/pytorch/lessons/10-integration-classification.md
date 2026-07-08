# 🏗️ Integration: Binary Classification with nn.Module
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Build a complete binary classifier using `nn.Module`.

## nn.Module Class

```python
class BinaryClassifier(nn.Module):
    def __init__(self, n_features):
        super().__init__()
        self.linear = nn.Linear(n_features, 1)

    def forward(self, x):
        return self.linear(x)  # raw logits
```

## Full Pipeline

```python
model = BinaryClassifier(n_features=4)
criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

for epoch in range(100):
    logits = model(X_train)
    loss = criterion(logits.squeeze(), y_train)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

## Evaluation

```python
with torch.no_grad():
    logits = model(X_test)
    probs = torch.sigmoid(logits)
    preds = (probs > 0.5).int()
    acc = (preds.squeeze() == y_test).float().mean()
```

<!-- 🤔 `BCEWithLogitsLoss` expects raw logits. Use `torch.sigmoid()` only at inference time. -->

## Run the Code

```bash
python code/10-integration-classification.py
```
