# 🏗️ Gradient Descent Step
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Manual gradient descent loop using autograd.

## Manual GD Loop

```python
x = torch.tensor([5.0], requires_grad=True)
lr = 0.1

for step in range(20):
    y = x ** 2 + 2 * x + 1  # f(x) = x² + 2x + 1
    y.backward()
    with torch.no_grad():
        x -= lr * x.grad     # gradient descent update
    x.grad.zero_()           # reset gradients
```

## Important: Zeroing Gradients

Gradients accumulate by default. Always call `zero_()` between steps.

## Learning Rate Effects

- Too high: diverges
- Too low: slow convergence
- Just right: steady decrease

<!-- 🤔 This manual loop shows what optimizers do internally. Next lesson: use `nn.Linear` and `optim.SGD`. -->

## Run the Code

```bash
python code/05-gradient-descent.py
```
