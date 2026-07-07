# 🔄 Rolling Windows
<!-- ⏱️ 15 min | 🔴 Advanced -->

**What You'll Learn:** Advanced rolling operations, custom window functions, expanding windows.

## Custom Rolling Functions

```python
def rolling_cv(x):
    return x.std() / x.mean()

df["rolling_cv"] = df["value"].rolling(10).apply(rolling_cv)
```

## Multiple Window Sizes

```python
df["ma_7"] = df["value"].rolling(7).mean()
df["ma_30"] = df["value"].rolling(30).mean()
df["ma_90"] = df["value"].rolling(90).mean()
```

## Weighted Windows

```python
weights = np.array([0.1, 0.2, 0.3, 0.4])
df["weighted"] = df["value"].rolling(4).apply(
    lambda x: np.sum(x * weights)
)
```

## Expanding Windows

```python
df["cummax"] = df["value"].expanding().max()
df["cummin"] = df["value"].expanding().min()
```

## Exponential Weighted

```python
df["ewm"] = df["value"].ewm(span=10).mean()
```

<!-- 🤔 Expanding windows consider all data up to current point. Rolling considers a fixed window. -->

## Run the Code

```bash
python code/24-rolling-windows.py
```
