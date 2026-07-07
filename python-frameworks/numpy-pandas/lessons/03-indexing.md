# 🎯 Indexing & Slicing
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Array indexing, slicing, fancy indexing, boolean masks.

## Basic Indexing

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
arr[0]       # [1 2 3]
arr[0, 1]    # 2
arr[-1, -1]  # 6
```

## Slicing

```python
arr[:, 0]    # [1 4]  — all rows, column 0
arr[0, :2]   # [1 2]  — row 0, first 2 columns
arr[:2, :2]  # [[1 2] [4 5]]
```

## Fancy Indexing

```python
arr = np.array([10, 20, 30, 40, 50])
arr[[0, 2, 4]]       # [10 30 50]
indices = np.array([1, 3])
arr[indices]         # [20 40]
```

## Boolean Masks

```python
arr = np.array([1, 2, 3, 4, 5])
mask = arr > 3
arr[mask]       # [4 5]
arr[arr % 2 == 0]  # [2 4]
```

<!-- 🧠 Slicing returns views (no copy). Fancy indexing returns a copy. -->

## Run the Code

```bash
python code/03-indexing.py
```
