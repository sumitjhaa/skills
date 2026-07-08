# 🏗️ Early Stopping
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Stop training when validation loss stops improving.

## Early Stopping Logic

```python
best_loss = float('inf')
patience = 10
counter = 0

for epoch in range(max_epochs):
    val_loss = validate(model, val_loader)

    if val_loss < best_loss:
        best_loss = val_loss
        counter = 0
        torch.save(model.state_dict(), 'best_model.pt')
    else:
        counter += 1
        if counter >= patience:
            print(f"Early stopping at epoch {epoch}")
            break
```

## Why

- Prevents overfitting
- Saves training time
- Automatically finds optimal stopping point

<!-- 🤔 Always save the best model (lowest val loss), not the last one. -->

## Run the Code

```bash
python code/17-early-stopping.py
```
