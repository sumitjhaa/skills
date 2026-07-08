# 🏗️ CNN on Image Data
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Train a CNN on 2D grid data.

## Architecture

```python
CNN(
  Conv2d(1, 16, 3) → ReLU → MaxPool(2)
  Conv2d(16, 32, 3) → ReLU → MaxPool(2)
  Flatten
  Linear(32*2*2, 1)
)
```

## Training Loop (same as MLP)

Batches of `(N, C, H, W)` tensors through conv layers, flatten before linear layers.

## Shape Progression

| Layer | Output Shape |
|-------|-------------|
| Input | (N, 1, 8, 8) |
| Conv(16, 3) + Pool | (N, 16, 4, 4) |
| Conv(32, 3) + Pool | (N, 32, 2, 2) |
| Flatten | (N, 128) |
| Linear(32*4, 1) | (N, 1) |

<!-- 🤔 CNNs use fewer parameters than MLPs for image data. -->

## Run the Code

```bash
python code/23-cnn-image.py
```
