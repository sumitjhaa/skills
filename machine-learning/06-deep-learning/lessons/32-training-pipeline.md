# 06.32 Full Training Pipeline

End-to-end training pipeline combining all components.

## Pipeline Overview

```
Data → Augment → Model → Loss → Backward → Clip → Optimizer → LR Schedule → Evaluate
```

## Components

1. **Data Loading**: Load dataset, shuffle, batch, preprocess
2. **Augmentation**: Apply transforms (random flip, crop, cutout, mixup)
3. **Model Forward**: Compute predictions
4. **Loss Computation**: Cross-entropy, label smoothing
5. **Backward Pass**: loss.backward()
6. **Gradient Clipping**: Clip gradient norm
7. **Optimizer Step**: Update parameters
8. **LR Schedule**: Adjust learning rate
9. **Evaluation**: Validation accuracy, loss, metrics
10. **Checkpointing**: Save best model, log metrics

## Training Loop Pseudocode

```python
for epoch in range(num_epochs):
    model.train()
    for batch in train_loader:
        x, y = augment(batch)
        logits = model(x)
        loss = criterion(logits, y)
        loss.backward()
        clip_grad_norm(model.parameters(), max_norm)
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()

    model.eval()
    for batch in val_loader:
        logits = model(batch.x)
        val_loss += criterion(logits, batch.y)
        val_acc += accuracy(logits, batch.y)

    log(epoch, train_loss, val_loss, val_acc, lr)
    save_checkpoint(model, optimizer, epoch, best_acc)
```

## Key Design Decisions

- **Loss scaling**: For mixed precision
- **Gradient accumulation**: For large effective batch
- **Sync batch norm**: For multi-GPU
- **EMA (Exponential Moving Average)**: Smoothed model weights for inference

## EMA of Weights

Maintain running average of parameters:

θ_ema = decay · θ_ema + (1-decay) · θ

Use θ_ema for validation and inference. Decay = 0.999. Reduces variance.

## Logging

Log to CSV/JSON:
- epoch, step, train_loss, val_loss, val_acc
- lr, grad_norm, batch_time
- ε (label smoothing), dropout rate

## Sweep Management

For hyperparameter tuning:
- Grid search or random search
- Log all configs and results
- Compare via validation accuracy

## Final Evaluation

1. Load best checkpoint (by validation accuracy)
2. Run on test set (ONCE at the end)
3. Report: test accuracy, test loss, model size, inference time

## Reproduction

Fixed seeds, deterministic algorithms, clear config file.
