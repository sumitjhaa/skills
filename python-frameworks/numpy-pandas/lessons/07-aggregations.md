# 📊 Aggregations
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Sum, mean, min, max, cumulative ops, axis parameter.

## Basic Aggregations

```python
arr = np.array([1, 2, 3, 4, 5])

np.sum(arr)     # 15
np.mean(arr)    # 3.0
np.min(arr)     # 1
np.max(arr)     # 5
np.std(arr)     # 1.41
np.var(arr)     # 2.0
```

## Axis Parameter

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

np.sum(arr, axis=0)  # [5 7 9]    — sum each column
np.sum(arr, axis=1)  # [6 15]     — sum each row
np.mean(arr, axis=0) # [2.5 3.5 4.5]
```

## Cumulative

```python
np.cumsum(arr)   # [1 3 6 10 15]  — cumulative sum
np.cumprod(arr)  # [1 2 6 24 120] — cumulative product
```

## Nan-safe Versions

```python
np.nanmean(arr)   # Ignores NaN
np.nansum(arr)
np.nanstd(arr)
```

<!-- 🤔 `axis=0` collapses rows (operates along columns). `axis=1` collapses columns. -->

## Run the Code

```bash
python code/07-aggregations.py
```
