# 🏗️ Autograd — Automatic Differentiation
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Use PyTorch's autograd to compute gradients automatically.

## requires_grad

```python
x = torch.tensor([2.0, 3.0], requires_grad=True)
y = x**2 + 2*x + 1
y.sum().backward()
print(x.grad)  # dy/dx = 2x + 2 → [6.0, 8.0]
```

## Gradient Flow

```python
x = torch.randn(3, requires_grad=True)
y = (x ** 2).sum()
y.backward()
print(x.grad)  # 2*x
```

## Detaching & No-Grad

```python
# Detach (no gradient)
z = x.detach()

# Context manager
with torch.no_grad():
    y = x * 2  # no gradient tracking
```

<!-- 🤔 `backward()` computes gradients but does not update parameters. You still need an optimizer for that. -->

## Run the Code

```bash
python code/04-autograd.py
```
