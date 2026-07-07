# 📚 MultiIndex
<!-- ⏱️ 15 min | 🔴 Advanced -->

**What You'll Learn:** Hierarchical indexing, creation, selection, stacking/unstacking.

## Creating MultiIndex

```python
arrays = [["A", "A", "B", "B"], [2023, 2024, 2023, 2024]]
index = pd.MultiIndex.from_arrays(arrays, names=["group", "year"])

df = pd.DataFrame({"value": [10, 20, 30, 40]}, index=index)
```

## Selection on MultiIndex

```python
df.loc["A"]                  # All rows for group A
df.loc[("A", 2024)]          # Specific row
df.xs(2024, level="year")    # All groups, year=2024
```

## Stack / Unstack

```python
df.unstack()      # Pivot inner index to columns
df.stack()        # Reverse
```

## MultiIndex Columns

```python
cols = pd.MultiIndex.from_tuples([("sales", "Q1"), ("sales", "Q2"), ("costs", "Q1")])
df = pd.DataFrame(rng.random((3, 3)), columns=cols)
```

<!-- 🤔 MultiIndex is powerful for grouped/panel data. Use `.xs()` for cross-sections. -->

## Run the Code

```bash
python code/21-multiindex.py
```
