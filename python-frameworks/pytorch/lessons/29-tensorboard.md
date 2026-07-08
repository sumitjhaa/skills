# 🏗️ TensorBoard
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Log metrics, histograms, and model graphs with TensorBoard.

## Setup

```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter('runs/experiment_name')
```

## Logging

```python
# Scalars (loss, accuracy)
writer.add_scalar('Loss/train', loss, epoch)

# Histograms (weight distributions)
writer.add_histogram('layer1/weights', model.layer1.weight, epoch)

# Model graph
writer.add_graph(model, dummy_input)

# Images
writer.add_images('predictions', image_grid, epoch)
```

## Viewing

```bash
tensorboard --logdir=runs
# Opens at http://localhost:6006
```

## Organization

```python
# Use hierarchical names for clean grouping
writer.add_scalar('Loss/train', ...)
writer.add_scalar('Loss/val', ...)
writer.add_scalar('Accuracy/train', ...)
```

<!-- 🤔 TensorBoard is essential for debugging training. Use `add_scalar` for metrics, `add_histogram` for weights. -->

## Run the Code

```bash
python code/29-tensorboard.py
```
