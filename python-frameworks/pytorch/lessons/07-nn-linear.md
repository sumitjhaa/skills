# 🏗️ nn.Linear Layer
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Use `nn.Linear` for trainable linear transformations.

## Basic Usage

```python
import torch.nn as nn

linear = nn.Linear(in_features=10, out_features=5)
x = torch.randn(3, 10)
y = linear(x)  # (3, 5)
```

## Parameters

```python
linear.weight  # shape (5, 10)
linear.bias    # shape (5,)
```

## Linear Regression with nn.Linear

```python
model = nn.Linear(1, 1)
loss_fn = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

for epoch in range(100):
    y_pred = model(X)
    loss = loss_fn(y_pred, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

<!-- 🤔 `nn.Linear` manages `weight` and `bias` as `Parameter` objects with `requires_grad=True`. -->

## Run the Code

```bash
python code/07-nn-linear.py
```
