# 🏗️ Mixed Precision Training
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Use `torch.cuda.amp` for faster training with less memory.

## Why Mixed Precision?

- FP16 uses half the memory of FP32
- Volta+ GPUs have Tensor Cores for FP16
- 1.5x-3x speedup with minimal accuracy loss

## Pattern

```python
scaler = torch.amp.GradScaler('cuda')

for X, y in loader:
    optimizer.zero_grad()
    with torch.amp.autocast('cuda'):
        loss = criterion(model(X), y)

    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

## What Happens

- Forward pass runs in FP16 where safe
- Loss is scaled up to prevent underflow
- Gradients are unscaled before optimizer step

<!-- 🤔 Always use AMP on Volta/V100 or newer GPUs. It's free performance. -->

## Run the Code

```bash
python code/32-mixed-precision.py
```
