# 🏗️ Optimizers
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Use PyTorch optimizers to update model parameters.

## Common Optimizers

```python
optim.SGD(model.parameters(), lr=0.01)           # SGD
optim.SGD(model.parameters(), lr=0.01, momentum=0.9)  # SGD + momentum
optim.Adam(model.parameters(), lr=0.001)          # Adam (default)
optim.RMSprop(model.parameters(), lr=0.01)        # RMSprop
optim.AdamW(model.parameters(), lr=0.001)         # Adam with decoupled weight decay
```

## Training Loop Pattern

```python
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(epochs):
    optimizer.zero_grad()
    output = model(x)
    loss = criterion(output, target)
    loss.backward()
    optimizer.step()
```

## Per-Parameter Options

```python
optimizer = torch.optim.SGD([
    {'params': model.features.parameters()},
    {'params': model.classifier.parameters(), 'lr': 1e-3},
], lr=1e-2)
```

<!-- 🤔 Adam is usually the best default. Use SGD+momentum for computer vision or when you want better generalization. -->

## Run the Code

```bash
python code/09-optimizers.py
```
