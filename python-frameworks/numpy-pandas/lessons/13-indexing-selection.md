# 🎯 Indexing & Selection
<!-- ⏱️ 10 min | 🟡 Intermediate -->

**What You'll Learn:** loc, iloc, column selection, conditional filtering.

## Column Selection

```python
df["name"]          # Series
df[["name", "age"]] # DataFrame
df.name             # Series (if column name is valid attr)
```

## Row Selection

```python
df.iloc[0]      # First row by integer position
df.iloc[1:3]    # Rows 1-2 by position
df.loc[0]       # First row by label
df.loc[1:3]     # Rows with labels 1-3 (inclusive!)
```

## Mixed Selection

```python
df.loc[0:3, ["name", "age"]]
df.iloc[0:3, 0:2]
```

## Conditional Filtering

```python
df[df["age"] > 30]
df[(df["age"] > 25) & (df["city"] == "NYC")]
df[df["name"].str.startswith("A")]
```

## isin

```python
df[df["city"].isin(["NYC", "SF"])]
```

<!-- 🧠 Use `loc` for label-based, `iloc` for integer-based. Never mix them. -->

## Run the Code

```bash
python code/13-indexing-selection.py
```
