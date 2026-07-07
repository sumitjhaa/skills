# 📡 Broadcasting
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** How NumPy handles arrays of different shapes during operations.

## The Broadcasting Rule

Two dimensions are compatible when they are **equal** or **one is 1**.

```python
a = np.array([[1], [2], [3]])  # shape (3, 1)
b = np.array([10, 20, 30])     # shape (3,)
a + b
# [[11 21 31]
#  [12 22 32]
#  [13 23 33]]
```

## Broadcasting Step by Step

```python
a = np.ones((3, 4))   # (3, 4)
b = np.array([1, 2, 3, 4])  # (4,) → broadcast (3, 4)
a + b
```

## Adding a New Axis

```python
arr = np.array([1, 2, 3])
arr[:, np.newaxis]  # (3, 1)
arr[np.newaxis, :]  # (1, 3)
```

## Common Broadcasting Patterns

```python
# Center data
data = np.random.randn(10, 3)  # 10 points, 3 features
mean = data.mean(axis=0)
centered = data - mean

# Normalize
std = data.std(axis=0)
normalized = (data - mean) / std
```

<!-- 🤔 Broadcasting avoids unnecessary memory copies. Use it instead of `np.tile()`. -->

## Run the Code

```bash
python code/04-broadcasting.py
```
