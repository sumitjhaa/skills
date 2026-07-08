# 🏗️ Fine-Tuning
<!-- ⏱️ 20 min | 🔶 Intermediate -->

**What You'll Learn:** Unfreeze and fine-tune all layers with a lower learning rate.

## Two-Phase Training

```python
# Phase 1: Train classifier only
for param in base.parameters():
    param.requires_grad = False
optimizer = optim.Adam(classifier.parameters(), lr=0.01)
train(model, loader, optimizer, epochs=5)

# Phase 2: Unfreeze, fine-tune all
for param in base.parameters():
    param.requires_grad = True
optimizer = optim.Adam(model.parameters(), lr=0.0001)  # lower LR
train(model, loader, optimizer, epochs=10)
```

## Why Lower LR for Fine-Tuning?

- Base features are already good
- High LR can destroy pretrained weights
- 10x-100x lower LR than training from scratch

## Differential Learning Rates

```python
optimizer = optim.Adam([
    {'params': base.parameters(), 'lr': 1e-5},
    {'params': classifier.parameters(), 'lr': 1e-3},
])
```

<!-- 🤔 Fine-tuning with a low LR is one of the most effective techniques in deep learning. -->

## Run the Code

```bash
python code/27-fine-tuning.py
```
