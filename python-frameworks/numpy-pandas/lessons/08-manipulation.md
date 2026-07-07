# 🔧 Array Manipulation
<!-- ⏱️ 10 min | 🟡 Intermediate -->

**What You'll Learn:** Reshape, concatenate, split, transpose, stacking.

## Reshaping

```python
arr = np.arange(12)
arr.reshape(3, 4)       # 3 rows, 4 cols
arr.reshape(2, 2, 3)    # 3D array
arr.reshape(-1, 4)      # Auto-infer dimension (-1)
```

## Concatenation

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6]])

np.concatenate([a, b], axis=0)  # Stack rows
np.vstack([a, b])               # Same
np.hstack([a, b.T])             # Stack columns
```

## Splitting

```python
arr = np.arange(10)
np.split(arr, [3, 7])    # [0 1 2], [3 4 5 6], [7 8 9]
np.vsplit(arr, 2)        # Split vertically
```

## Adding / Removing Dimensions

```python
arr[:, np.newaxis]       # Add axis (shape (3, 1))
np.expand_dims(arr, 1)   # Same
np.squeeze(arr)           # Remove dimensions of size 1
```

<!-- 🤔 `reshape(-1, n)` is a handy idiom: "infer the row count, give me n columns." -->

## Run the Code

```bash
python code/08-manipulation.py
```
