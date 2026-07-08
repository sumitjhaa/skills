# 🏗️ Multi-Layer Perceptron
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Train an MLP for multi-class classification.

## MLP Architecture

```python
class MLP(nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, out_dim),
        )

    def forward(self, x):
        return self.net(x)  # raw logits
```

## Training

```python
model = MLP(4, 32, 3)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(100):
    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()
        logits = model(X_batch)
        loss = criterion(logits, y_batch)
        loss.backward()
        optimizer.step()
```

<!-- 🤔 CrossEntropyLoss expects raw logits, not softmax outputs. -->

## Run the Code

```bash
python code/15-mlp-classification.py
```
