# 🏗️ Learning Rate Scheduling
<!-- ⏱️ 10 min | 🔶 Intermediate -->

**What You'll Learn:** Adjust learning rate during training with schedulers.

## Common Schedulers

```python
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.5)
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=50)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5)
scheduler = optim.lr_scheduler.OneCycleLR(optimizer, max_lr=0.1, steps_per_epoch=len(loader), epochs=epochs)
```

## Usage

```python
# Per-epoch scheduler
for epoch in range(epochs):
    train(...)
    scheduler.step()          # StepLR, CosineAnnealing
    # or
    scheduler.step(val_loss)  # ReduceLROnPlateau
```

## Why

- High LR early → fast progress
- Low LR later → fine-tune convergence

<!-- 🤔 ReduceLROnPlateau is intuitive — reduce LR when you stall. -->

## Run the Code

```bash
python code/18-lr-scheduling.py
```
