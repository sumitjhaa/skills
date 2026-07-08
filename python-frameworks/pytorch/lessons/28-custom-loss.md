# 🏗️ Custom Loss Functions
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Define custom loss functions as functions and nn.Module classes.

## As a Function

```python
def huber_loss(pred, target, delta=1.0):
    diff = pred - target
    abs_diff = diff.abs()
    quadratic = 0.5 * diff ** 2
    linear = delta * (abs_diff - 0.5 * delta)
    return torch.where(abs_diff <= delta, quadratic, linear).mean()
```

## As an nn.Module

```python
class FocalLoss(nn.Module):
    def __init__(self, gamma=2.0):
        super().__init__()
        self.gamma = gamma

    def forward(self, logits, targets):
        probs = torch.sigmoid(logits)
        bce = - (targets * torch.log(probs) +
                 (1 - targets) * torch.log(1 - probs))
        p_t = probs * targets + (1 - probs) * (1 - targets)
        return (bce * (1 - p_t) ** self.gamma).mean()
```

## Built-in Weighted Losses

```python
# For imbalanced classes
weights = torch.tensor([1.0, 10.0])
criterion = nn.CrossEntropyLoss(weight=weights)
criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
```

<!-- 🤔 Custom losses let you encode domain knowledge. Focal loss down-weights easy examples. -->

## Run the Code

```bash
python code/28-custom-loss.py
```
