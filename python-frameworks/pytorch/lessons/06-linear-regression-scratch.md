# 🏗️ Linear Regression from Scratch
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Implement linear regression with manually defined parameters and autograd.

## Model

```python
w = torch.randn(1, requires_grad=True)
b = torch.zeros(1, requires_grad=True)

def model(X):
    return X @ w + b
```

## Training Loop

```python
for epoch in range(100):
    y_pred = model(X)
    loss = ((y_pred - y) ** 2).mean()
    loss.backward()
    with torch.no_grad():
        w -= lr * w.grad
        b -= lr * b.grad
    w.grad.zero_()
    b.grad.zero_()
```

## Comparison

Compare learned `w`, `b` against true values used to generate data.

<!-- 🤔 This is the "by hand" version. Next lesson: `nn.Linear` does this for you. -->

## Run the Code

```bash
python code/06-linear-regression-scratch.py
```
