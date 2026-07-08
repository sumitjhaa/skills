# 🏗️ Tensor Basics
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Create PyTorch tensors, understand dtypes and devices.

## Creating Tensors

```python
import torch

# From data
t1 = torch.tensor([1, 2, 3])
t2 = torch.tensor([[1, 2], [3, 4]])

# Special tensors
z = torch.zeros(3, 4)
o = torch.ones(2, 3)
e = torch.eye(3)
r = torch.randn(3, 3)  # standard normal
```

## Dtypes & Device

```python
# Specify dtype
f = torch.tensor([1, 2], dtype=torch.float32)
i = torch.tensor([1, 2], dtype=torch.int64)

# Move to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
t = torch.tensor([1, 2, 3], device=device)

# Number of elements and shape
t.shape     # torch.Size([3])
t.numel()   # 3
```

## Size, Numel, and Rank

```python
t = torch.randn(2, 3, 4)
t.ndim       # 3
t.size()     # torch.Size([2, 3, 4])
t.numel()    # 24
```

<!-- 🤔 Tensors are like NumPy arrays but with GPU support and autograd. -->

## Run the Code

```bash
python code/01-tensor-basics.py
```
