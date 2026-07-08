# 🏗️ Batch Normalization
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Use BatchNorm to stabilize and accelerate training.

## BatchNorm1d

```python
model = nn.Sequential(
    nn.Linear(20, 64),
    nn.BatchNorm1d(64),  # normalizes activations
    nn.ReLU(),
    nn.Linear(64, 1),
)
```

## How It Works

Normalizes each feature to have mean 0, variance 1 across the batch, then applies learnable scale (`γ`) and shift (`β`).

## Benefits

- Faster convergence
- Allows higher learning rates
- Reduces sensitivity to initialization
- Mild regularization effect

## Training vs Eval

```python
model.train()  # uses batch statistics
model.eval()   # uses running averages
```

<!-- 🤔 Always call `model.eval()` before inference when using BatchNorm. -->

## Run the Code

```bash
python code/21-batch-norm.py
```
