# 🏗️ Convolutional Neural Networks (CNN)
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Conv2d, pooling, and building CNN architectures.

## Conv2d

```python
conv = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, padding=1)
# Input:  (N, 1, H, W) → Output: (N, 16, H, W)
```

## Pooling

```python
pool = nn.MaxPool2d(kernel_size=2, stride=2)  # halves spatial dims
pool = nn.AvgPool2d(kernel_size=2)
```

## Typical CNN Block

```python
nn.Sequential(
    nn.Conv2d(1, 32, 3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),       # downsample
    nn.Conv2d(32, 64, 3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),       # downsample again
    nn.Flatten(),
    nn.Linear(64 * 7 * 7, 10),  # depends on input size
)
```

## Key Concepts

- `kernel_size`: receptive field size
- `padding`: preserve spatial dimensions
- `stride`: step size (default 1)
- `out_channels`: number of filters (feature maps)

<!-- 🤔 More filters = more capacity. Start with 16-32 for small inputs. -->

## Run the Code

```bash
python code/22-cnn-basics.py
```
