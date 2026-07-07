# ➕ Array Operations
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Vectorized arithmetic, comparison operators, universal functions.

## Vectorized Arithmetic

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

a + b   # [5 7 9]
a * b   # [4 10 18]
a ** 2  # [1 4 9]
a > 2   # [False False True]
```

## Universal Functions (ufunc)

```python
np.sqrt(a)     # [1. 1.41 1.73]
np.exp(a)      # [2.72 7.39 20.09]
np.log(a)      # [0. 0.69 1.1]
np.sin(a)      # [0.84 0.91 0.14]
```

## Between Arrays and Scalars

```python
a + 10   # [11 12 13]
a * 2    # [2 4 6]
```

<!-- 🤔 Vectorized operations are orders of magnitude faster than Python loops. -->

## Run the Code

```bash
python code/02-operations.py
```
