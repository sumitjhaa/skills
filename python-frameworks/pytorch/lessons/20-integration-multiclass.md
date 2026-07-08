# 🏗️ Integration: Multi-Class Classification
<!-- ⏱️ 20 min | 🔶 Intermediate -->

**What You'll Learn:** Complete multi-class classification pipeline.

## Pipeline

1. Load/generate data
2. Create Dataset and DataLoaders
3. Define MLP with nn.Sequential
4. Training loop with validation
5. Early stopping with model saving
6. Test evaluation

## Key Code

```python
model = MLP(n_features, 64, n_classes)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5)

for epoch in range(200):
    train_loss = train_epoch(model, train_loader)
    val_loss = validate(model, val_loader)
    scheduler.step(val_loss)

    if is_best(val_loss, best_loss):
        save_checkpoint(model)
    elif early_stop():
        break
```

<!-- 🤔 This is the template you'll reuse for most classification projects. -->

## Run the Code

```bash
python code/20-integration-multiclass.py
```
