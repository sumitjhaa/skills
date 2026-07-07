# 🔄 Pivot Tables & Crosstab
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Pivot tables as Excel-style summary, crosstab for frequencies.

## Pivot Table

```python
pd.pivot_table(
    df,
    values="sales",
    index="region",
    columns="quarter",
    aggfunc="sum",
    margins=True,  # Show totals
)
```

## Multiple Aggregations

```python
pd.pivot_table(
    df,
    values="sales",
    index="region",
    columns="quarter",
    aggfunc=["sum", "mean"],
)
```

## Crosstab (Frequency)

```python
pd.crosstab(df["region"], df["segment"])
pd.crosstab(df["region"], df["segment"], normalize="index")  # Row %
pd.crosstab(df["region"], df["segment"], margins=True)
```

## Pivot with Multiple Values

```python
pd.pivot_table(
    df,
    values=["sales", "profit"],
    index="region",
    columns="quarter",
)
```

<!-- 🤔 `pivot_table` = GroupBy + reshape. Use `margins=True` for subtotals. -->

## Run the Code

```bash
python code/23-pivot-crosstab.py
```
