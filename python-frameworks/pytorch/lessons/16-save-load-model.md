# 🏗️ Saving & Loading Models
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Save and load model weights with `state_dict`.

## Save State Dict

```python
torch.save(model.state_dict(), 'model.pt')
```

## Load State Dict

```python
model = MLP(4, 32, 3)  # must create same architecture first
model.load_state_dict(torch.load('model.pt'))
model.eval()
```

## Save Full Model (discouraged)

```python
torch.save(model, 'model_full.pt')  # saves architecture + weights
model = torch.load('model_full.pt')
```

## Checkpoint with Optimizer

```python
checkpoint = {
    'epoch': epoch,
    'model_state': model.state_dict(),
    'optimizer_state': optimizer.state_dict(),
    'loss': loss,
}
torch.save(checkpoint, 'checkpoint.pt')
```

<!-- 🤔 Save `state_dict` (not the whole model) — it's smaller and more portable. -->

## Run the Code

```bash
python code/16-save-load-model.py
```
