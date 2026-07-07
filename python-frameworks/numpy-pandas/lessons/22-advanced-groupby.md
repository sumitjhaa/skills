# ⚡ Advanced GroupBy
<!-- ⏱️ 15 min | 🔴 Advanced -->

**What You'll Learn:** Custom aggregations, multiple functions, groupby with MultiIndex.

## Multiple Agg Functions

```python
df.groupby("category")["value"].agg(["sum", "mean", "std", "count"])
```

## Custom Aggregation

```python
def range_func(x):
    return x.max() - x.min()

df.groupby("category")["value"].agg(["mean", range_func, lambda x: x.quantile(0.75)])
```

## Named Aggregations

```python
df.groupby("category").agg(
    total=("value", "sum"),
    avg=("value", "mean"),
    spread=("value", lambda x: x.max() - x.min()),
)
```

## Apply with GroupBy

```python
df.groupby("category").apply(
    lambda g: g.nlargest(2, "value")
)
```

## GroupBy on Time

```python
df.set_index("date").groupby(pd.Grouper(freq="M"))["value"].sum()
```

<!-- 🧠 `GroupBy.apply()` is flexible but slower than `agg` or `transform`. -->

## Run the Code

```bash
python code/22-advanced-groupby.py
```
