# 🔗 Merge & Join
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** pd.merge, different join types, combining DataFrames.

## Merge Basics

```python
pd.merge(df1, df2, on="user_id")            # Inner join
pd.merge(df1, df2, on="user_id", how="left")  # Left join
pd.merge(df1, df2, left_on="id", right_on="user_id")
```

## Join Types

| how | Result |
|-----|--------|
| `inner` | Only matching keys |
| `left` | All keys from left |
| `right` | All keys from right |
| `outer` | All keys from both |

## Concatenate

```python
pd.concat([df1, df2])              # Stack rows
pd.concat([df1, df2], axis=1)      # Stack columns
pd.concat([df1, df2], ignore_index=True)  # Reset index
```

## Handling Suffixes

```python
pd.merge(df1, df2, on="id", suffixes=("_left", "_right"))
```

## Indicator

```python
result = pd.merge(df1, df2, on="id", how="outer", indicator=True)
result["_merge"].value_counts()
```

<!-- 🧠 Always check for key dtype mismatches before merging — int vs string will fail. -->

## Run the Code

```bash
python code/16-merge-join.py
```
