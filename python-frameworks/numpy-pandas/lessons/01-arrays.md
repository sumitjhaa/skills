# 🏗️ Project Setup & Arrays
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Install NumPy, create arrays, understand shapes and dtypes.

## Creating Arrays

```python
import numpy as np

# From list
arr = np.array([1, 2, 3, 4, 5])

# Zeros, ones, empty
zeros = np.zeros((3, 4))
ones = np.ones((2, 3))
eye = np.eye(3)  # Identity matrix

# Ranges
r = np.arange(10)     # [0 1 2 ... 9]
s = np.linspace(0, 1, 5)  # [0. 0.25 0.5 0.75 1.]
```

## Array Shape

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
arr.shape   # (2, 3)
arr.ndim    # 2
arr.size    # 6
```

## Data Types

```python
arr = np.array([1, 2, 3], dtype=np.float32)
arr.dtype   # float32

# Common dtypes: int32, int64, float32, float64, bool, complex64
```

<!-- 🤔 NumPy arrays are typed — all elements must be the same dtype. -->

## Run the Code

```bash
python code/01-arrays.py
```
